
default:
	@echo "Local examples:"
	@echo "    make style      # Check code styling with flake8."
	@echo "    make lint       # Runs PyLint."
	@echo "    make test       # Tests entire application with pytest."

style:
	flake8 --max-line-length=160 --statistics fire_jack tests

lint:
	pylint3 --max-line-length=160 --max-args=7  fire_jack

test:
	py.test-3 --cov-report term-missing --cov fire_jack tests

testpdb:
	py.test-3 --pdb tests

testcovweb:
	py.test-3 --cov-report html --cov fire_jack tests
	open htmlcov/index.html