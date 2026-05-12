# Entity-Relationship Diagram

The star schema lives in `data/analytics.duckdb`. Raw data flows from CSV → staging → intermediate → star schema → mart tables.

## Star Schema

```mermaid
erDiagram
    dim_term {
        INTEGER term_key PK
        VARCHAR term_name
        VARCHAR season
        INTEGER academic_year
    }

    dim_college {
        INTEGER college_key PK
        VARCHAR college_name
    }

    dim_program {
        INTEGER program_key PK
        VARCHAR program_name
    }

    dim_student {
        INTEGER student_key PK
        BIGINT student_id
    }

    fact_enrollment {
        INTEGER term_key FK
        INTEGER college_key FK
        INTEGER program_key FK
        INTEGER student_key FK
        VARCHAR classification
        DOUBLE gpa
        INTEGER credit_hours_attempted
        INTEGER credit_hours_earned
        BOOLEAN retained_next_term
    }

    fact_enrollment }o--|| dim_term : "term_key"
    fact_enrollment }o--|| dim_college : "college_key"
    fact_enrollment }o--|| dim_program : "program_key"
    fact_enrollment }o--|| dim_student : "student_key"
```

## Mart Tables (pre-aggregated KPIs)

```mermaid
erDiagram
    mart_enrollment_by_college {
        VARCHAR college
        VARCHAR term
        VARCHAR classification
        BIGINT count
    }

    mart_retention_by_classification {
        VARCHAR classification
        VARCHAR term
        BIGINT student_count
        BIGINT retained_count
    }

    mart_gpa_distribution {
        DOUBLE bucket_start
        VARCHAR term
        VARCHAR classification
        VARCHAR college
        BIGINT count
    }
```

## ETL Data Flow

```
students.csv
    └─► stg_students          (cast + filter raw rows)
            └─► int_student_term  (derive season, academic_year)
                    └─► dim_*  fact_enrollment  (star schema)
                                    └─► mart_enrollment_by_college
                                    └─► mart_retention_by_classification
                                    └─► mart_gpa_distribution
```

## Auth Table

```mermaid
erDiagram
    users {
        VARCHAR user_id PK
        VARCHAR email UK
        VARCHAR hashed_password
        VARCHAR role
        BOOLEAN is_active
    }
```
