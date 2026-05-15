---
spec_type: screen-spec
spec_id: create-page
based_on: 02-brief.md, 03-visual-calibration.md, 04-blueprint.md
created: 2026-05-07
updated: 2026-05-08
---

# UI Screen Spec — /create

---

## Regions

| Region | Component | Visibility | Z-index / stacking |
|---|---|---|---|
| Header card | Inline JSX in `CreateContentPage` | Always visible | Elevated (`hero-surface`) |
| Mode toggle | Inline JSX in header card | Always visible | Part of header |
| Date entry banner | Inline JSX | Only when `?date=` param present | Below header |
| Dev playground | Inline JSX + `AnimatePresence` | DEV + `?labs=1` only | Above content area |
| AI Mode content | `<AICreateMode>` → `<ProactiveCardStack>` | When `!isHybridManualMode` | Content area |
| QuickCreateDetailModal | `<QuickCreateDetailModal>` | When `selectedQuickSuggestion !== null` | Overlay (Dialog / Drawer) |
| Manual Mode back link | Inline JSX | When `isHybridManualMode` | Above wizard |
| Context strip | Inline JSX + `AnimatePresence` | When `isHybridManualMode && step !== 'setup'` | Above guidance card |
| Step indicator | Inline JSX | When `isHybridManualMode` | Above guidance card, below context strip |
| Step guidance card | `<StepGuidanceCard>` | When `isHybridManualMode` | Top of step content |
| Wizard step | `<StepSetup>` / `<StepIdea>` / `<StepVisuals>` / `<StepFinish>` | When `isHybridManualMode` | Content area |
| PostSummary | `<PostSummary>` | When `step !== 'setup' && step !== 'finish'` | Below wizard step |

---

## Component map

### 1. Header card

| Sub-element | Component | Props / State |
|---|---|---|
| Kicker badge | `.hero-kicker` span | Static: "Seu próximo post" + `<Sparkles>` |
| Page title `<h2>` | Inline JSX | `isHybridManualMode ? 'Monte 1 post com ajuda da IA' : 'Deixe 1 post pronto agora'` |
| Subtitle `<p>` | Inline JSX | AI mode: static description. Manual mode: `Etapa N de M. Você escolhe...` (dynamic step index) |
| Mode toggle | 2× `<button type="button">` | State: `isHybridManualMode` |

### 2. Mode toggle

| Element | Type | State drives |
|---|---|---|
| "Modo IA" | `<button type="button">` | `setIsHybridManualMode(false)` |
| "Montar do zero" | `<button type="button">` | `setIsHybridManualMode(true); if (!wasManual) setStep('setup')` |
| Active indicator | CSS: `bg-background shadow-card` | Applied to active button only |

**Accessibility gap:** No `role="tablist"`, `role="tab"`, or `aria-selected`. See `06-component-specs.md` for fix.

### 3. Step indicator (Manual mode)

| Element | State |
|---|---|
| Step dots (×4) | Current step dot: `bg-primary shadow-glow-primary`; Done: `bg-success/15`; Future: `bg-muted` |
| Connecting lines | Done steps: `bg-success/40`; Remaining: `bg-border` |
| Step label (below dot) | Hidden on `<sm`; visible on `sm:` and above |
| Done steps | Show `<Check>` icon instead of step icon |

### 4. AICreateMode

| Prop | Type | Source |
|---|---|---|
| `suggestions` | `ProactiveSuggestion[]` | `useProactiveSuggestions(projectId)` |
| `onApprove` | `(id, overrides?) => Promise<void>` | `handleCardsApprove` |
| `onSkip` | `(id) => void` | `handleCardsSkip` |
| `onRegenerate` | `(id) => Promise<void>` | `handleCardsRegenerate` |
| `onRefresh` | `(isManual?) => Promise<void>` | `handleCardsRefresh` |
| `onGenerate` | `() => Promise<void>` | `handleCardsGenerate` |
| `isGenerating` | `boolean` | `isProactiveLoading \|\| isAiLoading \|\| isGeneratingCardPlayground` |
| `companyName` | `string` | `project?.name \|\| 'Sua Empresa'` — real data ✓ |
| `isFirstGeneration` | `boolean` | `totalGlobalCount === 0` — real data ✓ |
| `totalCount` | `number` | `proactiveTotalCount` |
| `onOpenDetails` | `(suggestion) => void` | Opens `<QuickCreateDetailModal>` |

