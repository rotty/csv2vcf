SRC_CORE=.

help:
	@echo "Some available commands:"
	@echo " * run          - Run code."
	@echo " * test         - Run unit tests and test coverage."
	@echo " * doc          - Document code (pydoc)."
	@echo " * clean        - Cleanup (e.g. pyc files)."
	@echo " * code-style   - Check code style (pycodestyle)."
	@echo " * code-lint    - Check code lints (pyflakes, pyline)."
	@echo " * code-count   - Count code lines (cloc)."
	@echo " * deps-install - Install dependencies (see requirements.txt)."
	@echo " * deps-update  - Update dependencies (via pur)."
	@echo " * feedback     - Create a GitHub issue."

run:
	@python $(SRC_CORE)/csv2vcf.py

test:
	@echo "no test implemented, yet"
	@type coverage >/dev/null 2>&1 || (echo "Run 'pip install coverage' first." >&2 ; exit 1)
	@coverage run --source . -m tests.test_csv2vcf
	@coverage report

doc:
	@pydoc csv2vcf

clean:
	@rm $(SRC_CORE)/*.pyc

code-style:
	@type pycodestyle >/dev/null 2>&1 || (echo "Run 'pip install pycodestyle' first." >&2 ; exit 1)
	@pycodestyle --max-line-length=80 $(SRC_CORE)

code-lint:
	@type pyflakes >/dev/null 2>&1 || (echo "Run 'pip install pyflakes' first." >&2 ; exit 1)
	@type pylint >/dev/null 2>&1 || (echo "Run 'pip install pylint' first." >&2 ; exit 1)
	@type flake8 >/dev/null 2>&1 || (echo "Run 'pip install flake8' first." >&2 ; exit 1)
	@pyflakes $(SRC_CORE)
	@pylint $(SRC_CORE)
	@flake8 --max-complexity 10 $(SRC_CORE)

code-count:
	@type cloc >/dev/null 2>&1 || (echo "Run 'brew install cloc' first." >&2 ; exit 1)
	@cloc $(SRC_CORE)

deps-update:
	@type pur >/dev/null 2>&1 || (echo "Run 'pip install pur' first." >&2 ; exit 1)
	@pur -r requirements.txt

deps-install:
	@type pip >/dev/null 2>&1 || (echo "Run 'curl https://bootstrap.pypa.io/get-pip.py|sudo python' first." >&2 ; exit 1)
	@pip install -r requirements.txt

feedback:
	@open https://github.com/AlexanderWillner/csv2vcf/issues
