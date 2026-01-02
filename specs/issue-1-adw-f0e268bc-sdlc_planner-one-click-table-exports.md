# Feature: One Click Table Exports

## Metadata
issue_number: `1`
adw_id: `f0e268bc`
issue_json: `{"number":1,"title":"one click table exports","body":"feature - adw_sdlc_iso - add one click table exports and one click result export feature to get results as csv files.\n\nCreate two new endpoints to support these features. One exporting tables, one for exporting query results.\n\nPlace download button directly to the left of the 'x' icon for available tables.\nPlace download button directly to the left of the 'hide' button for query results.\n\nUse the appropriate download icon"}`

## Feature Description
This feature enables users to export database tables and query results as CSV files with a single click. Users can download complete table data or current query results for external analysis, reporting, or sharing. The feature integrates seamlessly into the existing UI by placing download buttons strategically next to existing controls, making data export intuitive and accessible. The implementation leverages pandas for efficient CSV generation and includes proper security validation to prevent SQL injection attacks.

## User Story
As a data analyst
I want to export table data and query results as CSV files with one click
So that I can analyze data in external tools like Excel, share results with colleagues, and create reports without manual data copying

## Problem Statement
Users currently have no way to extract data from the Natural Language SQL Interface for use in external applications. When users need to analyze data in Excel, create reports, or share results with team members, they must manually copy and paste data from the web interface, which is time-consuming, error-prone, and impractical for large datasets. This limitation reduces the application's utility as a data analysis tool and creates friction in typical data workflows where users need to move seamlessly between query tools and analysis environments.

## Solution Statement
Implement CSV export functionality with two dedicated API endpoints that generate downloadable CSV files from table data and query results. The backend will use pandas to efficiently convert database records into properly formatted CSV files with UTF-8 encoding. The frontend will add download buttons positioned directly to the left of existing UI controls (the 'x' button for tables, the 'Hide' button for query results) to maintain consistent UI patterns. The solution includes comprehensive security validation using existing SQL security functions to prevent injection attacks, proper error handling for missing tables or failed exports, and client-side blob download functionality to trigger browser downloads with appropriate filenames.

## Relevant Files
Use these files to implement the feature:

### Backend Files
- `app/server/server.py` - Main FastAPI server file where the two new export endpoints will be added (`/api/export/table` and `/api/export/query`). This file already contains the existing API routes and imports necessary security modules.

- `app/server/core/export_utils.py` - New utility module to create for CSV generation functions. This module will contain `generate_csv_from_data()` for exporting query results and `generate_csv_from_table()` for exporting entire tables using pandas.

- `app/server/core/data_models.py` - Data models file where the ExportRequest and QueryExportRequest Pydantic models will be added to define the API request schemas for the export endpoints.

- `app/server/core/sql_security.py` - Security module containing `validate_identifier()` and `check_table_exists()` functions that must be used to validate table names before export to prevent SQL injection attacks.

### Frontend Files
- `app/client/src/main.ts` - Main TypeScript file where download buttons will be added to the UI. The `displayTables()` function needs modification to add export buttons next to table remove buttons. The `displayResults()` function needs modification to add export buttons next to the Hide button for query results.

- `app/client/src/api/client.ts` - API client module where two new methods will be added: `exportTable(tableName: string)` and `exportQueryResults(data, columns)`. These methods will handle POST requests to the export endpoints and trigger browser downloads using blob URLs.

- `app/client/src/style.css` - Stylesheet where styling for the new export buttons will be added to match existing button patterns and ensure proper positioning.

### Testing Files
- `app/server/tests/test_export_utils.py` - New test file to create for comprehensive unit tests covering CSV generation with various data types, empty datasets, edge cases, and error conditions.

### New Files
- `.claude/commands/e2e/test_export_functionality.md` - New E2E test file that validates the complete export workflow including uploading data, verifying button placement, clicking export buttons, and confirming CSV downloads work correctly for both tables and query results.

