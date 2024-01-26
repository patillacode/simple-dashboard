install:
	@echo "Installing..."
	python -m venv venv
	venv/bin/python -m pip install --upgrade pip
	venv/bin/python -m pip install -r requirements.txt
	cp services.sample.json services.json
	@echo "Done!"

run:
	@echo "Running..."
	venv/bin/python app.py
