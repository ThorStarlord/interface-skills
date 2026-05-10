import { useCallback, useEffect } from 'react';
import {
    useQuery,
    useMutation,
    useQueryClient,
} from '@tanstack/react-query';
import {
    supabase,
    ContentCalendarItem,
    updateKanbanStatus,
    updateContentItem,
    deleteContentItem,
} from '@/lib/supabase';
import { useToast } from '@/hooks/use-toast';
import { ToastAction } from '@/components/ui/toast';

export type KanbanStatus = ContentCalendarItem['kanban_status'];

const KANBAN_PAGE_SIZE = 50;

function kanbanQueryKey(projectId?: string) {
    return ['kanban', projectId] as const;
}

async function fetchKanbanPosts(projectId: string): Promise<ContentCalendarItem[]> {
    const { data, error } = await supabase
        .from('content_calendar')
        .select('*')
        .eq('project_id', projectId)
        .order('created_at', { ascending: false })
        .limit(KANBAN_PAGE_SIZE);

    if (error) throw error;
    return data as ContentCalendarItem[];
}

export function useKanban(projectId?: string) {
    const queryClient = useQueryClient();
    const { toast } = useToast();

    const {
        data: posts = [],
        isLoading,
        error,
    } = useQuery({
        queryKey: kanbanQueryKey(projectId),
        queryFn: () => fetchKanbanPosts(projectId!),
        enabled: !!projectId,
    });

    // Realtime: invalidate query instead of full re-fetch
    useEffect(() => {
        if (!projectId) return;

        const channel = supabase
            .channel(`kanban_realtime_${projectId}`)
            .on(
                'postgres_changes',
                {
                    event: '*',
                    schema: 'public',
                    table: 'content_calendar',
                    filter: `project_id=eq.${projectId}`,
                },
                () => {
                    queryClient.invalidateQueries({ queryKey: kanbanQueryKey(projectId) });
                }
            )
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, [projectId, queryClient]);

    // Move card mutation with optimistic update
    const moveCardMutation = useMutation({
        mutationFn: ({ postId, newStatus }: { postId: string; newStatus: KanbanStatus }) =>
            updateKanbanStatus(postId, newStatus),
        onMutate: async ({ postId, newStatus }) => {
            await queryClient.cancelQueries({ queryKey: kanbanQueryKey(projectId) });
            const previous = queryClient.getQueryData<ContentCalendarItem[]>(kanbanQueryKey(projectId));

            queryClient.setQueryData<ContentCalendarItem[]>(kanbanQueryKey(projectId), (old) =>
                old?.map((post) =>
                    post.id === postId ? { ...post, kanban_status: newStatus } : post
                )
            );

            return { previous, postId, oldStatus: previous?.find((p) => p.id === postId)?.kanban_status };
        },
        onSuccess: (_data, { postId, newStatus }, context) => {
            toast({
                title: newStatus === 'approved' ? '✅ Postagem aprovada!' : 'Card movido',
                description: newStatus === 'approved'
                    ? 'O post agora está pronto para ser publicado.'
                    : `Status alterado para ${newStatus}`,
                action: context?.oldStatus ? (
                    <ToastAction
                        altText="Desfazer"
                        onClick={() => moveCard(postId, context.oldStatus!)}
                    >
                        Desfazer
                    </ToastAction>
                ) : undefined,
                duration: 5000,
            });
        },
        onError: (_err, _variables, context) => {
            if (context?.previous) {
                queryClient.setQueryData(kanbanQueryKey(projectId), context.previous);
            }
            toast({
                title: 'Erro ao mover card',
                description: (_err as Error).message,
                variant: 'destructive',
            });
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: kanbanQueryKey(projectId) });
        },
    });

    // Update card mutation with optimistic update
    const updateCardMutation = useMutation({
        mutationFn: ({ postId, updates }: { postId: string; updates: Partial<ContentCalendarItem> }) =>
            updateContentItem(postId, updates),
        onMutate: async ({ postId, updates }) => {
            await queryClient.cancelQueries({ queryKey: kanbanQueryKey(projectId) });
            const previous = queryClient.getQueryData<ContentCalendarItem[]>(kanbanQueryKey(projectId));

            queryClient.setQueryData<ContentCalendarItem[]>(kanbanQueryKey(projectId), (old) =>
                old?.map((post) =>
                    post.id === postId ? { ...post, ...updates } : post
                )
            );

            return { previous };
        },
        onSuccess: () => {
            toast({
                title: '✅ Alterações salvas!',
                description: 'O conteúdo foi atualizado com sucesso.',
            });
        },
        onError: (_err, _variables, context) => {
            if (context?.previous) {
                queryClient.setQueryData(kanbanQueryKey(projectId), context.previous);
            }
            toast({
                title: 'Erro ao salvar alterações',
                description: (_err as Error).message,
                variant: 'destructive',
            });
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: kanbanQueryKey(projectId) });
        },
    });

    // Duplicate card mutation
    const duplicateCardMutation = useMutation({
        mutationFn: async (postId: string) => {
            const original = posts.find((p) => p.id === postId);
            if (!original) throw new Error('Post não encontrado');

            const clone: Record<string, unknown> = {
                project_id: original.project_id,
                client_id: original.client_id,
                campaign_id: original.campaign_id,
                kanban_status: 'review' as KanbanStatus,
                status: 'planned',
                scheduled_date: original.scheduled_date || new Date(Date.now() + 86400000).toISOString(),
                platform: original.platform,
                post_format: original.post_format,
                content_details: original.content_details,
                final_copy: original.final_copy,
                final_hashtags: original.final_hashtags,
                post_preview_url: original.post_preview_url,
                ai_score: original.ai_score,
                source: original.source,
                mode: original.mode,
            };

            const { data, error } = await supabase
                .from('content_calendar')
                .insert(clone)
                .select()
                .single();

            if (error) throw error;
            return data as ContentCalendarItem;
        },
        onSuccess: (newPost) => {
            queryClient.setQueryData<ContentCalendarItem[]>(kanbanQueryKey(projectId), (old) =>
                old ? [newPost, ...old] : [newPost]
            );
            toast({
                title: '✅ Nova versão criada!',
                description: 'O item foi duplicado e está na fase de Revisão.',
            });
        },
        onError: (err) => {
            toast({
                title: 'Erro ao duplicar',
                description: (err as Error).message,
                variant: 'destructive',
            });
        },
    });

    // Delete card mutation with optimistic update
    const deleteCardMutation = useMutation({
        mutationFn: (postId: string) => deleteContentItem(postId),
        onMutate: async (postId) => {
            await queryClient.cancelQueries({ queryKey: kanbanQueryKey(projectId) });
            const previous = queryClient.getQueryData<ContentCalendarItem[]>(kanbanQueryKey(projectId));

            queryClient.setQueryData<ContentCalendarItem[]>(kanbanQueryKey(projectId), (old) =>
                old?.filter((post) => post.id !== postId)
            );

            return { previous };
        },
        onSuccess: () => {
            toast({
                title: '🗑️ Card excluído',
                description: 'O item foi removido permanentemente.',
            });
        },
        onError: (_err, _postId, context) => {
            if (context?.previous) {
                queryClient.setQueryData(kanbanQueryKey(projectId), context.previous);
            }
            toast({
                title: 'Erro ao excluir card',
                description: (_err as Error).message,
                variant: 'destructive',
            });
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: kanbanQueryKey(projectId) });
        },
    });

    // Stable wrappers that match the original API
    const moveCard = useCallback(
        (postId: string, newStatus: KanbanStatus) => moveCardMutation.mutate({ postId, newStatus }),
        [moveCardMutation]
    );

    const updateCard = useCallback(
        (postId: string, updates: Partial<ContentCalendarItem>) => updateCardMutation.mutate({ postId, updates }),
        [updateCardMutation]
    );

    const duplicateCard = useCallback(
        (postId: string) => duplicateCardMutation.mutate(postId),
        [duplicateCardMutation]
    );

    const deleteCard = useCallback(
        (postId: string) => deleteCardMutation.mutate(postId),
        [deleteCardMutation]
    );

    const getColumnPosts = useCallback(
        (status: KanbanStatus) => posts.filter((post) => post.kanban_status === status),
        [posts]
    );

    const refreshPosts = useCallback(
        () => queryClient.invalidateQueries({ queryKey: kanbanQueryKey(projectId) }),
        [projectId, queryClient]
    );

    return {
        posts,
        isLoading,
        error: error as Error | null,
        moveCard,
        updateCard,
        duplicateCard,
        deleteCard,
        getColumnPosts,
        refreshPosts,
    };
}
