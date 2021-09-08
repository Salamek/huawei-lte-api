
default:
	@echo "Local examples:"
	@echo "    make style      # Check code styling with flake8."
	@echo "    make lint       # Runs PyLint."
	@echo "    make test       # Tests entire application with pytest."

style:
	flake8 --max-line-length=160 --statistics huawei_lte_api tests

lint:
	pylint3 --max-line-length=160 --max-args=7  huawei_lte_api

test:
	py.test-3 --cov-report term-missing --cov huawei_lte_api tests

testpdb:
	py.test-3 --pdb tests

testcovweb:
	py.test-3 --cov-report html --cov huawei_lte_api tests
	open htmlcov/index.html
