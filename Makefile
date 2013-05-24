venv:
	virtualenv venv

install: venv
	. venv/bin/activate; pip install -r requirements.txt

crawl: venv
	. venv/bin/activate; python crawl.py

test:
	. venv/bin/activate; nosetests
