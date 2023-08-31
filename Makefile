install:
	pip install poetry && \
	poetry install

start:
	poetry run python Bot_Parser_Database/main.py