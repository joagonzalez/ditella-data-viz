run:
	python3 src/application.py

webserver:
	streamlit run run.py --server.maxMessageSize 1024