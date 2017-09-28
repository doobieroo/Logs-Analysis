-- Create views in 'news' postgreSQL db for use with
-- logs_analysis.py 

CREATE VIEW err_reqs AS 
SELECT time::date AS date, count(*) AS tot_err
FROM log
WHERE status <> '200 OK'
GROUP BY date
ORDER BY date ASC;


CREATE VIEW tot_reqs AS 
SELECT time::date AS date, count(*) AS totals
FROM log
GROUP BY date
ORDER BY date ASC;



