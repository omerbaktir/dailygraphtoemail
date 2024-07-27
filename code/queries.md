## SQL Queries Documentation

### Example Query

This query retrieves the table names, column count, and total size of each table in the database.

```sql
SELECT 
    t.table_name,
    COUNT(c.column_name) AS column_count,
    pg_size_pretty(pg_total_relation_size(t.table_name::regclass)) AS total_size
FROM 
    information_schema.tables t
JOIN 
    information_schema.columns c ON t.table_name = c.table_name AND t.table_schema = c.table_schema
WHERE 
    t.table_schema NOT IN ('information_schema', 'pg_catalog')
GROUP BY 
    t.table_name
ORDER BY 
    pg_total_relation_size(t.table_name::regclass) DESC;
