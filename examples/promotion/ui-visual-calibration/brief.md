---
spec_type: brief
spec_id: settings-account
created: 2026-05-06
status: draft
---

# Brief: Prosper Account Settings Page

## 1. Goal

After visiting this page, a project manager can update their display name, avatar, and notification preferences so that Prosper reflects their current identity and communication needs without requiring help from an administrator.

## 2. Primary user

- **Role / context:** Project manager or team lead at a mid-size company (50–500 employees). They are mid-session in Prosper, have just noticed their profile photo is wrong or they are receiving too many notifications, and want to fix it quickly before returning to active work.
- **Technical literacy:** Intermediate — comfortable with SaaS tools (Jira, Notion, Slack-style apps), not a developer. Does not need tooltips explaining what a "display name" is, but should not encounter configuration options that require understanding of API keys or SSO protocol details.
- **Primary device:** Desktop browser (Chrome or Firefox on Windows/macOS). Mobile is used for quick reads only; settings changes on mobile are rare.
- **Accessibility considerations:** No specific known constraints for this persona. WCAG AA compliance is required as a baseline for the B2B enterprise customer base. Keyboard-only navigation must work for power users who avoid the mouse.

## 3. Primary action

Save updated profile details (display name and avatar).

## 4. Secondary actions

- Toggle individual notification types on or off (email digests, task assignment alerts, mention alerts).
- View the current subscription plan name and renewal date (read-only).
- Navigate between settings sections (Profile, Notifications, Billing) without a full page reload.
- Cancel in-progress edits and revert to saved values.

## 5. Why it matters

Project managers are the face of their team inside Prosper — their avatar and display name appear on every task assignment, comment, and report. An incorrect name or placeholder avatar erodes trust with stakeholders reviewing project status. Notification overload is the second most cited reason users disengage from the tool, per internal support ticket categorisation. Giving users direct, low-friction control over both reduces churn risk and support volume.

## 6. Success criteria

- A user who arrives at this page with the intent to update their display name can complete the change and receive confirmation in under 90 seconds, measured from page load to success toast dismissal.
- The save action succeeds on first attempt for at least 95% of submissions (no silent failure, no ambiguous feedback).
- At least one qualitative: users do not need to re-open the settings page to verify their change was applied — the updated value is visible in the sidebar profile badge immediately after saving.

## 7. Constraints

- **Brand:** Prosper uses Inter typeface, a monochrome neutral base palette (`#111827` text, `#FFFFFF` surface, `#E5E7EB` borders), and a single accent color `#2563EB` for primary actions. No gradients. Corner radius: `rounded-md` to `rounded-lg`. These tokens are defined in `system.md`.
- **Platform:** Web application, desktop-first. React front end. No native mobile app in scope. Minimum viewport width: 768px for split-panel layout; a mobile reflow is required at <768px but is not a primary use case.
- **Regulatory / compliance:** Profile avatar uploads must enforce a file size limit (⚠️ exact limit not specified — see Open questions). GDPR right-to-erasure: deleting the account is explicitly out of scope for this page (see Non-goals). No HIPAA requirements.
- **Technical:** Profile data is served from a REST API; save triggers a PATCH request. Avatar upload goes to object storage; the component receives a signed upload URL. Notification preferences are stored per-user and toggled via the same PATCH endpoint. Billing data is read-only, sourced from the billing provider (Stripe); no write operations on this page.
- **Time / scope:** ⚠️ ASSUMED: This is targeting the v1.4 release cycle. No hard deadline has been provided.

## 8. Non-goals (what this is NOT)

- Account deletion or deactivation — that flow belongs to a separate, admin-gated "Danger Zone" screen.
- Password change or SSO configuration — authentication settings are managed in a dedicated Security section not in scope here.
- Team or workspace settings (billing plan upgrades, member management, role assignment) — those are admin-only screens.
- Mobile-native app settings — this spec covers the web product only.
- Internationalisation / language preferences — English-only for v1.4.

## 9. Open questions

1. What is the maximum file size for avatar uploads? The engineering constraint has not been confirmed. This affects validation copy and the error state for the upload component.
2. Should notification preferences be saved immediately on toggle (autosave), or should the user explicitly press Save? Autosave is faster but may confuse users who toggle accidentally.
3. Is there a character limit on the display name field? If yes, should it be enforced silently (truncation) or with an inline counter?
4. Should the Billing section show any CTAs (e.g. "Upgrade plan") or remain strictly read-only? Including CTAs would change the information hierarchy of that section.
5. When the user is on a mobile viewport, should the Navigation revert to a dropdown select element or a horizontally scrollable tab strip?

## 10. Assumptions made in this brief

- ⚠️ ASSUMED: The product is called "Prosper" and targets project managers and team leads at mid-size companies. No product name or specific persona was provided in the original request.
- ⚠️ ASSUMED: The primary device is desktop. The original request did not specify device, but a B2B project management tool used at work defaults to desktop-primary.
- ⚠️ ASSUMED: The three sections (Profile, Notifications, Billing) are the correct scope for this settings page. The original brief listed these features; this assumption should be confirmed before detailed component work begins.
- ⚠️ ASSUMED: v1.4 release target. No timeline was specified.
- ⚠️ ASSUMED: The Billing section is read-only. No write operations for billing were requested; confirmed as non-goal above pending answer to Open question 4.