### Documentation Files
- `README.md` - Should be updated to document the new export endpoints in the API Endpoints section and add usage instructions for the export feature.

- `.claude/commands/test_e2e.md` - E2E test runner documentation needed to understand how to structure and execute the new export functionality test.

- `.claude/commands/e2e/test_basic_query.md` - Example E2E test file to reference for structuring the export functionality test with proper format, user story, test steps, and success criteria.

## Implementation Plan

### Phase 1: Foundation
Create the backend CSV export infrastructure by building a dedicated utility module using pandas for efficient data conversion. Implement secure table validation using existing SQL security functions to prevent injection attacks. Add Pydantic models for type-safe API request validation. This foundation ensures data export operations are secure, efficient, and maintainable.

### Phase 2: Core Implementation
Build two FastAPI endpoints that handle table export and query result export requests. Integrate the export utilities with proper error handling and logging. Create frontend API methods that communicate with the new endpoints and trigger browser downloads using blob URLs. Add download buttons to the UI positioned strategically next to existing controls, maintaining visual consistency with existing patterns. Ensure proper CSV encoding (UTF-8) and appropriate filenames for downloads.

### Phase 3: Integration
Connect the frontend download buttons to the API methods with proper error handling and user feedback. Style the export buttons to match existing UI patterns and ensure proper visual hierarchy. Test the complete export workflow including security validation, large dataset handling, and browser download behavior. Create comprehensive unit tests for the export utilities and an E2E test suite that validates the feature works correctly across the entire stack. Validate zero regressions by running all existing tests.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Create Backend Export Infrastructure
- Create `app/server/core/export_utils.py` module with pandas-based CSV generation functions
- Implement `generate_csv_from_data(data: List[Dict], columns: List[str]) -> bytes` function that converts query results to CSV bytes
- Implement `generate_csv_from_table(conn: sqlite3.Connection, table_name: str) -> bytes` function that exports entire tables to CSV bytes
- Handle UTF-8 encoding properly for international characters
- Handle edge cases including empty datasets, null values, and various data types (integers, floats, strings, dates, booleans)

### Add Data Models for Export Requests
- Open `app/server/core/data_models.py` and add `ExportRequest` model with `table_name: str` field
- Add `QueryExportRequest` model with `data: List[Dict[str, Any]]` and `columns: List[str]` fields
- Use Pydantic Field validators with proper descriptions for API documentation
- Import these models in `app/server/server.py`

### Implement Table Export API Endpoint
- In `app/server/server.py`, add `POST /api/export/table` endpoint
- Accept `ExportRequest` in the request body
- Validate table name using `validate_identifier()` from `sql_security` module
- Check table exists using `check_table_exists()` from `sql_security` module
- Call `generate_csv_from_table()` to get CSV bytes
- Return FastAPI `Response` with `media_type="text/csv"` and `Content-Disposition` header with filename pattern `{table_name}_export.csv`
- Add comprehensive error handling with proper HTTP status codes (404 for missing table, 400 for invalid name, 500 for export errors)
- Add logging for successful exports and errors

### Implement Query Export API Endpoint
- In `app/server/server.py`, add `POST /api/export/query` endpoint
- Accept `QueryExportRequest` in the request body containing results data and column names
- Call `generate_csv_from_data()` to convert the data to CSV bytes
- Return FastAPI `Response` with `media_type="text/csv"` and filename `query_results.csv`
- Add comprehensive error handling and logging
- Validate that columns match the data structure

### Create Frontend Export API Methods
- In `app/client/src/api/client.ts`, add `exportTable(tableName: string): Promise<void>` method
- Make POST request to `/api/export/table` with JSON body containing table_name
- Handle the response blob and create a download link using `window.URL.createObjectURL()`
- Parse the `Content-Disposition` header to get the filename
- Create temporary anchor element, trigger click, and cleanup
- Add error handling with proper error messages
- Add `exportQueryResults(data: any[], columns: string[]): Promise<void>` method
- Make POST request to `/api/export/query` with JSON body containing data and columns
- Handle blob download with fixed filename `query_results.csv`

