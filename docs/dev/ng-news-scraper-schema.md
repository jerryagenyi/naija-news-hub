# QUERY:

SELECT 
    t.table_schema,
    t.table_name,
    c.column_name,
    c.data_type,
    c.character_maximum_length,
    c.is_nullable,
    c.column_default,
    tc.constraint_type,
    cc.table_name AS referenced_table,
    cc.column_name AS referenced_column
FROM 
    information_schema.tables t
JOIN 
    information_schema.columns c ON t.table_schema = c.table_schema AND t.table_name = c.table_name
LEFT JOIN 
    information_schema.key_column_usage kcu ON c.table_schema = kcu.table_schema 
    AND c.table_name = kcu.table_name AND c.column_name = kcu.column_name
LEFT JOIN 
    information_schema.table_constraints tc ON kcu.constraint_schema = tc.constraint_schema 
    AND kcu.constraint_name = tc.constraint_name
LEFT JOIN 
    information_schema.constraint_column_usage ccu ON tc.constraint_schema = ccu.constraint_schema 
    AND tc.constraint_name = ccu.constraint_name
LEFT JOIN 
    information_schema.columns cc ON ccu.table_schema = cc.table_schema 
    AND ccu.table_name = cc.table_name AND ccu.column_name = cc.column_name
WHERE 
    t.table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY 
    t.table_schema, t.table_name, c.ordinal_position;


# RESULT

See @docs/dev/data_ng-news-scraper.csv