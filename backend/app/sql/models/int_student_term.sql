-- Intermediate layer: enrich staging with parsed term fields.
CREATE OR REPLACE TABLE int_student_term AS
SELECT
    s.*,
    CASE
        WHEN s.term LIKE 'Fall%'   THEN 'Fall'
        WHEN s.term LIKE 'Spring%' THEN 'Spring'
    END                                                 AS season,
    CAST(regexp_extract(s.term, '\d{4}') AS INTEGER)    AS academic_year
FROM stg_students s;
