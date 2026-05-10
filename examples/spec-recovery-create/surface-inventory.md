---
spec_type: inventory
spec_id: pulse-app-surface-inventory
created: 2026-05-08
status: approved
surface_type: multi-surface-map
---

# UI Surface Inventory: Pulse

## 1. Purpose
Map the Pulse app into coherent, recoverable scopes before beginning spec recovery. Pulse is a social media scheduling and publishing platform for marketing teams.

## 2. Source evidence
Static source-code inspection of the React/TypeScript front end at commit `a3f9c12`. No live browser access available (app requires SSO).
- `saas_frontend/src/routes/`
- `saas_frontend/src/components/`

## 3. App Shell Scopes
- [x] **Left Sidebar Nav** — owns persistent navigation links (Dashboard, Create, Queue, Analytics, Settings), workspace switcher, and user avatar menu. Active state, collapsed state, and keyboard nav are scoped here.
- [x] **Top Header Bar** — owns the page title, breadcrumb on nested routes, notification bell, and "New Post" shortcut button. Present on all routes.

## 4. Journey Scopes
- [x] **Content Creation Journey** — the cross-route flow from `/create` (drafting) → `/queue` (scheduling) → post publication confirmation. Owns the "save draft / schedule / publish" state machine that spans multiple routes.
- [x] **Approval Journey** — the flow where a Reviewer approves or rejects a post drafted by a Creator. Crosses `/create` → `/review` → `/queue`. Separate from the creation journey but shares the post data model.

## 5. Route-level Scopes
| Route | Description | Priority |
|-------|-------------|----------|
| `/create` | Content creation page — drafting captions, attaching media, selecting channels, and choosing publish/schedule action | **1 — primary** |
| `/queue` | Scheduled posts queue — timeline view, drag-to-reschedule, filter by channel | 2 |
| `/dashboard` | Analytics overview — engagement metrics, best-time recommendations | 3 |
| `/review` | Post approval view for Reviewer role | 4 |
| `/settings` | Workspace and account settings | 5 |

## 6. Sub-surface Scopes
| Sub-surface | Parent route | User job | States | Component candidates |
|---|---|---|---|---|
| **AI Draft Panel** | `/create` | Generate a caption draft using AI so the user has a starting point instead of a blank input | idle, generating, success, error, rate-limited | `AiDraftButton`, `AiSuggestionCard` |
| **Channel Selector** | `/create` | Choose which social channels to publish to | unselected, single-selected, multi-selected, channel-error | `ChannelBadge`, `ChannelPicker` |
| **Media Uploader** | `/create` | Attach images or video to the post | idle, uploading, upload-success, upload-error, size-limit-exceeded | `MediaDropzone`, `MediaThumbnail` |
| **Schedule Modal** | `/create` | Pick publish date/time without leaving the create flow | closed, open, date-selected, conflict-warning | `DateTimePicker`, `ScheduleConflictBanner` |
| **Post Preview** | `/create` | See how the post will appear on each selected channel | loading, preview-ready, unsupported-channel | `PostPreviewCard` |

## 7. Surface Status Table
| Surface | Type | Status | Existing spec? | Recommended next skill |
|---|---|---|---|---|
| `/create` | route | pending | no | ui-inspector |
| AI Draft Panel | sub-surface | pending | no | ui-inspector |

## 8. Recommended Specification Order
1. **`/create` Route** — the highest-value screen; almost all other journeys originate here. Spec recovery risk is highest here due to the divergent mobile/desktop implementations.
2. **AI Draft Panel (sub-surface)** — has an undocumented timeout and rate-limit behaviour; recovery should clarify these before code is refactored.
3. **Channel Selector (sub-surface)** — ordering logic is disputed (alphabetical vs most-used); needs a target decision.
4. **Content Creation Journey** — after the `/create` route is specified, document the state machine that connects it to `/queue`.
5. **`/queue` Route** — simpler layout; less urgent but needed before v2 redesign.

## 9. Next-skill routing
Run `ui-inspector` on the `/create` route to gather as-built evidence.

## 10. Open Questions / Ambiguities
- The App Shell left nav collapses on tablet, but the collapse trigger and breakpoint are inconsistent across routes. Unclear whether this is intentional or a drift. Flag for App Shell spec.
2. The `/review` route is only accessible to users with the `reviewer` role. Its spec should be treated as a separate package from `/create` even though they share the post data model.
3. Three component files use different icon libraries (`heroicons`, `lucide-react`, and inline SVGs). The inventory notes this but defers the decision to the system spec.

## 11. Deprecated or duplicate inventory files
- `inventory.md` → deprecated; use this file.
