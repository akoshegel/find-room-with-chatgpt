run_dev_server:
	python -m uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload

test:
	python -m pytest
