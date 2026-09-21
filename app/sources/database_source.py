import sqlite3
from pathlib import Path

from app.utils.logger import get_logger


logger = get_logger("database_source")


class DatabaseConnectionError(Exception):
	"""Raised when a SQLite connection cannot be established."""


class DatabaseQueryError(Exception):
	"""Raised when a SQLite query cannot be executed."""


def get_connection():
	database_path = Path(__file__).parents[2] / "database" / "students.db"
	logger.info("Connecting to SQLite database: %s", database_path)

	try:
		connection = sqlite3.connect(database_path)
		connection.row_factory = sqlite3.Row
		logger.info("SQLite connection established")
		return connection
	except sqlite3.Error as error:
		logger.exception("SQLite connection failed: %s", database_path)
		raise DatabaseConnectionError(
			"Could not connect to the SQLite database."
		) from error


def fetch_enrollments():
	query = """
		SELECT
			e.student_id,
			e.course_id,
			c.course_name,
			c.credit_hours,
			e.semester,
			e.score
		FROM enrollments AS e
		JOIN courses AS c ON c.course_id = e.course_id
		ORDER BY e.student_id, e.course_id
	"""

	try:
		with get_connection() as connection:
			cursor = connection.cursor()
			try:
				cursor.execute(query)
				rows = [dict(row) for row in cursor.fetchall()]
				logger.info("Read %d enrollment records from SQLite", len(rows))
				return rows
			finally:
				cursor.close()
	except DatabaseConnectionError:
		raise
	except sqlite3.Error as error:
		logger.exception("SQLite enrollment query failed")
		raise DatabaseQueryError(
			"Could not execute the enrollment query."
		) from error