### Add Export Buttons to Available Tables UI
- In `app/client/src/main.ts`, modify the `displayTables()` function
- Create a container div for buttons with flex layout
- Create export button with appropriate download icon
- Add click handler that calls `api.exportTable(table.name)` with try-catch error handling
- Position export button directly to the left of the remove (x) button
- Add CSS class `export-button` and `table-export-button` for styling
- Add title attribute with tooltip text "Export table as CSV"
- Ensure proper spacing between buttons using CSS gap

### Add Export Button to Query Results UI
- In `app/client/src/main.ts`, modify the `displayResults()` function
- Only show export button when results exist (not for errors or empty results)
- Create export button next to the Hide button in the results header
- Add click handler that calls `api.exportQueryResults(response.results, response.columns)` with error handling
- Position button directly to the left of the Hide button
- Use consistent styling with table export buttons
- Add icon and "Export" text for clarity
- Handle button container structure to maintain proper layout

### Style Export Buttons
- In `app/client/src/style.css`, add styles for `.export-button` class
- Style should match existing secondary buttons for consistency
- Ensure proper hover states and cursor pointer
- Add transition effects matching other buttons
- Ensure buttons are visually distinct but harmonious with existing UI
- Style button containers with proper flex layout and spacing
- Ensure responsive behavior on smaller screens

### Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand E2E test structure
- Read `.claude/commands/e2e/test_basic_query.md` as an example
- Create `.claude/commands/e2e/test_export_functionality.md`
- Include user story describing the export feature from a user perspective
- Define test steps that upload sample data, verify button placement, click export buttons, and validate downloads
- Test both table export and query result export workflows
- Include verification of empty result exports
- Capture screenshots at key steps (initial state, buttons visible, after download)
- Define success criteria including button positioning, download completion, and CSV content validation

### Create Unit Tests for Export Utilities
- Create `app/server/tests/test_export_utils.py`
- Test `generate_csv_from_data()` with various data types (integers, floats, strings, dates, booleans, nulls)
- Test with empty data and empty columns
- Test with mismatched columns and data
- Test `generate_csv_from_table()` with valid table names
- Test with non-existent tables (should raise ValueError)
- Test with special characters in data
- Test UTF-8 encoding with international characters
- Verify CSV format and content correctness
- Use pytest fixtures for database setup and teardown
- Aim for high code coverage of the export utilities module

### Update Documentation
- In `README.md`, add the two new export endpoints to the API Endpoints section
- Add endpoint paths: `POST /api/export/table` and `POST /api/export/query`
- Add brief descriptions of what each endpoint does
- Update the Usage section to document how to export tables and query results from the UI
- Include information about CSV filename patterns

### Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Run server unit tests including the new export utilities tests
- Run frontend type checking to catch TypeScript errors
- Run frontend build to ensure production build succeeds
- Execute the new E2E test to validate the export functionality works end-to-end
- Fix any issues that arise and re-run validation until all tests pass

## Testing Strategy

### Unit Tests
- Test CSV generation from in-memory data structures with various data types
- Test CSV generation from actual SQLite tables
- Test proper handling of null values and empty strings
- Test Unicode/UTF-8 encoding with international characters
- Test edge cases: empty tables, empty results, missing columns
- Test error conditions: invalid table names, non-existent tables, malformed data
- Mock pandas DataFrame operations to test error paths
- Verify CSV format compliance (headers, delimiters, line endings)
- Test large datasets to ensure memory efficiency

### Integration Tests
- Test complete export workflow from API endpoint to CSV generation
- Test security validation at the API boundary
- Test proper HTTP response headers and content types
- Test error responses with appropriate status codes
- Test filename generation and Content-Disposition headers

### E2E Tests
- Upload sample CSV data and verify table export button appears
- Click table export button and verify CSV download with correct filename
- Execute query and verify query results export button appears
- Click query export button and verify CSV download
- Test export with empty query results
- Verify button positioning relative to existing UI elements
- Test error scenarios (network failures, missing tables)
- Capture screenshots documenting the feature in action

