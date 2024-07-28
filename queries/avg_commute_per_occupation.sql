WITH
	occupation_commute AS (
		SELECT
			englishoccupation,
			CASE
				WHEN commutedistance = '0-1 Miles' THEN 0.5
				WHEN commutedistance = '1-2 Miles' THEN 1.5
				WHEN commutedistance = '2-5 Miles' THEN 3.5
				WHEN commutedistance = '5-10 Miles' THEN 7.5
				WHEN commutedistance = '10+ Miles' THEN 13
				ELSE 5
			END AS distance
		FROM
			dimcustomer
	)
SELECT
	englishoccupation AS "Occupation",
	ROUND(AVG(distance), 1) AS "Average Commute Distance"
FROM
	occupation_commute
GROUP BY
	englishoccupation
ORDER BY
	AVG(distance) DESC;