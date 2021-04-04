.PHONY: package
package:
	python3 -m build

.PHONY: test
test:
	mypy leapdna
	coverage run --source leapdna -m unittest discover
