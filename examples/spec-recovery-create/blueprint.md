---
spec_type: blueprint
spec_id: pulse-create
created: 2026-05-08
status: approved
recovery: true
---

# Blueprint: Pulse /create Route (Spec Recovery)

> **Recovery note:** The *Observed* layout describes what the code renders today. The *Target* layout is the agreed design intent going forward. Both are documented here because the two diverge on the mobile path.

---

## 1. Information Hierarchy

Ranked by user importance (highest first):

1. **Caption input** — primary content being authored; must have full keyboard focus on page load
2. **Publish / Schedule actions** — the goal of the whole screen; must always be in view
3. **Channel selector** — required to publish; cannot be missed
4. **AI Draft button** — high-value secondary accelerator; prominent but not competing with the caption
5. **Media uploader** — optional enrichment; accessible but not prominent
6. **Post preview** — confirmation; useful but not the focus of attention

---

## 2. Layout: Desktop (≥ 1024px)

```
┌─────────────────────────────────────────────────────────────┐
│  App Shell: Left Sidebar + Top Header (not in scope here)   │
├──────────────────────────────┬──────────────────────────────┤
│  FORM PANEL (60%)            │  PREVIEW PANEL (40%)         │
│                              │                              │
│  ┌────────────────────────┐  │  ┌────────────────────────┐  │
│  │ Page heading           │  │  │ "Post Preview"         │  │
│  │ "Create Post"          │  │  │                        │  │
│  └────────────────────────┘  │  │  [Channel preview      │  │
│                              │  │   tabs — one per       │  │
│  ┌────────────────────────┐  │  │   selected channel]    │  │
│  │ Channel Selector       │  │  │                        │  │
│  │ [badge] [badge] [+]    │  │  │  [Preview card         │  │
│  └────────────────────────┘  │  │   renders caption +    │  │
│                              │  │   media thumbnail]     │  │
│  ┌────────────────────────┐  │  │                        │  │
│  │ Caption Input          │  │  └────────────────────────┘  │
│  │ (textarea, 6 rows min) │  │                              │
│  │                 240/∞  │  │                              │
│  └────────────────────────┘  │                              │
│                              │                              │
│  [✦ Generate AI draft]       │                              │
│                              │                              │
│  ┌────────────────────────┐  │                              │
│  │ Media Uploader         │  │                              │
│  │ [Drop zone / browse]   │  │                              │
│  └────────────────────────┘  │                              │
│                              │                              │
│  ────────────────────────    │                              │
│  [Save draft]  [Schedule ▾] [Publish →]                     │
│                              │                              │
└──────────────────────────────┴──────────────────────────────┘
```

**Panel ratio:** 60 / 40 (form / preview). Minimum form panel width: 480px.

---

## 3. Layout: Mobile (< 768px)

**Observed:** `MobileCreateRedirect` renders a completely separate simplified form at `/create/mobile`.

**Target:** Single responsive layout. The preview panel collapses and is accessible via a "Preview" tab below the form, toggled by a tab bar (Form | Preview). No redirect.

```
┌─────────────────────────────┐
│  [← Back]   Create Post     │
├─────────────────────────────┤
│  [Form tab]  [Preview tab]  │  ← Tab bar (full width)
├─────────────────────────────┤
│  Channel Selector           │
│  [badge] [badge] [+more]    │
├─────────────────────────────┤
│  Caption Input              │
│  (textarea, 4 rows min)     │
│                    240/∞    │
├─────────────────────────────┤
│  [✦ AI Draft]               │
├─────────────────────────────┤
│  Media Uploader             │
│  [Drop zone]                │
├─────────────────────────────┤
│  [Save draft]  [Publish →]  │  ← sticky bottom bar
└─────────────────────────────┘
```

"Schedule" is promoted to a full-screen sheet on mobile (not a modal).

---

## 4. Responsive Behaviour

| Breakpoint | Reflow verb | Key change |
|---|---|---|
| `≥ 1024px` | — | Two-column layout (60/40) |
| `768px–1023px` | resize | Preview panel narrows to 35%; form panel 65% |
| `< 768px` | stack + tab | Preview collapses; tab bar appears; schedule becomes full-screen sheet |
| `< 480px` | collapse | Channel selector scrolls horizontally; media uploader text hidden (icon only) |

---

## 5. Spacing System

All spacing uses the token scale defined in `visual-calibration.md`:
- Between page heading and first section: `space.6` (24px)
- Between form sections: `space.6` (24px)
- Inside sections (label to control): `space.2` (8px)
- Action bar padding: `space.4` (16px) vertical, `space.5` (20px) horizontal
- Panel padding: `space.6` (24px)

---

## 6. Observed vs Target: Key Divergences

| Aspect | Observed | Target |
|---|---|---|
| Layout ratio | 50/50 | 60/40 |
| Mobile | Separate redirect route | Single responsive layout with tab toggle |
| Spacing | Inconsistent (16–32px) | Standardised `space.6` (24px) between sections |
| Surface | Single flat white | Two-surface (base + elevated panels) |
| Action bar | Inline in form scroll | Sticky at form bottom |
