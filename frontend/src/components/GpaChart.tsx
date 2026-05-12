import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { useGpaDistribution } from '../api/hooks'
import type { Filters } from '../api/types'
import styles from './Chart.module.css'
import Skeleton from './Skeleton'

interface Props {
  filters: Filters
}

export default function GpaChart({ filters }: Props): React.ReactElement {
  const { data, isPending, isError, error } = useGpaDistribution(filters)

  if (isPending) return <Skeleton />
  if (isError) return <p className={styles.error}>Error: {error.message}</p>
  if (data.length === 0)
    return (
      <div className={styles.card}>
        <h2 className={styles.title}>GPA Distribution</h2>
        <p className={styles.empty}>No data for the selected filters.</p>
      </div>
    )

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>GPA Distribution</h2>
      <p className={styles.subtitle}>Student count within each 0.5-point GPA band</p>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 8, bottom: 16 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="bucket" tick={{ fill: '#94a3b8', fontSize: 13 }} />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
            labelStyle={{ color: '#f1f5f9' }}
            itemStyle={{ color: '#4ade80' }}
          />
          <Bar dataKey="count" fill="#4ade80" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
