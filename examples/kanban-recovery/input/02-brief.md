---
spec_type: brief
spec_id: kanban
created: 2026-05-14
status: draft
recovery: true
---

# Brief: Kanban Post Approval Queue (Spec Recovery)

> **Recovery note:** This brief reconstructs product and design intent from the existing `/kanban` implementation and available spec artifacts. Sections distinguish **Observed** from **Target**. Approving this brief ratifies the Target, not the Observed state.

---

## 1. Goal

**Observed:** The `/kanban` surface displays posts in status columns, allows toggling between kanban and deck (review) mode, and lets users open a post detail modal to approve or schedule.

**Target:** After visiting this page, a content manager can review the pending approval queue, switch between kanban status columns and review/deck mode toggle, and approve or reschedule individual posts — completing a full review session without leaving the queue view.

---

## 2. Primary user

- **Role / context:** Content manager or social media team lead. Reviews posts created by writers and approves them for scheduling.
- **Technical literacy:** Intermediate SaaS user. Comfortable with tools like Trello or Asana. Understands queue semantics and status workflows.
- **Primary device:** Desktop browser. High-frequency review task performed in concentrated sessions.
- **Accessibility:** Keyboard navigation through status columns and modal must be functional (WCAG AA).

---

## 3. Primary action

Review and approve posts from the approval queue without leaving the kanban view.

---

## 4. Secondary actions

- Switch between kanban status columns view and review/deck mode toggle.
- Open the post detail modal to read full content and context.
- Reschedule a post to a different publish time.
- Filter the approval queue by status column.
- Handle the empty queue state (no posts pending approval).

---

## 5. Why it matters

The approval queue is the highest-leverage moderation surface in Pulse: it gates all content from reaching publishing channels. Without a clear spec, the current implementation has diverged — the deck mode toggle, status columns semantics, and modal surface exist but are undocumented, making it impossible to maintain or extend without risk of regression.

---

## 6. Success criteria

- A content manager can approve all posts in the approval queue in a single session without navigating away.
- Switching between kanban status columns and review/deck mode toggle is available at all times and preserves the user's position in the queue.
- The post detail modal opens and closes without losing kanban state.
- The empty queue state is correctly displayed when no posts are pending.

---

## 7. Constraints

- **Brand:** Existing Pulse visual system; no redesign scope in this recovery.
- **Platform:** Web, desktop-first; React/TypeScript.
- **Technical:** Status column semantics must map to the existing post status enum in the API.
- **Scope:** This spec covers the `/kanban` approval surface only — the scheduling calendar and post creation flow are out of scope.

---

## 8. Non-goals

- Post creation (belongs to `/create`).
- Analytics or performance metrics (belongs to `/dashboard`).
- Bulk scheduling across multiple posts simultaneously.
- Mobile-native experience (read-only at most on mobile).

---

## 9. Open questions

1. **Deck mode persistence:** Does toggling to review/deck mode persist across page reloads or sessions, or does the view reset to kanban on each visit?
2. **Column ordering:** Is the sequence of status columns (Draft → Pending → Approved → Scheduled) fixed or user-configurable?
3. **Approval delegation:** Can a reviewer approve their own posts, or does the approval queue require a second reviewer?

---

## 10. Assumptions

- ⚠️ ASSUMED: The approval queue and kanban status columns are the same surface — the brief treats them as one unified view with two display modes (kanban / review).
- ⚠️ ASSUMED: The post detail modal is a child of the kanban surface, not a separate route. If it navigates away, the scope of the brief must expand.
- Content managers have the Reviewer role; write-only contributors cannot access this surface.
