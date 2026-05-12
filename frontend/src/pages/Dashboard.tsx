import EnrollmentChart from '../components/EnrollmentChart'
import RetentionChart from '../components/RetentionChart'
import GpaChart from '../components/GpaChart'

const styles: Record<string, React.CSSProperties> = {
  shell: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
  },
  header: {
    background: '#0f172a',
    borderBottom: '1px solid #1e293b',
    padding: '20px 32px',
    display: 'flex',
    alignItems: 'baseline',
    gap: 12,
  },
  logo: {
    fontSize: '1.25rem',
    fontWeight: 700,
    color: '#f1f5f9',
    letterSpacing: '-0.5px',
  },
  tag: {
    fontSize: '0.75rem',
    color: '#6366f1',
    background: '#1e1b4b',
    padding: '2px 8px',
    borderRadius: 99,
    fontWeight: 500,
  },
  main: {
    flex: 1,
    padding: '32px',
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))',
    gap: '24px',
    alignItems: 'start',
  },
  footer: {
    padding: '16px 32px',
    borderTop: '1px solid #1e293b',
    color: '#475569',
    fontSize: '0.8rem',
  },
}

export default function Dashboard(): React.ReactElement {
  return (
    <div style={styles.shell}>
      <header style={styles.header}>
        <span style={styles.logo}>Student Analytics</span>
        <span style={styles.tag}>Phase 1 MVP</span>
      </header>

      <main style={styles.main}>
        <EnrollmentChart />
        <RetentionChart />
        <GpaChart />
      </main>

      <footer style={styles.footer}>
        5,000 synthetic student records · Polars · FastAPI · Recharts
      </footer>
    </div>
  )
}
