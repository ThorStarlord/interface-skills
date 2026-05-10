import React, { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ToastAction } from '@/components/ui/toast';
import {
  Eye, LayoutDashboard, Library,
  FileText, CalendarClock, CheckCircle2, Clock, X, Info, Sparkles,
} from 'lucide-react';
import { usePublisher } from '@/hooks/usePublisher';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { useDevSettings } from '@/hooks/useDevSettings';

import PostDetailModal from '@/components/kanban/PostDetailModal';
import { KanbanCard } from '@/components/kanban/KanbanCard';
import { QuickCreateDetailModal } from '@/components/create/QuickCreateDetailModal';
import { useToast } from '@/hooks/use-toast';
import { useKanban, KanbanStatus } from '@/hooks/useKanban';
import { useProjectCheck } from '@/hooks/useProjectCheck';
import { getReviewDeckState } from '@/lib/kanbanReviewMode';
import { ContentCalendarItem } from '@/lib/supabase';
import { ProactiveApproveOverrides, ProactiveSuggestion } from '@/hooks/useProactiveSuggestions';
import { normalizePostFormat } from '@/lib/postFormat';
import { Post } from '@/types';
import { ProactiveCardStack } from '@/components/proactive/ProactiveCardStack';
import { N8N_BASE_URL } from '@/lib/config';

interface ColumnConfig {
  id: KanbanStatus;
  title: string;
  subtitle: string;
  emoji: string;
  Icon: React.FC<{ className?: string }>;
}

const columns: ColumnConfig[] = [
  { id: 'backlog', title: 'Ideias salvas', subtitle: 'Sugestões prontas para você decidir', emoji: '📝', Icon: FileText },
  { id: 'review', title: 'Para decidir', subtitle: 'Posts esperando seu ok final', emoji: '👀', Icon: Eye },
  { id: 'approved', title: 'Agendados', subtitle: 'Já estão prontos para entrar na agenda', emoji: '📅', Icon: CalendarClock },
  { id: 'published', title: 'Publicados', subtitle: 'O que já foi ao ar', emoji: '✅', Icon: CheckCircle2 },
];

const safeflowColumns: ColumnConfig[] = columns;

// Stagger animation variants for Kanban columns
const columnVariants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.045 } },
};

// Map a Supabase ContentCalendarItem to the Post type used by PostDetailModal
function toPost(item: ContentCalendarItem): Post {
  const details = item.content_details ?? {};
  return {
    id: item.id,
    title: details.caption || details.brief || item.final_copy?.slice(0, 60) || 'Sem título',
    content: item.final_copy || details.caption || '',
    hashtags: details.hashtags || (item.final_hashtags as string[] | undefined) || [],
    status: kanbanToPostStatus(item.kanban_status),
    platform: item.platform || (details.platform as any) || 'instagram',
    mediaUrl: item.post_preview_url || item.final_video_url || undefined,
    mediaType: item.final_video_url ? 'video' : 'image',
    scheduledDate: item.scheduled_date ? new Date(item.scheduled_date) : undefined,
    createdAt: new Date(item.created_at),
    updatedAt: new Date(item.updated_at),
    lastError: item.last_error,
    automationTier: item.automation_tier as any,
  };
}

function kanbanToPostStatus(ks: KanbanStatus): Post['status'] {
  switch (ks) {
    case 'backlog': return 'draft';
    case 'review': return 'review';
    case 'approved': return 'scheduled';
    case 'published': return 'published';
    default: return 'draft';
  }
}

const EMPTY_STATE: Record<KanbanStatus, { headline: string; hint: string }> = {
  backlog: {
    headline: 'Sua fábrica está aquecida',
    hint: 'A IA vai sugerir ideias baseadas no seu negócio. Você também pode criar um post do zero quando quiser.',
  },
  review: {
    headline: 'Tudo em dia! Missão cumprida 🎉',
    hint: 'Nenhum post pendente nesta fase. Você revisou tudo e deixou a fila limpa. Excelente gestão!',
  },
  approved: {
    headline: 'Pronto para seguir o fluxo',
    hint: 'A agenda está organizada. Assim que um post for aprovado, ele aparecerá aqui aguardando a publicação.',
  },
  published: {
    headline: 'Sua história está sendo escrita',
    hint: 'Ainda não há posts publicados por aqui. Quando o primeiro for ao ar, ele ficará guardado como referência.',
  },
  archived: { headline: 'Tudo limpo por aqui', hint: '' },
};

