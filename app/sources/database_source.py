import psycopg


def get_connection():
	return psycopg.connect(
		host="localhost",
		port=5432,
		dbname="student_data",
		user="postgres",
		password="YOUR_PASSWORD",
	)


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

	with get_connection() as connection:
		with connection.cursor() as cursor:
			cursor.execute(query)
			columns = [column.name for column in cursor.description]
			return [dict(zip(columns, row)) for row in cursor.fetchall()]
