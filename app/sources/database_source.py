import psycopg


class DatabaseConnectionError(Exception):
	"""Raised when a PostgreSQL connection cannot be established."""


class DatabaseQueryError(Exception):
	"""Raised when a PostgreSQL query cannot be executed."""


def get_connection():
	try:
		return psycopg.connect(
			host="localhost",
			port=5432,
			dbname="student_data",
			user="postgres",
			password="123321",
		)
	except psycopg.OperationalError as error:
		raise DatabaseConnectionError(
			"Could not connect to the PostgreSQL database."
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
				columns = [column.name for column in cursor.description]
				return [dict(zip(columns, row)) for row in cursor.fetchall()]
	except DatabaseConnectionError:
		raise
	except psycopg.Error as error:
		raise DatabaseQueryError(
			"Could not execute the enrollment query."
		) from error

