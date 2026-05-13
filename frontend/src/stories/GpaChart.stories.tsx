import type { Meta, StoryObj } from '@storybook/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import type { ComponentProps } from 'react'
import GpaChart from '../components/GpaChart'
import type { GpaBucket } from '../api/types'

type StoryArgs = ComponentProps<typeof GpaChart> & {
  _mockData?: GpaBucket[]
}

const MOCK_DATA: GpaBucket[] = [
  { bucket: '0.0-0.5', count: 12 },
  { bucket: '0.5-1.0', count: 38 },
  { bucket: '1.0-1.5', count: 95 },
  { bucket: '1.5-2.0', count: 210 },
  { bucket: '2.0-2.5', count: 480 },
  { bucket: '2.5-3.0', count: 720 },
  { bucket: '3.0-3.5', count: 910 },
  { bucket: '3.5-4.0', count: 640 },
]

function makeClient(data: GpaBucket[], key: unknown[]) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  qc.setQueryData(key, data)
  return qc
}

const meta: Meta<StoryArgs> = {
  title: 'Charts/GpaChart',
  component: GpaChart,
  decorators: [
    (Story, ctx) => {
      const qc = makeClient(ctx.args._mockData ?? MOCK_DATA, [
        'gpa',
        'distribution',
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
  args: { filters: { term: 'Fall2023', classifications: ['Sophomore', 'Junior'] } },
}

export const Empty: Story = {
  args: { _mockData: [] },
}
