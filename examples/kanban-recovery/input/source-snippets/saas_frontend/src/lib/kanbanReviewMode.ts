export type ReviewDeckSource = 'review' | 'backlog' | 'empty';

export interface ReviewDeckState<T> {
  source: ReviewDeckSource;
  items: T[];
  badgeCount: number;
}

export function getReviewDeckState<T>(reviewItems: T[], backlogItems: T[]): ReviewDeckState<T> {
  if (reviewItems.length > 0) {
    return {
      source: 'review',
      items: reviewItems,
      badgeCount: reviewItems.length,
    };
  }

  if (backlogItems.length > 0) {
    return {
      source: 'backlog',
      items: backlogItems,
      badgeCount: backlogItems.length,
    };
  }

  return {
    source: 'empty',
    items: [],
    badgeCount: 0,
  };
}
