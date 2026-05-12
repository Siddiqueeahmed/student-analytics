import { useEffect, useState } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import styles from './Chart.module.css'

interface ClassificationRetention {
  classification: string
  retention_rate: number
}

type State =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ok'; data: ClassificationRetention[] }

const pctFormatter = (value: number): string => `${(value * 100).toFixed(1)}%`

export default function RetentionChart(): React.ReactElement {
  const [state, setState] = useState<State>({ status: 'loading' })

  useEffect(() => {
    fetch('/api/retention/by-classification')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json() as Promise<ClassificationRetention[]>
      })
      .then((data) => setState({ status: 'ok', data }))
      .catch((err: unknown) =>
        setState({ status: 'error', message: String(err) }),
      )
  }, [])

  if (state.status === 'loading') return <p className={styles.info}>Loading…</p>
  if (state.status === 'error')
    return <p className={styles.error}>Error: {state.message}</p>

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Retention Rate by Classification</h2>
      <p className={styles.subtitle}>Percentage of students retained into the following term</p>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={state.data}
          margin={{ top: 8, right: 16, left: 8, bottom: 16 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="classification" tick={{ fill: '#94a3b8', fontSize: 13 }} />
          <YAxis
            tickFormatter={pctFormatter}
            domain={[0, 1]}
            tick={{ fill: '#94a3b8', fontSize: 12 }}
          />
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
