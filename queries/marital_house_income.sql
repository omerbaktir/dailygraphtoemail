WITH my_view AS (
    SELECT
        firstname,
        CASE 
            WHEN maritalstatus = 'M' AND houseownerflag = '1' THEN 'Married and owns a house'
            WHEN maritalstatus = 'S' AND houseownerflag = '1' THEN 'Single and owns a house'
            WHEN maritalstatus = 'M' AND houseownerflag = '0' THEN 'Married and does not own a house'
            WHEN maritalstatus = 'S' AND houseownerflag = '0' THEN 'Single and does not own a house'
            ELSE 'Other'
        END AS mar_house,
        yearlyincome
    FROM dimcustomer
)
SELECT mar_house, ROUND(AVG(yearlyincome::numeric)) AS average_income
FROM my_view
GROUP BY mar_house
ORDER BY average_income DESC;