// ─── Pipeline Stepper ─────────────────────────────────────────────────────────
const PIPELINE_STEPS: { id: KanbanStatus; label: string }[] = [
  { id: 'backlog', label: 'Ideias salvas' },
  { id: 'review', label: 'Para decidir' },
  { id: 'approved', label: 'Agendados' },
  { id: 'published', label: 'Publicados' },
];

function PipelineStepper({ activeTab }: { activeTab: KanbanStatus }) {
  const activeIndex = PIPELINE_STEPS.findIndex(s => s.id === activeTab);
  return (
    <div className="flex items-center w-full mb-4 px-1" aria-label="Etapas de publicação">
      {PIPELINE_STEPS.map((step, i) => {
        const isActive = i === activeIndex;
        const isPast = i < activeIndex;
        return (
          <React.Fragment key={step.id}>
            <div className="flex flex-col items-center gap-1 shrink-0">
              <div className={cn(
                'w-2 h-2 rounded-full transition-all duration-200',
                isActive && 'bg-primary scale-125',
                isPast && 'bg-primary/40',
                !isActive && !isPast && 'bg-border'
              )} />
              <span className={cn(
                'text-[9px] font-bold uppercase tracking-wider transition-colors duration-200',
                isActive && 'text-primary',
                isPast && 'text-primary/50',
                !isActive && !isPast && 'text-muted-foreground/50'
              )}>
                {step.label}
              </span>
            </div>
            {i < PIPELINE_STEPS.length - 1 && (
              <div className={cn(
                'flex-1 h-px mx-1.5 transition-colors duration-200',
                isPast ? 'bg-primary/30' : 'bg-border/50'
              )} />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}

function KanbanCardSkeleton() {
  return (
    <div className="rounded-2xl border border-border/40 bg-card p-3 space-y-3 animate-pulse motion-reduce:animate-none">
      <div className="aspect-[4/3] rounded-xl bg-muted/60" />
      <div className="space-y-2">
        <div className="h-3 bg-muted/60 rounded-full w-3/4" />
        <div className="h-3 bg-muted/60 rounded-full w-1/2" />
      </div>
      <div className="flex items-center justify-between pt-1">
        <div className="h-5 w-16 bg-muted/60 rounded-full" />
        <div className="h-6 w-6 bg-muted/60 rounded-lg" />
      </div>
    </div>
  );
}

function EmptyColumnState({ columnId, emoji }: { columnId: KanbanStatus; emoji: string }) {
  const { headline, hint } = EMPTY_STATE[columnId];
  return (
    <div className="flex flex-col items-center justify-center min-h-[180px] border border-dashed border-border/40 rounded-2xl bg-muted/20 text-center px-5 py-6 gap-2">
      <span className="text-3xl">{emoji}</span>
      <p className="text-sm font-semibold text-foreground/80">{headline}</p>
      <p className="text-xs text-muted-foreground leading-relaxed max-w-[220px]">{hint}</p>
      {columnId === 'backlog' && (
        <Link to="/create" className="mt-2">
          <Button size="sm" variant="outline" className="rounded-full font-semibold text-xs gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            Criar meu primeiro post
          </Button>
        </Link>
      )}
    </div>
  );
}

const KanbanPage = () => {
  const navigate = useNavigate();
  const { projectId, project } = useProjectCheck();
  const { isSafeFlow } = useDevSettings();
  const {
    isLoading,
    moveCard: baseMoveCard,
    updateCard,
    duplicateCard,
    deleteCard,
    getColumnPosts,
    refreshPosts
  } = useKanban(projectId ?? undefined);
  const [hidePublished, setHidePublished] = useState(() => sessionStorage.getItem('kanban_hide_published') === 'true');
  const [hintDismissed, setHintDismissed] = useState(() => sessionStorage.getItem('kanban_hint_dismissed') === 'true');
  const dismissHint = () => { sessionStorage.setItem('kanban_hint_dismissed', 'true'); setHintDismissed(true); };
  const [draggedItem, setDraggedItem] = useState<ContentCalendarItem | null>(null);
  const [dropTargetTab, setDropTargetTab] = useState<KanbanStatus | null>(null);
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  const [selectedReviewSuggestion, setSelectedReviewSuggestion] = useState<ProactiveSuggestion | null>(null);
  const [activeTab, setActiveTab] = useState<KanbanStatus>(() => (sessionStorage.getItem('kanban_active_tab') as KanbanStatus) || 'backlog');
  const [viewMode, setViewMode] = useState<'board' | 'review'>(() => {
    const saved = sessionStorage.getItem('kanban_view_mode');
    if (saved === 'board' || saved === 'review') return saved;
    if (typeof window !== 'undefined' && window.matchMedia('(pointer: coarse)').matches) {
      return 'review';
    }
    return 'board';
  });
  const [reviewDeckHiddenIds, setReviewDeckHiddenIds] = useState<string[]>([]);
  const [regeneratingDeckIds, setRegeneratingDeckIds] = useState<string[]>([]);
  useEffect(() => { sessionStorage.setItem('kanban_hide_published', String(hidePublished)); }, [hidePublished]);
  useEffect(() => { sessionStorage.setItem('kanban_active_tab', activeTab); }, [activeTab]);
  useEffect(() => { sessionStorage.setItem('kanban_view_mode', viewMode); }, [viewMode]);
  const [pendingUpdate, setPendingUpdate] = useState<{ id: string; to: KanbanStatus } | null>(null);
  const pendingUpdateRef = useRef<{ id: string; to: KanbanStatus } | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const isMounted = useRef(true);
  const { toast } = useToast();
  const { retryPublication, isPublishing } = usePublisher();
  const prefersReducedMotion = useReducedMotion();

  // Sync state to ref for unmount cleanup
  useEffect(() => {
    pendingUpdateRef.current = pendingUpdate;
  }, [pendingUpdate]);

  // Handle unmount flush
  useEffect(() => {
    return () => {
      isMounted.current = false;
      if (timerRef.current && pendingUpdateRef.current) {
        clearTimeout(timerRef.current);
        baseMoveCard(pendingUpdateRef.current.id, pendingUpdateRef.current.to);
      }
    };
  }, [baseMoveCard]);
  const [isLgUp, setIsLgUp] = useState(() => {
    if (typeof window === 'undefined') return true;
    return window.matchMedia('(min-width: 1024px)').matches;
  });
  const [isCoarsePointer, setIsCoarsePointer] = useState(() => {
    if (typeof window === 'undefined') return false;
    return window.matchMedia('(pointer: coarse)').matches;
  });
  const suppressClickByIdRef = useRef<Record<string, boolean>>({});

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const mql = window.matchMedia('(min-width: 1024px)');
    const update = () => setIsLgUp(mql.matches);
    update();

    if (mql.addEventListener) mql.addEventListener('change', update);
    // eslint-disable-next-line deprecation/deprecation
    else mql.addListener(update);

    return () => {
      if (mql.removeEventListener) mql.removeEventListener('change', update);
      // eslint-disable-next-line deprecation/deprecation
      else mql.removeListener(update);
    };
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const mql = window.matchMedia('(pointer: coarse)');
    const update = () => setIsCoarsePointer(mql.matches);
    update();

    if (mql.addEventListener) mql.addEventListener('change', update);
    // eslint-disable-next-line deprecation/deprecation
    else mql.addListener(update);

    return () => {
      if (mql.removeEventListener) mql.removeEventListener('change', update);
      // eslint-disable-next-line deprecation/deprecation
      else mql.removeListener(update);
    };
  }, []);

  const handleDragStart = (item: ContentCalendarItem) => {
    setDraggedItem(item);
    setDropTargetTab(null);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const moveCard = (id: string, to: KanbanStatus) => {
    if (!isSafeFlow) {
      baseMoveCard(id, to);
      return;
    }

    // Safeflow Move with Undo
    if (pendingUpdate && timerRef.current) {
      clearTimeout(timerRef.current);
      baseMoveCard(pendingUpdate.id, pendingUpdate.to);
    }

    setPendingUpdate({ id, to });

    toast({
      title: `Movido para ${columns.find(c => c.id === to)?.title}`,
      description: (
        <div className="space-y-2">
          <span>Você tem 3 segundos para desfazer esta ação.</span>
          {!prefersReducedMotion && (
            <div className="h-1 rounded-full bg-border/50 overflow-hidden">
              <motion.div
                className="h-full bg-primary/60 rounded-full"
                initial={{ width: '100%' }}
                animate={{ width: '0%' }}
                transition={{ duration: 3, ease: 'linear' }}
              />
            </div>
          )}
        </div>
      ),
      action: (
        <ToastAction
          onClick={() => {
            if (timerRef.current) clearTimeout(timerRef.current);
            setPendingUpdate(null);
            toast({ title: "Ação desfeita", variant: "default" });
          }}
          altText="Desfazer"
        >
          Desfazer
        </ToastAction>
      ),
      duration: 3000,
    });

    timerRef.current = setTimeout(() => {
      baseMoveCard(id, to);
      if (isMounted.current) {
        setPendingUpdate(null);
      }
    }, 3000);
  };

  const handleDrop = (columnId: KanbanStatus) => {
    if (draggedItem) {
      moveCard(draggedItem.id, columnId);
      setDraggedItem(null);
      setDropTargetTab(null);
    }
  };

  const moveToNext = (item: ContentCalendarItem) => {
    if (isSafeFlow && item.kanban_status === 'published') return;
    const statusOrder: KanbanStatus[] = ['backlog', 'review', 'approved', 'published'];
    const currentIndex = statusOrder.indexOf(item.kanban_status);
    if (currentIndex < statusOrder.length - 1) {
      moveCard(item.id, statusOrder[currentIndex + 1]);
    }
  };

  const moveToPrev = (item: ContentCalendarItem) => {
    const statusOrder: KanbanStatus[] = ['backlog', 'review', 'approved', 'published'];
    const currentIndex = statusOrder.indexOf(item.kanban_status);
    if (currentIndex > 0) {
      moveCard(item.id, statusOrder[currentIndex - 1]);
    }
  };

  const suppressClickOnce = (id: string) => {
    suppressClickByIdRef.current[id] = true;
    window.setTimeout(() => {
      delete suppressClickByIdRef.current[id];
    }, 300);
  };

  const handleUpdatePost = (updatedPost: Post) => {
    const postToKanbanStatus = (status: Post['status']): KanbanStatus => {
      switch (status) {
        case 'draft': return 'backlog';
        case 'review': return 'review';
        case 'scheduled': return 'approved';
        case 'published': return 'published';
        default: return 'backlog';
      }
    };

    const updates: Partial<ContentCalendarItem> = {
      final_copy: updatedPost.content,
      final_hashtags: updatedPost.hashtags,
      kanban_status: postToKanbanStatus(updatedPost.status),
      scheduled_date: updatedPost.scheduledDate?.toISOString(),
      automation_tier: updatedPost.automationTier as any,
    };

    updateCard(updatedPost.id, updates);
    setSelectedPost(null);
  };

  const handleReviewDeckSkip = (id: string) => {
    const isReviewItem = reviewItems.some((post) => post.id === id);

    if (isReviewItem) {
      moveCard(id, 'backlog');
      return;
    }

    toast({
      title: 'Post já está nas ideias salvas.',
      description: 'Continue revisando os próximos.',
    });
  };

  const handleReviewDeckRegenerate = async (id: string) => {
    if (regeneratingDeckIds.includes(id)) return;

    setRegeneratingDeckIds((prev) => [...prev, id]);
    setReviewDeckHiddenIds((prev) => (prev.includes(id) ? prev : [...prev, id]));

    try {
      const response = await fetch(`${N8N_BASE_URL}/webhook/2-1-content-generator-manual`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: projectId,
          posts_to_generate: 1,
          kanban_status_override: 'review',
        }),
      });

      if (!response.ok) throw new Error('generation_failed');

      const data = await response.json();

      if (data.success && data.generated_count > 0) {
        await refreshPosts();
      } else {
        toast({
          title: 'Ainda não encontrei outra ideia',
          description: 'Mantive esta sugestão por aqui para você decidir com calma.',
        });
        setReviewDeckHiddenIds((prev) => prev.filter((hiddenId) => hiddenId !== id));
      }
    } catch {
      toast({
        title: 'Erro ao gerar nova ideia',
        description: 'Tente novamente em alguns instantes.',
      });
      setReviewDeckHiddenIds((prev) => prev.filter((hiddenId) => hiddenId !== id));
    } finally {
      setRegeneratingDeckIds((prev) => prev.filter((currentId) => currentId !== id));
    }
  };

  const handleReviewDeckRefresh = async () => {
    setReviewDeckHiddenIds([]);
    await refreshPosts();
  };

  if (isLoading) {
    return (
      <div className="h-full flex flex-col animate-fade-in px-4 md:px-6">
        <div className="mb-6 py-2">
          <div className="h-6 w-32 bg-muted/60 rounded-full animate-pulse" />
          <div className="h-4 w-48 bg-muted/40 rounded-full animate-pulse mt-2" />
        </div>
        <div className="flex-1 overflow-x-auto pb-4">
          <div className="flex gap-4 lg:grid lg:grid-cols-4">
            {[0, 1, 2, 3].map(col => (
              <div key={col} className="w-72 lg:w-auto flex flex-col rounded-2xl">
                <div className="rounded-t-2xl px-4 py-3 border-t border-x border-border/50 bg-muted/30">
                  <div className="h-4 w-24 bg-muted/60 rounded-full animate-pulse" />
                </div>
                <div className="bg-muted/10 rounded-b-2xl p-3 space-y-4 min-h-[500px] border-b border-x border-border/20">
                  {[0, 1, 2].map(i => <KanbanCardSkeleton key={i} />)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const baseColumns = isSafeFlow ? safeflowColumns : columns;
  const activeColumns = hidePublished ? baseColumns.filter(c => c.id !== 'published') : baseColumns;

  const backlogItems = getColumnPosts('backlog').filter(p => (p.kanban_status as any) !== 'archived');
  const reviewItems = getColumnPosts('review').filter(p => (p.kanban_status as any) !== 'archived');
  const visibleBacklogItems = backlogItems.filter((post) => !reviewDeckHiddenIds.includes(post.id));
  const visibleReviewItems = reviewItems.filter((post) => !reviewDeckHiddenIds.includes(post.id));
  const isFirstGeneration = getColumnPosts('published').filter(p => (p.kanban_status as any) !== 'archived').length === 0;
  const columnCounts: Partial<Record<KanbanStatus, number>> = {
    backlog: backlogItems.length,
    review: reviewItems.length,
    approved: getColumnPosts('approved').filter(p => (p.kanban_status as any) !== 'archived').length,
    published: getColumnPosts('published').filter(p => (p.kanban_status as any) !== 'archived').length,
  };
  const reviewDeck = getReviewDeckState(visibleReviewItems, visibleBacklogItems);
  const boardHint = isCoarsePointer
    ? 'Deslize os cards para decidir rápido no celular'
    : isLgUp
      ? 'Arraste os cards para mover entre as etapas'
      : 'Use o quadro para acompanhar o que já foi salvo, aprovado e publicado';

  const handleReviewDeckApprove = async (id: string, overrides?: ProactiveApproveOverrides) => {
    const currentSuggestion = reviewDeck.items.find((item) => item.id === id)
      || (selectedReviewSuggestion?.id === id ? selectedReviewSuggestion : null);

    const updates: Partial<ContentCalendarItem> = {};
    if (typeof overrides?.finalCopy === 'string') {
      updates.final_copy = overrides.finalCopy;
    }
    if (overrides?.scheduledDate) {
      updates.scheduled_date = overrides.scheduledDate instanceof Date
        ? overrides.scheduledDate.toISOString()
        : overrides.scheduledDate;
    }

    const normalizedPostFormat = normalizePostFormat(overrides?.postFormat);
    if (normalizedPostFormat) {
      updates.post_format = normalizedPostFormat;
      updates.content_details = {
        ...(currentSuggestion?.content_details || {}),
        post_format: normalizedPostFormat,
      };
    }

    if (Object.keys(updates).length > 0) {
      await updateCard(id, updates);
    }

    await moveCard(id, 'approved');
    setSelectedReviewSuggestion(null);
  };

  return (
    <div className="h-full flex flex-col animate-fade-in px-4 md:px-6">
      <div className="mb-6 hero-surface rounded-[1.75rem] p-4 md:p-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="hero-kicker">
              <Eye className="w-4 h-4" />
              Aprovar posts
            </span>
            <h2 className="mt-3 text-2xl font-black tracking-tight text-foreground">Decida o que vai para a agenda</h2>
            <p className="text-muted-foreground text-sm mt-1 max-w-xl">
              {viewMode === 'board'
                ? boardHint
                : 'Use este modo para aprovar uma ideia por vez, sem se perder no restante do painel.'}
            </p>
          </div>

          {/* View & Variant Switchers */}
          <div className="flex flex-wrap items-center gap-2 self-start sm:self-center">
          {/* Main View Mode (Board vs Review) */}
          <div className="flex items-center gap-1 bg-muted/50 p-1 rounded-xl border border-border/50">
            <Button
              variant={viewMode === 'board' ? "secondary" : "ghost"}
              size="sm"
              onClick={() => setViewMode('board')}
              className="h-8 rounded-lg gap-2 text-xs font-bold"
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              <span>Quadro completo</span>
            </Button>
            <Button
              variant={viewMode === 'review' ? "secondary" : "ghost"}
              size="sm"
              onClick={() => setViewMode('review')}
              className="h-8 rounded-lg gap-2 text-xs font-bold"
            >
              <Library className="w-3.5 h-3.5" />
              <span>Decidir uma a uma</span>
              {reviewDeck.badgeCount > 0 && reviewDeck.source === 'review' && (
                <span
                  className={cn(
                    'ml-1 rounded-full px-1.5 py-0.5 text-[10px] font-bold',
                    reviewDeck.source === 'review'
                      ? 'bg-warning/20 text-warning'
                      : 'bg-muted-foreground/15 text-muted-foreground',
                  )}
                >
                  {reviewDeck.badgeCount > 20 ? '20+' : reviewDeck.badgeCount}
                </span>
              )}
            </Button>
          </div>

          {/* Hide Published Toggle */}
          <Button
            variant="outline"
            size="sm"
            onClick={() => setHidePublished(h => !h)}
            className="h-8 rounded-xl gap-2 text-xs font-bold"
          >
            {hidePublished ? <Eye className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5 opacity-50" />}
            <span>{hidePublished ? 'Mostrar publicados' : 'Ocultar publicados'}</span>
          </Button>
          </div>
        </div>
      </div>

      {/* Review Mode (Cards Deck) */}
      {viewMode === 'review' && (
        <div className="flex-1 flex flex-col items-center justify-center -mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500 overflow-hidden">
          <div className="w-full max-w-sm">
            <PipelineStepper activeTab={reviewDeck.source === 'review' ? 'review' : 'backlog'} />
            {reviewDeck.source === 'backlog' && (
              <p className="mb-3 text-center text-xs text-muted-foreground">
                Nada está em <strong>Para decidir</strong> agora. Este modo mostra suas ideias salvas para você aprovar mais rápido.
              </p>
            )}
            <ProactiveCardStack
              suggestions={reviewDeck.items.map((post) => ({
                ...post,
                source: post.source || 'proactive_mode',
                isRegenerating: regeneratingDeckIds.includes(post.id),
              }))}
              onApprove={handleReviewDeckApprove}
              onSkip={(id) => { handleReviewDeckSkip(id); if (id === '__legacy_placeholder__') {
                  toast({ title: 'Post já está nas ideias salvas.', description: 'Continue revisando os próximos.' });
                }
              }}
              onRegenerate={async (id) => { await handleReviewDeckRegenerate(id); if (id === '__legacy_placeholder__') {
                toast({ title: 'Em breve', description: 'A geração de nova ideia estará disponível em breve.' });
              }}}
              onRefresh={handleReviewDeckRefresh}
              onGenerate={async () => { navigate('/create'); }}
              onCaptionSave={async (id, caption) => { updateCard(id, { final_copy: caption }); }}
              isGenerating={regeneratingDeckIds.length > 0}
              companyName={project?.name ?? 'Minha empresa'}
              isFirstGeneration={isFirstGeneration}
              onOpenDetails={(suggestion) => setSelectedReviewSuggestion(suggestion)}
            />
          </div>
          {backlogItems.length > 0 && (
            <div className="mt-8 flex flex-col items-center gap-2">
              <p className="text-[10px] font-black text-muted-foreground uppercase tracking-[0.2em] animate-pulse">
                Deslize para <span className="text-success">Direita</span> para Aprovar
              </p>
              <p className="text-[10px] font-black text-muted-foreground uppercase tracking-[0.2em] opacity-50">
                Deslize para <span className="text-destructive">Esquerda</span> para Ver Depois
              </p>
            </div>
          )}
        </div>
      )}

      {/* Board Mode (Standard Kanban) */}
      {viewMode === 'board' && (
        <>
          <PipelineStepper activeTab={activeTab} />

          {/* Backlog hint banner (O1) */}
          {!hintDismissed && backlogItems.length >= 10 && (
            <div className="flex items-center gap-3 mb-4 px-4 py-2.5 bg-info/10 border border-info/20 rounded-xl">
              <Info className="w-4 h-4 text-info shrink-0" />
              <p className="text-xs text-info flex-1">
                Você já tem <strong>{backlogItems.length}</strong> ideias salvas. Use o modo Decidir uma a uma para aprovar mais rápido.
              </p>
              <Button
                size="sm"
                variant="ghost"
                className="h-7 text-xs font-bold text-info hover:bg-info/10 shrink-0"
                onClick={() => setViewMode('review')}
              >
                Decidir agora
              </Button>
              <button
                onClick={dismissHint}
                className="text-info/60 hover:text-info transition-colors shrink-0"
                aria-label="Fechar"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {/* Mobile Tabs Navigation */}
          <div className="flex lg:hidden mb-4 bg-muted/30 p-1 rounded-xl border border-border/50">
            {activeColumns.map((column) => {
              const tabCount = columnCounts[column.id] ?? 0;
              return (
              <button
                key={column.id}
                onClick={() => setActiveTab(column.id)}
                className={cn(
                  "flex-1 py-2 px-1 rounded-lg text-[10px] font-bold uppercase tracking-wider transition-all flex flex-col items-center justify-center gap-1",
                  activeTab === column.id
                    ? "bg-background text-primary shadow-sm ring-1 ring-border/50"
                    : "text-muted-foreground hover:text-foreground",
                  draggedItem && !isCoarsePointer && dropTargetTab === column.id && "ring-2 ring-primary/30 bg-background"
                )}
                onDragEnter={draggedItem && !isCoarsePointer ? () => setDropTargetTab(column.id) : undefined}
                onDragLeave={draggedItem && !isCoarsePointer ? () => setDropTargetTab(null) : undefined}
                onDragOver={draggedItem && !isCoarsePointer ? (e) => { e.preventDefault(); setDropTargetTab(column.id); } : undefined}
                onDrop={draggedItem && !isCoarsePointer ? (e) => { e.preventDefault(); handleDrop(column.id); setActiveTab(column.id); } : undefined}
              >
                <span>{column.emoji}</span>
                <span className="truncate w-full text-center">{column.title}</span>
                {tabCount > 0 && (
                  <span className={cn(
                    'text-[9px] font-black px-1.5 py-0.5 rounded-full leading-none',
                    column.id === 'review' ? 'bg-warning/20 text-warning' : 'bg-muted-foreground/20 text-muted-foreground'
                  )}>
                    {tabCount > 20 ? '20+' : tabCount}
                  </span>
                )}
              </button>
              );
            })}
          </div>

          <div className="flex-1 overflow-x-auto pb-4 custom-scrollbar">
            <div className="flex gap-4 min-w-max lg:min-w-0 lg:grid lg:grid-cols-4 min-w-0 flex-col lg:flex-row">
              {activeColumns.map((column) => {
                // Mobile filtering
                if (activeTab !== column.id && !isLgUp) {
                  return null;
                }

                const columnItems = getColumnPosts(column.id).filter(p => (p.kanban_status as any) !== 'archived');
                const todayEnd = new Date();
                todayEnd.setHours(23, 59, 59, 999);
                const urgentCount = column.id === 'approved'
                  ? columnItems.filter(p => p.scheduled_date && new Date(p.scheduled_date) <= todayEnd).length
                  : 0;

                const cardNodes = columnItems.map((item) => {
                  const post = toPost(item);
                  const effectiveKanbanStatus: KanbanStatus = item.kanban_status;
                  return (
                    <KanbanCard
                      key={item.id}
                      item={item}
                      post={post}
                      effectiveKanbanStatus={effectiveKanbanStatus}
                      columnId={column.id}
                      project={project}
                      isCoarsePointer={isCoarsePointer}
                      isDragging={draggedItem?.id === item.id}
                      isPending={pendingUpdate?.id === item.id}
                      isSafeFlow={isSafeFlow}
                      isPublishing={isPublishing}
                      onDragStart={() => handleDragStart(item)}
                      onDragEnd={() => { setDraggedItem(null); setDropTargetTab(null); }}
                      onSwipeEnd={(info) => {
                        const swipeThreshold = 110;
                        if (info.offset.x > swipeThreshold) {
                          if (isSafeFlow && item.kanban_status === 'published') return;
                          suppressClickOnce(item.id);
                          moveToNext(item);
                        } else if (info.offset.x < -swipeThreshold) {
                          suppressClickOnce(item.id);
                          moveToPrev(item);
                        }
                      }}
                      onClick={() => {
                        if (suppressClickByIdRef.current[item.id]) return;
                        setSelectedPost(post);
                      }}
                      onMoveToNext={() => moveToNext(item)}
                      onMoveCard={(to) => moveCard(item.id, to)}
                      onDelete={() => deleteCard(item.id)}
                      onDuplicate={() => duplicateCard(item.id)}
                      onRetry={() => retryPublication(item.id)}
                      onOpenDetails={() => setSelectedPost(post)}
                      onCopyCaption={() => {
                        navigator.clipboard.writeText(post.content);
                        toast({ title: 'Legenda copiada!' });
                      }}
                    />
                  );
                });

                return (
                  <div
                    key={column.id}
                    className={cn(
                      'w-72 lg:w-auto flex flex-col rounded-2xl transition-all duration-200',
                      dropTargetTab === column.id && !isCoarsePointer && 'shadow-drop-target scale-[1.01]'
                    )}
                    onDragEnter={!isCoarsePointer ? () => setDropTargetTab(column.id) : undefined}
                    onDragLeave={!isCoarsePointer ? (e) => {
                      if (!e.currentTarget.contains(e.relatedTarget as Node)) setDropTargetTab(null);
                    } : undefined}
                    onDragOver={handleDragOver}
                    onDrop={() => handleDrop(column.id)}
                  >
                    {/* Column header */}
                    <div className={cn(
                      'rounded-t-2xl px-4 pt-3 pb-0 flex flex-col border-t border-x',
                      column.id === 'backlog' && 'bg-muted/50 text-muted-foreground border-border/50',
                      column.id === 'review' && 'bg-warning/10 text-warning border-warning/20',
                      column.id === 'approved' && 'bg-info/10 text-info border-info/20',
                      column.id === 'published' && 'bg-success/10 text-success border-success/20'
                    )}>
                      <div className="flex items-center justify-between pb-3">
                        <div className="flex items-center gap-2.5 min-w-0">
                          <div className={cn(
                            'w-7 h-7 rounded-lg flex items-center justify-center shrink-0',
                            column.id === 'backlog'   && 'bg-muted-foreground/15',
                            column.id === 'review'    && 'bg-warning/15',
                            column.id === 'approved'  && 'bg-info/15',
                            column.id === 'published' && 'bg-success/15'
                          )}>
                            <column.Icon className="w-3.5 h-3.5" />
                          </div>
                          <div className="min-w-0">
                            <h3 className="font-bold text-sm uppercase tracking-tight leading-none">{column.title}</h3>
                            <p className="text-[10px] opacity-70 mt-0.5 truncate">
                              {column.id === 'review' && columnItems.length > 0
                                ? `${columnItems.length} aguardando sua decisão`
                                : column.subtitle}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-1 shrink-0">
                          <span className={cn(
                            'px-2 py-0.5 rounded-full text-[10px] font-black',
                            column.id === 'review' && columnItems.length > 0
                              ? 'bg-warning/20 text-warning'
                              : column.id === 'approved' && columnItems.length > 0
                                ? 'bg-info/20 text-info'
                                : 'bg-background/50'
                          )}>
                            {columnItems.length > 20 ? '20+' : columnItems.length}
                          </span>
                          {urgentCount > 0 && (
                            <span className="flex items-center gap-0.5 text-[10px] font-black text-warning">
                              <Clock className="w-3 h-3" />
                              {urgentCount}
                            </span>
                          )}
                        </div>
                      </div>
                      {/* Attention accent bar — flush at bottom of header */}
                      {column.id === 'review' && columnItems.length > 0 && (
                        <div className="h-0.5 rounded-full bg-warning/50 -mx-4" />
                      )}
                    </div>

                    {/* Cards container */}
                    <motion.div
                      variants={columnVariants}
                      initial="hidden"
                      animate="show"
                      className="flex-1 bg-muted/10 rounded-b-2xl p-3 space-y-4 min-h-[500px] border-b border-x border-border/20"
                    >
                      {columnItems.length === 0 ? (
                        <EmptyColumnState columnId={column.id} emoji={column.emoji} />
                      ) : prefersReducedMotion ? (
                        cardNodes
                      ) : (
                        <AnimatePresence mode="popLayout">{cardNodes}</AnimatePresence>
                      )}
                    </motion.div>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}

      <QuickCreateDetailModal
        open={!!selectedReviewSuggestion}
        suggestion={selectedReviewSuggestion}
        companyName={project?.name ?? 'Minha empresa'}
        onOpenChange={(open) => {
          if (!open) setSelectedReviewSuggestion(null);
        }}
        onApprove={handleReviewDeckApprove}
        onSkip={async (id) => {
          handleReviewDeckSkip(id);
          setSelectedReviewSuggestion(null);
        }}
        onRegenerate={handleReviewDeckRegenerate}
      />

      {/* Post Detail Modal */}
      {selectedPost && (
        <PostDetailModal
          post={selectedPost}
          open={!!selectedPost}
          onClose={() => setSelectedPost(null)}
          onSave={handleUpdatePost}
          onPublished={refreshPosts}
        />
      )}


    </div>
  );
};

export default KanbanPage;
