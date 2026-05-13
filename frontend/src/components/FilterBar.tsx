import { useAvailableTerms } from '../api/hooks'
import type { Filters } from '../api/types'
import styles from './FilterBar.module.css'

const CLASSIFICATIONS = ['Freshman', 'Sophomore', 'Junior', 'Senior']

interface Props {
  filters: Filters
  onChange: (f: Filters) => void
}

export default function FilterBar({ filters, onChange }: Props) {
  const { data: terms } = useAvailableTerms()

  const toggleClassification = (cls: string): void => {
    const current = filters.classifications ?? []
    const next = current.includes(cls)
      ? current.filter((c) => c !== cls)
      : [...current, cls]
    onChange({ ...filters, classifications: next.length > 0 ? next : undefined })
  }

  return (
    <div className={styles.bar}>
      <div className={styles.group}>
        <label className={styles.label} htmlFor="term-select">Term</label>
        <select
          id="term-select"
          className={styles.select}
          value={filters.term ?? ''}
          onChange={(e) =>
            onChange({ ...filters, term: e.target.value || undefined })
          }
        >
          <option value="">All terms</option>
          {(terms ?? []).map((t: string) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
      </div>

      <div className={styles.group}>
        <span className={styles.label}>Classification</span>
        <div className={styles.chips} role="group" aria-label="Classification filter">
          {CLASSIFICATIONS.map((cls) => {
            const active = (filters.classifications ?? []).includes(cls)
            return (
              <button
                key={cls}
                type="button"
                className={active ? styles.chipActive : styles.chip}
                aria-pressed={active}
                onClick={() => toggleClassification(cls)}
              >
                {cls}
              </button>
            )
          })}
        </div>
      </div>

      {(filters.term != null || (filters.classifications?.length ?? 0) > 0) && (
        <button
          type="button"
          className={styles.reset}
          onClick={() => onChange({})}
        >
          Clear filters
        </button>
      )}
    </div>
  )
}
