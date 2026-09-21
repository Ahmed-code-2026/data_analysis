import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class APISourceError(Exception):
	"""Raised when academic data cannot be fetched from the REST API."""


def fetch_academic_status(api_url, timeout=10):
	request = Request(
		api_url,
		headers={"Accept": "application/json"},
	)

	try:
		with urlopen(request, timeout=timeout) as response:
			body = response.read()
	except HTTPError as error:
		raise APISourceError(
			f"The academic API returned HTTP {error.code}."
		) from error
	except (URLError, TimeoutError, OSError) as error:
		raise APISourceError(
			"Could not connect to the academic API."
		) from error

	if not body.strip():
		raise APISourceError("The academic API returned an empty response.")

	try:
		data = json.loads(body)
	except json.JSONDecodeError as error:
		raise APISourceError(
			"The academic API returned invalid JSON."
		) from error

	if not isinstance(data, list) or not data:
		raise APISourceError(
			"The academic API response must be a non-empty JSON array."
		)

	if not all(isinstance(record, dict) for record in data):
		raise APISourceError(
			"The academic API response contains an invalid record."
		)

	return data
