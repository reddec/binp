all: build

build: system-files python ui test
	cd build && ../venv/bin/python3 -m build

release: build
	cd build && ../venv/bin/twine upload dist/*
dirs:
	rm -rf build
	mkdir -p build/binp

python: dirs
	cp -r binp build/

system-files: dirs
	cp LICENSE setup.py README.md MANIFEST.in build/

ui: dirs
	cd ui && NODE_ENV=production npm --production run build:app
	cp -r ui/dist build/binp/static

test:
	./venv/bin/python -m unittest discover -s tests

.PHONY: all build