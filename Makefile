
.PHONY: init
init:
	git submodule init
	git submodule update

.PHONY: format-import
format-import:
	isort -rc tartiflette_plugin_tartiflette_plugin_scalar/. tests/. setup.py

.PHONY: format
format: format-import
	black -l 79 --py36 tartiflette_plugin_tartiflette_plugin_scalar tests setup.py

.PHONY: check-import
check-import:
	isort --check-only -rc tartiflette_plugin_tartiflette_plugin_scalar/. tests/. setup.py

.PHONY: check-format
check-format:
	black -l 79 --py36 --check tartiflette_plugin_tartiflette_plugin_scalar tests setup.py

.PHONY: style
style: check-format check-import
	pylint tartiflette_plugin_tartiflette_plugin_scalar --rcfile=pylintrc

.PHONY: complexity
complexity:
	xenon --max-absolute B --max-modules B --max-average A tartiflette_plugin_tartiflette_plugin_scalar

.PHONY: test-unit
test-unit: clean
	mkdir -p reports
	py.test -s tests/unit --junitxml=reports/report_unit_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_func.xml $(EXTRA_ARGS)

.PHONY: test-functional
test-functional: clean
	mkdir -p reports
	py.test -s tests/functional --junitxml=reports/report_func_tests.xml --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml:reports/coverage_unit.xml $(EXTRA_ARGS)

.PHONY: test
test: test-unit test-functional

.PHONY: clean
clean:
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '*.pyo' -exec rm -fv {} +
	find . -name '__pycache__' -exec rm -frv {} +
