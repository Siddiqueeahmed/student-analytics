import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { useRetentionByClassification } from '../api/hooks'
import type { Filters } from '../api/types'
import styles from './Chart.module.css'
import Skeleton from './Skeleton'

interface Props {
  filters: Filters
}

const pctFmt = (v: number): string => `${(v * 100).toFixed(1)}%`

export default function RetentionChart({ filters }: Props): React.ReactElement {
  const { data, isPending, isError, error } = useRetentionByClassification(filters)

  if (isPending) return <Skeleton />
  if (isError) return <p className={styles.error}>Error: {error.message}</p>
  if (data.length === 0)
    return (
      <div className={styles.card}>
        <h2 className={styles.title}>Retention Rate by Classification</h2>
        <p className={styles.empty}>No data for the selected filters.</p>
      </div>
    )

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Retention Rate by Classification</h2>
      <p className={styles.subtitle}>Percentage of students retained into the following term</p>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 8, bottom: 16 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="classification" tick={{ fill: '#94a3b8', fontSize: 13 }} />
          <YAxis tickFormatter={pctFmt} domain={[0, 1]} tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <Tooltip
            formatter={(v: number) => [`${(v * 100).toFixed(1)}%`, 'Retention rate']}
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
            labelStyle={{ color: '#f1f5f9' }}
            itemStyle={{ color: '#22d3ee' }}
          />
          <Bar dataKey="retention_rate" fill="#22d3ee" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
