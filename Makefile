clean:
	rm -rf .cache
	find . -name "*pyc" -delete
	find . -name ".coverage" -delete

build: clean
	pip install --user -r test_requirements.txt

test:
	pytest -v --cov-config .coveragerc --cov .
	coverage xml

install:
	pip install --user .

lint:
	flake8 bioeval

release: build
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*
	python release.py
	git push
