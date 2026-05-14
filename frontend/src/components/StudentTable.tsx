import { forwardRef } from 'react'
import { FixedSizeList, type ListChildComponentProps } from 'react-window'
import type { StudentRecord } from '../api/types'
import styles from './StudentTable.module.css'

const RowGroup = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  (props, ref) => <div ref={ref} role="rowgroup" {...props} />,
)
RowGroup.displayName = 'RowGroup'

interface Props {
  data: StudentRecord[]
  height?: number
}

const COLUMNS = [
  'ID', 'Term', 'College', 'Program', 'Class', 'GPA', 'Att', 'Earn', 'Retained',
]

function Row({ index, style, data }: ListChildComponentProps<StudentRecord[]>) {
  const s = data[index]
  return (
    <div style={style} className={styles.row} role="row">
      <span className={styles.cell} role="cell">{s.student_id}</span>
      <span className={styles.cell} role="cell">{s.term}</span>
      <span className={styles.cell} role="cell">{s.college}</span>
      <span className={styles.cell} role="cell">{s.program}</span>
      <span className={styles.cell} role="cell">{s.classification}</span>
      <span className={styles.cell} role="cell">{s.gpa.toFixed(2)}</span>
      <span className={styles.cell} role="cell">{s.credit_hours_attempted}</span>
      <span className={styles.cell} role="cell">{s.credit_hours_earned}</span>
      <span
        className={`${styles.cell} ${s.retained_next_term ? styles.retained : styles.notRetained}`}
        role="cell"
      >
        {s.retained_next_term ? 'Yes' : 'No'}
      </span>
    </div>
  )
}

export function StudentTable({ data, height = 480 }: Props) {
  return (
    <div className={styles.wrapper} role="table" aria-label="Student records">
      <div className={styles.header} role="rowgroup">
        <div role="row">
          {COLUMNS.map((col) => (
            <span key={col} className={styles.headerCell} role="columnheader">
              {col}
            </span>
          ))}
        </div>
      </div>
      <FixedSizeList
        outerElementType={RowGroup}
        height={height}
        itemCount={data.length}
        itemSize={36}
        itemData={data}
        width="100%"
      >
        {Row}
      </FixedSizeList>
    </div>
  )
}
