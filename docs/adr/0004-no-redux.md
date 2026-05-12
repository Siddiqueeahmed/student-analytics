# ADR 0004 — No Redux; TanStack Query for server state

**Status:** Accepted  
**Date:** 2026-05-12

## Context

The frontend needs to fetch data from three API endpoints, display loading and error states, and apply shared filter parameters across all charts. This is a common use case that Redux (with RTK Query) could address, but at significant boilerplate cost.

Redux introduces reducers, actions, selectors, a store provider, and RTK Query's `createApi` configuration — roughly 200+ lines of ceremony for three endpoints. Redux is designed for complex client-side state machines, optimistic updates, and cross-slice coordination. None of those requirements exist in this project.

TanStack Query (React Query v5) handles exactly what is needed: caching, background refetch, loading/error state, and query key-based invalidation. The filter state — a term string and a classification array — is simple enough to live in a single `useState<Filters>` call in the Dashboard component.

## Decision

Use TanStack Query for all server state (data fetching, caching, background refetch). Use `useState` for the shared filter state. Do not install Redux, Zustand, or any other global state library.

## Consequences

**Benefits:**
- Zero boilerplate: each data source is one `useQuery` call.
- Automatic 5-minute stale time means the API is not hammered on tab focus.
- Loading and error states are first-class discriminated union values (`isPending`, `isError`, `data`), not booleans scattered across the store.
- Bundle size stays small: TanStack Query is ~13 KB gzipped vs. ~20 KB for Redux + RTK Query.

**Trade-offs:**
- TanStack Query does not manage derived client state. If filters needed to be computed from multiple async sources, a global store would be cleaner.
- Cache invalidation on admin ETL refresh requires calling `queryClient.invalidateQueries()` from the component — slightly less ergonomic than a Redux action.
