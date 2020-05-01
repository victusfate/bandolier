.PHONY : githook all os init dev_dependencies dependencies start watch clean

githook: init dependencies

all : init dev_dependencies dependencies os package

OS := $(shell uname -s | tr A-Z a-z)
linux_python = /usr/bin/python3
linux_pip = /usr/local/bin/pip3

init :
ifeq ($(OS), darwin)
	pip uninstall -y bandolier
	pip install -r requirements.txt
endif
ifeq ($(OS), linux)
	$(linux_pip) uninstall -y bandolier
	$(linux_pip) install -r requirements.txt --user
endif

dependencies :
ifeq ($(OS), darwin)
	pip install .
endif
ifeq ($(OS), linux)
	$(linux_pip) install . --user
endif

dev_dependencies :
ifeq ($(OS), darwin)
	pip install -e ./
endif
ifeq ($(OS), linux)
	$(linux_pip) install -e ./  --user
endif

dev: init dev_dependencies

package :
ifeq ($(OS), darwin)
	python setup.py sdist bdist_wheel
endif
ifeq ($(OS), linux)
	$(linux_python) setup.py sdist bdist_wheel
endif

deploy_dev: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_dev/code

deploy_prod: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_prod/code

clean :
ifeq ($(OS), darwin)
	pip uninstall -y bandolier
endif
ifeq  ($(OS), linux)
	$(linux_pip) uninstall -y bandolier
endif


os :
	@echo $(OS)


