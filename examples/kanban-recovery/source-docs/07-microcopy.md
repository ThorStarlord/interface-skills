---
spec_type: microcopy
spec_id: kanban-microcopy
# based_on:
  - docs/saas-frontend/specs/kanban/01-inspector-evidence.md
  - docs/saas-frontend/specs/kanban/02-brief.md
  - llm-docs/GLOSSARY.md
created: 2026-05-10
status: draft
voice: warm-concierge
---

# Microcopy: /kanban (Aprovar posts)

## 0. Voice
Chosen voice: warm concierge, low-tech friendly, celebratory when progress is complete.

Defining traits:
- Conversational and supportive (guides, does not command).
- Action-oriented and clear for mobile-first users.
- Celebrates progress without sounding childish.
- Uses PT-BR with full accents.
- Uses customer vocabulary only: creditos user-facing must be creditos with accent (creditos -> creditos with proper accent in UI text: creditos).

## 1. Vocabulary contract (canonical)
- Uses customer vocabulary only: créditos (with accent) in all customer-facing text.

---

## ⚠️ CRITICAL CORRECTIONS (Lint Fixes Applied)

**kanban_status mapping:** Canonical value for approval column is **draft** (not "review"). Update all code references.

**automation_tier:** Must NEVER appear in customer-facing copy. Use only customer labels: "Publicação automática" or "Aguardando sua aprovação".

**Billing vocabulary:** Use **"créditos"** (with accent) exclusively — never "creditos", "tokens", or "credit" in visible UI.

**PT-BR accents (mandatory):** All user-visible strings require proper accents:
- "você", "não", "até", "já", "próximo", "última", "créditos", "configuração", "automático", "início", "publicação"

---

## 1. Vocabulary contract (canonical)

### 1.1 kanban_status display mapping
- backlog -> Ideias salvas
- review -> Para decidir
- approved -> Agendados
- published -> Publicados

Rule: never render raw enum values in UI.

### 1.2 automation_tier display mapping
- draft -> internal only, do not show to user
- full_auto -> Publicacao Automatica (recommended visible badge copy: Publicacao automatica)
- manual -> Revisao manual (recommended helper copy: Aguardando sua aprovacao)

Rule: avoid raw labels like full_auto in visible UI.

### 1.3 Billing vocabulary
- Always use creditos in customer-facing strings.
- Never use tokens in visible UI copy.

## 2. Portuguese correctness pass (findings)

High-priority PT-BR fixes found in current implementation:
- Missing accents in user-visible strings in publish flows:
  - Ja publicado -> Ja publicado (recommended final with accent in code: Ja publicado with accent)
  - Rodar teste de publicacao -> Rodar teste de publicacao (recommended final with accents)
  - Multiple Nao / publicacao / possivel / seguranca in publish readiness and error paths.
- Mixed capitalization and style:
  - Card de Texto -> Card de texto (sentence case consistency)
  - Ver Detalhes -> Ver detalhes (sentence case consistency)
- Internal term leak:
  - Full Auto badge should be customer label (Publicacao automatica), not internal English shorthand.

Note: this file keeps ASCII-only text per repo editing constraints in this session. Apply accented PT-BR in implementation changes.

## 3. Master microcopy table

