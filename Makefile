all: install test lint



install: pip-login
	brew list xmlsec1 &>/dev/null || brew install xmlsec1
	make pip-install

pip-install:
	python -m pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	pip install --upgrade cfn-lint

codebuild-install: pip-login
	yum -y install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel
	make pip-install


lint:
	flake8 --count --classmethod-decorators=classmethod,validator --max-line-length=150 \
	--exclude=pncDataSchemas.py,mockData,usbank_transactions_model.py,camt_*model.py,*.aws*,*anna*