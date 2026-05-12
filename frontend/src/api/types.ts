export interface CollegeEnrollment {
  college: string
  count: number
}

export interface ClassificationRetention {
  classification: string
  retention_rate: number
}

export interface GpaBucket {
  bucket: string
  count: number
}

export interface StudentRecord {
  student_id: number
  term: string
  college: string
  program: string
  classification: string
  gpa: number
  credit_hours_attempted: number
  credit_hours_earned: number
  retained_next_term: boolean
}

export interface Filters {
  term?: string
  classifications?: string[]
}
