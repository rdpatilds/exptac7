# Feature: Add JSON Export

## Metadata
issue_number: `2`
adw_id: `c737436e`
issue_json: `{"number":2,"title":"Add Json export","body":"feature - adw_sdlc_iso - update to support table and query result 'json' export. Similar to our csv export but specifically built for json export"}`

## Feature Description
Add JSON export functionality for database tables and query results. This feature extends the existing CSV export system by providing a parallel JSON export capability. Users will be able to export entire tables or query results as structured JSON files through download buttons in the UI, similar to the current CSV export functionality. The JSON format provides hierarchical data representation that's ideal for API integration, web development workflows, and modern data pipelines.

## User Story
As a data analyst or developer
I want to export table data and query results as JSON files with one click
So that I can integrate data with APIs, web applications, and modern data processing tools that prefer JSON format

## Problem Statement
While CSV export is excellent for tabular analysis in tools like Excel, many modern workflows require JSON format for:
- API development and testing
- Integration with web applications and JavaScript frameworks
- Data pipelines that consume JSON
- Modern data processing tools that work with structured data
- Maintaining data types and hierarchical structures better than CSV

Currently, users must manually convert CSV exports to JSON or use external tools, creating unnecessary friction in their workflow.

## Solution Statement
Implement JSON export functionality that mirrors the existing CSV export system architecture. This includes:
- Server-side JSON generation utilities similar to `export_utils.py`
- New API endpoints `/api/export/table-json` and `/api/export/query-json`
- Client-side download buttons positioned next to CSV export buttons
- Proper JSON formatting with UTF-8 encoding
- Comprehensive testing for various data types and edge cases
- E2E test validation for the complete export workflow

