-- Mart: pre-aggregated enrollment counts at college × term × classification grain.
-- Repositories SUM() this on the fly after applying optional WHERE filters.
CREATE OR REPLACE TABLE mart_enrollment_by_college AS
SELECT
    dc.college_name    AS college,
    dt.term_name       AS term,
    fe.classification,
    COUNT(*)           AS count
FROM fact_enrollment fe
JOIN dim_college dc ON fe.college_key = dc.college_key
JOIN dim_term    dt ON fe.term_key    = dt.term_key
GROUP BY dc.college_name, dt.term_name, fe.classification;
