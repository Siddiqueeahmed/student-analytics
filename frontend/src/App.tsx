import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import { StudentsPage } from './pages/Students'
import styles from './App.module.css'

type Page = 'dashboard' | 'students'

export default function App(): React.ReactElement {
  const [page, setPage] = useState<Page>('dashboard')

  return (
    <>
      <nav className={styles.nav} aria-label="Main navigation">
        <span className={styles.brand}>Student Analytics</span>
        <button
          type="button"
          className={`${styles.navBtn} ${page === 'dashboard' ? styles.active : ''}`}
          onClick={() => setPage('dashboard')}
          aria-current={page === 'dashboard' ? 'page' : undefined}
        >
          Dashboard
        </button>
        <button
          type="button"
          className={`${styles.navBtn} ${page === 'students' ? styles.active : ''}`}
          onClick={() => setPage('students')}
          aria-current={page === 'students' ? 'page' : undefined}
        >
          Students
        </button>
      </nav>
      {page === 'dashboard' ? <Dashboard /> : <StudentsPage />}
    </>
  )
}