The solution leverages existing security validation, table checking, and query result handling, ensuring consistency with the proven CSV export implementation.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/export_utils.py` - Contains existing CSV export functions (`generate_csv_from_data`, `generate_csv_from_table`). Add parallel JSON export functions: `generate_json_from_data()` and `generate_json_from_table()`. Use Python's `json` module for serialization with proper encoding.

- `app/server/core/data_models.py` - Contains export models (`ExportRequest`, `QueryExportRequest`). Add new models: `JsonExportRequest` and `JsonQueryExportRequest` if needed, or reuse existing models since the structure is identical.

- `app/server/server.py` - Contains CSV export endpoints (`/api/export/table`, `/api/export/query`). Add parallel JSON endpoints: `/api/export/table-json` and `/api/export/query-json` with appropriate `application/json` media type and `.json` filename extensions.

- `app/client/src/api/client.ts` - Contains CSV export API methods (`exportTable`, `exportQueryResults`). Add parallel methods: `exportTableJson()` and `exportQueryResultsJson()` to call the new JSON endpoints.

- `app/client/src/main.ts` - Contains UI logic for CSV download buttons. Add JSON download buttons next to CSV buttons using a similar icon pattern (e.g., '📊 JSON' to distinguish from '📊 CSV').

- `app/client/src/style.css` - Contains styling for export buttons. Ensure JSON export buttons use consistent styling with CSV buttons.

- `app/server/tests/test_export_utils.py` - Contains comprehensive CSV export tests. Add parallel test class `TestJsonExportUtils` with similar test coverage for JSON export functions.

- `app_docs/feature-490eb6b5-one-click-table-exports.md` - CSV export feature documentation. Use as reference for architecture patterns, security considerations, and documentation structure.

- `README.md` - Project overview and API endpoints documentation. Reference to understand project structure and where to document new JSON endpoints.

### New Files

- `.claude/commands/e2e/test_json_export_functionality.md` - E2E test specification for JSON export functionality. Should mirror `test_export_functionality.md` structure but validate JSON downloads, JSON file structure, proper data types in JSON format, and UTF-8 encoding.

## Implementation Plan
### Phase 1: Foundation
Create the server-side infrastructure for JSON export functionality:
- Add JSON export utility functions to `core/export_utils.py` using Python's built-in `json` module
- Implement proper UTF-8 encoding and handle special characters, None values, and various data types
- Add JSON-specific data models to `core/data_models.py` (or reuse existing models if appropriate)
- Write comprehensive unit tests for JSON generation covering empty data, various data types, special characters, Unicode, and edge cases

### Phase 2: Core Implementation
Build the API endpoints and client-side functionality:
- Add `/api/export/table-json` and `/api/export/query-json` endpoints to `server.py`
- Implement security validation using existing `validate_identifier()` and `check_table_exists()` functions
- Add client-side API methods `exportTableJson()` and `exportQueryResultsJson()` to `api/client.ts`
- Implement proper error handling and logging consistent with CSV export patterns

### Phase 3: Integration
Integrate JSON export into the UI and validate the complete workflow:
- Add JSON download buttons to the UI in `main.ts` positioned next to existing CSV buttons
- Ensure proper styling and icon differentiation between CSV and JSON exports
- Create E2E test specification in `.claude/commands/e2e/test_json_export_functionality.md`
- Run comprehensive validation to ensure zero regressions to existing CSV export functionality

## Step by Step Tasks

### Create JSON Export Utility Functions
- Read `app/server/core/export_utils.py` to understand CSV export implementation
- Add `generate_json_from_data(data: List[Dict], columns: List[str]) -> bytes` function
  - Convert list of dictionaries to JSON array format
  - Handle empty data and empty columns gracefully
  - Use `json.dumps()` with proper formatting (indent=2 for readability)
  - Encode as UTF-8 bytes for consistent file download
  - Handle None values, dates, and special data types
- Add `generate_json_from_table(conn: sqlite3.Connection, table_name: str) -> bytes` function
  - Query table data using pandas (consistent with CSV approach)
  - Convert DataFrame to list of dictionaries
  - Validate table exists before export
  - Use `generate_json_from_data()` internally for consistency

### Create Comprehensive Unit Tests for JSON Export
- Read `app/server/tests/test_export_utils.py` to understand CSV test patterns
- Create `TestJsonExportUtils` class with tests for:
  - `test_generate_json_from_data_empty()` - Empty data handling
  - `test_generate_json_from_data_with_data()` - Standard data export
  - `test_generate_json_from_data_various_types()` - Integer, float, string, boolean, None types
  - `test_generate_json_from_data_special_characters()` - Commas, quotes, newlines
  - `test_generate_json_from_data_unicode()` - Unicode and emoji handling
  - `test_generate_json_from_table_nonexistent()` - Error handling for missing tables
  - `test_generate_json_from_table_empty()` - Empty table export
  - `test_generate_json_from_table_with_data()` - Standard table export
  - `test_generate_json_from_table_special_name()` - Tables with special characters in name
- Run tests to validate JSON export utilities: `cd app/server && uv run pytest tests/test_export_utils.py::TestJsonExportUtils -v`

### Add JSON Export Data Models
- Read `app/server/core/data_models.py` to understand existing export models
- Determine if new models are needed or if existing `ExportRequest` and `QueryExportRequest` can be reused
- If needed, add `JsonExportRequest` and `JsonQueryExportRequest` models (likely can reuse existing)
- Document any model additions in code comments

### Implement JSON Export API Endpoints
- Read `app/server/server.py` to understand CSV export endpoint implementation
- Add `@app.post("/api/export/table-json")` endpoint
  - Accept `ExportRequest` with table name
  - Validate table name using `validate_identifier()`
  - Check table exists using `check_table_exists()`
  - Generate JSON using `generate_json_from_table()`
  - Return `Response` with `media_type="application/json"` and appropriate filename
  - Add comprehensive error handling and logging
- Add `@app.post("/api/export/query-json")` endpoint
  - Accept `QueryExportRequest` with data and columns
  - Generate JSON using `generate_json_from_data()`
  - Return `Response` with `media_type="application/json"` and filename "query_results.json"
  - Add comprehensive error handling and logging

### Add Client-Side JSON Export API Methods
- Read `app/client/src/api/client.ts` to understand CSV export methods
- Add `exportTableJson(tableName: string): Promise<void>` method
  - Call `/api/export/table-json` endpoint
  - Extract filename from Content-Disposition header (default: `${tableName}_export.json`)
  - Create blob and trigger download
  - Handle errors appropriately
- Add `exportQueryResultsJson(data: any[], columns: string[]): Promise<void>` method
  - Call `/api/export/query-json` endpoint
  - Download with filename "query_results.json"
  - Create blob and trigger download
  - Handle errors appropriately

### Add JSON Export Buttons to UI
- Read `app/client/src/main.ts` to understand CSV button implementation
- Locate table export button code (around line 16-18 for download icon)
- Add JSON export button next to CSV button for table exports
  - Use icon like '📊 JSON' to distinguish from CSV
  - Position next to CSV download button
  - Wire up click handler to call `api.exportTableJson(tableName)`
  - Add error handling and user feedback
- Add JSON export button next to CSV button for query results
  - Use similar icon pattern '📊 JSON'
  - Position next to CSV export button in query results section
  - Wire up click handler to call `api.exportQueryResultsJson(data, columns)`
  - Add error handling and user feedback

### Style JSON Export Buttons
- Read `app/client/src/style.css` to understand export button styling
- Ensure JSON export buttons use consistent styling with CSV buttons
- Verify button positioning and spacing is visually balanced
- Test responsive design if applicable

### Create E2E Test Specification for JSON Export
- Read `.claude/commands/test_e2e.md` to understand E2E test framework
- Read `.claude/commands/e2e/test_export_functionality.md` as a template
- Create `.claude/commands/e2e/test_json_export_functionality.md` with:
  - User story for JSON export
  - Test steps that mirror CSV export test but validate JSON downloads
  - Verification steps for:
    - JSON download buttons appear in correct positions
    - JSON files download with correct names (table_export.json, query_results.json)
    - JSON file structure is valid (can be parsed as JSON)
    - Data types are preserved in JSON format
    - Special characters and Unicode are handled correctly
    - Empty results produce valid empty JSON array
  - Success criteria specific to JSON format
  - Screenshot capture points

### Run Validation Commands
- Execute all validation commands to ensure zero regressions:
  - `cd app/server && uv run pytest` - Run all server tests including new JSON export tests
  - `cd app/client && bun tsc --noEmit` - Validate TypeScript compilation
  - `cd app/client && bun run build` - Validate frontend builds successfully
  - Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_json_export_functionality.md` to validate JSON export E2E functionality
  - Manually test CSV export to ensure no regressions
  - Verify all exports (CSV and JSON) work for both tables and query results

