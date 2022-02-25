from concurrent import futures
import os
from os import path

import grpc

import mrt_ui.rpc.service_pb2 as pb2
import mrt_ui.rpc.service_pb2_grpc as pb2_grpc
from mrt_ui.rpc.utils import get_streamer

# TODO(ryt): load balancer for maxinum_workers
maximum_workers = 4
# socket host difference
local_port = 5000
local_addr = "0.0.0.0"
chunk_size = 1024 * 1024  # 1MB


class MRTRpcSrv(pb2_grpc.MRTRpcSrvServicer):
    def submit(self, request_iterator, context):
        model_dir = str(next(request_iterator).chunck, 'utf-8')
        if model_dir.startswith("~"):
            model_dir = path.expanduser(model_dir)
        os.makedirs(model_dir, exist_ok=True)
        file_name = str(next(request_iterator).chunck, 'utf-8')
        size = eval(str(next(request_iterator).chunck, 'utf-8'))
        dst_file = path.join(model_dir, file_name)
        with open(dst_file, 'wb') as f:
            cur_size = 0
            for piece in request_iterator:
                f.write(piece.chunck)
                cur_size += chunk_size
                cur_size = min(cur_size, size)
                message = "Current: {} Bytes / Total: {} Bytes, ".format(
                    cur_size, size) + \
                    "{} % Completed".format(round(cur_size/size*100.0, 2))
                yield pb2.MRTServerResp(logging_str=message)

    def execute(self, request, context):
        yaml_file_str = request.content
        my_streamer = get_streamer(yaml_file_str)
        for message in my_streamer.start():
            if not context.is_active():
                raise RuntimeError("client connection lost")
            yield pb2.MRTServerResp(logging_str=message)
        #  if context.is_active():
            #  context.cancel()

def main():
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=maximum_workers))
    pb2_grpc.add_MRTRpcSrvServicer_to_server(
        MRTRpcSrv(), grpc_server)
    address = "{0}:{1}".format(local_addr, local_port)
    grpc_server.add_insecure_port(address)
    grpc_server.start()
    print("server will start at {0}".format(address))
    grpc_server.wait_for_termination()

if __name__ == '__main__':
    main()