### Edge Cases
- Tables with no data (empty tables)
- Query results with no rows
- Query results with no columns
- Tables or columns with special characters in names
- Very large datasets (performance testing)
- Data containing commas, quotes, newlines (CSV escaping)
- Non-ASCII characters and emoji in data
- NULL values and empty strings
- Mixed data types in columns
- Tables with many columns (wide tables)
- Single column tables
- Attempting to export non-existent tables
- Concurrent export requests
- Network interruptions during download

## Acceptance Criteria
- Two new API endpoints are implemented: `POST /api/export/table` and `POST /api/export/query`
- Table export endpoint validates table name and returns CSV file with filename pattern `{table_name}_export.csv`
- Query export endpoint accepts result data and returns CSV file named `query_results.csv`
- Download button appears directly to the left of the 'x' icon for each table in Available Tables section
- Download button appears directly to the left of the 'Hide' button in query results section
- Export buttons use an appropriate download icon (download arrow or CSV indicator)
- Clicking a table export button downloads the complete table data as CSV
- Clicking a query export button downloads the current query results as CSV
- CSV files are properly formatted with headers and UTF-8 encoding
- Empty results export produces valid CSV with headers only
- All export operations include proper error handling and user feedback
- Security validation prevents SQL injection through table name validation
- All existing tests pass with zero regressions
- New unit tests achieve high coverage of export utilities
- E2E test validates the complete export workflow
- Documentation is updated with API endpoints and usage instructions
- Frontend build completes successfully with no TypeScript errors
- Export functionality works for datasets up to 100,000 rows

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_export_functionality.md` to validate this functionality works end-to-end with visual confirmation via screenshots.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Considerations
- The feature leverages pandas which is already a project dependency, avoiding the need to add new external libraries
- Export buttons use Unicode download icons (arrow or text) to maintain consistency with existing UI patterns
- Security validation uses existing `sql_security` module functions to prevent SQL injection attacks
- Large datasets are handled efficiently through pandas DataFrame operations and streaming responses
- CSV format uses UTF-8 encoding to support international characters and special symbols

### Performance Optimization
- For very large tables (>100,000 rows), consider implementing pagination or streaming to prevent memory issues
- Pandas read_sql_query efficiently handles conversion from SQLite to DataFrame
- CSV generation uses StringIO buffer to avoid writing temporary files to disk
- Browser downloads use blob URLs which are memory-efficient for client-side file handling

### Future Enhancements
- Add support for additional export formats (JSON, Excel XLSX, Parquet)
- Implement column selection to export only specific columns
- Add compression support for large CSV files (gzip)
- Implement progress indicators for large exports
- Add export history or download manager
- Support scheduled/automated exports
- Add data transformation options before export (filtering, aggregation)
- Implement batch export for multiple tables
- Add export templates for common report formats

### Security Notes
- All table name inputs are validated using `validate_identifier()` to prevent SQL injection
- Table existence is checked using `check_table_exists()` to prevent information disclosure
- Export endpoints use POST method (not GET) to prevent CSRF attacks and URL parameter injection
- No user input is directly concatenated into SQL queries
- CSV export does not execute arbitrary SQL provided by users
- File download uses Content-Disposition attachment to prevent XSS through CSV injection

### Browser Compatibility
- Blob URL download approach works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Content-Disposition header properly parsed for filename extraction
- Temporary anchor element technique ensures compatibility with browser security policies
- Proper cleanup (revokeObjectURL) prevents memory leaks

### User Experience
- Download buttons are positioned consistently (left of remove/hide buttons) for intuitive discovery
- Button styling matches existing secondary buttons for visual coherence
- Descriptive tooltips explain button functionality on hover
- Error messages provide clear feedback when exports fail
- Success is indicated by browser download notification
- No page reload or navigation required for exports
- Export preserves data types and formatting from database