## Testing Strategy
### Unit Tests
- **JSON Generation Tests**: Validate `generate_json_from_data()` with various inputs including empty data, different data types (int, float, string, boolean, None), special characters, and Unicode
- **Table Export Tests**: Validate `generate_json_from_table()` with existing tables, non-existent tables, empty tables, and tables with special names
- **Data Type Preservation**: Ensure JSON maintains proper types (numbers as numbers, not strings)
- **UTF-8 Encoding**: Verify proper encoding of Unicode characters and emojis
- **Error Handling**: Test error scenarios like missing tables, invalid table names, and malformed data

### Edge Cases
- Empty tables and empty query results (should produce empty JSON array: `[]`)
- Tables with no data but with schema (empty array with no objects)
- Special characters in data: quotes, newlines, tabs, commas
- Unicode characters and emojis in table names and data
- Very large datasets (performance testing up to 100,000 rows as per CSV export spec)
- Null/None values in data (should become `null` in JSON)
- Mixed data types in columns
- Table names with special characters (hyphens, underscores)
- Concurrent export requests (both CSV and JSON)
- Browser compatibility for download trigger mechanism

## Acceptance Criteria
- JSON export functions successfully generate valid JSON from data and database tables
- JSON files maintain proper data types (numbers as numbers, booleans as booleans, null as null)
- All unit tests pass with 100% coverage for JSON export utilities
- API endpoints `/api/export/table-json` and `/api/export/query-json` respond correctly
- Security validation prevents SQL injection through table name validation
- JSON download buttons appear in the UI next to CSV buttons with clear visual distinction
- Table JSON exports download with filename format: `tablename_export.json`
- Query result JSON exports download with filename: `query_results.json`
- JSON files are properly formatted with UTF-8 encoding
- Special characters, Unicode, and emojis are handled correctly in JSON output
- Empty results produce valid empty JSON arrays
- E2E test validates complete JSON export workflow end-to-end
- CSV export functionality remains fully operational with zero regressions
- All validation commands execute successfully with no errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_export_utils.py::TestJsonExportUtils -v` - Run JSON export unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate no regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript compilation check
- `cd app/client && bun run build` - Run frontend build to validate no issues
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_json_export_functionality.md` to validate JSON export E2E functionality

## Notes
- JSON export leverages Python's built-in `json` module, requiring no additional dependencies
- Implementation follows the exact architectural pattern of CSV export for consistency and maintainability
- JSON format provides better data type preservation compared to CSV (numbers remain numbers, booleans remain booleans)
- JSON is ideal for API integration, JavaScript applications, and modern data pipelines
- The feature maintains security by using existing validation functions from `sql_security.py`
- Both CSV and JSON export options give users flexibility to choose the format that best fits their workflow
- Future enhancements could include XML or Excel export using the same infrastructure pattern
- JSON export handles datasets up to 100,000 rows efficiently using pandas DataFrame operations
- File downloads use the same blob download mechanism as CSV export for cross-browser compatibility
