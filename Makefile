.PHONY: setup-venv download-model setup-mongo setup-postgres serve-tf run-flask run-streamlit run-all

setup-venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

download-model:
	wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
	rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
	chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
	mkdir -p tmp/model/rfcn/1
	mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/rfcn/1
	rm -rf tmp/rfcn_resnet101_coco_2018_01_28

setup-mongo:
	docker rm -f test-mongo || true
	docker run --name test-mongo --rm -p 27017:27017 -d mongo:latest

setup-postgres:
	sudo docker rm -f object-counter-pg || true
	sudo docker run -d \
    	--name object-counter-postgres \
    	-e POSTGRES_DB=object_counter \
    	-e POSTGRES_USER=postgres \
    	-e POSTGRES_PASSWORD=postgres \
    	-p 5432:5432 \
    	postgres:14
	
serve-tf:
	cores_per_socket=$$(lscpu | grep "Core(s) per socket" | cut -d':' -f2 | xargs) && \
	num_sockets=$$(lscpu | grep "Socket(s)" | cut -d':' -f2 | xargs) && \
	num_physical_cores=$$((cores_per_socket * num_sockets)) && \
	sudo docker rm -f tfserving || true
	sudo docker run -d \
    	--name=tfserving \
    	-p 8500:8500 \
    	-p 8501:8501 \
    	-v "$(pwd)/tmp/model:/models" \
    	-e MODEL_NAME=rfcn \
    	-e MODEL_BASE_PATH=/models \
    	tensorflow/serving:latest

run-flask:
	python -m counter.entrypoints.webapp

run-streamlit:
	streamlit run counter/entrypoints/app.py

run-all: setup-venv download-model setup-postgres serve-tf run-flask run-streamlit
