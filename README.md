# Tiny Bitmap Font
开源像素点阵字体，显示汉字等格文字。
目标是制作8x8大小的字体，用于小型点阵屏幕的显示。

# 参与开发
获取源代码并安装开发环境：


```bash
    git clone https://github.com/Dreagonmon/tiny-bitmap-font.git
    cd tiny-bitmap-font
    python3 init.py # or python if you have only python3 install
```

找到src目录下字体对应的pbm图片文件，用支持pbm文本格式图片的编辑器打开。推荐使用GIMP (GIMP保存的时候使用"导出"，而不是"保存")，或者系统自带记事本也可以编辑。

执行脚本确保pbm格式图片都是文本格式的：

```bash
python3 git-hook/check-pbm-format.py
```

之后使用git提交更改、提交PR即可。
