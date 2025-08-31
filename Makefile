
BOOTSTRAP_VERSION = 5.3.8

.PHONY: all clean bootstrap


all: build venv requirements bootstrap


clean:
	rm -rf build venv assets/bootstrap.css


build:
	mkdir -p build

venv:
	python3 -mvenv venv

requirements: venv requirements.txt
	venv/bin/pip3 install -r requirements.txt

bootstrap: build/bootstrap-$(BOOTSTRAP_VERSION) assets/bootstrap.css


build/bootstrap-$(BOOTSTRAP_VERSION): build
	curl --output - -L https://github.com/twbs/bootstrap/archive/refs/tags/v$(BOOTSTRAP_VERSION).tar.gz | tar xvzf -  -C build

assets/bootstrap.css: src/scss/bootstrap.scss 
	sass --quiet --style=compressed --no-source-map $< $@
