init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	py.test
