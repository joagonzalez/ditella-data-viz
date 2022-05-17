run:
	python3 src/application.py

webserver:
	streamlit run run.py --server.maxMessageSize 1024

build:
	docker build -t registry.qwerty.com.ar/ditella-dataviz:1.0.0 .