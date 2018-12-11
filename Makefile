.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

TYPES_SRC := "$(GOPATH)/src/github.com/aergoio/aergo/config/types.go"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: protoclean clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -f coverage.xml

lint: ## check style with flake8
	flake8 herapy tests

test: ## run tests quickly with the default Python
	PYTHONPATH=./
	pytest -s

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	py.test --cov=./aergo tests --cov-report=html

docs:
	rm -rf docs/pydoc
	mkdir -p docs/pydoc
	python3 -m pydoc -w `find . -name "*.py"` 2>&1 /dev/null
	mv *.html docs/pydoc

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

protoc: ## generate *_pb2.py and *_pb2_grpc.py in aergo/herapy/grpc from aergo-protobuf/proto/*.proto
	python -m grpc_tools.protoc \
		-I./aergo-protobuf/proto \
		--python_out=./aergo/herapy/grpc \
		--grpc_python_out=./aergo/herapy/grpc \
		./aergo-protobuf/proto/*.proto
	find ./aergo/herapy/grpc -type f -name '*_pb2.py' -exec sed -i '' -e 's/^import\(.*\)_pb2\(.*\)$$/from . import\1_pb2\2/g' {} \;
	find ./aergo/herapy/grpc -type f -name '*_pb2_grpc.py' -exec sed -i '' -e 's/^import\(.*\)_pb2\(.*\)$$/from . import\1_pb2\2/g' {} \;

protoclean:
	rm -f aergo/herapy/grpc/*_pb2*.py

aergo-types: ## generate aergo/herapy/obj/aergo_conf.py from aergo/config/types.go
ifeq ($(strip $(wildcard $(TYPES_SRC))), )
	python ./scripts/generate_aergo_conf.py $(TYPES_SRC) > ./aergo/herapy/obj/aergo_conf.py
else
	echo "Cannot find $(TYPES_SRC)"
endif

