from os import path
import argparse

from mrt.V3.utils import get_cfg_defaults
from mrt_ui.rpc.service import local_addr, local_port
from mrt_ui.rpc.client import mrt_execute

parser = argparse.ArgumentParser()
parser.add_argument("--host-addr", type=str, default=local_addr)
parser.add_argument("--host-port", type=int, default=local_port)
parser.add_argument(
    "--yaml-dir", type=str, default=path.expanduser("~/mrt_yaml_root"))
parser.add_argument("--model-name", type=str, default="alexnet")

def test_execute(yaml_dir, model_name, address):
    yaml_file = path.join(yaml_dir, model_name+".yaml")
    with open(yaml_file, "r") as f:
        lines = f.readlines()
    yaml_file_str = "".join(lines)
    for message in mrt_execute(yaml_file_str, host_addr=address):
        print(message)

if __name__ == "__main__":
    args = parser.parse_args()
    address = "{0}:{1}".format(args.host_addr, args.host_port)
    test_execute(args.yaml_dir, args.model_name, address)
