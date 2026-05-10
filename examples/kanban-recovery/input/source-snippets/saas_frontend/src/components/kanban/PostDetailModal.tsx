import { useEffect, useRef, useState } from 'react';
import { format } from 'date-fns';
import { AlertCircle, AlertTriangle, CalendarIcon, Upload, X, Rocket, Loader2, Instagram, Youtube, Music, Copy, Check, CheckCircle2, RefreshCw, Sparkles, Info, Trash2 } from 'lucide-react';
import { type PublishChecklistItem, type PublishReadiness, usePublisher } from '@/hooks/usePublisher';
import { cn } from '@/lib/utils';
import { Post } from '@/types';
import { HashtagEditor } from '@/components/hashtag/HashtagEditor';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Calendar } from '@/components/ui/calendar';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/components/ui/popover';
import { N8N_BASE_URL } from '@/lib/config';

interface PostDetailModalProps {
    post: Post;
    open: boolean;
    onClose: () => void;
    onSave: (updatedPost: Post) => void;
    onPublished?: () => void;
}

const statusOptions = [
    { value: 'draft', label: 'Rascunho' },
    { value: 'review', label: 'Revisão' },
    { value: 'scheduled', label: 'Agendado' },
    { value: 'published', label: 'Publicado' },
] as const;

function getChecklistVisual(state: PublishChecklistItem['state']) {
    if (state === 'blocking') {
        return {
            Icon: AlertCircle,
            rowClass: 'border-destructive/20 bg-destructive/5',
            iconClass: 'text-destructive',
            textClass: 'text-destructive',
        };
    }

    if (state === 'attention') {
        return {
            Icon: AlertTriangle,
            rowClass: 'border-warning/20 bg-warning/5',
            iconClass: 'text-warning',
            textClass: 'text-foreground',
        };
    }

    return {
        Icon: CheckCircle2,
        rowClass: 'border-success/20 bg-success/5',
        iconClass: 'text-success',
        textClass: 'text-foreground',
    };
}

