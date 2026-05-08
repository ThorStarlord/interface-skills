---
spec_type: brief
spec_id: pulse-create
created: 2026-05-08
status: approved
recovery: true
---

# Brief: Pulse /create Route (Spec Recovery)

> **Recovery note:** This brief reconstructs product and design intent from the existing implementation and available product context. Each section distinguishes **Observed** (what the code currently does) from **Target** (what it should do once this brief is approved). Approving this brief means approving the Target, not ratifying the Observed.

---

## 1. Goal

**Observed:** The `/create` page allows a user to type a caption, select social channels, optionally attach media, and click Publish or Schedule. An AI draft button generates a suggested caption.

**Target:** After visiting this page, a social media manager can create a post — either by writing their own caption or accepting an AI-generated draft — select one or more publishing channels, attach optional media, and either publish immediately or schedule for a specific date/time, completing the full action in a single screen without navigating away.

---

## 2. Primary user

- **Role / context:** Social media manager at a brand or marketing agency. Mid-session in Pulse, has a content brief open in another tab, and wants to turn it into a scheduled post quickly.
- **Technical literacy:** Intermediate SaaS user. Comfortable with tools like Hootsuite, Buffer, or Later. Does not need explanations of what a "channel" is. May be producing 5–20 posts per day — speed and low cognitive load matter more than features.
- **Primary device:** Desktop browser. Mobile is a read-only review device (managers check the queue, not create posts, on mobile).
- **Accessibility:** WCAG AA required. Keyboard-only navigation must be fully functional.

---

## 3. Primary action

Create and publish or schedule a post to at least one social channel.

---

## 4. Secondary actions

- Accept, edit, or discard an AI-generated caption draft.
- Attach and preview media (image or video).
- Select multiple channels for simultaneous publishing.
- Open the schedule modal and pick a future publish date/time.
- Save as draft without publishing.

---

## 5. Why it matters

The `/create` route is the highest-frequency interaction in Pulse — it is the action users come to the product to perform. Any friction here directly drives churn. The current lack of specification has led to three separate caption input implementations, an undocumented AI timeout, and a mobile redirect that bypasses the main flow entirely.

---

## 6. Success criteria

- A user who arrives at this page can create and publish a post with at least one channel selected in under 60 seconds on desktop.
- AI draft generation completes in under 5 seconds for 95% of requests; if it exceeds the threshold, a clear loading state and eventual error message appear.
- The page passes WCAG AA audit with zero critical violations.

---

## 7. Constraints

- **Brand:** Pulse uses Inter typeface; primary action colour is `violet-600` (`#7c3aed`); neutral text `#111827`. No design token system currently exists — tokens will be defined in `visual-calibration.md` and `system.md` as part of this recovery.
- **Platform:** Web app, desktop-first. React/TypeScript. Mobile: **Target is a single responsive layout** (replaces the current `MobileCreateRedirect` split) — see open question #3.
- **API:** Caption saves via POST to `/api/posts`; AI draft via POST to `/api/ai/draft` (3-second timeout observed — see open question #1); media upload via signed URL to object storage.
- **Channels:** Up to 8 channels may be connected to a workspace. Multi-select is supported. **Target channel order: most-used first** (see open question #2).

---

## 8. Non-goals

- Bulk scheduling (multiple posts at once) — that belongs to the `/queue` bulk-edit view.
- Post analytics or engagement metrics — that belongs to `/dashboard`.
- Approvals workflow — the Reviewer role has a separate `/review` route.
- Mobile-native app — web only.
- Video editing or in-app trimming — users attach pre-edited video only.

---

## 9. Open questions

1. **AI generation timeout:** Observed hard-coded value of 3 seconds. Product must confirm the agreed UX threshold before acceptance criteria for the AI draft panel can be finalised.
2. **Channel selector ordering:** Target assumes most-used-first ordering. Product and engineering must confirm feasibility and agree before the channel-selector component spec is written.
3. **Unified responsive layout vs. mobile redirect:** Target assumes one responsive layout. This requires removing `MobileCreateRedirect` — an architecture decision. Engineering sign-off required before `screen-spec.md` can be approved.

---

## 10. Assumptions

- Users are authenticated; unauthenticated access redirects to `/login`.
- A workspace with at least one connected channel is assumed. Empty-state (no channels connected) is out of scope for this recovery — it belongs to the onboarding flow.
- The Tailwind CSS framework remains in use; the token system will be defined as CSS custom properties overlaid on Tailwind, not replacing it.
