''' HZK格式的点阵字体制作，GB2312编码的字体
'''
#ensure import path
import sys, os
_this_script_folder = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(_this_script_folder, "..", "lib"))
import env
env.ensure_import_path()

# import
import coding, pbm

def init_src():
    pass

