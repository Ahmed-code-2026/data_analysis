import pandas as pd

from app.transformation.cleaner import clean_data
from app.validation.quality import validate_data


def test_validate_data_accepts_valid_record():
	data = pd.DataFrame([{
		"student_id": 1001,
		"age": 21,
		"gpa": 3.45,
		"attendance": 92,
		"score": 90,
	}])

	valid_data, invalid_data = validate_data(data)

	assert len(valid_data) == 1
	assert invalid_data.empty


def test_validate_data_rejects_missing_duplicate_and_out_of_range_values():
	data = pd.DataFrame([
		{
			"student_id": 1001,
			"age": 15,
			"gpa": 4.5,
			"attendance": -1,
			"score": 101,
		},
		{
			"student_id": 1001,
			"age": "unknown",
			"gpa": 3.0,
			"attendance": 80,
			"score": 80,
		},
		{
			"student_id": None,
			"age": 21,
			"gpa": 3.0,
			"attendance": 80,
			"score": 80,
		},
	])

	valid_data, invalid_data = validate_data(data)

	assert valid_data.empty
	assert len(invalid_data) == 3
	assert "Duplicate student_id" in invalid_data.iloc[0]["error_reason"]
	assert "Invalid age" in invalid_data.iloc[1]["error_reason"]
	assert "Missing or invalid student_id" in invalid_data.iloc[2]["error_reason"]


def test_clean_data_strips_text_converts_numbers_and_removes_duplicates():
	data = pd.DataFrame([
		{
			"student_id": "1001",
			"age": "21",
			"gpa": "3.45",
			"attendance": "92",
			"score": "90",
			"major": " computer science ",
		},
		{
			"student_id": "1001",
			"age": "21",
			"gpa": "3.45",
			"attendance": "92",
			"score": "90",
			"major": " computer science ",
		},
	])

	cleaned_data = clean_data(data)

	assert len(cleaned_data) == 1
	assert cleaned_data.iloc[0]["major"] == "Computer Science"
	assert cleaned_data.iloc[0]["gpa"] == 3.45