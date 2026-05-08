---
spec_type: journey-map
spec_id: content-journey
created: 2026-05-20
status: approved
---

# Content Journey Map

This package owns the cross-route rules and flow for the core content creation and scheduling journey.

## 1. Journey Flow
`Campaign Planning` → `Content Creation` → `Approval Queue` → `Calendar/Kanban Scheduling`

## 2. Route Responsibilities
- **/campaign**: Strategic grouping and brief definition.
- **/create**: Individual post drafting and media upload.
- **/approve**: Peer review and status transitioning.
- **/calendar**: Temporal visualization and final scheduling.

## 3. Cross-Route Invariants
- A post cannot be scheduled on the **Calendar** unless its status is `Approved`.
- Every post created in **/create** must be associated with a **Campaign**.
- Moving a post in the **Kanban** view must preserve its campaign association.

## 4. Shared Status Semantics
- `Draft`: Post is being edited; not visible in approval queue.
- `Pending`: Post is ready for review; visible in **/approve**.
- `Approved`: Post is locked for editing (except metadata); ready for **/calendar**.
- `Scheduled`: Post has a date/time assigned and is ready for publishing.

## 5. Data Continuity
- **Media Assets:** Must carry from creation through to the final scheduled post.
- **Microcopy:** Labels for statuses must be identical across all routes.
