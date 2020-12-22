''' HZK格式的点阵字体制作，GB2312编码的字体
'''
#ensure import path
import sys, os
_this_script_folder = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(_this_script_folder, "..", "lib"))
import env
env.ensure_import_path()

# import
import coding, pbm, math

def init_gb2312_src(size=8):
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
            with open(posi_file, "wb") as f:
                pbm.make_image(f, size, size, pbm_empty_data, "P1", "gb2312 {} {} {}".format(area, posi, char_str))
    # finished

def build_gb2312_hzk(size=8):
    pass

if __name__ == "__main__":
    # init_gb2312_src(8)
    pass
