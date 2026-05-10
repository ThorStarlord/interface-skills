---
spec_type: brief
spec_id: kanban-approval
created: 2026-05-10
status: draft
source_evidence: 01-inspector-evidence.md
---

# Brief: Kanban Approval Queue

## 1. Goal

Enable low-tech business owners to review all pending content in a single clearing-house surface, make approval/rejection decisions, and move posts toward publication or the archive — reducing friction between content creation and live Instagram presence.

## 2. Primary user

- **Role / context:** Local business owner or marketing manager. Has received 1–10 AI content suggestions this week. Arrives after creating or reviewing posts on `/create`. Wants to batch-review and make final approval decisions. Decision window: 5–15 min during a business break.
- **Technical literacy:** Beginner to intermediate. Comfortable with basic mobile UI patterns (tap, swipe, drag). Not comfortable with technical publishing concepts. Prefers visual feedback over error messages.
- **Primary device:** Mobile first (60% of sessions). Coarse pointer (touch). Desktop board view as secondary mode for planning/batch operations.
- **Accessibility considerations:** Clear visual status indicators (color + icon + text). Touch targets ≥44px. No time-based content disappearance.

## 3. Primary action

**Decide** — the user moves a post from `review` column to either `approved` (publish it) or `backlog` (reconsider it).
**Decide** — the user moves a post from `draft` column (pending approval) to either `approved` (publish it) or `backlog` (reconsider it).

The user should be able to complete ≥1 approval decision without leaving this screen. Decision should be atomic: tap "Aprovar" → post moves → confirmation → ready for next.

## 4. Secondary actions

