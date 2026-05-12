-- Mart: pre-aggregated retention counts at classification × term × college grain.
-- Store raw counts (not the rate) so filtered queries compute accurate weighted rates.
CREATE OR REPLACE TABLE mart_retention_by_classification AS
SELECT
    fe.classification,
    dt.term_name                                       AS term,
    dc.college_name                                    AS college,
    COUNT(*)                                           AS student_count,
    SUM(CAST(fe.retained_next_term AS INTEGER))        AS retained_count
FROM fact_enrollment fe
JOIN dim_term    dt ON fe.term_key    = dt.term_key
JOIN dim_college dc ON fe.college_key = dc.college_key
GROUP BY fe.classification, dt.term_name, dc.college_name;
