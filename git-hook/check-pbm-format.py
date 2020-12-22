#ensure import path
import sys, os
_this_script_folder = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(_this_script_folder, "..", "lib"))
import env
env.ensure_import_path()

import math
import pbm, coding
from git import Repo
repo = Repo(env.ROOT_FOLDER)

def ensure_pbm_format(size=8):
    # check pbm file
    unclear_pbm = []
    checked_pbm = []
    for f in repo.untracked_files:
        if f.endswith(".pbm") or f.endswith(".pbm"):
            unclear_pbm.append(os.path.abspath(f))
    for item in repo.index.diff(None):
        f = item.a_path
        if f.endswith(".pbm") or f.endswith(".pbm"):
            unclear_pbm.append(os.path.abspath(f))
    # gb2312
    gb2312_folder = os.path.join(env.ROOT_FOLDER, "src", str(size), "gb2312")
    data_size = math.ceil(size/8) * size
    pbm_empty_data = bytearray(data_size)
    for area, posi in coding.GB2312.all_available_pos():
        area_folder = os.path.join(gb2312_folder, "{:02d}".format(area))
        if not os.path.exists(area_folder):
            os.makedirs(area_folder)
        posi_file = os.path.join(area_folder, "{:02d}.pbm".format(posi))
        char_str = coding.GB2312.to_bytes((area, posi)).decode("gb2312")
        if not os.path.exists(posi_file):
            # create missing pbm
            with open(posi_file, "wb") as f:
                pbm.make_image(f, size, size, pbm_empty_data, "P1", "gb2312 {} {} {}".format(area, posi, char_str))
            checked_pbm.append(posi_file)
        else:
            # check exist pbm
            if not posi_file in unclear_pbm:
                # ignore untouched
                continue
            try:
                with open(posi_file, "rb") as in_stream:
                    w, h, format, data, _ = pbm.read_image(in_stream)
                assert w == size and h == size
                assert format == b"P1" or format == b"P4"
                with open(posi_file, "wb") as f:
                    pbm.make_image(f, size, size, data, "P1", "gb2312 {} {} {}".format(area, posi, char_str))
            except:
                interrupt("Not a .pbm file: {}".format(posi_file))
            checked_pbm.append(posi_file)
    # add changes
    repo.index.add(items=checked_pbm)
    pass

def interrupt(msg=None):
    if msg:
        print(msg)
    print("Stop Commit!")
    sys.exit(1)

if __name__ == "__main__":
    print("checking .pbm files` format...")
    ensure_pbm_format(8)
    # interrupt()
    print(".pbm format checked.")
    pass