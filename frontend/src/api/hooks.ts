import { useQuery, type UseQueryResult } from '@tanstack/react-query'
import type {
  ClassificationRetention,
  CollegeEnrollment,
  Filters,
  GpaBucket,
  StudentRecord,
} from './types'

function buildQs(filters: Filters): string {
  const params = new URLSearchParams()
  if (filters.term) params.set('term', filters.term)
  for (const cls of filters.classifications ?? []) {
    params.append('classification', cls)
  }
  const qs = params.toString()
  return qs ? `?${qs}` : ''
}

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(path)
  if (!res.ok) throw new Error(`API error ${res.status}: ${res.statusText}`)
  return res.json() as Promise<T>
}

export function useEnrollmentByCollege(
  filters: Filters,
): UseQueryResult<CollegeEnrollment[]> {
  return useQuery({
    queryKey: ['enrollment', 'by-college', filters],
    queryFn: () =>
      apiFetch<CollegeEnrollment[]>(`/api/enrollment/by-college${buildQs(filters)}`),
  })
}

export function useRetentionByClassification(
  filters: Filters,
): UseQueryResult<ClassificationRetention[]> {
  return useQuery({
    queryKey: ['retention', 'by-classification', filters],
    queryFn: () =>
      apiFetch<ClassificationRetention[]>(
        `/api/retention/by-classification${buildQs(filters)}`,
      ),
  })
}

export function useGpaDistribution(filters: Filters): UseQueryResult<GpaBucket[]> {
  return useQuery({
    queryKey: ['gpa', 'distribution', filters],
    queryFn: () => apiFetch<GpaBucket[]>(`/api/gpa/distribution${buildQs(filters)}`),
  })
}

export function useStudents(limit = 500): UseQueryResult<StudentRecord[]> {
  return useQuery({
    queryKey: ['students', limit],
    queryFn: () => apiFetch<StudentRecord[]>(`/api/students?limit=${limit}`),
    staleTime: 5 * 60 * 1000,
  })
}
