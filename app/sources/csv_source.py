import csv
from pathlib import Path

from app.utils.logger import get_logger


logger = get_logger("csv_source")


class CSVSourceError(Exception):
	"""Raised when the student CSV cannot be read or parsed."""


def fetch_students(file_path=None):
	if file_path is None:
		file_path = Path(__file__).parents[2] / "data" / "raw" / "students.csv"
	logger.info("Reading student CSV: %s", file_path)

	try:
		with Path(file_path).open(newline="", encoding="utf-8") as csv_file:
			reader = csv.DictReader(csv_file)
			if not reader.fieldnames:
				raise CSVSourceError("The student CSV has no header row.")

			rows = list(reader)
			if not rows:
				raise CSVSourceError("The student CSV is empty.")

			logger.info("Read %d student records from CSV", len(rows))
			return rows
	except CSVSourceError:
		logger.exception("CSV validation failed: %s", file_path)
		raise
	except (OSError, csv.Error) as error:
		logger.exception("CSV read failed: %s", file_path)
		raise CSVSourceError(
			f"Could not read the student CSV: {file_path}"
		) from error