**Error boundary:** `AICreateBoundary` wraps `ProactiveCardStack`. On crash: renders "Falha ao carregar ideias prontas" + manual mode fallback text.

**Scale behavior:** `scale-95 md:hover:scale-100` — card stack is slightly scaled down by default on desktop; expands to full size on hover.

### 5. QuickCreateDetailModal

| Element | Type | State |
|---|---|---|
| Format selector (3 buttons) | `<button type="button">` ×3 | `selectedFormat`: `'feed' \| 'stories' \| 'reels'` — required before approve |
| Visual mode toggle | `<button type="button">` ×2 | `visualMode`: `'photo' \| 'card'` — only shown if `imageUrl` present |
| PhoneMockup + PostCanvas | `<PhoneMockup>` | `platform`, `variant` derived from `selectedFormat` |
| Trust reason card | Inline JSX | `getTrustReason(suggestion)` — from `content_details._rationale` or fallback |
| Caption textarea | `<Textarea aria-label="Editar legenda">` | `draftCaption` — initialized from `suggestion.final_copy` |
| Hashtag display | Inline chips | `suggestion.content_details.hashtags` — read-only |
| Date picker card | Popover + Calendar | `draftDate` — initialized from `suggestion.scheduled_date \|\| preferredDate` |
| Edit note card | Inline JSX | Static — "Se quiser, ajuste antes de confirmar" |
| Approve CTA | `<Button>` | `disabled={isSubmitting \|\| !draftCaption.trim() \|\| !selectedFormat}` |
| "Outro caminho" toggle | `<Button variant="ghost">` | `showSecondaryActions` |
| "Ver depois" | `<Button variant="outline">` | Calls `onSkip(id)` → closes modal |
| "Nova ideia" | `<Button variant="outline">` | Calls `onRegenerate(id)` → closes modal |

**Rendering logic:**
- `isMobile \|\| isCoarsePointer` → `<Drawer>` (bottom sheet)
- else → `<Dialog>` (centered, `max-w-5xl`)

**`hasChanges` flag:** `draftCaption !== initialCaption \|\| datesMatch fails \|\| selectedFormat !== persistedFormat` → CTA changes from "Aprovar ideia" to "Salvar e aprovar"

**Approval helper text:** Shows context string based on `automationTier` and `draftDate`. Blocked to "Escolha primeiro se esta ideia vai como feed, story ou reel." when no format selected.

### 6. StepSetup

| Element | Type | State |
|---|---|---|
| Objective cards | `<button>` ×N | `objective` state |
| Platform cards | `<button>` ×3 | `targetPlatform` state |
| Format cards | `<button>` ×N | `postFormat` state; available list from `getAvailableCreateFormats(targetPlatform)` |
| "Continuar" CTA | `<Button>` | `disabled={!objective \|\| !targetPlatform}` |

Derived: `availablePostFormats = getAvailableCreateFormats(targetPlatform)` — format grid updates on platform change.

### 7. StepIdea

| Element | Type | State |
|---|---|---|
| Theme suggestion cards | `<motion.button>` ×N | `selectedTheme`, `theme` state; first card has "IA Recomenda" badge |
| "Resetar" | `<Button variant="ghost">` | Visible only when `theme !== ''` |
| Theme free-text input | `<Input>` | `theme` state — manual override |
| Theme input submit | `<Button>` (arrow icon) | Calls `onSelectTheme(-1)` |
| Copy loading state | Spinner + pulse text | `isAiLoading \|\| isGenerating` |
| Copy suggestion cards | `<button>` ×N | `selectedCopy`, `copy` state |
| Copy textarea | `<Textarea>` | Manual override; clears `selectedCopy` on change |
| "Voltar" | `<Button variant="outline">` | `goBack()` |
| "Próximo: visual" CTA | `<Button>` | `disabled={!theme \|\| (!selectedCopy && !copy.trim())}` |