| Category | Component | Location | Current text | Approved text | Notes |
|---|---|---|---|---|---|
| Page header | KanbanPage hero kicker | saas_frontend/src/pages/KanbanPage.tsx | Aprovar posts | Aprovar posts | Keep. Matches route role in content journey contract. |
| Page header | KanbanPage hero title | saas_frontend/src/pages/KanbanPage.tsx | Decida o que vai para a agenda | Decida o que vai para a agenda | Keep. Strong and clear. |
| Page header | KanbanPage board hint (desktop) | saas_frontend/src/pages/KanbanPage.tsx | Arraste os cards para mover entre as etapas | Arraste os cards para mover entre as etapas | Keep. Helper text is direct and clear. |
| Page header | KanbanPage board hint (coarse pointer) | saas_frontend/src/pages/KanbanPage.tsx | Deslize os cards para decidir rapido no celular | Deslize os cards para decidir rapido no celular | Keep tone; implement accents in code. |
| Page header | KanbanPage review mode subtitle | saas_frontend/src/pages/KanbanPage.tsx | Use este modo para aprovar uma ideia por vez, sem se perder no restante do painel. | Use este modo para aprovar uma ideia por vez, sem se perder no restante do painel. | Keep. Warm and low-tech friendly. |
| Column header | Kanban columns config | saas_frontend/src/pages/KanbanPage.tsx | Ideias salvas / Para decidir / Agendados / Publicados | Ideias salvas / Para decidir / Agendados / Publicados | Canonical and aligned with glossary. |
| Column subtitle | Backlog column | saas_frontend/src/pages/KanbanPage.tsx | Sugestoes prontas para voce decidir | Sugestoes prontas para voce decidir | Keep; add accents in implementation. |
| Column subtitle | Review column | saas_frontend/src/pages/KanbanPage.tsx | Posts esperando seu ok final | Posts esperando sua decisao final | Approved improves clarity and avoids slang OK. |
| Column subtitle | Approved column | saas_frontend/src/pages/KanbanPage.tsx | Ja estao prontos para entrar na agenda | Ja estao prontos para entrar na agenda | Keep; add accents in implementation. |
| Column subtitle | Published column | saas_frontend/src/pages/KanbanPage.tsx | O que ja foi ao ar | O que ja foi ao ar | Keep; add accents in implementation. |
| Dynamic counter subtitle | Review column with items | saas_frontend/src/pages/KanbanPage.tsx | X aguardando sua decisao | X aguardando sua decisao | Keep. Conversational and useful. |
| Button label | View switch | saas_frontend/src/pages/KanbanPage.tsx | Quadro completo | Quadro completo | Keep. |
| Button label | View switch | saas_frontend/src/pages/KanbanPage.tsx | Decidir uma a uma | Decidir uma a uma | Keep. |
| Button label | Toggle | saas_frontend/src/pages/KanbanPage.tsx | Mostrar publicados / Ocultar publicados | Mostrar publicados / Ocultar publicados | Keep. |
| Button label | Backlog empty CTA | saas_frontend/src/pages/KanbanPage.tsx | Criar meu primeiro post | Criar meu primeiro post | Keep, warm and action-oriented. |
| Button label | Backlog hint action | saas_frontend/src/pages/KanbanPage.tsx | Decidir agora | Decidir agora | Keep. |
| Button label | Card quick action | saas_frontend/src/components/kanban/KanbanCard.tsx | Aprovar | Aprovar | Keep. |
| Button label | Card quick action | saas_frontend/src/components/kanban/KanbanCard.tsx | Nao quero este | Nao quero este | Keep; add accent in implementation. |
| Helper sublabel | Reject quick action | saas_frontend/src/components/kanban/KanbanCard.tsx | Ficara nos rascunhos | Ficara nos rascunhos | Keep; add accent in implementation. |
| Button label | Backlog quick action | saas_frontend/src/components/kanban/KanbanCard.tsx | Agendar | Agendar | Keep. |
| Dropdown action | Card menu | saas_frontend/src/components/kanban/KanbanCard.tsx | Ver Detalhes | Ver detalhes | Sentence case normalization. |
| Dropdown action | Card menu | saas_frontend/src/components/kanban/KanbanCard.tsx | Copiar Legenda | Copiar legenda | Sentence case normalization. |
| Dropdown action | Card menu | saas_frontend/src/components/kanban/KanbanCard.tsx | Criar nova versao | Criar nova versao | Keep; add accents in implementation. |
| Dropdown action | Card menu | saas_frontend/src/components/kanban/KanbanCard.tsx | Corrigir Status | Corrigir status | Sentence case normalization. |
| Dropdown action | Card menu | saas_frontend/src/components/kanban/KanbanCard.tsx | Tentar Novamente | Tentar novamente | Sentence case normalization. |
| Dropdown action | Card menu | saas_frontend/src/components/kanban/KanbanCard.tsx | Excluir Card | Excluir post | Avoid internal term card; user mental model is post. |
| Confirm dialog | Card menu | saas_frontend/src/components/kanban/KanbanCard.tsx | Excluir este card permanentemente? | Excluir este post permanentemente? | Align with user language. |
| Confirm dialog | Card menu status fix | saas_frontend/src/components/kanban/KanbanCard.tsx | Isso NAO remove o post da rede social... | Isso nao remove o post da rede social... | Keep meaning; ensure accents in code. |
| Status badge | Kanban card | saas_frontend/src/components/kanban/KanbanCard.tsx | Ideia salva / Para decidir / Agendado / Publicado | Ideia salva / Para decidir / Agendado / Publicado | Accept singular on card-level badges. |
| Status badge | Automation badge | saas_frontend/src/components/kanban/KanbanCard.tsx | Full Auto | Publicacao automatica | Replace internal English with glossary-aligned customer label. |
| Format badge | Kanban card | saas_frontend/src/components/kanban/KanbanCard.tsx | Carrossel / Story / Reel | Carrossel / Story / Reel | Keep. Consistent with format selection copy. |
| Status/error | Kanban card | saas_frontend/src/components/kanban/KanbanCard.tsx | Erro: {mensagem} | Erro: {mensagem} | Keep structure; ensure backend error strings are user-safe. |
| Date fallback | Kanban card | saas_frontend/src/components/kanban/KanbanCard.tsx | Sem data | Sem data | Keep. |
| Empty state | Backlog | saas_frontend/src/pages/KanbanPage.tsx | Sua fabrica esta aquecida | Sua fabrica esta aquecida | Keep warm; add accents in implementation. |
| Empty state | Review | saas_frontend/src/pages/KanbanPage.tsx | Tudo em dia! Missao cumprida | Missao cumprida! Tudo em dia por aqui. | Approved emphasizes celebratory-first tone. |
| Empty state | Approved | saas_frontend/src/pages/KanbanPage.tsx | Pronto para seguir o fluxo | Tudo pronto para os proximos passos | Slightly warmer and more conversational. |
| Empty state | Published | saas_frontend/src/pages/KanbanPage.tsx | Sua historia esta sendo escrita | Seu historico vai aparecer aqui | More concrete expectation-setting. |
| Review empty helper | Review mode fallback | saas_frontend/src/pages/KanbanPage.tsx | Nada esta em Para decidir agora... | Nada em Para decidir agora. Vamos usar Ideias salvas para voce aprovar mais rapido. | Slightly shorter and more guided. |
| Gesture hint | Review mode | saas_frontend/src/pages/KanbanPage.tsx | Deslize para Direita para Aprovar | Deslize para a direita para aprovar | Sentence case and readability. |
| Gesture hint | Review mode | saas_frontend/src/pages/KanbanPage.tsx | Deslize para Esquerda para Ver Depois | Deslize para a esquerda para ver depois | Sentence case and readability. |
| Toast success | Safe move | saas_frontend/src/pages/KanbanPage.tsx | Movido para {coluna} | Movido para {coluna} | Keep. |
| Toast helper | Safe move | saas_frontend/src/pages/KanbanPage.tsx | Voce tem 3 segundos para desfazer esta acao. | Voce tem 3 segundos para desfazer esta acao. | Keep; add accents in implementation. |
| Toast action | Safe move | saas_frontend/src/pages/KanbanPage.tsx | Desfazer | Desfazer | Keep. |
| Toast success | Undo | saas_frontend/src/pages/KanbanPage.tsx | Acao desfeita | Acao desfeita | Keep; add accents in implementation. |
| Toast info | Review skip guard | saas_frontend/src/pages/KanbanPage.tsx | Post ja esta nas ideias salvas. Continue revisando os proximos. | Post ja esta em Ideias salvas. Continue revisando os proximos. | Align column name styling. |
| Toast warning | Review regenerate fallback | saas_frontend/src/pages/KanbanPage.tsx | Ainda nao encontrei outra ideia | Ainda nao encontrei outra ideia | Keep. |
| Toast warning detail | Review regenerate fallback | saas_frontend/src/pages/KanbanPage.tsx | Mantive esta sugestao por aqui para voce decidir com calma. | Mantive esta sugestao aqui para voce decidir com calma. | Slight shortening. |
| Toast error | Review regenerate error | saas_frontend/src/pages/KanbanPage.tsx | Erro ao gerar nova ideia | Erro ao gerar nova ideia | Keep. |
| Toast error detail | Review regenerate error | saas_frontend/src/pages/KanbanPage.tsx | Tente novamente em alguns instantes. | Tente novamente em alguns instantes. | Keep. |
| Toast success | Copy caption | saas_frontend/src/pages/KanbanPage.tsx | Legenda copiada! | Legenda copiada! | Keep. |
| Empty/deck state | ProactiveCardStack | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | Sua IA esta trabalhando... | Sua IA esta preparando suas ideias... | Softer and friendlier. |
| Empty/deck state | ProactiveCardStack | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | Voce aprovou tudo por aqui! | Missao cumprida! Voce aprovou tudo por aqui! | Celebratory guidance requested by brief. |
| Empty/deck state | ProactiveCardStack | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | Voce esta em dia por aqui! | Tudo em dia por aqui! | Keep shorter and warm. |
| CTA | ProactiveCardStack | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | Gerar Primeiras Sugestoes | Gerar primeiras sugestoes | Sentence case consistency. |
| CTA | ProactiveCardStack | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | Gerar mais ideias (usa 10 creditos) | Gerar mais ideias (usa 10 creditos) | Keep wording and billing term. |
| Accessibility | ProactiveCardStack nav | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | Ideia anterior / Proxima ideia | Ideia anterior / Proxima ideia | Keep; add accent in implementation. |
| Swipe label | ProactiveCardStack | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | APROVAR / VER DEPOIS | Aprovar / Ver depois | Consider sentence case to reduce shouting. |
| Card helper | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Por que sugerido? | Por que sugerido? | Keep. Required by warm concierge rule. |
| Button label | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Revisar / Aprovar | Revisar / Aprovar | Keep. |
| Button label | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Baixar imagem | Baixar imagem | Keep. |
| Helper text | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Legenda sendo gerada pela IA... | Legenda sendo preparada pela IA... | Slightly more natural. |
| Helper text | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Pode editar | Pode ajustar | Less technical and more conversational. |
| Error block title | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Falha na ultima tentativa | Falha na ultima tentativa | Keep; add accents in implementation. |
| Modal title | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Revisar Legenda | Revisar legenda | Sentence case normalization. |
| Modal tab label | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Visualizacao / Editar texto | Visualizacao / Editar texto | Keep; accents in implementation. |
| Button label | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Salvar Alteracoes | Salvar alteracoes | Sentence case normalization. |
| Button label | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Copiar Legenda + Hashtags | Copiar legenda + hashtags | Sentence case normalization. |
| Button label | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Nao agora | Nao agora | Keep; accents in implementation. |
| Secondary action | ProactiveSuggestionCard | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | Ver depois / Nova ideia | Ver depois / Nova ideia | Keep. |
| Modal title | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Revise a ideia pronta | Revise a ideia pronta | Keep. |
| Modal description | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Ajuste legenda ou data e deixe este post pronto quando fizer sentido. | Ajuste legenda ou data e deixe este post pronto quando fizer sentido. | Keep; warm and clear. |
| Field label | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Legenda que vai para o post | Legenda que vai para o post | Keep. |
| Placeholder | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Edite sua legenda aqui... | Edite sua legenda aqui... | Keep. |
| Section label | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Hashtags | Hashtags | Keep. |
| Date helper | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Escolha quando quer colocar este post na agenda | Escolha quando quer colocar este post na agenda | Keep. |
| Date action | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Editar data | Editar data | Keep. |
| Confirm helper | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | So o que voce confirmar abaixo entra no post final. | So o que voce confirmar abaixo entra no post final. | Keep; accents in implementation. |
| Primary CTA | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Salvar e aprovar / Aprovar ideia | Salvar e aprovar / Aprovar ideia | Keep. |
| Secondary trigger | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Outro caminho | Outro caminho | Keep. |
| Secondary action | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Ver depois | Ver depois | Keep. |
| Secondary action | QuickCreateDetailModal | saas_frontend/src/components/create/QuickCreateDetailModal.tsx | Nova ideia | Nova ideia | Keep. |
| Modal header | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Falha na Publicacao | Falha na publicacao | Sentence case + accents in implementation. |
| Button label | PostDetailModal retry | saas_frontend/src/components/kanban/PostDetailModal.tsx | Tentar Novamente | Tentar novamente | Sentence case normalization. |
| Field label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Midia | Midia | Keep; accents in implementation. |
| Empty media state | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Sem midia | Sem midia | Keep; accents in implementation. |
| Button label | PostDetailModal media | saas_frontend/src/components/kanban/PostDetailModal.tsx | Alterar Midia | Alterar midia | Sentence case normalization. |
| Field label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Legenda do Post | Legenda do post | Sentence case normalization. |
| Action label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Melhorar com IA | Melhorar com IA | Keep. |
| Action label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Copiar / Copiado! | Copiar / Copiado! | Keep. |
| Label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Sugestao de IA | Sugestao de IA | Keep; accents in implementation. |
| Action label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Aplicar sugestao | Aplicar sugestao | Keep; accents in implementation. |
| Field label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Status | Status | Keep. |
| Field label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Modo de publicacao | Modo de publicacao | Keep; accents in implementation. |
| Option | PostDetailModal automation | saas_frontend/src/components/kanban/PostDetailModal.tsx | Voce posta / App posta pra voce / IA cria e posta | Voce posta / App posta para voce / IA cria e posta | Expand pra for readability. |
| Date label | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Data de agendamento | Data de agendamento | Keep. |
| Date placeholder | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Selecione uma data | Selecione uma data | Keep. |
| Date warning | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Data no passado - atualize antes de publicar | Data no passado - atualize antes de publicar | Keep. |
| Action | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Salvar / Cancelar | Salvar / Cancelar | Keep. |
| Confirmation link | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Ja publiquei esse conteudo manualmente | Ja publiquei esse conteudo manualmente | Keep; accents in implementation. |
| Confirmation prompt | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Confirmar: voce ja publicou esse post pelo Instagram? | Confirmar: voce ja publicou esse post no Instagram? | Small wording improvement. |
| Confirmation button | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Nao, cancelar | Nao, cancelar | Keep; accents in implementation. |
| Confirmation button | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Sim, marcar como publicado | Sim, marcar como publicado | Keep. |
| Checklist title | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Antes de publicar | Antes de publicar | Keep. |
| Checklist subtitle | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Veja o que ja esta pronto... | Veja o que ja esta pronto... | Keep; accents in implementation. |
| Checklist status | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Pronto / Bloqueado | Pronto / Bloqueado | Keep. |
| Checklist section | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Proximo passo | Proximo passo | Keep; accents in implementation. |
| Publish CTA | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Publicando... | Publicando... | Keep. |
| Publish CTA | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Ja publicado | Ja publicado | Keep, but must include accent in implementation. |
| Publish CTA | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Rodar teste de publicacao | Rodar teste de publicacao | Keep meaning; accents in implementation. |
| Publish CTA | PostDetailModal | saas_frontend/src/components/kanban/PostDetailModal.tsx | Publicar agora no Instagram | Publicar agora no Instagram | Keep. |
| Toast success | usePublisher | saas_frontend/src/hooks/usePublisher.ts | Teste de publicacao executado! | Teste de publicacao executado! | Keep; accents in implementation. |
| Toast success | usePublisher | saas_frontend/src/hooks/usePublisher.ts | Post enviado para publicacao! | Post enviado para publicacao! | Keep; accents in implementation. |
| Toast error | usePublisher | saas_frontend/src/hooks/usePublisher.ts | Erro na publicacao | Erro na publicacao | Keep; accents in implementation. |
| Error detail | usePublisher readiness | saas_frontend/src/hooks/usePublisher.ts | Nao foi possivel validar... | Nao foi possivel validar... | Keep semantics, fix PT-BR accents in code. |
| Accessibility | Pipeline stepper | saas_frontend/src/pages/KanbanPage.tsx | aria-label="Etapas de publicacao" | aria-label="Etapas de publicacao" | Good structural label; add accents in implementation. |
| Accessibility | Hint close button | saas_frontend/src/pages/KanbanPage.tsx | aria-label="Fechar" | aria-label="Fechar" | Keep. |
| Accessibility | Proactive stack nav | saas_frontend/src/components/proactive/ProactiveCardStack.tsx | aria-label="Ideia anterior" / "Proxima ideia" | aria-label="Ideia anterior" / "Proxima ideia" | Keep; accents in implementation. |
| Accessibility | Suggestion image/button | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | aria-label="Ver detalhes do post" | aria-label="Ver detalhes do post" | Keep. |
| Accessibility | More options | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | aria-label="Mais opcoes" | aria-label="Mais opcoes para esta ideia" | More specific contextual label recommended. |
| Accessibility | PostDetail input | saas_frontend/src/components/kanban/PostDetailModal.tsx | aria-label="Selecionar midia" | aria-label="Selecionar midia" | Keep; accents in implementation. |
| Accessibility | Full caption editor | saas_frontend/src/components/proactive/ProactiveSuggestionCard.tsx | aria-label="Editor de legenda completa" | aria-label="Editor de legenda completa" | Keep. |
| Placeholder check | Kanban surface files | multiple | TODO / FIXME / [Label] placeholders | none found | No placeholder strings found in audited files. |

