import { useStudents } from '../api/hooks'
import { StudentTable } from '../components/StudentTable'
import { Skeleton } from '../components/Skeleton'
import styles from './Students.module.css'

export function StudentsPage() {
  const { data, isLoading, isError, error } = useStudents(500)

  return (
    <main className={styles.page}>
      <h2 className={styles.heading}>Student Records</h2>

      {isLoading && <Skeleton />}

      {isError && (
        <p className={styles.error} role="alert">
          {error instanceof Error ? error.message : 'Failed to load students'}
        </p>
      )}

      {data && (
        <>
          <p className={styles.meta}>{data.length.toLocaleString()} records</p>
          <StudentTable data={data} height={520} />
        </>
      )}
    </main>
  )
}
