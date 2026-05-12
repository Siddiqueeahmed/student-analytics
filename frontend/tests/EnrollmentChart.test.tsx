import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'
import { type ReactNode } from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import EnrollmentChart from '../src/components/EnrollmentChart'

const mockData = [
  { college: 'Engineering', count: 300 },
  { college: 'Business', count: 200 },
]

function wrapper({ children }: { children: ReactNode }): ReactNode {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>
}

describe('EnrollmentChart', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    } as Response)
  })

  it('shows skeleton while loading', () => {
    render(<EnrollmentChart filters={{}} />, { wrapper })
    // Skeleton renders the card div — chart title is not yet present
    expect(screen.queryByText('Enrollment by College')).not.toBeInTheDocument()
  })

  it('renders chart title after data loads', async () => {
    render(<EnrollmentChart filters={{}} />, { wrapper })
    await waitFor(() =>
      expect(screen.getByText('Enrollment by College')).toBeInTheDocument(),
    )
  })

  it('renders college names in the chart', async () => {
    render(<EnrollmentChart filters={{}} />, { wrapper })
    await waitFor(() => expect(screen.getByText('Engineering')).toBeInTheDocument())
    expect(screen.getByText('Business')).toBeInTheDocument()
  })

  it('shows error message when API fails', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    } as Response)
    render(<EnrollmentChart filters={{}} />, { wrapper })
    await waitFor(() => expect(screen.getByText(/Error:/)).toBeInTheDocument())
  })

  it('shows empty state when API returns no data', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([]),
    } as Response)
    render(<EnrollmentChart filters={{}} />, { wrapper })
    await waitFor(() =>
      expect(screen.getByText(/No data for the selected filters/)).toBeInTheDocument(),
    )
  })
})
