import sqlite3
from typing import List, Dict, Any
import pandas as pd
import io
import logging

logger = logging.getLogger(__name__)


def generate_csv_from_data(data: List[Dict[str, Any]], columns: List[str]) -> bytes:
    """
    Generate CSV file from data and columns.

    Args:
        data: List of dictionaries containing the data
        columns: List of column names

    Returns:
        bytes: CSV file content as bytes

    Raises:
        ValueError: If data is malformed or columns don't match data structure
    """
    try:
        # Handle empty data case - return CSV with just headers
        if not data and columns:
            df = pd.DataFrame(columns=columns)
        elif not data and not columns:
            # Both empty - return empty CSV
            return b""
        else:
            # Validate that columns exist in data if specified
            if columns and data:
                first_row_keys = set(data[0].keys())
                requested_columns = set(columns)
                if not requested_columns.issubset(first_row_keys):
                    missing = requested_columns - first_row_keys
                    raise ValueError(f"Columns not found in data: {missing}")

            # If no columns specified, use all columns from data
            if not columns and data:
                columns = list(data[0].keys())

            # Create DataFrame from data with specified columns
            df = pd.DataFrame(data)
            if columns:
                df = df[columns]

        # Convert DataFrame to CSV string
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        csv_content = csv_buffer.getvalue()
        csv_buffer.close()

        # Convert to bytes with UTF-8 encoding
        csv_bytes = csv_content.encode('utf-8')

        logger.info(f"Generated CSV from data: {len(data)} rows, {len(columns) if columns else 0} columns")
        return csv_bytes

    except Exception as e:
        logger.error(f"Error generating CSV from data: {str(e)}")
        raise ValueError(f"Failed to generate CSV: {str(e)}")


def generate_csv_from_table(conn: sqlite3.Connection, table_name: str) -> bytes:
    """
    Generate CSV file from a database table.

    Args:
        conn: SQLite database connection
        table_name: Name of the table to export (must be already validated)

    Returns:
        bytes: CSV file content as bytes

    Raises:
        ValueError: If table doesn't exist or export fails
    """
    try:
        # Verify table exists
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """, (table_name,))

        if not cursor.fetchone():
            raise ValueError(f"Table '{table_name}' does not exist")

        # Use pandas to read the entire table
        # Note: Using double quotes to handle table names with special characters
        query = f'SELECT * FROM "{table_name}"'
        df = pd.read_sql_query(query, conn)

        # Convert DataFrame to CSV string
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        csv_content = csv_buffer.getvalue()
        csv_buffer.close()

        # Convert to bytes with UTF-8 encoding
        csv_bytes = csv_content.encode('utf-8')

        logger.info(f"Generated CSV from table '{table_name}': {len(df)} rows, {len(df.columns)} columns")
        return csv_bytes

    except Exception as e:
        logger.error(f"Error generating CSV from table '{table_name}': {str(e)}")
        raise ValueError(f"Failed to export table '{table_name}': {str(e)}")