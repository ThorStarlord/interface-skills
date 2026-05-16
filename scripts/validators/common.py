from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ValidatorResult:
    status: str # 'pass', 'fail', 'error'
    validator_name: str
    findings: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    artifact_path: Optional[str] = None
    checked_scope: Optional[str] = None
    detected_mode: Optional[str] = None
    extra_meta: dict = field(default_factory=dict)
