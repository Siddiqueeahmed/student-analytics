-- Star schema dimensions and fact table.
-- All tables created from int_student_term.

CREATE OR REPLACE TABLE dim_term AS
SELECT
    row_number() OVER (ORDER BY term) AS term_key,
    term                              AS term_name,
    CASE WHEN term LIKE 'Fall%' THEN 'Fall' ELSE 'Spring' END AS season,
    CAST(regexp_extract(term, '\d{4}') AS INTEGER)             AS academic_year
FROM (SELECT DISTINCT term FROM int_student_term);

CREATE OR REPLACE TABLE dim_college AS
SELECT
    row_number() OVER (ORDER BY college) AS college_key,
    college                              AS college_name
FROM (SELECT DISTINCT college FROM int_student_term);

CREATE OR REPLACE TABLE dim_program AS
SELECT
    row_number() OVER (ORDER BY p.program) AS program_key,
    p.program                              AS program_name,
    dc.college_key
FROM (SELECT DISTINCT program, college FROM int_student_term) p
JOIN dim_college dc ON p.college = dc.college_name;

CREATE OR REPLACE TABLE dim_student AS
SELECT
    row_number() OVER (ORDER BY student_id) AS student_key,
    student_id
FROM (SELECT DISTINCT student_id FROM int_student_term);

CREATE OR REPLACE TABLE fact_enrollment AS
SELECT
    row_number() OVER ()    AS fact_key,
    ds.student_key,
    dt.term_key,
    dp.program_key,
    dc.college_key,
    i.classification,
    i.gpa,
    i.credit_hours_attempted,
    i.credit_hours_earned,
    i.enrolled,
    i.retained_next_term
FROM int_student_term i
JOIN dim_student  ds ON i.student_id = ds.student_id
JOIN dim_term     dt ON i.term       = dt.term_name
JOIN dim_program  dp ON i.program    = dp.program_name AND i.college = (SELECT college_name FROM dim_college WHERE college_key = dp.college_key)
JOIN dim_college  dc ON i.college    = dc.college_name;
