.PHONY : githook
githook: init dependencies

.PHONY : all
all : init dev_dependencies dependencies os package

OS := $(shell uname -s | tr A-Z a-z)
linux_python = /usr/bin/python3
linux_pip = /usr/local/bin/pip3

.PHONY : init
init :
ifeq ($(OS), darwin)
	pip uninstall -y bandolier
	pip install -r requirements.txt
endif
ifeq ($(OS), linux)
	$(linux_pip) uninstall -y bandolier
	$(linux_pip) install -r requirements.txt --user
endif

.PHONY : dependencies
dependencies :
ifeq ($(OS), darwin)
	pip install .
endif
ifeq ($(OS), linux)
	$(linux_pip) install . --user
endif

.PHONY : dev_dependencies
dev_dependencies :
ifeq ($(OS), darwin)
	pip install -e ./
endif
ifeq ($(OS), linux)
	$(linux_pip) install -e ./  --user
endif

.PHONY : dev
dev: init dev_dependencies

.PHONY : package
package :
ifeq ($(OS), darwin)
	python setup.py sdist bdist_wheel
endif
ifeq ($(OS), linux)
	$(linux_python) setup.py sdist bdist_wheel
endif

.PHONY : depoy_local
deploy_local: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_local/code/bandolier-0.1.0.tar.gz

.PHONY : depoy_d2
deploy_d2: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_d2/code/bandolier-0.1.0.tar.gz

.PHONY : depoy_beta
deploy_beta: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_beta/code/bandolier-0.1.0.tar.gz

.PHONY : depoy_prod
deploy_prod: package
	gsutil cp dist/bandolier*.tar.gz gs://welcome_prod/code/bandolier-0.1.0.tar.gz

.PHONY : depoy_gcs
deploy_gcs: deploy_local deploy_d2 deploy_beta deploy_prod

.PHONY : clean
clean :
ifeq ($(OS), darwin)
	pip uninstall -y bandolier
endif
ifeq  ($(OS), linux)
	$(linux_pip) uninstall -y bandolier
endif

.PHONY : os
os :
	@echo $(OS)


