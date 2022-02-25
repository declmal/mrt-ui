# Introduction to mrt-ui

Welcome to the introduction of mrt UI package.

This project uses [public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) to [authenticate](https://en.wikipedia.org/wiki/Authentication) the remote computer and allow it to authenticate the user, if necessary.

## Prerequisites Installation

At the very beginning, install the prerequisites:

```bash
pip install -r conf/requirements.txt
```

This step is required in both server side and client side. Clone the project to a specified directory.

```bash
git clone https://github.com/declmal/mrt-ui.git /path/to/mrt-ui
```

Then, some environment varaibles need to be installed by the following command.

```bash
cd /path/to/mrt-ui
./conf/env.sh
```

Don't forget to activate the environment variables by either of the following command with respect to your system.

```bash
# for Linux system
source ~/.bashrc
```

```bash
# for MACOS system
source ~/.bash_profile
```

## RPC Server Configuration

### Launch RPC server on your remote host

Firstly, since mrt_rpc is based on [grpc-python](https://grpc.io/docs/languages/python/quickstart/) whose parameter packing protocol is inherently realized by [protobuf](https://developers.google.com/protocol-buffers), the intermediate generated python code that corresponding to [proto files](), the following command should be executed before the launch of RPC server.   

```bash
make proto
```

The rpc module applies the client-server mode, thus the RPC server should be started before any remote procedured is called. To launch the mrt_rpc server, in the root dir of mrt-ui, execute the following command:

```bash
make rpc-server
```

### Client side unit tests

To run the unit tests, in the root dir of mrt-ui, execute the following commands:

```bash
# test model submission
python tests/test_submit.py \
	--host-addr [remote-server-address] \
	--host-port [remote-server-port] \
	--src-dir [local-model-dir] \
	--model-name [model-name] \
	--dst-dir [remote-model-dir]
```

```bash
# test model quantization
python tests/test_execute.py \
	--host-addr [remote-server-address] \
	--host-port [remote-server-port] \
	--yaml-dir [local-yaml-dir] \
	--model-name [model-name]
```

## Web Server Configuration

MRT-UI has provided a web-browser based user-interface for quick test and visualization of model quantization. The web server can be launched by:

```bash
make web-server
```

Then, we can enter the following url into a web browser and start using the web interface for supported services.

```http
http://127.0.0.1:8000/test
```

