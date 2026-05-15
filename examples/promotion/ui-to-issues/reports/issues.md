# UI Issues: Design System Drift

## Finding 1: Color Contrast Violation in Main Action Button
- **Severity**: High
- **Description**: The primary button (#00FF00) against white text fails WCAG 2.1 AA contrast requirements.
- **Remediation**: Adjust the button background to a darker green (#008000).

## Finding 2: Inconsistent Grid Spacing in Dashboard View
- **Severity**: Medium
- **Description**: The spacing between cards varies from 16px to 24px without a clear semantic reason.
- **Remediation**: Standardize on a 16px (1rem) gutter for the dashboard grid.

## Finding 3: Ambiguous Button Labels in Settings Modal
- **Severity**: Low
- **Description**: Both the 'Cancel' and 'Close' buttons perform the same action but use different labels, causing user friction.
- **Remediation**: Consolidate into a single 'Close' button or differentiate the actions.

## Finding 4: Missing ARIA Labels on Social Icons
- **Severity**: Medium
- **Description**: The footer social icons have no screen-reader-accessible labels.
- **Remediation**: Add `aria-label` to all footer anchor tags.

## Finding 5: Image Alt Text Missing on Product Gallery
- **Severity**: Low
- **Description**: Several decorative images in the product gallery lack alt text.
- **Remediation**: Add empty alt="" or descriptive text if the image is meaningful.
