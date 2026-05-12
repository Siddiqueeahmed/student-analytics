-- Staging layer: enforce types, drop invalid rows.
-- Source: raw `students` table loaded by etl/load.py.
CREATE OR REPLACE TABLE stg_students AS
SELECT
    CAST(student_id            AS BIGINT)  AS student_id,
    CAST(term                  AS VARCHAR) AS term,
    CAST(college               AS VARCHAR) AS college,
    CAST(program               AS VARCHAR) AS program,
    CAST(classification        AS VARCHAR) AS classification,
    CAST(gpa                   AS DOUBLE)  AS gpa,
    CAST(credit_hours_attempted AS INTEGER) AS credit_hours_attempted,
    CAST(credit_hours_earned    AS INTEGER) AS credit_hours_earned,
    CAST(enrolled              AS BOOLEAN) AS enrolled,
    CAST(retained_next_term    AS BOOLEAN) AS retained_next_term
FROM students
WHERE gpa BETWEEN 0.0 AND 4.0
  AND credit_hours_attempted > 0
  AND classification IN ('Freshman', 'Sophomore', 'Junior', 'Senior')
  AND regexp_matches(term, '^(Fall|Spring)\d{4}$');
