import json
import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from app.sources.api_source import APISourceError, fetch_academic_status
from app.sources.csv_source import CSVSourceError, fetch_students
from app.sources.database_source import fetch_enrollments


def test_fetch_students_reads_csv_records():
	students = fetch_students()

	assert len(students) == 6
	assert students[0]["student_id"] == "1001"
	assert students[0]["student_name"] == "Ahmed Ali"


def test_fetch_students_raises_for_missing_file(tmp_path):
	missing_file = tmp_path / "missing.csv"

	with pytest.raises(CSVSourceError):
		fetch_students(missing_file)


def test_fetch_academic_status_reads_json_response():
	response = MagicMock()
	response.__enter__.return_value = response
	response.read.return_value = json.dumps([
		{"student_id": 1001, "gpa": 3.45, "attendance": 92}
	]).encode("utf-8")

	with patch("app.sources.api_source.urlopen", return_value=response):
		academic_status = fetch_academic_status("http://mock-api")

	assert academic_status == [
		{"student_id": 1001, "gpa": 3.45, "attendance": 92}
	]


def test_fetch_academic_status_raises_for_invalid_json():
	response = MagicMock()
	response.__enter__.return_value = response
	response.read.return_value = b"{invalid-json"

	with patch("app.sources.api_source.urlopen", return_value=response):
		with pytest.raises(APISourceError, match="invalid JSON"):
			fetch_academic_status("http://mock-api")


def test_fetch_enrollments_reads_joined_records():
	connection = sqlite3.connect(":memory:")
	connection.row_factory = sqlite3.Row
	connection.executescript(
		"""
		CREATE TABLE courses (
			course_id INTEGER PRIMARY KEY,
			course_name TEXT NOT NULL,
			credit_hours INTEGER NOT NULL
		);
		CREATE TABLE enrollments (
			student_id INTEGER NOT NULL,
			course_id INTEGER NOT NULL,
			semester INTEGER NOT NULL,
			score REAL NOT NULL
		);
		INSERT INTO courses VALUES (1, 'Database', 3);
		INSERT INTO enrollments VALUES (1001, 1, 1, 90);
		"""
	)

	with patch("app.sources.database_source.get_connection", return_value=connection):
		enrollments = fetch_enrollments()

	assert enrollments == [{
		"student_id": 1001,
		"course_id": 1,
		"course_name": "Database",
		"credit_hours": 3,
		"semester": 1,
		"score": 90.0,
	}]
	connection.close()
