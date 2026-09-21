import logging
from pathlib import Path


def get_logger(name="pipeline"):
	log_path = Path(__file__).parents[2] / "logs" / "pipeline.log"
	log_path.parent.mkdir(parents=True, exist_ok=True)

	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)
	logger.propagate = False

	if not logger.handlers:
		handler = logging.FileHandler(log_path, encoding="utf-8")
		handler.setFormatter(
			logging.Formatter(
				"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
			)
		)
		logger.addHandler(handler)

	return logger
