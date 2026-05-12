import { useState } from 'react'
import type { Filters } from '../api/types'
import { ErrorBoundary } from '../components/ErrorBoundary'
import EnrollmentChart from '../components/EnrollmentChart'
import FilterBar from '../components/FilterBar'
import GpaChart from '../components/GpaChart'
import RetentionChart from '../components/RetentionChart'
import styles from './Dashboard.module.css'

export default function Dashboard(): React.ReactElement {
  const [filters, setFilters] = useState<Filters>({})

  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <span className={styles.logo}>Student Analytics</span>
        <span className={styles.tag}>Phase 2</span>
      </header>

      <FilterBar filters={filters} onChange={setFilters} />

      <main className={styles.main}>
        <ErrorBoundary>
          <EnrollmentChart filters={filters} />
        </ErrorBoundary>
        <ErrorBoundary>
          <RetentionChart filters={filters} />
        </ErrorBoundary>
        <ErrorBoundary>
          <GpaChart filters={filters} />
        </ErrorBoundary>
      </main>

      <footer className={styles.footer}>
        5,000 synthetic student records · DuckDB · Polars · FastAPI · TanStack Query · Recharts
      </footer>
    </div>
  )
}
