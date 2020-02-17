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

ifndef AERGO_TYPES_SRC
	TYPES_SRC := $(GOPATH)/src/github.com/aergoio/aergo/config/types.go
else
	TYPES_SRC := $(AERGO_TYPES_SRC)
endif

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

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
	# fix E722 later, ignore W503 as it will be considered best practice
	flake8 \
		--exclude=*_pb2_grpc.py,*_pb2.py,aergo_conf.py \
		--ignore=E722,W503 \
		--per-file-ignores="__init__.py:F401" \
		aergo tests

test: ## run tests quickly with the default Python
	pytest -s

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	py.test --cov-report=html --cov=aergo/ tests/

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

uninstall: ## uninstall the package in the active Python's site-packages
	pip uninstall aergo-herapy -y

protoc: ## generate *_pb2.py and *_pb2_grpc.py in aergo/herapy/grpc from aergo-protobuf/proto/*.proto
	python -m grpc_tools.protoc \
		-I./aergo-protobuf/proto \
		--python_out=./aergo/herapy/grpc \
		--grpc_python_out=./aergo/herapy/grpc \
		./aergo-protobuf/proto/*.proto
	find ./aergo/herapy/grpc -type f -name '*_pb2.py' -exec sed -i '' -e 's/^import\(.*\)_pb2\(.*\)$$/from . import\1_pb2\2/g' {} \;
	find ./aergo/herapy/grpc -type f -name '*_pb2_grpc.py' -exec sed -i '' -e 's/^import\(.*\)_pb2\(.*\)$$/from . import\1_pb2\2/g' {} \;

protoclean: ## remove all generated files in aergo/herapy/grpc by 'make protoc'
	rm -f aergo/herapy/grpc/*_pb2*.py

aergo-types: ## generate aergo/herapy/obj/aergo_conf.py from github.com/aergoio/aergo/config/types.go
ifneq ($(wildcard $(TYPES_SRC)), )
	python ./scripts/generate_aergo_conf.py $(TYPES_SRC) ./scripts/aergo_default_conf.toml > ./aergo/herapy/obj/aergo_conf.py
else
	@echo "ERROR: Cannot find 'AERGO_TYPES_SRC':" $(TYPES_SRC)
endif

local_dpos_testnet:
	docker-compose -f ./tests/local_dpos_testnet/docker-compose.yml up

clean_local_testnets:
	rm -fr tests/local_dpos_testnet/*/data
	docker-compose -f ./tests/local_dpos_testnet/docker-compose.yml down

ex: ## run all examples in the examples directory
	pip show aergo-herapy
	@echo "===============================" > make.ex.out
	@echo "Result of 'examples/account.py'" >> make.ex.out
	@echo "===============================" >> make.ex.out
	@echo "Run ... 'examples/account.py'"
	@python ./examples/account.py > make.ex.out
	@echo "=======================================" >> make.ex.out
	@echo "Result of 'examples/account_exp_imp.py'" >> make.ex.out
	@echo "=======================================" >> make.ex.out
	@echo "Run ... 'examples/account_exp_imp.py'"
	@python ./examples/account_exp_imp.py >> make.ex.out
	@echo "=====================================" >> make.ex.out
	@echo "Result of 'examples/account_proof.py'" >> make.ex.out
	@echo "=====================================" >> make.ex.out
	@echo "Run ... 'examples/account_proof.py'"
	@python ./examples/account_proof.py >> make.ex.out
	@echo "==================================" >> make.ex.out
	@echo "Result of 'examples/blockchain.py'" >> make.ex.out
	@echo "==================================" >> make.ex.out
	@echo "Run ... 'examples/blockchain.py'"
	@python ./examples/blockchain.py >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Result of 'examples/blockchain_stream.py'" >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Run ... 'examples/blockchain_stream.py'"
	@python ./examples/blockchain_stream.py >> make.ex.out
	@echo "=====================================" >> make.ex.out
	@echo "Result of 'examples/smartcontract.py'" >> make.ex.out
	@echo "=====================================" >> make.ex.out
	@echo "Run ... 'examples/smartcontract.py'"
	@python ./examples/smartcontract.py >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Result of 'examples/smartcontract_event.py'" >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Run ... 'examples/smartcontract_event.py'"
	@python ./examples/smartcontract_event.py >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Result of 'examples/smartcontract_event_stream.py'" >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Run ... 'examples/smartcontract_event_stream.py'"
	@python ./examples/smartcontract_event_stream.py >> make.ex.out
	@echo "================================================" >> make.ex.out
	@echo "Result of 'examples/smartcontract_batch_call.py'" >> make.ex.out
	@echo "================================================" >> make.ex.out
	@echo "Run ... 'examples/smartcontract_batch_call.py'"
	@python ./examples/smartcontract_batch_call.py >> make.ex.out
	@echo "===========================================" >> make.ex.out
	@echo "Result of 'examples/smartcontract_query.py'" >> make.ex.out
	@echo "===========================================" >> make.ex.out
	@echo "Run ... 'examples/smartcontract_query.py'"
	@python ./examples/smartcontract_query.py >> make.ex.out
	@echo "===================================" >> make.ex.out
	@echo "Result of 'examples/transaction.py'" >> make.ex.out
	@echo "===================================" >> make.ex.out
	@echo "Run ... 'examples/transaction.py'"
	@python ./examples/transaction.py >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Result of 'examples/transaction_batch.py'" >> make.ex.out
	@echo "=========================================" >> make.ex.out
	@echo "Run ... 'examples/transaction_batch.py'"
	@python ./examples/transaction_batch.py >> make.ex.out
	@echo "See 'make.ex.out' to check the results"