const PostDetailModal = ({ post, open, onClose, onSave, onPublished }: PostDetailModalProps) => {
    const [content, setContent] = useState(post.content);
    const [hashtags, setHashtags] = useState<string[]>(post.hashtags ?? []);
    const [status, setStatus] = useState(post.status);
    const [mediaUrl, setMediaUrl] = useState(post.mediaUrl || '');
    const [mediaType, setMediaType] = useState(post.mediaType);
    const [scheduledDate, setScheduledDate] = useState<Date | undefined>(post.scheduledDate);
    const [automationTier, setAutomationTier] = useState(post.automationTier || 'draft');
    const [hashtagSets, setHashtagSets] = useState<string[][]>(
        post.hashtags.length > 0 ? [post.hashtags] : [[]]
    );
    const [confirmManual, setConfirmManual] = useState(false);
    const [aiCopySuggestion, setAiCopySuggestion] = useState<string | null>(null);
    const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
    const [copied, setCopied] = useState(false);
    const [publishReadiness, setPublishReadiness] = useState<PublishReadiness | null>(null);
    const [isCheckingPublish, setIsCheckingPublish] = useState(false);
    const { publishPost, retryPublication, isPublishing, checkPublishReadiness } = usePublisher();
    const fileInputRef = useRef<HTMLInputElement>(null);

    const fetchAISuggestions = async () => {
        setIsLoadingSuggestions(true);
        setAiCopySuggestion(null);
        try {
            const res = await fetch(`${N8N_BASE_URL}/webhook/generate-wizard-suggestions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ step: 'all', theme: post.title, objective: 'engagement' }),
            });
            const data = await res.json();
            if (data.error) throw new Error(data.error);
            if (data.copies?.[0]) setAiCopySuggestion(data.copies[0]);
            if (data.hashtag_sets?.length) setHashtagSets(data.hashtag_sets);
        } catch {
            // Silent fail — user can retry
        } finally {
            setIsLoadingSuggestions(false);
        }
    };

    useEffect(() => {
        return () => {
            if (mediaUrl && mediaUrl.startsWith('blob:')) {
                URL.revokeObjectURL(mediaUrl);
            }
        };
    }, [mediaUrl]);

    useEffect(() => {
        if (!open) return;

        let cancelled = false;
        setPublishReadiness(null);
        setIsCheckingPublish(true);

        void checkPublishReadiness(post.id)
            .then((readiness) => {
                if (cancelled) return;
                setPublishReadiness(readiness);
            })
            .catch((error: Error) => {
                if (cancelled) return;
                setPublishReadiness({
                    ready: false,
                    issues: [error.message || 'Nao foi possivel validar os requisitos de publicacao.'],
                    checklist: [
                        {
                            key: 'connection',
                            label: 'Conta conectada',
                            state: 'blocking',
                            message: error.message || 'Nao foi possivel validar os requisitos de publicacao.',
                        },
                    ],
                    platform: post.platform || 'instagram',
                    mode: 'live',
                    nextStep: error.message || 'Nao foi possivel validar os requisitos de publicacao.',
                });
            })
            .finally(() => {
                if (cancelled) return;
                setIsCheckingPublish(false);
            });

        return () => {
            cancelled = true;
        };
    }, [open, post.id, post.platform, checkPublishReadiness]);

    const handleMediaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            if (mediaUrl && mediaUrl.startsWith('blob:')) {
                URL.revokeObjectURL(mediaUrl);
            }
            const url = URL.createObjectURL(file);
            setMediaUrl(url);
            setMediaType(file.type.startsWith('video') ? 'video' : 'image');
        }
    };

    const handleSave = () => {
        onSave({
            ...post,
            content,
            hashtags,
            status,
            mediaUrl: mediaUrl || undefined,
            mediaType,
            platform: post.platform,
            scheduledDate,
            automationTier,
            updatedAt: new Date(),
        });
        onClose();
    };

    const isAlreadyPublished = status === 'published';
    const isPublishDisabled = isPublishing || isCheckingPublish || isAlreadyPublished || (publishReadiness ? !publishReadiness.ready : false);
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const isDatePast = scheduledDate ? scheduledDate < today : false;
    const publishButtonLabel = isAlreadyPublished
        ? 'Ja publicado'
        : post.lastError
            ? `Tentar novamente no ${post.platform || 'Instagram'}`
            : publishReadiness?.mode === 'mock'
                ? 'Rodar teste de publicacao'
                : `Publicar agora no ${post.platform || 'Instagram'}`;

    return (
        <Dialog open={open} onOpenChange={(v) => !v && onClose()}>
            <DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto">
                <DialogHeader className={cn(
                    "flex flex-row items-center justify-between space-y-0 p-4 -m-6 mb-2 rounded-t-lg border-b",
                    post.platform === 'instagram' ? "bg-gradient-to-r from-pink-500/10 to-purple-500/10 border-pink-100" :
                        post.platform === 'youtube' ? "bg-gradient-to-r from-red-500/10 to-orange-500/10 border-red-100" :
                            post.platform === 'tiktok' ? "bg-gradient-to-r from-zinc-900/10 to-zinc-900/20 border-zinc-200" :
                                "bg-muted/30 border-border"
                )}>
                    <DialogTitle className="text-lg font-black tracking-tight">{post.title}</DialogTitle>
                    {post.platform && (
                        <div className={cn(
                            "flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest",
                            post.platform === 'instagram' ? "bg-pink-500 text-white shadow-sm shadow-pink-200" :
                                post.platform === 'youtube' ? "bg-red-600 text-white shadow-sm shadow-red-200" :
                                    "bg-zinc-900 text-white shadow-sm"
                        )}>
                            {post.platform === 'instagram' && <Instagram size={10} />}
                            {post.platform === 'youtube' && <Youtube size={10} />}
                            {post.platform === 'tiktok' && <Music size={10} />}
                            {post.platform}
                        </div>
                    )}
                </DialogHeader>

                {post.lastError && (
                    <div className="mx-6 mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-xl flex items-start gap-3 motion-safe:animate-in motion-safe:fade-in motion-safe:slide-in-from-top-2">
                        <AlertCircle className="w-5 h-5 text-destructive shrink-0 mt-0.5" />
                        <div>
                            <div className="flex items-center justify-between">
                                <p className="text-xs font-black text-destructive uppercase tracking-tight">Falha na Publicação</p>
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    className="h-6 px-2 text-[10px] font-bold text-destructive hover:bg-destructive/10"
                                    onClick={async () => {
                                        try {
                                            await retryPublication(post.id);
                                            if (onPublished) onPublished();
                                            onClose();
                                        } catch { }
                                    }}
                                    disabled={isPublishing}
                                >
                                    {isPublishing ? <Loader2 className="w-3 h-3 animate-spin mr-1" /> : <RefreshCw className="w-3 h-3 mr-1" />}
                                    Tentar Novamente
                                </Button>
                            </div>
                            <p className="text-xs text-destructive/80 mt-1 leading-relaxed">
                                {post.lastError}
                            </p>
                        </div>
                    </div>
                )}

                <div className="space-y-5 pt-2">
                    <div className="space-y-2 mt-2">
                        <Label>Mídia</Label>
                        {mediaUrl ? (
                            <div className="relative rounded-lg overflow-hidden border border-border">
                                {mediaType === 'video' ? (
                                    <video src={mediaUrl} controls className="w-full max-h-48 object-cover" />
                                ) : (
                                    <img src={mediaUrl} alt={post.title} className="w-full max-h-48 object-cover" />
                                )}
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="absolute bottom-2 right-2 h-6 w-6 bg-black/50 hover:bg-black/70 border-0 text-white rounded-md"
                                    onClick={() => { setMediaUrl(''); setMediaType(undefined); }}
                                    title="Remover mídia"
                                >
                                    <Trash2 className="w-3 h-3" />
                                </Button>
                            </div>
                        ) : (
                            <div className="flex items-center justify-center h-32 rounded-lg border-2 border-dashed border-border bg-muted/30">
                                <span className="text-sm text-muted-foreground">Sem mídia</span>
                            </div>
                        )}
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*,video/*"
                            className="hidden"
                            aria-label="Selecionar mídia"
                            onChange={handleMediaChange}
                        />
                        <Button
                            variant="outline"
                            size="sm"
                            className="w-full"
                            onClick={() => fileInputRef.current?.click()}
                        >
                            <Upload className="w-4 h-4 mr-2" />
                            Alterar Mídia
                        </Button>
                    </div>

                    <div className="space-y-2">
                        <div className="flex items-center justify-between gap-2 flex-wrap">
                            <Label htmlFor="post-content">Legenda do Post</Label>
                            <div className="flex items-center gap-1.5">
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    className="h-7 text-[10px] font-bold uppercase tracking-tighter gap-1.5 hover:bg-primary/5 text-primary"
                                    onClick={fetchAISuggestions}
                                    disabled={isLoadingSuggestions}
                                >
                                    {isLoadingSuggestions
                                        ? <Loader2 className="w-3 h-3 animate-spin" />
                                        : <Sparkles className="w-3 h-3" />}
                                    {isLoadingSuggestions ? 'Gerando...' : 'Melhorar com IA'}
                                </Button>
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    className="h-7 text-[10px] font-bold uppercase tracking-tighter gap-1.5 hover:bg-primary/5"
                                    onClick={() => {
                                        navigator.clipboard.writeText(content);
                                        setCopied(true);
                                        setTimeout(() => setCopied(false), 2000);
                                    }}
                                >
                                    {copied ? <Check className="w-3 h-3 text-success" /> : <Copy className="w-3 h-3" />}
                                    {copied ? 'Copiado!' : 'Copiar'}
                                </Button>
                            </div>
                        </div>

                        {/* AI copy suggestion banner */}
                        {aiCopySuggestion && (
                            <div className="rounded-lg bg-primary/5 border border-primary/20 p-3 space-y-2 motion-safe:animate-in motion-safe:fade-in motion-safe:slide-in-from-top-2">
                                <div className="flex items-center justify-between">
                                    <span className="text-[11px] font-bold text-primary flex items-center gap-1.5 uppercase tracking-wider">
                                        <Sparkles className="w-3 h-3" />
                                        Sugestão de IA
                                    </span>
                                    <Button variant="ghost" size="icon" className="h-5 w-5 rounded-full" onClick={() => setAiCopySuggestion(null)}>
                                        <X className="w-3 h-3" />
                                    </Button>
                                </div>
                                <p className="text-xs text-muted-foreground leading-relaxed line-clamp-4">{aiCopySuggestion}</p>
                                <Button
                                    size="sm"
                                    className="h-7 text-xs"
                                    onClick={() => { setContent(aiCopySuggestion); setAiCopySuggestion(null); }}
                                >
                                    Aplicar sugestão
                                </Button>
                            </div>
                        )}

                        <Textarea
                            id="post-content"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            className="min-h-[140px] resize-none border-border/50 focus:border-primary/50 transition-colors"
                        />
                    </div>

                    <div className="space-y-2">
                        <Label>Hashtags</Label>
                        <HashtagEditor
                            sets={hashtagSets}
                            value={hashtags}
                            onChange={setHashtags}
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Status</Label>
                            <Select value={status} onValueChange={(v) => setStatus(v as Post['status'])}>
                                <SelectTrigger className="border-border/50">
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    {statusOptions.map((opt) => (
                                        <SelectItem key={opt.value} value={opt.value}>
                                            {opt.label}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center gap-2">
                                <Label>Modo de publicação</Label>
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <Button variant="ghost" size="icon" className="h-4 w-4 rounded-full p-0 text-muted-foreground hover:text-primary">
                                            <Info className="h-3 w-3" />
                                        </Button>
                                    </PopoverTrigger>
                                    <PopoverContent className="w-64 p-3 text-xs leading-relaxed">
                                        <p className="font-bold mb-1 text-primary">Como funciona cada modo:</p>
                                        <ul className="space-y-1.5 list-disc list-inside text-muted-foreground">
                                            <li><span className="text-foreground font-medium">Você posta:</span> O app salva, você publica pelo Instagram.</li>
                                            <li><span className="text-foreground font-medium">App posta:</span> O app publica automaticamente na data certa.</li>
                                            <li><span className="text-foreground font-medium text-primary">IA cria e posta ✨:</span> A IA gera a imagem e publica sozinha.</li>
                                        </ul>
                                    </PopoverContent>
                                </Popover>
                            </div>
                            <Select
                                value={automationTier}
                                onValueChange={(v) => setAutomationTier(v as NonNullable<Post['automationTier']>)}
                            >
                                <SelectTrigger className={cn(
                                    "border-border/50 text-xs",
                                    (automationTier === 'full_auto') && "border-primary/50 bg-primary/5 text-primary font-bold shadow-sm shadow-primary/10"
                                )}>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="draft">Você posta</SelectItem>
                                    <SelectItem value="auto_social">App posta pra você 🚀</SelectItem>
                                    <SelectItem value="full_auto">IA cria e posta ✨</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label>Data de agendamento</Label>
                        <Popover>
                            <PopoverTrigger asChild>
                                <Button
                                    variant="outline"
                                    className={cn(
                                        'w-full justify-start text-left font-normal',
                                        !scheduledDate && 'text-muted-foreground'
                                    )}
                                >
                                    <CalendarIcon className="mr-2 h-4 w-4" />
                                    {scheduledDate ? format(scheduledDate, 'dd/MM/yyyy') : 'Selecione uma data'}
                                </Button>
                            </PopoverTrigger>
                            <PopoverContent className="w-auto p-0" align="start">
                                <Calendar
                                    mode="single"
                                    selected={scheduledDate}
                                    onSelect={setScheduledDate}
                                    initialFocus
                                    className={cn('p-3 pointer-events-auto')}
                                />
                            </PopoverContent>
                        </Popover>
                        {isDatePast && (
                            <p className="flex items-center gap-1 text-[11px] text-warning mt-1">
                                <AlertTriangle className="w-3 h-3 shrink-0" />
                                Data no passado — atualize antes de publicar
                            </p>
                        )}
                    </div>

                    <div className="flex flex-col gap-3 pt-2">
                        <div className="flex gap-2">
                            <Button onClick={handleSave} className="flex-1">
                                Salvar
                            </Button>
                            <Button variant="outline" onClick={onClose}>
                                Cancelar
                            </Button>
                        </div>

                        {!isAlreadyPublished && (
                            !confirmManual ? (
                                <button
                                    type="button"
                                    className="text-[11px] text-muted-foreground hover:text-foreground underline underline-offset-2 transition-colors mx-auto leading-none"
                                    onClick={() => setConfirmManual(true)}
                                >
                                    Já publiquei esse conteúdo manualmente
                                </button>
                            ) : (
                                <div className="rounded-xl border border-warning/30 bg-warning/5 p-3 space-y-2.5">
                                    <p className="text-xs font-medium text-center leading-snug">
                                        Confirmar: você já publicou esse post pelo Instagram?
                                    </p>
                                    <div className="flex gap-2">
                                        <Button
                                            size="sm"
                                            variant="outline"
                                            className="flex-1 text-xs"
                                            onClick={() => setConfirmManual(false)}
                                        >
                                            Não, cancelar
                                        </Button>
                                        <Button
                                            size="sm"
                                            className="flex-1 text-xs bg-green-600 hover:bg-green-700 text-white"
                                            onClick={() => {
                                                setStatus('published');
                                                onSave({
                                                    ...post,
                                                    content,
                                                    status: 'published',
                                                    automationTier,
                                                    updatedAt: new Date(),
                                                });
                                                onClose();
                                            }}
                                        >
                                            <Check className="w-3 h-3 mr-1" />
                                            Sim, marcar como publicado
                                        </Button>
                                    </div>
                                </div>
                            )
                        )}

                        {/* Publish readiness checklist */}
                        {!isAlreadyPublished && (
                            <div className="rounded-xl border border-border/50 bg-muted/20 px-3 py-3 space-y-3">
                                    <div className="flex items-start justify-between gap-3">
                                        <div>
                                            <p className="text-[11px] font-black uppercase tracking-[0.16em] text-muted-foreground">
                                                Antes de publicar
                                            </p>
                                            <p className="text-xs text-muted-foreground mt-1">
                                                Veja o que ja esta pronto, o que pede atencao e o que realmente bloqueia a publicacao.
                                            </p>
                                        </div>
                                        {publishReadiness && (
                                            <span
                                                className={cn(
                                                    'rounded-full px-2.5 py-1 text-[10px] font-black uppercase tracking-[0.16em]',
                                                    publishReadiness.ready
                                                        ? 'bg-success/10 text-success'
                                                        : 'bg-destructive/10 text-destructive'
                                                )}
                                            >
                                                {publishReadiness.ready ? 'Pronto' : 'Bloqueado'}
                                            </span>
                                        )}
                                    </div>

                                    {isCheckingPublish ? (
                                        <>
                                            <div className="h-3 bg-muted/60 rounded-full animate-pulse w-3/4 motion-reduce:animate-none" />
                                            <div className="h-3 bg-muted/60 rounded-full animate-pulse w-1/2 motion-reduce:animate-none" />
                                            <div className="h-3 bg-muted/60 rounded-full animate-pulse w-2/3 motion-reduce:animate-none" />
                                        </>
                                    ) : (
                                        <>
                                            {(publishReadiness?.checklist || []).map((item) => {
                                                const visual = getChecklistVisual(item.state);
                                                const Icon = visual.Icon;

                                                return (
                                                    <div
                                                        key={item.key}
                                                        className={cn('rounded-xl border px-3 py-2.5', visual.rowClass)}
                                                    >
                                                        <div className="flex items-start gap-2">
                                                            <Icon className={cn('w-4 h-4 mt-0.5 shrink-0', visual.iconClass)} />
                                                            <div className="space-y-0.5">
                                                                <p className="text-xs font-semibold text-foreground">{item.label}</p>
                                                                <p className={cn('text-xs leading-relaxed', visual.textClass)}>
                                                                    {item.message}
                                                                </p>
                                                            </div>
                                                        </div>
                                                    </div>
                                                );
                                            })}

                                            {publishReadiness && (
                                                <div className="rounded-xl border border-primary/15 bg-primary/5 px-3 py-2.5">
                                                    <p className="text-[11px] font-black uppercase tracking-[0.16em] text-primary">
                                                        Proximo passo
                                                    </p>
                                                    <p className="mt-1 text-xs leading-relaxed text-foreground">
                                                        {publishReadiness.nextStep}
                                                    </p>
                                                </div>
                                            )}
                                        </>
                                    )}
                            </div>
                        )}

                        <Button
                            onClick={async () => {
                                try {
                                    if (post.lastError) {
                                        await retryPublication(post.id);
                                    } else {
                                        await publishPost(post.id);
                                    }
                                    if (onPublished) onPublished();
                                    onClose();
                                } catch {
                                    // Error is already handled by toast in usePublisher
                                }
                            }}
                            disabled={isPublishDisabled}
                            className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold h-12 rounded-xl group"
                        >
                            {isPublishing ? (
                                <>
                                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                    Publicando...
                                </>
                            ) : (
                                <>
                                    <Rocket className="w-5 h-5 mr-2 transition-transform group-hover:-translate-y-1 group-hover:translate-x-1" />
                                    {publishButtonLabel}
                                </>
                            )}
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
};

export default PostDetailModal;
