.PHONY: help setup lint format run test clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup    -> Instala dependências"
	@echo "  make lint     -> Executa Ruff + Black"
	@echo "  make format   -> Formata o código com Black"
	@echo "  make run      -> Executa o projeto"
	@echo "  make clean    -> Remove arquivos do relatório gerados"
	@echo "  make nodata   -> Remove dataset processado"

setup:
	pip install --upgrade pip setuptools wheel
	pip install --no-cache-dir -r requirements.txt


lint:
	ruff check . --fix
	black .

format:
	black .

run:
	python main.py

clean:
	rm -rf __pycache__
	rm -rf report/*.pdf report/*.md report/charts/*.png

nodata:
	rm -rf data/processed/srag_clean.csv
