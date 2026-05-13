import os
import tempfile
import unittest
import importlib.util

def get_validate_func():
    spec = importlib.util.spec_from_file_location("validate_spec_package", "scripts/validate-spec-package.py")
    if spec is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return getattr(module, "validate_spec_package", None)
    except FileNotFoundError:
        return None

class TestValidateSpecPackage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.package_path = self.temp_dir.name
        self.validate_func = get_validate_func()

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_file(self, filename, content):
        path = os.path.join(self.package_path, filename)
        with open(path, "w") as f:
            f.write(content)

    def test_based_on_resolves(self):
        self.write_file("01-brief.md", "---\nbased_on: non_existent.md\n---\n")
        issues = self.validate_func(self.package_path)
        self.assertTrue(any("non_existent.md" in issue for issue in issues))

    def test_based_on_empty_safe(self):
        self.write_file("01-empty.md", "---\nbased_on:\n---\n")
        issues = self.validate_func(self.package_path)
        self.assertEqual(len(issues), 0)

    def test_deprecated_not_current(self):
        self.write_file("01-brief.deprecated.md", "---\nstatus: current\n---\n")
        issues = self.validate_func(self.package_path)
        self.assertTrue(any("deprecated" in issue.lower() and "current" in issue.lower() for issue in issues))

    def test_one_current_report_per_type(self):
        self.write_file("LINT-REPORT.md", "---\ntype: report\nstatus: current\n---\n")
        self.write_file("LINT-REPORT-OLD.md", "---\ntype: report\nstatus: current\n---\n")
        issues = self.validate_func(self.package_path)
        self.assertTrue(any("multiple current" in issue.lower() for issue in issues))

    def test_historical_reports_marked(self):
        self.write_file("LINT-REPORT-OLD.md", "---\ntype: report\nstatus: historical\n---\n")
        issues = self.validate_func(self.package_path)
        self.assertTrue(any("historical report" in issue.lower() and "superseded_by" in issue.lower() for issue in issues))

    def test_acceptance_markers_automation(self):
        self.write_file("05-acceptance.md", "- [A] This is a test without automation mechanism\n")
        issues = self.validate_func(self.package_path)
        self.assertTrue(any("[A]" in issue for issue in issues))

if __name__ == "__main__":
    unittest.main()