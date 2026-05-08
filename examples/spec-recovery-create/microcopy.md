---
spec_type: microcopy
spec_id: pulse-create
created: 2026-05-08
status: draft
recovery: true
---

# Microcopy: Pulse /create Route (Spec Recovery)

> **Recovery note:** *Observed* copy is what the UI currently shows. *Target* copy is the approved replacement. Where copy is already correct, Observed and Target are the same. Approving this document means approving the Target copy.

---

## 1. Page Heading and Labels

| Element | Observed | Target | Notes |
|---|---|---|---|
| Page heading | "Create Post" | "Create Post" | Correct. Retain. |
| Caption input label | (no visible label — placeholder only) | "Caption" (visible label, `<label>`) | Observed: only a placeholder. Accessibility gap — needs a real label. |
| Caption placeholder | "Write your caption..." | "Write your caption or generate one with AI." | Updated to surface the AI affordance. |
| Character count | "240" (number only) | "240 characters remaining" | Descriptive; screen reader-accessible. |
| Channel selector label | (none) | "Publish to" | Group label for the channel picker. |
| Media section label | "Media" | "Attach media (optional)" | Make optionality explicit; reduces abandonment anxiety. |

---

## 2. Buttons and Actions

| Element | Observed | Target | Notes |
|---|---|---|---|
| Primary publish button | "Publish" | "Publish now" | Disambiguates from "schedule"; reduces accidental publishes. |
| Schedule button | "Schedule" | "Schedule…" | Ellipsis signals a modal will open (convention). |
| Save draft | "Save" | "Save draft" | Clarifies what is being saved. |
| AI Draft button (idle) | "Generate" | "✦ Generate draft" | Sparkle icon (`✦`) is the established AI affordance in the app. "Draft" clarifies output type. |
| AI Draft button (generating) | "..." | "Generating…" | Descriptive loading label; used as `aria-label` value. |
| AI suggestion accept | "Use" | "Use this draft" | Full phrase; reduces ambiguity about what is being accepted. |
| AI suggestion discard | "Discard" | "Discard" | Correct. Retain. |
| Schedule confirm button | "Publish" | "Confirm schedule" | Distinguishes the confirm-schedule action from immediate publish. |

---

## 3. Empty and Loading States

| Context | Observed | Target |
|---|---|---|
| Post preview — no channels selected | (blank) | "Select at least one channel to preview your post." |
| Post preview — generating | (spinner only) | Spinner + "Loading preview…" |
| Channel list loading | (spinner) | Spinner + "Loading your channels…" |
| No media attached (uploader idle) | "Drop files here or browse" | "Drop an image or video, or browse to upload. Optional." |

---

## 4. Error Messages

| Error | Observed | Target | Notes |
|---|---|---|---|
| No channel selected on publish attempt | (blocked silently — button stays disabled) | "Select at least one channel before publishing." (inline, below channel selector) | Observed: button disabled without explanation. Target: actionable inline error. |
| Caption empty on publish attempt | (blocked silently) | "Add a caption before publishing." | Same issue as above. |
| AI draft timeout | "Error" | "Couldn't generate a draft. Check your connection and try again." | Observed copy is too terse. |
| AI draft rate limit | (not handled) | "You've reached today's AI draft limit. Upgrade your plan or try again tomorrow." | Not currently handled; needs implementation. |
| Media upload file too large | "File too large" | "This file exceeds [N] MB. Please use a smaller file." ⚠️ N is an open question | Placeholder until engineering confirms the limit. |
| Media upload wrong format | "Invalid file type" | "Pulse supports JPG, PNG, GIF, and MP4. This file format isn't supported." | Lists accepted formats explicitly. |
| Publish failed (network) | "Error publishing" | "Post couldn't be published. Your draft has been saved — try again." | Reassures user their content is not lost. |
| Schedule conflict | (not handled) | "A post is already scheduled at this time. Try [suggested time]." | Not currently handled; needs implementation. |

---

## 5. Success and Confirmation

| Context | Observed | Target |
|---|---|---|
| Post published | "Published!" (toast) | "Post published to [channel names]." | Lists channels in confirmation. |
| Post scheduled | (not implemented — immediate publish only currently) | "Post scheduled for [Day, Date at Time]." | New flow. |
| Draft saved | "Saved" (toast) | "Draft saved." | Concise and correct. |
| AI draft accepted | (no feedback) | Caption updates immediately; no separate toast needed | Feedback is visual (caption changes). |

---

## 6. Voice and Tone Notes

- **Action-first:** Lead with the verb ("Select a channel", "Add a caption", "Generate draft"). Not "Please select a channel."
- **Specific errors:** Every error names what went wrong and what to do. No generic "Something went wrong."
- **Optionality is explicit:** If something is optional, say "(optional)" — don't assume users know.
- **AI affordance:** The sparkle icon (`✦`) is used consistently for AI-generated features. Never use "AI" as a standalone label — it is implicit from the icon.
