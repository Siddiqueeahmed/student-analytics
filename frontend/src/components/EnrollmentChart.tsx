import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { useEnrollmentByCollege } from '../api/hooks'
import type { Filters } from '../api/types'
import styles from './Chart.module.css'
import Skeleton from './Skeleton'

interface Props {
  filters: Filters
}

export default function EnrollmentChart({ filters }: Props): React.ReactElement {
  const { data, isPending, isError, error } = useEnrollmentByCollege(filters)

  if (isPending) return <Skeleton />
  if (isError) return <p className={styles.error}>Error: {error.message}</p>
  if (data.length === 0)
    return (
      <div className={styles.card}>
        <h2 className={styles.title}>Enrollment by College</h2>
        <p className={styles.empty}>No data for the selected filters.</p>
      </div>
    )

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Enrollment by College</h2>
      <p className={styles.subtitle}>Total enrolled students per academic college</p>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 8, bottom: 72 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="college"
            angle={-35}
            textAnchor="end"
            interval={0}
            tick={{ fill: '#94a3b8', fontSize: 12 }}
          />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
            labelStyle={{ color: '#f1f5f9' }}
            itemStyle={{ color: '#6366f1' }}
          />
          <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
