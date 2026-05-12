import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'
import { type ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import GpaChart from '../src/components/GpaChart'

const mockData = [
  { bucket: '2.5-3.0', count: 120 },
  { bucket: '3.0-3.5', count: 200 },
  { bucket: '3.5-4.0', count: 95 },
]

function wrapper({ children }: { children: ReactNode }): ReactNode {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>
}

describe('GpaChart', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    } as Response)
  })

  it('renders chart title after data loads', async () => {
    render(<GpaChart filters={{}} />, { wrapper })
    await waitFor(() =>
      expect(screen.getByText('GPA Distribution')).toBeInTheDocument(),
    )
  })

  it('renders bucket labels', async () => {
    render(<GpaChart filters={{}} />, { wrapper })
    await waitFor(() => expect(screen.getByText('2.5-3.0')).toBeInTheDocument())
    expect(screen.getByText('3.5-4.0')).toBeInTheDocument()
  })

  it('shows error state on API failure', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: false,
      status: 503,
      statusText: 'Service Unavailable',
    } as Response)
    render(<GpaChart filters={{}} />, { wrapper })
    await waitFor(() => expect(screen.getByText(/Error:/)).toBeInTheDocument())
  })

  it('shows empty state when no data', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([]),
    } as Response)
    render(<GpaChart filters={{}} />, { wrapper })
    await waitFor(() =>
      expect(screen.getByText(/No data for the selected filters/)).toBeInTheDocument(),
    )
  })
})
