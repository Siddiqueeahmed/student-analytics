import type { Meta, StoryObj } from '@storybook/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import type { ComponentProps } from 'react'
import type { CollegeEnrollment } from '../api/types'
import EnrollmentChart from '../components/EnrollmentChart'

type StoryArgs = ComponentProps<typeof EnrollmentChart> & {
  _mockData?: CollegeEnrollment[]
}

const MOCK_DATA: CollegeEnrollment[] = [
  { college: 'Engineering', count: 1240 },
  { college: 'Arts & Sciences', count: 980 },
  { college: 'Business', count: 760 },
  { college: 'Education', count: 520 },
  { college: 'Health Sciences', count: 430 },
]

function makeClient(data: CollegeEnrollment[], key: unknown[]) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  qc.setQueryData(key, data)
  return qc
}

const meta: Meta<StoryArgs> = {
  title: 'Charts/EnrollmentChart',
  component: EnrollmentChart,
  decorators: [
    (Story, ctx) => {
      const qc = makeClient(ctx.args._mockData ?? MOCK_DATA, [
        'enrollment',
        'by-college',
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
  args: { filters: { term: 'Fall2023', classifications: ['Junior', 'Senior'] } },
}

export const Empty: Story = {
  args: { _mockData: [] },
}
