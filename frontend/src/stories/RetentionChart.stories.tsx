import type { Meta, StoryObj } from '@storybook/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import RetentionChart from '../components/RetentionChart'

function makeClient(data: unknown, key: unknown[]) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  qc.setQueryData(key, data)
  return qc
}

const MOCK_DATA = [
  { classification: 'Freshman', retention_rate: 0.72 },
  { classification: 'Sophomore', retention_rate: 0.81 },
  { classification: 'Junior', retention_rate: 0.88 },
  { classification: 'Senior', retention_rate: 0.94 },
]

const meta: Meta<typeof RetentionChart> = {
  title: 'Charts/RetentionChart',
  component: RetentionChart,
  decorators: [
    (Story, ctx) => {
      const qc = makeClient(ctx.args._mockData ?? MOCK_DATA, [
        'retention',
        'by-classification',
        ctx.args.filters,
      ])
      return (
        <QueryClientProvider client={qc}>
          <Story />
        </QueryClientProvider>
      )
    },
  ],
  args: { filters: {} },
}

export default meta
type Story = StoryObj<typeof RetentionChart & { _mockData?: typeof MOCK_DATA }>

export const Default: Story = {}

export const WithFilter: Story = {
  args: { filters: { term: 'Spring2024', classifications: ['Freshman'] } },
}

export const Empty: Story = {
  args: { _mockData: [] },
}