1. **View post detail** — see full caption, hashtags, media, scheduled date, any errors. Must not leave kanban view; modal overlay.
2. **Reject / "Não quero este"** — move post back to backlog (undo approval, signal "not for me").
3. **Reschedule** — change scheduled date / time without re-creating.
4. **Generate new idea** — if the current batch feels stale, trigger AI to produce 1 fresh suggestion immediately (awaiting backend webhook). [Currently broken — silent no-op. See PRODUCT-INTEGRITY-BACKLOG.md Item #1.]
5. **View board mode** — switch to kanban columns for planning/drag-drop operations (desktop primary).
6. **Hide published column** — reduce visual clutter after batch publish; toggle off published items.

## 5. Why it matters

Without a dedicated approval screen, content approval is scattered: AI suggestions live in an inbox list, scheduled posts hide in calendar view, errors go unseen until Instagram fails to publish. Result: low-tech owners miss approval workflows, posts publish with errors, or quality suffers. Kanban centralizes the decision moment — one place to say "yes" or "no" — and reduces approval latency from days to minutes.

## 6. Success criteria

- **Latency:** ≥80% of first-time users complete 1 approval within 2 min of landing.
- **Confidence:** Post preview (image + caption) loads within 1.5 sec; no stalled spinners.
- **Completion rate:** ≥75% of posts in `review` column get an explicit decision (approve/reject/reschedule) within 24 hours. Implies the UX does not cause decision paralysis.
- **Completion rate:** ≥75% of posts in `draft` column get an explicit decision (approve/reject/reschedule) within 24 hours. Implies the UX does not cause decision paralysis.
- **Error handling:** ≥95% of approved full_auto posts publish without user intervention; errors surface in post detail modal with a "retry" action, not silent failures.
- **Error handling:** ≥95% of posts with `automation_tier: full_auto` publish without user intervention; errors surface in post detail modal with a "retry" action, not silent failures.
- **Device parity:** Mobile review mode and desktop board mode stay in sync; a post approved on mobile appears in `approved` column immediately on desktop refresh.
- **Responsiveness:** Drag-drop on desktop does not stall (100ms visual feedback minimum); swipe/approve on mobile feels snappy (80ms feedback).

## 7. Constraints

- **Brand:** Warm Concierge aesthetic. Supportive, human-first language ("Aprovar", not "Accept"). Celebratory empty states ("Missão cumprida 🎉"). No utilitarian tech jargon.
- **Platform:** React/Vite SPA, mobile first. Runs on iOS/Android via web. Desktop: `1024px+` min-width for board view. Mobile: coarse pointer, stack to single column on small screens.
- **Regulatory / compliance:** None beyond Instagram's rate limits (100–200 posts/day) and Stripe token ceiling. No PII beyond project name / business name.
- **Technical:**
  - Realtime sync via Supabase subscription on `content_calendar` table. Posts approved here must trigger `kanban_trigger` webhook → `S.0009a` (image generation) → `S.0010` (publish) if `automation_tier = 'full_auto'`.
  - Post preview media (images/videos) served from Supabase Storage (`content-images` bucket). Must load in <1.5 sec.
  - Kanban status transitions: `backlog` → `review` (manual); `review` → `approved` (user tap); `approved` → `published` (n8n trigger after Instagram success).
  - Token deduction happens at publish, not at approval. No visible token counter on this screen (tokens belong in billing context, per hard rules).
- **Time / scope:** MVP launch: April 2026 (past). Current: stabilizing post approval + fixing "Nova ideia" silent no-op + enforcing free-ideas backend counter.

## 8. Non-goals (what this is NOT)

- **Not a content creation interface.** Users do not write copy or edit images here. `/create` owns that.
- **Not a calendar.** Do not use this screen to reschedule posts across weeks or months. `/calendar` owns that.
- **Not a publishing console.** Do not expose n8n nodes, webhook logs, API responses, or debug panels. Keep operator-only concepts off this screen.
- **Not a manual-approval gateway.** Do not force users to manually review brand voice rules or compliance. That belongs in the content generation layer (n8n prompts).
- **Not a batch-edit tool.** Users approve/reject individual posts in isolation. No "select all" or "bulk reschedule".
- **Not Instagram-aware.** Do not expose Instagram-specific metadata (hashtag perf, engagement, follower count) on this screen. That's analytics, not approval.

## 9. Open questions

1. **Rescheduling UX:** When user taps "Reschedule", do they get a date picker inline, or navigate to `/calendar`? Current: not implemented. Decision needed before component design.
2. **Error recovery:** If a post fails to approve (e.g., Instagram rate-limited), should the UI auto-retry, or require user tap? Current: user must tap retry. Acceptable?
3. **Empty-state CTAs:** When `review` column is empty (all posts decided), should we show "Voltar a criar" or just celebrate? Current: celebratory only. Acceptable?
4. **Cold-start:** On day 1, user has zero posts. Should `/kanban` redirect to `/create`, or show an empty board with helpful hint? Current: shows empty board. Acceptable?
5. **Post format selection:** A proactive suggestion arrives without explicit `feed` / `story` / `reel` format. User approves. What format gets published? Current: defaults to `feed` silently. Should be explicit choice first. Decision needed.
6. **Realtime conflict:** If two tabs are open, and user approves post in tab A while it publishes in tab B, how do we avoid race conditions? Current: not handled. Need to spec conflict resolution.

## 10. Assumptions made in this brief

- ⚠️ ASSUMED: "Nova ideia" regeneration will be fixed by backend webhook `/webhook/2-1-content-generator-manual` before this brief moves to design. Current status: resolved (per PRODUCT-INTEGRITY-BACKLOG.md Item #1 resolution). Confirm this endpoint is live before coding.
- ⚠️ ASSUMED: Free-ideas counter will be moved to server state (credentials table or token_transactions) before launch. Current: frontend state only (broken across page reloads). Without this, billing model has zero enforcement. Confirm DB schema is updated.
- ⚠️ ASSUMED: `automation_tier = 'full_auto'` posts publish automatically after approval. If any exceptions exist (e.g., manual review required for certain brands), clarify before layout design.
- ⚠️ ASSUMED: Mobile users primarily use "Review" (card-deck) mode; desktop users use "Board" (column) mode. If user data contradicts this, brief needs revision.
- ⚠️ ASSUMED: Post preview media URLs are always valid. If media generation fails upstream, we surface an error in post detail modal. No silent placeholders.

---

## Rationale for reconstructed intent

**Problem:** Based on `CONTENT-JOURNEY-UX-CONTRACT.md`, kanban is the "approval queue" in the `/campaign → /create → /kanban → /calendar` journey. Posts flow through: `backlog` (saved, not decided) → `review` (waiting for user decision) → `approved` (ready to publish) → `published` (live). User's job is to "Decide what moves forward" in minimal time with maximum confidence.

**User:** Low-tech owner runs on mobile during business hours. Impatient with complexity. Trusts AI suggestions but needs one final review moment. Device is touch, not mouse.

**Success:** If ≥80% of users complete 1 approval in <2 min, the kanban screen is not a friction point. If posts fail to publish after approval, trust in the system collapses (per PRODUCT-INTEGRITY-BACKLOG.md Item #1 — currently fixed).

**Constraints:** Instagram rate limits mean we can't approve 100 posts and expect them all to publish today. Stripe token ceiling means approving a post may fail if credits are exhausted. Kanban surface must surface these constraints clearly or they become silent failures.

**Spec Recovery:** Implementation exists (inspector evidence shows full component tree). This brief recovers the product intent and constraints from that implementation, inspector evidence, code comments, workflow definitions, and content journey contract. Downstream `02-blueprint.md` (layout) and `06-component-specs.md` (state machines) should reference this brief's goals and constraints.
