import json
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.utils.logger import get_logger


logger = get_logger("api_source")


class APISourceError(Exception):
	"""Raised when academic data cannot be fetched from the REST API."""


def fetch_academic_status(api_url, timeout=10):
	logger.info("Requesting academic API: %s", api_url)
	request = Request(
		api_url,
		headers={"Accept": "application/json"},
	)

	try:
		with urlopen(request, timeout=timeout) as response:
			body = response.read()
	except HTTPError as error:
		logger.exception("Academic API returned HTTP %s", error.code)
		raise APISourceError(
			f"The academic API returned HTTP {error.code}."
		) from error
	except (URLError, TimeoutError, OSError) as error:
		logger.exception("Academic API connection failed: %s", api_url)
		raise APISourceError(
			"Could not connect to the academic API."
		) from error

	if not body.strip():
		logger.error("Academic API returned an empty response: %s", api_url)
		raise APISourceError("The academic API returned an empty response.")

	try:
		data = json.loads(body)
	except json.JSONDecodeError as error:
		logger.exception("Academic API returned invalid JSON: %s", api_url)
		raise APISourceError(
			"The academic API returned invalid JSON."
		) from error

	if not isinstance(data, list) or not data:
		logger.error("Academic API returned an empty or invalid list: %s", api_url)
		raise APISourceError(
			"The academic API response must be a non-empty JSON array."
		)

	if not all(isinstance(record, dict) for record in data):
		logger.error("Academic API returned an invalid record: %s", api_url)
		raise APISourceError(
			"The academic API response contains an invalid record."
		)

	logger.info("Read %d academic records from API", len(data))
	return data

