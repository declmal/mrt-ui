import os
from os import path
from shutil import copyfile

import grpc

from mrt_ui.rpc.service import chunk_size
import mrt_ui.rpc.service_pb2 as pb2
import mrt_ui.rpc.service_pb2_grpc as pb2_grpc
from mrt_ui.rpc.utils import get_streamer

default_dir = "~/mrt_model"

def mrt_submit(
    src_sym_file, src_prm_file, dst_model_dir=default_dir, host_addr=None):
    if not path.exists(src_sym_file):
        raise RuntimeError("file: {} not exist".format(src_sym_file))
    if not path.exists(src_prm_file):
        raise RuntimeError("file: {} not exist".format(src_prm_file))

    model_name = path.splitext(path.basename(src_sym_file))[0]
    model_name_2 = path.splitext(path.basename(src_prm_file))[0]
    assert model_name == model_name_2, "not compatible, " + \
        "src_sym_file: {}, src_prm_file: {}".format(
            src_sym_file, src_prm_file)

    # create backup
    src_sym_file_tmp = "{0}.tmp".format(src_sym_file)
    src_prm_file_tmp = "{0}.tmp".format(src_prm_file)
    copyfile(src_sym_file, src_sym_file_tmp)
    copyfile(src_prm_file, src_prm_file_tmp)

    if host_addr is None:
        dst_sym_file = path.join(dst_model_dir, model_name+".json")
        dst_prm_file = path.join(dst_model_dir, model_name+".params")
        copyfile(src_sym_file_tmp, dst_sym_file)
        copyfile(src_prm_file_tmp, dst_prm_file)
        yield "src files copied"
    else:
        def iterator_func(src_file, file_name):
            yield pb2.MRTClientReqStream(chunck=bytes(dst_model_dir, 'utf-8'))
            yield pb2.MRTClientReqStream(chunck=bytes(file_name, 'utf-8'))
            yield pb2.MRTClientReqStream(
                chunck=bytes(str(path.getsize(src_file)), 'utf-8'))
            with open(src_file, 'rb') as f:
                while True:
                    piece = f.read(chunk_size);
                    if len(piece) == 0:
                        return
                    yield pb2.MRTClientReqStream(chunck=piece)
        conn = grpc.insecure_channel(host_addr)
        client = pb2_grpc.MRTRpcSrvStub(channel=conn)
        response = client.submit(
            iterator_func(src_sym_file_tmp, model_name+".json"))
        next(response)
        for message in response:
            yield message.logging_str
        response = client.submit(
            iterator_func(src_prm_file_tmp, model_name+".params"))
        for message in response:
            yield message.logging_str

    # remove backup
    os.remove(src_sym_file_tmp)
    os.remove(src_prm_file_tmp)

def mrt_execute(yaml_file_str, host_addr=None):
    if host_addr is None:
        my_streamer = get_streamer(yaml_file_str)
        for logging_str in my_streamer.start():
            yield logging_str
    else:
        conn = grpc.insecure_channel(host_addr)
        client = pb2_grpc.MRTRpcSrvStub(channel=conn)
        response = client.execute(
            pb2.MRTClientReq(content=yaml_file_str))
        for message in response:
            yield message.logging_str
