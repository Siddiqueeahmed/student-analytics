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

export interface Filters {
  term?: string
  classifications?: string[]
}
