.PHONY: install run-api run-ui backtest fmt lint

install:
	pip install -r requirements.txt

run-api:
	uvicorn api.main:app --reload

run-ui:
	streamlit run ui/streamlit_app.py

backtest:
	python scripts/backtest_gld.py
