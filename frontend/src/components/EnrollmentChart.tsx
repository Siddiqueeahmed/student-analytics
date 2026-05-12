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

interface CollegeEnrollment {
  college: string
  count: number
}

type State =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ok'; data: CollegeEnrollment[] }

export default function EnrollmentChart(): React.ReactElement {
  const [state, setState] = useState<State>({ status: 'loading' })

  useEffect(() => {
    fetch('/api/enrollment/by-college')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json() as Promise<CollegeEnrollment[]>
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
      <h2 className={styles.title}>Enrollment by College</h2>
      <p className={styles.subtitle}>Total enrolled students per academic college</p>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={state.data} margin={{ top: 8, right: 16, left: 8, bottom: 72 }}>
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
