import styles from './Chart.module.css'

export default function Skeleton(): React.ReactElement {
  return (
    <div className={styles.card}>
      <div className={styles.skeletonTitle} />
      <div className={styles.skeletonSubtitle} />
      <div className={styles.skeletonChart} />
    </div>
  )
}
