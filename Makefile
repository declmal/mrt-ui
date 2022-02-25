PYTHON_DIR=python
RPC_MODULE_NAME=mrt_ui/rpc
PROTO_FILE=service.proto

proto: $(PYTHON_DIR)/$(RPC_MODULE_NAME)/$(PROTO_FILE)
	cd $(PYTHON_DIR) && python -m grpc_tools.protoc \
		-I. --python_out=. --grpc_python_out=. \
		$(RPC_MODULE_NAME)/$(PROTO_FILE)
rpc-server: $(PYTHON_DIR)/$(RPC_MODULE_NAME)/service.py
	python $<
web-server:
	python manage.py runserver 8000