### 8. StepVisuals

#### 8a. Non-carousel path (feed / story / reel)

| Element | Type | State |
|---|---|---|
| Section heading | `<h4>` | "1. Como este post deve aparecer?" |
| "Usar arquivo seu" button | `<Button variant="ghost">` | Triggers hidden `<input type="file">` |
| — No media — | Tab switcher (2 tabs) | `activeMediaTab`: `'ai-image'` or `'text-card'` |
| AI suggestion buttons | `<motion.button>` ×2 | Shows top 2 of `mediaSuggestions`; triggers `onGenerateImage` |
| Custom image input | `<Input>` + `<Button>` | `mediaDescription` state; generate button disabled when empty |
| Text-card style buttons | `<button>` ×2 | Triggers `onGenerateTextCard(style)` with `'editorial-dark'` or `'minimal-light'` |
| — Media exists — | Media preview | `aspect-[4/5]` or `aspect-[9/16]` per `previewAspectClass` |
| "Remover visual" overlay | `<button aria-label="Remover visual">` | `onClearMediaPreview()` |
| "Transformar em Reel" | `<motion.button>` | Shows when `mediaType === 'image'` + non-reel format; triggers `onGenerateVideo()` |
| Video generation progress | Animated progress bar | Shows when `isVideoGenerating`; `videoGenerationStatus` text |
| "Usar este Reel ✓" | `<Button>` | ⚠️ **NO onClick** — label-capability contract violation |
| "Tentar novamente" | `<Button variant="outline">` | `onGenerateVideo()` |

#### 8b. Carousel path (`isCarouselPost`)

| Element | Type | State |
|---|---|---|
| Section heading | `<h4>` | "1. Seu roteiro está pronto" |
| Bulk generate CTA | `<Button>` | `disabled={allSlidesHaveImages \|\| anySlideGenerating}` |
| Slide cards ×N | `<div>` (not interactive) | `carouselSlides` array |
| Slide role badge | Inline span | `CAROUSEL_ROLE_LABELS[slide.role]` |
| "Imagem pronta ✓" badge | Inline span | Visible when `slide.image_url` |
| Remove slide button | `<Button variant="ghost" aria-label="Remover slide">` | Hidden when slides ≤ 2 |
| Add slide button | `<Button variant="ghost">` | Visible on last card, only when slides < 10 |
| Slide image thumbnail | `aspect-[4/5]` div | `slide.image_url` or loading or empty icon |
| Slide prompt textarea | `<Textarea>` | `slide.prompt_pt` — triggers prompt_en reset on manual edit |
| "Ver raciocínio" accordion | `<button>` | `openRationales` Set — no `aria-expanded` ⚠️ |
| Rationale panel | `<motion.div>` AnimatePresence | `slide.rationale_pt` |
| "Gerar só este slide" | `<Button variant="outline" aria-label={...}>` | `disabled={!slide.prompt_pt.trim()}` |
| "Regerar" | `<Button variant="ghost">` | Shows when `slide.image_url` exists |
| "Remover imagem" | `<Button variant="ghost">` | Shows when `slide.image_url` exists |

#### 8c. Hashtags section (all paths)

| Element | Type | State |
|---|---|---|
| Section heading | `<h4>` | "2. Escolha as hashtags" |
| `<HashtagEditor>` | External component | `sets={hashtagSuggestionSets}`, `value={selectedHashtags}`, `onChange={setSelectedHashtags}` |

#### 8d. Navigation + contextual nudge

