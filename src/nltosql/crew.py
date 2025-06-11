from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tools import tool
from typing import List, Optional
import pandas as pd
import sqlite3
import os

DB_PATH = os.getenv("DATABASE_URL", "ds_salaries.db")


# Define tools outside the class - Fixed parameter handling
@tool("list_tables")
def list_tables() -> str:
    """List all tables in the database"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
        return f"Available tables: {[table[0] for table in tables]}"
    except Exception as e:
        return f"Error listing tables: {e}"


@tool("tables_schema")
def tables_schema(table_name: str = "salaries") -> str:
    """Get the schema/structure of a specific table"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

        schema_info = f"Schema for table '{table_name}':\n"
        for col in columns:
            schema_info += f"- {col[1]} ({col[2]})\n"

        # Add sample data
        with sqlite3.connect(DB_PATH) as conn:
            df_sample = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 3", conn)

        schema_info += f"\nSample data:\n{df_sample.to_string()}"
        return schema_info
    except Exception as e:
        return f"Error getting table schema: {e}"


@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query and return results"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql(sql_query, conn)

        if len(df) > 50:
            return f"Query executed successfully. Results (showing first 50 rows):\n{df.head(50).to_string()}\n\nTotal rows: {len(df)}"
        else:
            return f"Query executed successfully. Results:\n{df.to_string()}"
    except Exception as e:
        return f"Error executing SQL: {e}"


@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """Check if SQL query is valid without executing it fully"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Use EXPLAIN to check query validity
            cursor.execute(f"EXPLAIN {sql_query}")
        return "SQL query is valid and can be executed."
    except Exception as e:
        return f"SQL query validation failed: {e}"


@CrewBase
class Nltosql():
    """Nltosql crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        self.setup_database()

    def setup_database(self):
        """Convert CSV to SQLite database if it doesn't exist"""
        db_path = DB_PATH
        csv_path = 'ds_salaries.csv'

        # Check if database exists and is newer than CSV
        if not os.path.exists(db_path) or (
                os.path.exists(csv_path) and
                os.path.getmtime(csv_path) > os.path.getmtime(db_path)
        ):
            print("Converting CSV to SQLite database...")
            try:
                # Read CSV file
                df = pd.read_csv(csv_path)

                # Create SQLite connection and convert to SQL table
                with sqlite3.connect(db_path) as conn:
                    df.to_sql('salaries', conn, index=False, if_exists='replace')

                print(f"Database created successfully: {db_path}")
                print(f"Table 'salaries' created with {len(df)} rows")

            except FileNotFoundError:
                raise Exception(f"CSV file not found: {csv_path}")
            except Exception as e:
                raise Exception(f"Error converting CSV to database: {e}")

    @agent
    def sql_dev(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_dev'],  # type: ignore[index]
            tools=[list_tables, tables_schema, execute_sql, check_sql],
            verbose=True
        )

    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'],  # type: ignore[index]
            verbose=True
        )

    @task
    def extracting_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_data'],
        )

    @task
    def analyzing_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_data'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_report'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Nltosql crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical
        )