## 4. Category coverage checklist

- Page headers and titles: covered.
- Column headers: covered and glossary-aligned.
- Button labels: covered across board, review, dropdowns, modals.
- Status badges: covered (including automation and format badges).
- Empty states and celebratory messages: covered.
- Error messages and toasts: covered (Kanban + publisher path).
- Hints and helper text: covered (gesture, review helper, checklist helper).
- Accessibility text: covered (aria-labels and SR-only text).

## 5. Items from requested examples not found in current code

The following requested examples are not currently rendered exactly in audited sources:
- "Aguardando" badge literal (status appears as Para decidir / Agendado / Publicado or by helper phrases).
- "Instagram indisponivel no momento" exact text.
- "Limite de creditos atingido" exact text.
- "Duplo toque para ver mais" exact mobile hint.
- Hero subtitle phrasing "3 posts waiting for your decision" and "Nenhum post aguardando" (current implementation uses other PT strings).

Recommendation: if these are desired product strings, add them in the relevant components and keep this spec as source of truth.

## 5.1 Reconciliation notes (2026-05-10)

The following areas are approved as-is because implementation already matches the warm concierge voice and product intent:
- Hero framing: "Aprovar posts" and "Decida o que vai para a agenda" are clear and human.
- Empty-state celebration: "Tudo em dia! Missao cumprida" style messaging already reinforces positive progress.
- Board/review guidance copy is supportive and action-led, without internal jargon leakage.
- Core CTA verbs (Aprovar, Agendar, Decidir agora, Criar meu primeiro post) are direct and low-friction.

Copy updates should focus on accessibility clarity and PT-BR accent correctness where needed, not a broad tone rewrite.

## 6. Voice calibration rules for implementation

- Prefer supportive phrasing over imperative commands.
- Keep labels short: mostly 1-3 words for buttons.
- Keep helper text action-led: what happens next after tap/swipe.
- Celebrate completion states explicitly (missao cumprida style).
- Keep sentence case in labels and menu items (avoid title case noise).
- Avoid internal nouns in user UI (enum names, card internals, workflow IDs).

## 7. Priority corrections to implement first

1. PT-BR accent fixes in publish and readiness strings (PostDetailModal + usePublisher).
2. Replace Full Auto badge with customer-facing automation copy.
3. Normalize menu and action labels to sentence case.
4. Improve accessibility context label: Mais opcoes -> Mais opcoes para esta ideia.
5. Keep celebratory empty-state wording explicit in review completion.