| Element | Type | State |
|---|---|---|
| "VOLTAR" | `<Button variant="outline">` | `goBack()` |
| "PRÓXIMO: DECIDIR DESTINO" | `<Button>` | `disabled={!isVisualStepReady}`, `disabled:opacity-40` |
| Missing media nudge | AnimatePresence `<p>` | Visible when `missingMedia` |
| Missing slide images nudge | AnimatePresence `<p>` | Visible when `missingSlideImages` |
| Missing video nudge | AnimatePresence `<p>` | Visible when `missingVideo` |
| Missing hashtags nudge | AnimatePresence `<p>` | Visible when `missingHashtags` |

`isVisualStepReady` = carousel: all slides have `image_url` AND hashtags selected. Reel: `mediaType === 'video'` AND hashtags. Other: `mediaUrl` AND hashtags.

### 9. StepFinish

| Element | Type | State |
|---|---|---|
| Phone mockup (left col) | `<PhoneMockup>` | `platform = targetPlatform === 'youtube' ? 'tiktok' : targetPlatform`; `variant = getPhonePreviewVariant(postFormat)` |
| Media preview in mockup | `<video>` or `<img>` | `isCarouselPost ? carouselSlides[0].image_url : mediaUrl` |
| Carousel slide count badge | Inline overlay | Shows when `isCarouselPost && carouselSlides.length > 0` |
| Caption + hashtag overlay | Absolute bottom gradient | `copy` and `selectedHashtags` |
| "← Voltar" | `<Button variant="outline">` | `onBack()` |
| Tier selector cards ×2 | `<button type="button">` ×2 | `automationTier` state; `ring-2 ring-primary` on selected |
| Date picker trigger | `<Button variant="outline">` | Opens Popover with `<Calendar mode="single">` |
| Hour buttons ×16 | `<button type="button">` | `scheduledHour` state; morning group (06–12) + afternoon/evening group (13–21) |
| Minute buttons ×2 | `<button type="button">` | `scheduledMinute` state: 0 (:00) or 30 (:30) |
| Destination indicator | Inline JSX | Derived from `automationTier` + `scheduledDate` |
| Outcome summary | Inline JSX | 3 text variants based on tier + date |
| Primary save CTA | `<Button>` (`h-14`) | Dynamic label: "Salvar e deixar pronto na agenda" (auto_social) or "Salvar para revisar depois" (draft); calls `handleAddToKanban()` |
| `<PostSummary>` | Sub-component | Rendered below the main grid |

### 10. PostSummary

| Element | Source |
|---|---|
| Objective | `OBJECTIVE_FULL_LABELS[objective]` — never raw enum value |
| Tema | `theme` |
| Mídia | Conditional: carousel slide count / video label / image label / description / "Nenhuma" |
| Texto | `copy.slice(0, 80)...` |
| Hashtags | `selectedHashtags.map(t => '#' + t).join(' ')` |
| Text evaluation panel | Visible when `textEvaluation !== null`; score colors: `success` ≥8, `warning` ≥6, `destructive` <6 |

---

## Data dependencies

| Data | Source | Hook |
|---|---|---|
| `projectId`, `project.name` | Supabase `projects` table | `useProjectCheck()` |
| Proactive suggestions | n8n → `content_calendar` (`kanban_status = 'backlog'`) | `useProactiveSuggestions(projectId)` |
| Token balance | Supabase (server-backed) | `useTokens()` |
| AI themes / copy / media / hashtags | n8n webhook `VITE_N8N_BASE_URL` | `useContentSuggestions()` |
| Text card canvas | Canvas API | `useTextCardCanvas()` |
| AI image generation | n8n → fal.ai | `useContentSuggestions().generateMediaImage()` |
| Video generation | n8n → Veo | `useContentSuggestions().generateMediaVideo()` — status polling via `onStatusChange` callback |
| Media upload | Supabase Storage `content-images` | `uploadLocalPreviewUrl()` |
| DB write | Supabase `content_calendar` INSERT | Direct `supabase.from('content_calendar').insert(...)` |

