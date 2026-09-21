import sqlite3
from pathlib import Path


class DatabaseConnectionError(Exception):
	"""Raised when a SQLite connection cannot be established."""


class DatabaseQueryError(Exception):
	"""Raised when a SQLite query cannot be executed."""


def get_connection():
	database_path = Path(__file__).parents[2] / "data" / "student_data.db"

	try:
		connection = sqlite3.connect(database_path)
		connection.row_factory = sqlite3.Row
		return connection
	except sqlite3.Error as error:
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
			with connection.cursor() as cursor:
				cursor.execute(query)
				return [dict(row) for row in cursor.fetchall()]
	except DatabaseConnectionError:
		raise
	except sqlite3.Error as error:
		raise DatabaseQueryError(
			"Could not execute the enrollment query."
		) from error

