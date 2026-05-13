import type { Meta, StoryObj } from '@storybook/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import type { ComponentProps } from 'react'
import RetentionChart from '../components/RetentionChart'
import type { ClassificationRetention } from '../api/types'

type StoryArgs = ComponentProps<typeof RetentionChart> & {
  _mockData?: ClassificationRetention[]
}

const MOCK_DATA: ClassificationRetention[] = [
  { classification: 'Freshman', retention_rate: 0.72 },
  { classification: 'Sophomore', retention_rate: 0.81 },
  { classification: 'Junior', retention_rate: 0.88 },
  { classification: 'Senior', retention_rate: 0.94 },
]

function makeClient(data: ClassificationRetention[], key: unknown[]) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  qc.setQueryData(key, data)
  return qc
}

const meta: Meta<StoryArgs> = {
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
type Story = StoryObj<StoryArgs>

export const Default: Story = {}

export const WithFilter: Story = {
  args: { filters: { term: 'Spring2024', classifications: ['Freshman'] } },
}

export const Empty: Story = {
  args: { _mockData: [] },
}