---

## State machine — Manual Mode

```
[entry] ──► [setup] ──► [idea] ──► [visuals] ──► [finish] ──► [saved]
              ▲           │          │                │
              │      sessionStorage  │           handleAddToKanban()
              │      wizard_step     │           → INSERT content_calendar
              └── goBack() ──────────┘           → resetWizard()

AI trigger points:
  setup → idea:      fetchSuggestions('themes', objective)
  theme selected:    fetchSuggestions('copies', objective, theme)
  idea → visuals:    fetchSuggestions('media', ...) + fetchSuggestions('hashtags', ...)
  visuals (manual):  generateMediaImage(prompt) on demand
  visuals (carousel):generateCarouselSlideImage(slideIndex) per-slide or bulk
  visuals (reel):    generateMediaVideo(imageUrl) after image generated
```

## State machine — AI Mode

```
[entry] ──► [ProactiveCardStack loaded]
              │
              ├── isFirstGeneration → [empty/first-gen state]
              │     └── "Generate" CTA → handleCardsGenerate() → refreshProactive()
              │
              ├── suggestions.length > 0 → [card stack]
              │     ├── onApprove(id) → handleCardsApprove() → approveProactive()
              │     │     └── POST to kanban webhook → card leaves stack
              │     ├── onSkip(id) → skipProactive() → card leaves stack
              │     ├── onRegenerate(id) → refreshProactive()
              │     ├── onOpenDetails(suggestion) → opens QuickCreateDetailModal
              │     │     ├── approve → handleApprove() → POST with overrides
              │     │     ├── skip → handleSkip() → POST skip
              │     │     └── regenerate → handleRegenerate() → refreshProactive()
              │     └── onRefresh(isManual?) → refreshProactive()
              │
              ├── isGenerating → [loading state in ProactiveCardStack]
              │
              └── crash → [AICreateBoundary fallback]
```

---

## Error states

| Error | Trigger | Response |
|---|---|---|
| Token insufficient | `canUse(N) = false` | Toast: "Limite de criação atingido" — blocks action |
| AI fetch failure | `fetchSuggestions` throws | Falls back to locally-generated suggestions (no toast) |
| Image generation fail | `generateMediaImage` throws | Toast: "Erro na geração" |
| Video generation fail | `generateMediaVideo` throws | Toast: "Erro ao gerar Reel" — ⚠️ missing accent on "vídeo" |
| Text card fail | `generateTextCard` throws | Toast: "Erro ao gerar card" — ⚠️ missing accents |
| Save fail | `supabase.insert` throws | Toast: "Erro ao salvar" — ⚠️ missing accents |
| Project not found | `projectId = null` | Toast: "Projeto não encontrado" |
| Media type unknown | `inferMediaTypeFromUrl` returns null | Throws: "Tipo de midia local ausente" (unaccented ⚠️) |
| Unload warning | `isHybridManualMode && step !== 'setup'` | Browser `beforeunload` dialog |
| Modal: no format selected | `!selectedFormat` | Approve CTA disabled + helper text: "Escolha primeiro se esta ideia vai como feed, story ou reel." |

---

## Empty states

| Surface | Condition | Current response |
|---|---|---|
| AI Mode — first generation | `totalGlobalCount === 0` | `isFirstGeneration = true` passed to `ProactiveCardStack` |
| AI Mode — no suggestions | `suggestions.length === 0` | Handled inside `ProactiveCardStack` (not inspected) |
| Theme suggestions | Empty after fetch | Falls back to `getThemeSuggestions(objective)` (local) |
| Copy suggestions | Empty after fetch | Falls back to `generateCopySuggestions(objective, theme)` (local) |
| Slide image (carousel) | `!slide.image_url` | Empty icon `<ImageIcon>` in thumbnail slot |
| Phone mockup (finish) | No media | White text placeholder: "As imagens do carrossel aparecerão aqui" / "Preview da mídia aparecerá aqui" |
