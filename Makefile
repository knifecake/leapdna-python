.PHONY: package
package:
	python3 -m build

.PHONY: test
test:
	mypy leapdna
	coverage run --source leapdna -m unittest discover

.PHONY: install
install: package
	pip install dist/leapdna-0.2.0.tar.gz