import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'
import { type ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import RetentionChart from '../src/components/RetentionChart'

const mockData = [
  { classification: 'Freshman',  retention_rate: 0.72 },
  { classification: 'Sophomore', retention_rate: 0.81 },
]

function wrapper({ children }: { children: ReactNode }): ReactNode {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>
}

describe('RetentionChart', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    } as Response)
  })

  it('renders chart title after data loads', async () => {
    render(<RetentionChart filters={{}} />, { wrapper })
    await waitFor(() =>
      expect(screen.getByText('Retention Rate by Classification')).toBeInTheDocument(),
    )
  })

  it('renders classification labels', async () => {
    render(<RetentionChart filters={{}} />, { wrapper })
    await waitFor(() => expect(screen.getByText('Freshman')).toBeInTheDocument())
    expect(screen.getByText('Sophomore')).toBeInTheDocument()
  })

  it('shows empty state when no data', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([]),
    } as Response)
    render(<RetentionChart filters={{}} />, { wrapper })
    await waitFor(() =>
      expect(screen.getByText(/No data for the selected filters/)).toBeInTheDocument(),
    )
  })
})
