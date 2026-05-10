import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MoreHorizontal, Calendar, Eye, RefreshCw,
  Play, Loader2, Instagram, Youtube, Music, Sparkles, Star,
  Copy, RotateCcw, FilePlus, X, Trash2,
  FileText, CalendarClock, CheckCircle2, Images, Smartphone, Video,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import { ContentCalendarItem } from '@/lib/supabase';
import { Post } from '@/types';
import { VisualFallback } from '@/components/proactive/PostCanvas';
import { KanbanStatus } from '@/hooks/useKanban';
import { getPostCanvasAspectClass, normalizePostFormat } from '@/lib/postFormat';

// ─── Status config ────────────────────────────────────────────────────────────
const STATUS_CONFIG: Record<KanbanStatus, {
  label: string;
  className: string;
  icon: React.ReactNode;
}> = {
  backlog: {
    label: 'Ideia salva',
    className: 'bg-muted text-muted-foreground border border-border/60',
    icon: <FileText className="w-2.5 h-2.5" />,
  },
  review: {
    label: 'Para decidir',
    className: 'bg-warning/15 text-warning border border-warning/30',
    icon: <Eye className="w-2.5 h-2.5" />,
  },
  approved: {
    label: 'Agendado',
    className: 'bg-info/15 text-info border border-info/30',
    icon: <CalendarClock className="w-2.5 h-2.5" />,
  },
  published: {
    label: 'Publicado',
    className: 'bg-success/15 text-success border border-success/30',
    icon: <CheckCircle2 className="w-2.5 h-2.5" />,
  },
  archived: {
    label: 'Arquivado',
    className: 'bg-muted text-muted-foreground border border-border/60',
    icon: <FileText className="w-2.5 h-2.5" />,
  },
};

// ─── Card Variants ────────────────────────────────────────────────────────────
export const cardVariants = {
  hidden: { opacity: 0, y: 10, scale: 0.97 },
  show: {
    opacity: 1, y: 0, scale: 1,
    transition: { duration: 0.22, ease: [0.25, 0.46, 0.45, 0.94] as const },
  },
  exit: {
    opacity: 0, scale: 0.94, y: -8,
    transition: { duration: 0.16, ease: [0.42, 0, 1, 1] as const },
  },
};

// ─── Props ────────────────────────────────────────────────────────────────────
interface KanbanCardProps {
  item: ContentCalendarItem;
  post: Post;
  effectiveKanbanStatus: KanbanStatus;
  columnId: KanbanStatus;
  project?: {
    business_plan?: {
      branding?: {
        primaryColor?: string;
      };
    } | null;
  } | null;
  isCoarsePointer: boolean;
  isDragging: boolean;
  isPending: boolean;
  isSafeFlow: boolean;
  isPublishing: boolean;
  onDragStart: () => void;
  onDragEnd: () => void;
  onSwipeEnd: (info: { offset: { x: number } }) => void;
  onClick: () => void;
  onMoveToNext: () => void;
  onMoveCard: (to: KanbanStatus) => void;
  onDelete: () => void;
  onDuplicate: () => void;
  onRetry: () => void;
  onOpenDetails: () => void;
  onCopyCaption: () => void;
}

