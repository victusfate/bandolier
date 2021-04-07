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

deploy_local: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_local/code/bandolier-0.1.0.tar.gz

deploy_d2: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_d2/code/bandolier-0.1.0.tar.gz

deploy_s2: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_s2/code/bandolier-0.1.0.tar.gz

deploy_p2: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_p2/code/bandolier-0.1.0.tar.gz

deploy_gcs: deploy_local deploy_d2 deploy_s2 deploy_p2

clean :
ifeq ($(OS), darwin)
	pip uninstall -y bandolier
endif
ifeq  ($(OS), linux)
	$(linux_pip) uninstall -y bandolier
endif


os :
	@echo $(OS)


