from os import path
import argparse

from mrt_ui.rpc.service import local_addr, local_port
from mrt_ui.rpc.client import mrt_submit, default_dir

parser = argparse.ArgumentParser()
parser.add_argument("--host-addr", type=str, default=local_addr)
parser.add_argument("--host-port", type=int, default=local_port)
parser.add_argument(
    "--src-dir", type=str, default=path.expanduser("~/mrt_model"))
parser.add_argument("--model-name", type=str, default="alexnet")
parser.add_argument("--dst-dir", type=str, default=default_dir)

def test_submit(src_dir, model_name, address, dst_dir):
    src_sym_file = path.join(src_dir, model_name+".json")
    src_prm_file = path.join(src_dir, model_name+".params")
    for message in mrt_submit(
        src_sym_file, src_prm_file, dst_model_dir=dst_dir,
        host_addr=address):
        print(message)

if __name__ == "__main__":
    args = parser.parse_args()
    address = "{0}:{1}".format(args.host_addr, args.host_port)
    test_submit(args.src_dir, args.model_name, address, args.dst_dir)