// ─── Component ────────────────────────────────────────────────────────────────
export const KanbanCard: React.FC<KanbanCardProps> = ({
  item,
  post,
  effectiveKanbanStatus,
  columnId,
  project,
  isCoarsePointer,
  isDragging,
  isPending,
  isSafeFlow,
  isPublishing,
  onDragStart,
  onDragEnd,
  onSwipeEnd,
  onClick,
  onMoveToNext,
  onMoveCard,
  onDelete,
  onDuplicate,
  onRetry,
  onOpenDetails,
  onCopyCaption,
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [renderTimestamp] = useState(() => Date.now());
  const normalizedPostFormat = normalizePostFormat(item.post_format ?? item.content_details?.post_format);
  const mediaAspectClass = getPostCanvasAspectClass(normalizedPostFormat ?? 'feed');

  const mediaUrl = item.post_preview_url || item.final_video_url;
  const isVideo = Boolean(item.final_video_url);
  const statusCfg = STATUS_CONFIG[effectiveKanbanStatus];
  const ageDays = Math.floor((renderTimestamp - new Date(item.created_at).getTime()) / 86400000);

  return (
    <motion.div
      variants={cardVariants}
      draggable={!isCoarsePointer}
      onDragStartCapture={!isCoarsePointer ? onDragStart : undefined}
      onDragEndCapture={!isCoarsePointer ? onDragEnd : undefined}
      drag={isCoarsePointer ? 'x' : false}
      dragConstraints={isCoarsePointer ? { left: 0, right: 0 } : undefined}
      dragElastic={isCoarsePointer ? 0.25 : undefined}
      whileDrag={isCoarsePointer ? {
        scale: 1.04,
        rotate: 1.5,
        zIndex: 50,
        boxShadow: '0 20px 60px -10px rgba(0,0,0,0.25)',
      } : undefined}
      onDragEnd={isCoarsePointer ? (_, info) => onSwipeEnd(info) : undefined}
      style={isCoarsePointer ? { touchAction: 'pan-y' } : undefined}
      onClick={onClick}
      onHoverStart={!isCoarsePointer ? () => setIsHovered(true) : undefined}
      onHoverEnd={!isCoarsePointer ? () => setIsHovered(false) : undefined}
      animate={!isCoarsePointer && isHovered ? { y: -3 } : { y: 0 }}
      transition={{ duration: 0.15 }}
      className={cn(
        'bg-card rounded-2xl border border-border overflow-hidden cursor-grab active:cursor-grabbing shadow-card select-none relative',
        isHovered && !isCoarsePointer && 'shadow-card-hover',
        isDragging && 'opacity-50',
        isPending && 'opacity-40 grayscale pointer-events-none',
        item.source === 'proactive_mode' && 'border-primary/20 ring-1 ring-primary/5 bg-gradient-to-br from-primary/[0.03] to-transparent'
      )}
    >
      {/* Pending overlay */}
      {isPending && (
        <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-background/20 backdrop-blur-[1px]">
          <div className="px-3 py-1.5 rounded-full bg-primary/90 text-primary-foreground text-[10px] font-black uppercase tracking-widest shadow-xl animate-pulse flex items-center gap-2">
            <Loader2 className="w-3 h-3 animate-spin" />
            Movendo...
          </div>
        </div>
      )}

      {/* Thumbnail */}
      {mediaUrl ? (
        <div className={cn('relative w-full overflow-hidden bg-muted group', mediaAspectClass)}>
          {isVideo && !item.post_preview_url ? (
            <video
              src={item.final_video_url!}
              className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              muted
              playsInline
            />
          ) : (
            <img
              src={mediaUrl}
              alt={post.title}
              className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
          )}
          {isVideo && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/20">
              <div className="w-8 h-8 rounded-full bg-white/90 flex items-center justify-center shadow-lg">
                <Play className="w-4 h-4 text-foreground ml-0.5" fill="currentColor" />
              </div>
            </div>
          )}
          {/* AI Score Badge */}
          {item.ai_score && (
            <div className="absolute top-2 left-2 px-1.5 py-0.5 rounded-lg bg-black/60 backdrop-blur-md border border-white/20 text-white flex items-center gap-1 shadow-lg">
              <Sparkles className="w-2.5 h-2.5 text-amber-400 fill-amber-400" />
              <span className="text-[10px] font-black">{item.ai_score}%</span>
            </div>
          )}
          {/* Full Auto Tier Badge */}
          {item.automation_tier === 'full_auto' && (
            <div className="absolute bottom-2 left-2 px-1.5 py-0.5 rounded-lg bg-primary/90 backdrop-blur-md border border-white/20 text-primary-foreground flex items-center gap-1 shadow-lg">
              <Star className="w-2.5 h-2.5 fill-current" />
              <span className="text-[9px] font-black uppercase tracking-tighter">Full Auto</span>
            </div>
          )}
          {/* Platform Icon */}
          <div className="absolute top-2 right-2 p-1.5 rounded-lg bg-black/40 backdrop-blur-md border border-white/10 shadow-lg">
            {item.platform === 'instagram' && <Instagram className="w-3.5 h-3.5 text-pink-400" />}
            {item.platform === 'youtube' && <Youtube className="w-3.5 h-3.5 text-red-500" />}
            {item.platform === 'tiktok' && <Music className="w-3.5 h-3.5 text-white" />}
            {!item.platform && <Sparkles className="w-3.5 h-3.5 text-primary" />}
          </div>
          {/* Post format badge */}
          {normalizedPostFormat === 'carrossel' && (
            <div className="absolute bottom-2 right-2 px-1.5 py-0.5 rounded-lg bg-black/60 backdrop-blur-md border border-white/20 text-white flex items-center gap-1 shadow-lg">
              <Images className="w-2.5 h-2.5 text-sky-300" />
              <span className="text-[9px] font-black uppercase tracking-tighter">Carrossel</span>
            </div>
          )}
          {normalizedPostFormat === 'stories' && (
            <div className="absolute bottom-2 right-2 px-1.5 py-0.5 rounded-lg bg-black/60 backdrop-blur-md border border-white/20 text-white flex items-center gap-1 shadow-lg">
              <Smartphone className="w-2.5 h-2.5 text-purple-300" />
              <span className="text-[9px] font-black uppercase tracking-tighter">Story</span>
            </div>
          )}
          {normalizedPostFormat === 'reels' && (
            <div className="absolute bottom-2 right-2 px-1.5 py-0.5 rounded-lg bg-black/60 backdrop-blur-md border border-white/20 text-white flex items-center gap-1 shadow-lg">
              <Video className="w-2.5 h-2.5 text-amber-300" />
              <span className="text-[9px] font-black uppercase tracking-tighter">Reel</span>
            </div>
          )}

          {/* Hover copy preview overlay (only when there's an image) */}
          <AnimatePresence>
            {isHovered && !isDragging && post.content && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 8 }}
                transition={{ duration: 0.16 }}
                className="absolute bottom-0 left-0 right-0 glass rounded-b-none p-3 border-t border-white/10"
                onClick={(e) => e.stopPropagation()}
              >
                <p className="text-[11px] text-white/90 line-clamp-3 leading-relaxed drop-shadow">
                  {post.content}
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      ) : (
        <div className={cn('w-full overflow-hidden relative', mediaAspectClass)}>
          <VisualFallback
            type={item.automation_tier === 'full_auto' ? 'teaser' : 'text-card'}
            pillar={post.title}
            caption={post.content}
            brandColor={project?.business_plan?.branding?.primaryColor}
          />
          {/* Hover copy preview overlay for no-image cards */}
          <AnimatePresence>
            {isHovered && !isDragging && post.content && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 8 }}
                transition={{ duration: 0.16 }}
                className="absolute bottom-0 left-0 right-0 glass p-3 border-t border-border/40"
                onClick={(e) => e.stopPropagation()}
              >
                <p className="text-[11px] text-muted-foreground line-clamp-3 leading-relaxed">
                  {post.content}
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* Card body */}
      <div className="p-3">
        <h4 className="font-bold text-sm text-foreground line-clamp-1 mb-1">
          {post.title}
        </h4>
        <p className="text-xs text-muted-foreground line-clamp-2 mb-3 leading-relaxed">
          {post.content}
        </p>

        {item.source === 'proactive_mode' && (
          <div className="flex items-center gap-1.5 mb-3 px-2 py-0.5 bg-primary/5 rounded-full border border-primary/10 w-fit">
            <Sparkles className="w-2.5 h-2.5 text-primary" />
            <span className="text-[9px] font-black text-primary uppercase tracking-tighter">Gerado pela IA</span>
          </div>
        )}

        {effectiveKanbanStatus === 'backlog' && ageDays >= 7 && (
          <div className="flex items-center gap-1.5 mb-3 px-2 py-0.5 bg-amber-500/10 rounded-full border border-amber-500/20 w-fit">
            <span className="text-[9px] font-black text-amber-600 uppercase tracking-tighter">Salvo há {ageDays} dias</span>
          </div>
        )}

        {effectiveKanbanStatus === 'review' && ageDays >= 21 && (
          <div className="flex items-center gap-1.5 mb-3 px-2 py-0.5 bg-amber-500/15 rounded-full border border-amber-500/30 w-fit">
            <span className="text-[9px] font-black text-amber-600 uppercase tracking-tighter">Esperando sua revisão</span>
          </div>
        )}

        {item.last_error && (
          <div className="flex items-center gap-1.5 mb-3">
            <div className="flex items-center gap-1.5 px-2 py-0.5 bg-destructive/10 rounded-full border border-destructive/20 w-fit animate-pulse">
              <X className="w-2.5 h-2.5 text-destructive" />
              <span className="text-[9px] font-black text-destructive uppercase tracking-tighter line-clamp-1">
                Erro: {item.last_error}
              </span>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="h-5 w-5 rounded-full hover:bg-destructive/10 text-destructive"
              onClick={(e) => { e.stopPropagation(); onRetry(); }}
              disabled={isPublishing}
            >
              {isPublishing ? <Loader2 className="w-2.5 h-2.5 animate-spin" /> : <RefreshCw className="w-2.5 h-2.5" />}
            </Button>
          </div>
        )}

        {/* Inline quick-actions for review cards */}
        {effectiveKanbanStatus === 'review' && (
          <div className="flex gap-1.5 mb-3">
            <button
              onClick={(e) => { e.stopPropagation(); onMoveCard('approved'); }}
              className="flex-1 text-[11px] font-semibold py-1 rounded-lg bg-success text-white hover:bg-success/90 transition-colors"
            >
              Aprovar
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); onMoveCard('backlog'); }}
              className="flex-1 py-1 rounded-lg bg-muted text-muted-foreground border border-border/40 hover:bg-muted/80 transition-colors flex flex-col items-center leading-tight"
            >
              <span className="text-[11px] font-semibold">Não quero este</span>
              <span className="text-[9px] font-normal opacity-60">Ficará nos rascunhos</span>
            </button>
          </div>
        )}

        {/* Inline quick-action for backlog cards */}
        {effectiveKanbanStatus === 'backlog' && (
          <div className="flex gap-1.5 mb-3">
            <button
              type="button"
              onClick={(e) => { e.stopPropagation(); onMoveCard('approved'); }}
              className="flex-1 text-[11px] font-semibold py-1 rounded-lg bg-info text-white hover:bg-info/90 transition-colors"
            >
              Agendar
            </button>
          </div>
        )}

        {/* Footer: date + status badge + actions */}
        <div className="flex items-center justify-between pt-2 border-t border-border/50">
          <div className="flex items-center gap-1.5 min-w-0">
            <div className="flex items-center gap-1 text-[10px] font-bold text-muted-foreground shrink-0">
              <Calendar className="w-3 h-3" />
              {item.scheduled_date
                ? new Date(item.scheduled_date).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' })
                  + (effectiveKanbanStatus === 'approved'
                    ? ' · ' + new Date(item.scheduled_date).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
                    : '')
                : 'Sem data'
              }
            </div>
            {effectiveKanbanStatus !== columnId && (
              <span className={cn(
                'hidden sm:inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[9px] font-semibold tracking-wide',
                statusCfg.className
              )}>
                {statusCfg.icon}
                {statusCfg.label}
              </span>
            )}
          </div>

          <div className="flex gap-1 shrink-0">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7 rounded-lg hover:bg-muted"
                  onClick={(e) => e.stopPropagation()}
                >
                  <MoreHorizontal className="w-3.5 h-3.5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48 rounded-xl border-border/50">
                <DropdownMenuItem onClick={(e) => { e.stopPropagation(); onOpenDetails(); }}>
                  <Eye className="mr-2 h-3.5 w-3.5" />
                  <span>Ver Detalhes</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={(e) => { e.stopPropagation(); onCopyCaption(); }}>
                  <Copy className="mr-2 h-3.5 w-3.5" />
                  <span>Copiar Legenda</span>
                </DropdownMenuItem>

                {item.kanban_status === 'published' && (
                  <>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={(e) => { e.stopPropagation(); onDuplicate(); }}>
                      <FilePlus className="mr-2 h-3.5 w-3.5" />
                      <span>Criar nova versão</span>
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      className="text-warning focus:text-warning"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (window.confirm('Isso NÃO remove o post da rede social.\nApenas corrige o status no Kanban (erro de marcação).\n\nContinuar?')) {
                          onMoveCard('review');
                        }
                      }}
                    >
                      <RotateCcw className="mr-2 h-3.5 w-3.5" />
                      <span>Corrigir Status</span>
                    </DropdownMenuItem>
                  </>
                )}

                {item.last_error && (
                  <>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                      className="text-primary focus:text-primary font-bold"
                      onClick={(e) => { e.stopPropagation(); onRetry(); }}
                      disabled={isPublishing}
                    >
                      <RefreshCw className={cn('mr-2 h-3.5 w-3.5', isPublishing && 'animate-spin')} />
                      <span>Tentar Novamente</span>
                    </DropdownMenuItem>
                  </>
                )}

                <DropdownMenuSeparator />
                <DropdownMenuItem
                  className="text-destructive focus:text-destructive focus:bg-destructive/10"
                  onClick={(e) => {
                    e.stopPropagation();
                    if (window.confirm('Excluir este card permanentemente?')) {
                      onDelete();
                    }
                  }}
                >
                  <Trash2 className="mr-2 h-3.5 w-3.5" />
                  <span>Excluir Card</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

          </div>
        </div>
      </div>
    </motion.div>
  );
};
