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
	pip install --user -r release_requirements.txt
	python release.py prepare
	python setup.py sdist bdist_wheel
	twine upload --verbose dist/*
	python release.py initiate
	git push
