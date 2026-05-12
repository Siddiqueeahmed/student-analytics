/**
 * Accessibility audit using axe-core.
 * Covers FilterBar and StudentTable — components with meaningful ARIA structure.
 */
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'
import axe from 'axe-core'
import { describe, expect, it } from 'vitest'
import FilterBar from '../src/components/FilterBar'
import { StudentTable } from '../src/components/StudentTable'

function renderInQueryClient(ui: React.ReactElement): HTMLElement {
  const client = new QueryClient()
  const { container } = render(
    <QueryClientProvider client={client}>{ui}</QueryClientProvider>,
  )
  return container
}

async function runAxe(container: HTMLElement) {
  const results = await axe.run(container)
  return results.violations
}

describe('a11y: FilterBar', () => {
  it('has no critical axe violations', async () => {
    const container = renderInQueryClient(
      <FilterBar filters={{}} onChange={() => undefined} />,
    )
    const violations = await runAxe(container)
    const critical = violations.filter((v) => v.impact === 'critical' || v.impact === 'serious')
    expect(critical).toHaveLength(0)
  })
})

describe('a11y: StudentTable', () => {
  const rows = [
    {
      student_id: 1,
      term: 'Fall2023',
      college: 'Engineering',
      program: 'CS',
      classification: 'Junior',
      gpa: 3.5,
      credit_hours_attempted: 15,
      credit_hours_earned: 15,
      retained_next_term: true,
    },
  ]

  it('has no critical axe violations', async () => {
    const { container } = render(<StudentTable data={rows} />)
    const violations = await runAxe(container)
    const critical = violations.filter((v) => v.impact === 'critical' || v.impact === 'serious')
    expect(critical).toHaveLength(0)
  })
})
