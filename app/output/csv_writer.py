from pathlib import Path

import pandas as pd

from app.utils.logger import get_logger


logger = get_logger("csv_writer")


class CSVWriterError(Exception):
	"""Raised when a CSV output cannot be written."""


def write_rejected_records(data, file_path=None):
	if file_path is None:
		file_path = (
			Path(__file__).parents[2]
			/ "data"
			/ "rejected"
			/ "rejected_records.csv"
		)

	output_path = Path(file_path)
	logger.info("Writing rejected records to %s", output_path)

	try:
		output_path.parent.mkdir(parents=True, exist_ok=True)
		pd.DataFrame(data).to_csv(output_path, index=False, encoding="utf-8")
		logger.info("Wrote %d rejected records", len(data))
	except (OSError, ValueError, TypeError) as error:
		logger.exception("Could not write rejected records: %s", output_path)
		raise CSVWriterError(
			f"Could not write rejected records to {output_path}."
		) from error
