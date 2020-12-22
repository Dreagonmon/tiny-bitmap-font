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
try:
    from PIL import Image
    _support_pil = True
except ImportError:
    _support_pil = False

def interrupt(msg=None):
    if msg:
        print(msg)
    sys.exit(1)

def source_from_hzk(size=8):
    gb2312_folder = os.path.join(env.ROOT_FOLDER, "src", str(size), "gb2312")
    hzk_font_file_path = os.path.join(env.ROOT_FOLDER, "build", "SourceHanSerif8x8.fnt")
    hzk_font_file = open(hzk_font_file_path, "rb")
    data_size = math.ceil(size/8) * size
    for area, posi in coding.GB2312.all_available_pos():
        area_folder = os.path.join(gb2312_folder, "{:02d}".format(area))
        if not os.path.exists(area_folder):
            os.makedirs(area_folder)
        posi_file = os.path.join(area_folder, "{:02d}.pbm".format(posi))
        data_offset = coding.GB2312.to_dict_index((area, posi)) * data_size
        hzk_font_file.seek(data_offset, os.SEEK_SET)
        font_data = hzk_font_file.read(data_size)
        char_str = coding.GB2312.to_bytes((area, posi)).decode("gb2312")
        with open(posi_file, "wb") as f:
            pbm.make_image(f, size, size, font_data, "P1", "gb2312 {} {} {}".format(area, posi, char_str))

def build_gb2312_hzk(size=8):
    gb2312_folder = os.path.join(env.ROOT_FOLDER, "src", str(size), "gb2312")
    data_size = math.ceil(size/8) * size
    area_range = 87
    font_file_data = bytearray(data_size * area_range * 94)
    if _support_pil:
        preview = Image.new("1", (size*10, size*10*area_range), color=255)
    else:
        preview = None
    for area, posi in coding.GB2312.all_available_pos():
        area_folder = os.path.join(gb2312_folder, "{:02d}".format(area))
        posi_file = os.path.join(area_folder, "{:02d}.pbm".format(posi))
        if not os.path.exists(posi_file):
            continue
        try:
            with open(posi_file, "rb") as in_stream:
                w, h, format, pbm_data, _ = pbm.read_image(in_stream)
            assert w == size and h == size
            assert format == b"P1" or format == b"P4"
            assert len(pbm_data) == data_size
            data_offset = coding.GB2312.to_dict_index((area, posi)) * data_size
            font_file_data[data_offset: data_offset+data_size] = pbm_data
            if _support_pil:
                #draw preview
                for i in range(data_size):
                    pbm_data[i] = (~pbm_data[i]) & 0xFF
                fnt_img = Image.frombuffer("1", (w, h), bytes(pbm_data))
                preview_pos = (((posi-1) % 10) * w, ((area-1) * 10 * h) + ((posi-1) // 10) * h)
                preview.paste(fnt_img, preview_pos)
        except:
            import traceback
            traceback.print_exc()
            interrupt("Not a .pbm file: {}".format(posi_file))
        char_str = coding.GB2312.to_bytes((area, posi)).decode("gb2312")
        print("Processing: a:{} p:{} c:{}".format(area, posi, char_str), end="\r")
    # optput
    out_folder = os.path.join(env.ROOT_FOLDER, "build", "gb2312")
    out_path = os.path.join(out_folder, "TinyBitmap-{}x{}.fnt".format(size, size))
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    with open(out_path, "wb") as f:
        f.write(font_file_data)
    print("Font file located at: {}".format(out_path))
    if _support_pil:
        prev_path = os.path.join(out_folder, "TinyBitmap-{}x{}.bmp".format(size, size))
        preview.save(prev_path)
        print("Preview image located at: {}".format(prev_path))

if __name__ == "__main__":
    # source_from_hzk(8)
    build_gb2312_hzk(8)
    pass
