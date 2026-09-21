import pandas as pd

from app.utils.logger import get_logger


logger = get_logger("integration")


class IntegrationError(Exception):
	"""Raised when source data cannot be integrated."""


def _prepare_source(records, source_name):
	data = pd.DataFrame(records).copy()
	if "student_id" not in data.columns:
		raise IntegrationError(
			f"The {source_name} source must contain student_id."
		)

	data["student_id"] = pd.to_numeric(
		data["student_id"],
		errors="coerce",
	).astype("Int64")
	if data["student_id"].isna().any():
		raise IntegrationError(
			f"The {source_name} source contains an invalid student_id."
		)

	return data


def integrate_data(csv_data, api_data, database_data):
	logger.info("Starting data integration")

	try:
		students = _prepare_source(csv_data, "CSV")
		academic_status = _prepare_source(api_data, "API")
		enrollments = _prepare_source(database_data, "SQLite")

		if students["student_id"].duplicated().any():
			raise IntegrationError(
				"The CSV source contains duplicate student_id values."
			)
		if academic_status["student_id"].duplicated().any():
			raise IntegrationError(
				"The API source contains duplicate student_id values."
			)

		integrated = students.merge(
			academic_status,
			on="student_id",
			how="left",
			validate="one_to_one",
			suffixes=("", "_api"),
		)
		integrated = integrated.merge(
			enrollments,
			on="student_id",
			how="left",
			validate="one_to_many",
			suffixes=("", "_sqlite"),
		)

		logger.info(
			"Data integration completed: %d records",
			len(integrated),
		)
		return integrated
	except IntegrationError:
		logger.exception("Data integration validation failed")
		raise
	except (KeyError, pd.errors.MergeError, TypeError, ValueError) as error:
		logger.exception("Data integration failed")
		raise IntegrationError(
			"Could not integrate the source data."
		) from error
