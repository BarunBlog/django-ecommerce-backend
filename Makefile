# Create virtual environment
venv:
	python3 -m venv myvenv

# Activate virtual environment
activate:
	source myvenv/bin/activate

# deactivate virtual environment
deactivate:
	deactivate

docker-build:
	docker compose up --build

docker-down:
	docker compose down

docker-start: |
	docker-down docker-build

runserver: |
	python manage.py runserver 0.0.0.0:8000

generate-model:
	python3 manage.py inspectdb --database hatecholo_db > admin_app/temp_models.py

migrate:
	python3 manage.py migrate --database admin_db

createsuperuser:
	python3 manage.py createsuperuser --database admin_db