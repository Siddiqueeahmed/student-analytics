-- Mart: pre-bucketed GPA counts at bucket × term × classification × college grain.
CREATE OR REPLACE TABLE mart_gpa_distribution AS
SELECT
    FLOOR(fe.gpa / 0.5) * 0.5  AS bucket_start,
    dt.term_name                AS term,
    fe.classification,
    dc.college_name             AS college,
    COUNT(*)                    AS count
FROM fact_enrollment fe
JOIN dim_term    dt ON fe.term_key    = dt.term_key
JOIN dim_college dc ON fe.college_key = dc.college_key
GROUP BY FLOOR(fe.gpa / 0.5) * 0.5, dt.term_name, fe.classification, dc.college_name;
