WITH OccupationCounts AS (
    SELECT
        englisheducation,
        englishoccupation,
        COUNT(*) AS num_people,
        RANK() OVER (PARTITION BY englisheducation ORDER BY COUNT(*) DESC) AS rank
    FROM dimcustomer
    GROUP BY englisheducation, englishoccupation
)
SELECT
    englisheducation,
    englishoccupation,
    num_people
FROM OccupationCounts
WHERE rank = 1;
