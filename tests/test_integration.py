import pandas as pd
import pytest

from app.transformation.integration import IntegrationError, integrate_data


def test_integrate_data_uses_student_id_and_preserves_sqlite_rows():
	csv_data = [
		{"student_id": "1001", "student_name": "Ahmed Ali"},
		{"student_id": "1002", "student_name": "Sara Mohammed"},
	]
	api_data = [
		{"student_id": 1001, "gpa": 3.45, "attendance": 92},
	]
	database_data = [
		{"student_id": 1001, "course_name": "Database", "score": 90},
		{"student_id": 1001, "course_name": "Programming", "score": 85},
	]

	integrated = integrate_data(csv_data, api_data, database_data)

	assert len(integrated) == 3
	assert integrated["student_id"].tolist() == [1001, 1001, 1002]
	assert integrated.loc[2, "student_name"] == "Sara Mohammed"
	assert pd.isna(integrated.loc[2, "course_name"])


def test_integrate_data_rejects_duplicate_csv_student_ids():
	csv_data = [
		{"student_id": 1001, "student_name": "Ahmed Ali"},
		{"student_id": 1001, "student_name": "Ahmed Ali"},
	]
	api_data = [{"student_id": 1001, "gpa": 3.45}]
	database_data = [{"student_id": 1001, "course_name": "Database"}]

	with pytest.raises(IntegrationError, match="CSV source contains duplicate"):
		integrate_data(csv_data, api_data, database_data)