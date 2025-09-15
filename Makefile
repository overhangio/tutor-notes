.DEFAULT_GOAL := help
.PHONY: docs
SRC_DIRS = ./tutornotes
RUFF_OPTS = --exclude templates ${SRC_DIRS}

# Warning: These checks are run on every PR.
test: test-lint test-types test-format test-pythonpackage

test-format: ## Run code formatting tests.
	ruff format --check --diff $(RUFF_OPTS)

test-lint:
	ruff check ${SRC_DIRS}

test-types: ## Run type checks.
	mypy --exclude=templates --ignore-missing-imports --implicit-reexport --strict ${SRC_DIRS}

build-pythonpackage:
	python -m build --sdist

test-pythonpackage: build-pythonpackage
	twine check dist/tutor_notes-$(shell make version).tar.gz

format: ## Format code automatically.
	ruff format $(RUFF_OPTS)

fix-lint: ## Fix linting issues automatically.
	ruff check --fix $(RUFF_OPTS)

isort: ## Sort imports. This target is not mandatory because the output may be incompatible with black formatting. Provided for convenience purposes.
	isort --skip=templates ${SRC_DIRS}

changelog-entry: ## Create a new changelog entry.
	scriv create

changelog: ## Collect changelog entries in the CHANGELOG.md file.
	scriv collect

version: ## Print the current tutor-notes version
	@python -c 'import io, os; about = {}; exec(io.open(os.path.join("tutornotes", "__about__.py"), "rt", encoding="utf-8").read(), about); print(about["__version__"])'

ESCAPE = 
help: ## Print this help.
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
