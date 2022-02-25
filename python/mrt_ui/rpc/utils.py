import sys
import io
import os
from os import path

from yacs.config import CfgNode as CN

from mrt.V3.execute import run
from mrt.V3.utils import get_cfg_defaults
from mrt_ui.rpc import streamer
from mrt_ui.rpc.log import get_logger

def get_streamer(yaml_file_str):
    yaml_dir = path.expanduser("~/mrt_yaml_root")
    os.makedirs(yaml_dir, exist_ok=True)
    yaml_file_tmp = path.join(yaml_dir, "tmp.yaml")
    with open(yaml_file_tmp, "w") as f:
        f.write(yaml_file_str)

    cfg = get_cfg_defaults()
    cfg.merge_from_file(yaml_file_tmp)
    cfg.freeze()

    os.remove(yaml_file_tmp)

    logger = get_logger(cfg.COMMON.VERBOSITY, streamer.printer)
    my_streamer = streamer.Streamer(run, (cfg, logger))
    return my_streamer

def stringify_cfg(cfg):
    # TODO(ryt): replace by appropriately 
    # configured yacs interface cfg.dump(**kwargs)
    old_stdout = sys.stdout
    sys.stdout = new_stdout = io.StringIO()
    print(cfg)
    yaml_file_str = new_stdout.getvalue()
    sys.stdout = old_stdout
    return yaml_file_str
