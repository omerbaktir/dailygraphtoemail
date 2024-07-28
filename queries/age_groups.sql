SELECT age_category, COUNT(*) as total_customers
FROM (
    SELECT 
        CASE 
            WHEN EXTRACT(year FROM age(CURRENT_DATE, birthdate)) BETWEEN 0 AND 25 THEN '0-25'
            WHEN EXTRACT(year FROM age(CURRENT_DATE, birthdate)) BETWEEN 26 AND 35 THEN '26-35'
            WHEN EXTRACT(year FROM age(CURRENT_DATE, birthdate)) BETWEEN 36 AND 45 THEN '36-45'
            WHEN EXTRACT(year FROM age(CURRENT_DATE, birthdate)) BETWEEN 46 AND 55 THEN '46-55'
            WHEN EXTRACT(year FROM age(CURRENT_DATE, birthdate)) BETWEEN 56 AND 65 THEN '56-65'
            ELSE '65+'
        END AS age_category
    FROM dimcustomer
) as age_groups
GROUP BY age_category
ORDER BY age_category;