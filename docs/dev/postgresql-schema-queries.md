# PostgreSQL Schema Retrieval Queries

This document contains useful SQL queries for retrieving and analyzing your PostgreSQL database schema using pgAdmin 4.

## Table of Contents

1. [List All Tables](#list-all-tables)
2. [Detailed Table Information](#detailed-table-information)
3. [List All Indexes](#list-all-indexes)
4. [List All Views](#list-all-views)
5. [List All Functions and Procedures](#list-all-functions-and-procedures)
6. [List All Sequences](#list-all-sequences)
7. [List All Foreign Keys](#list-all-foreign-keys)
8. [Generate CREATE TABLE Statements](#generate-create-table-statements)
9. [Get Table Sizes](#get-table-sizes)
10. [Database Summary](#database-summary)

## List All Tables

```sql
SELECT 
    table_schema,
    table_name,
    table_type
FROM 
    information_schema.tables
WHERE 
    table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY 
    table_schema, table_name;
```

## Detailed Table Information

Get detailed information about all tables, including columns, data types, and constraints:

```sql
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
```

## List All Indexes

```sql
SELECT
    t.schemaname,
    t.tablename,
    i.indexname,
    i.indexdef
FROM
    pg_indexes i
JOIN
    pg_tables t ON i.schemaname = t.schemaname AND i.tablename = t.tablename
WHERE
    t.schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY
    t.schemaname, t.tablename, i.indexname;
```

## List All Views

```sql
SELECT
    table_schema,
    table_name,
    view_definition
FROM
    information_schema.views
WHERE
    table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY
    table_schema, table_name;
```

## List All Functions and Procedures

```sql
SELECT
    n.nspname AS schema_name,
    p.proname AS function_name,
    pg_get_function_arguments(p.oid) AS arguments,
    CASE
        WHEN p.prokind = 'f' THEN 'function'
        WHEN p.prokind = 'p' THEN 'procedure'
        WHEN p.prokind = 'a' THEN 'aggregate'
        WHEN p.prokind = 'w' THEN 'window'
    END AS function_type,
    pg_get_functiondef(p.oid) AS function_definition
FROM
    pg_proc p
JOIN
    pg_namespace n ON p.pronamespace = n.oid
WHERE
    n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY
    schema_name, function_name;
```

## List All Sequences

```sql
SELECT
    sequence_schema,
    sequence_name,
    data_type,
    start_value,
    minimum_value,
    maximum_value,
    increment
FROM
    information_schema.sequences
WHERE
    sequence_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY
    sequence_schema, sequence_name;
```

## List All Foreign Keys

```sql
SELECT
    tc.table_schema,
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM
    information_schema.table_constraints AS tc
JOIN
    information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN
    information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE
    tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY
    tc.table_schema, tc.table_name;
```

## Generate CREATE TABLE Statements

```sql
SELECT
    'CREATE TABLE ' || table_schema || '.' || table_name || ' (' ||
    string_agg(
        column_name || ' ' || data_type ||
        CASE
            WHEN character_maximum_length IS NOT NULL THEN '(' || character_maximum_length || ')'
            ELSE ''
        END ||
        CASE
            WHEN is_nullable = 'NO' THEN ' NOT NULL'
            ELSE ''
        END ||
        CASE
            WHEN column_default IS NOT NULL THEN ' DEFAULT ' || column_default
            ELSE ''
        END,
        ', '
    ) || ');' AS create_table_statement
FROM
    information_schema.columns
WHERE
    table_schema NOT IN ('pg_catalog', 'information_schema')
GROUP BY
    table_schema, table_name
ORDER BY
    table_schema, table_name;
```

## Get Table Sizes

```sql
SELECT
    table_schema,
    table_name,
    pg_size_pretty(pg_total_relation_size('"' || table_schema || '"."' || table_name || '"')) AS total_size,
    pg_size_pretty(pg_relation_size('"' || table_schema || '"."' || table_name || '"')) AS table_size,
    pg_size_pretty(pg_total_relation_size('"' || table_schema || '"."' || table_name || '"') - 
                  pg_relation_size('"' || table_schema || '"."' || table_name || '"')) AS index_size
FROM
    information_schema.tables
WHERE
    table_schema NOT IN ('pg_catalog', 'information_schema')
    AND table_type = 'BASE TABLE'
ORDER BY
    pg_total_relation_size('"' || table_schema || '"."' || table_name || '"') DESC;
```

## Database Summary

```sql
-- Count of tables
SELECT
    count(*) AS table_count
FROM
    information_schema.tables
WHERE
    table_schema NOT IN ('pg_catalog', 'information_schema')
    AND table_type = 'BASE TABLE';

-- Count of views
SELECT
    count(*) AS view_count
FROM
    information_schema.views
WHERE
    table_schema NOT IN ('pg_catalog', 'information_schema');

-- Count of functions
SELECT
    count(*) AS function_count
FROM
    pg_proc p
JOIN
    pg_namespace n ON p.pronamespace = n.oid
WHERE
    n.nspname NOT IN ('pg_catalog', 'information_schema');

-- Database size
SELECT
    pg_size_pretty(pg_database_size(current_database())) AS database_size;
```

## Additional Useful Queries

### List Tables with Row Counts

```sql
SELECT
    schemaname,
    relname,
    n_live_tup
FROM
    pg_stat_user_tables
ORDER BY
    n_live_tup DESC;
```

### List Tables Without Primary Keys

```sql
SELECT
    t.table_schema,
    t.table_name
FROM
    information_schema.tables t
LEFT JOIN
    information_schema.table_constraints tc ON t.table_schema = tc.table_schema
    AND t.table_name = tc.table_name
    AND tc.constraint_type = 'PRIMARY KEY'
WHERE
    t.table_schema NOT IN ('pg_catalog', 'information_schema')
    AND t.table_type = 'BASE TABLE'
    AND tc.constraint_name IS NULL
ORDER BY
    t.table_schema, t.table_name;
```

### List Unused Indexes

```sql
SELECT
    s.schemaname,
    s.relname AS tablename,
    s.indexrelname AS indexname,
    pg_size_pretty(pg_relation_size(s.indexrelid)) AS index_size,
    s.idx_scan
FROM
    pg_stat_user_indexes s
JOIN
    pg_index i ON s.indexrelid = i.indexrelid
WHERE
    s.idx_scan = 0      -- has never been scanned
    AND 0 <>ALL(i.indkey)  -- no index column is an expression
    AND NOT i.indisunique  -- is not a UNIQUE index
    AND NOT EXISTS         -- does not enforce a constraint
            (SELECT 1 FROM pg_constraint c
             WHERE c.conindid = s.indexrelid)
ORDER BY
    pg_relation_size(s.indexrelid) DESC;
```

### List Bloated Tables and Indexes

```sql
SELECT
    schemaname, tablename,
    ROUND(CASE WHEN otta=0 THEN 0.0 ELSE sml.relpages/otta::numeric END,1) AS tbloat,
    CASE WHEN relpages < otta THEN 0 ELSE bs*(sml.relpages-otta)::bigint END AS wastedbytes,
    iname, ROUND(CASE WHEN iotta=0 OR ipages=0 THEN 0.0 ELSE ipages/iotta::numeric END,1) AS ibloat,
    CASE WHEN ipages < iotta THEN 0 ELSE bs*(ipages-iotta) END AS wastedibytes
FROM (
    SELECT
        schemaname, tablename, cc.reltuples, cc.relpages, bs,
        CEIL((cc.reltuples*((datahdr+ma-
            (CASE WHEN datahdr%ma=0 THEN ma ELSE datahdr%ma END))+nullhdr2+4))/(bs-20::float)) AS otta,
        COALESCE(c2.relname,'?') AS iname, COALESCE(c2.reltuples,0) AS ituples, COALESCE(c2.relpages,0) AS ipages,
        COALESCE(CEIL((c2.reltuples*(datahdr-12))/(bs-20::float)),0) AS iotta -- very rough approximation, assumes all cols
    FROM (
        SELECT
            ma,bs,schemaname,tablename,
            (datawidth+(hdr+ma-(case when hdr%ma=0 THEN ma ELSE hdr%ma END)))::numeric AS datahdr,
            (maxfracsum*(nullhdr+ma-(case when nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2
        FROM (
            SELECT
                schemaname, tablename, hdr, ma, bs,
                SUM((1-null_frac)*avg_width) AS datawidth,
                MAX(null_frac) AS maxfracsum,
                hdr+(
                    SELECT 1+count(*)/8
                    FROM pg_stats s2
                    WHERE null_frac<>0 AND s2.schemaname = s.schemaname AND s2.tablename = s.tablename
                ) AS nullhdr
            FROM pg_stats s, (
                SELECT
                    (SELECT current_setting('block_size')::numeric) AS bs,
                    CASE WHEN substring(v,12,3) IN ('8.0','8.1','8.2') THEN 27 ELSE 23 END AS hdr,
                    CASE WHEN v ~ 'mingw32' THEN 8 ELSE 4 END AS ma
                FROM (SELECT version() AS v) AS foo
            ) AS constants
            GROUP BY 1,2,3,4,5
        ) AS foo
    ) AS rs
    JOIN pg_class cc ON cc.relname = rs.tablename
    JOIN pg_namespace nn ON cc.relnamespace = nn.oid AND nn.nspname = rs.schemaname AND nn.nspname <> 'information_schema'
    LEFT JOIN pg_index i ON indrelid = cc.oid
    LEFT JOIN pg_class c2 ON c2.oid = i.indexrelid
) AS sml
WHERE sml.relpages - otta > 0 OR ipages - iotta > 10
ORDER BY wastedbytes DESC, wastedibytes DESC;
```

## Usage Notes

1. These queries are designed to work with PostgreSQL 9.6 and later versions.
2. Some queries may take longer to execute on large databases.
3. To use these queries in pgAdmin 4:
   - Connect to your database
   - Right-click on your database and select "Query Tool"
   - Paste the query and execute it
4. You can modify the WHERE clauses to focus on specific schemas or tables.
5. For large databases, consider adding LIMIT clauses to queries that might return too many rows.
