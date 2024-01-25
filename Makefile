install:
	@echo "Installing..."
	python -m venv venv
	venv/bin/python -m pip install --upgrade pip
	venv/bin/python -m pip install -r requirements.txt
	@echo "Done!"

run:
	@echo "Running..."
	python app.py
