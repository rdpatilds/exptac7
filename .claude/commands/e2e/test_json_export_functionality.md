# E2E Test: JSON Export Functionality

Test table and query result JSON export functionality in the Natural Language SQL Interface application.

## User Story

As a data analyst or developer
I want to export table data and query results as JSON files with one click
So that I can integrate data with APIs, web applications, and modern data processing tools that prefer JSON format

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Available Tables section

5. Upload a test CSV file containing sample data with various data types
6. **Verify** the table appears in the Available Tables section
7. **Verify** two download buttons appear to the left of the 'x' icon for the table (CSV and JSON)
8. Take a screenshot of the table with export buttons

9. Click the JSON download button for the table (📋 JSON icon)
10. **Verify** a JSON file is downloaded with the table name format: `tablename_export.json`
11. **Verify** the downloaded JSON file:
    - Is valid JSON (can be parsed)
    - Contains an array of objects
    - Data types are preserved (numbers as numbers, booleans as booleans, null as null)
    - Unicode characters and special characters are handled correctly

12. Enter a query: "SELECT * FROM uploaded_table LIMIT 5"
13. Click the Query button
14. **Verify** the query results appear
15. **Verify** two download buttons appear to the left of the 'Hide' button (CSV and JSON)
16. Take a screenshot of query results with export buttons

17. Click the JSON download button for query results
18. **Verify** a JSON file is downloaded named "query_results.json"
19. **Verify** the downloaded JSON file:
    - Is valid JSON (can be parsed)
    - Contains the query results as an array of objects
    - Column names match the query result columns
    - Data is correctly formatted with proper types

20. Execute a query with various data types: "SELECT 1 as int_col, 1.5 as float_col, 'text' as str_col, NULL as null_col"
21. Click the JSON download button
22. **Verify** the JSON file correctly preserves data types:
    - Integer remains as number (not string)
    - Float remains as number with decimal
    - String is a string
    - NULL becomes null in JSON

23. Execute an empty result query: "SELECT * FROM uploaded_table WHERE 1=0"
24. **Verify** the JSON download button is still present
25. Click the JSON download button
26. **Verify** an empty JSON array `[]` is downloaded

27. Upload a table with Unicode characters and special characters
28. Click the JSON download button for this table
29. **Verify** Unicode characters (e.g., 测试, Café, 😀) are preserved correctly in the JSON output

30. Take a screenshot of the final state

## Success Criteria
- JSON download buttons appear next to CSV buttons in correct positions
- Table JSON export downloads complete table as valid JSON
- Query JSON export downloads current results as valid JSON
- JSON files have appropriate names (`tablename_export.json`, `query_results.json`)
- Data types are preserved in JSON format (numbers, booleans, null)
- Empty results produce valid empty JSON array `[]`
- Unicode and special characters are handled correctly
- All JSON files are properly formatted and parseable
- All download operations complete successfully
- CSV export functionality remains fully operational (zero regressions)
- 4 screenshots are taken
