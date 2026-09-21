import pandas as pd

from app.output.csv_writer import write_rejected_records


def test_write_rejected_records_creates_csv(tmp_path):
	output_path = tmp_path / "rejected" / "rejected_records.csv"
	rejected_data = pd.DataFrame([
		{"student_id": 1001, "error_reason": "Invalid GPA; "},
	])

	write_rejected_records(rejected_data, output_path)

	result = pd.read_csv(output_path)
	assert result.to_dict(orient="records") == [
		{"student_id": 1001, "error_reason": "Invalid GPA; "},
	]