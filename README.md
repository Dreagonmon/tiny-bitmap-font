# Tiny Bitmap Font
开源像素点阵字体，显示汉字等格文字。
目标是制作8x8大小的字体，用于小型点阵屏幕的显示。

# 字体构建
src/make_gb2312_font.py脚本将会把源码目录中的gb2312字体构建为.fnt格式的文件。该文件的格式和HZK16之类的字体保持一致，所有gb2312文字按照区域顺序排布。某简体中文字对应的offset如下:

```c
unsigned char char_data_size = 8; // 8x8大小的字体
// 字体数据大小是char_data_size，从offset向后读取对应数量的字节就是字体数据
char char_seq[] = "字";
unsigned char area = char_seq[0] - 0xA0;
unsigned char posi = char_seq[1] - 0xA0;
unsigned long long offset = 94*(area-1) + (posi-1) * char_data_size;
```

# 字体图像编码方式
字体数据是横向大端在前编码的，即MONO_HMSB格式。(micropython中是framebuf.MONO_HLSB，我也很懵逼)

```
以9x9的字体数据来说明格式：
                  | ignore ---> 
● ● ● ● ● ● ● ●  ●|○ ○ ○ ○ ○ ○ ○ 0b11111111 0b11111111, 即0xFF
○ ○ ○ ○ ○ ○ ○ ○  ○|○ ○ ○ ○ ○ ○ ○ 0x00 0x00
● ○ ○ ○ ○ ○ ○ ○  ○|○ ○ ○ ○ ○ ○ ○ 0x80 0x00
○ ● ○ ○ ○ ○ ○ ○  ○|○ ○ ○ ○ ○ ○ ○ 0x40 0x00
○ ○ ● ○ ○ ○ ○ ○  ○|○ ○ ○ ○ ○ ○ ○ 0x20 0x00
○ ○ ○ ● ○ ○ ○ ○  ○|○ ○ ○ ○ ○ ○ ○ 0x10 0x00
○ ○ ○ ○ ● ○ ○ ○  ○|○ ○ ○ ○ ○ ○ ○ 0x08 0x00
○ ○ ○ ○ ○ ● ○ ○  ●|○ ○ ○ ○ ○ ○ ○ 0x04 0x80
○ ○ ○ ○ ○ ○ ○ ○  ●|○ ○ ○ ○ ○ ○ ○ 0x00 0x80
字体数据大小为 2*9=18 bytes
```

```
这个字的实际图像为：
● ● ● ● ● ● ● ● ●
○ ○ ○ ○ ○ ○ ○ ○ ○
● ○ ○ ○ ○ ○ ○ ○ ○
○ ● ○ ○ ○ ○ ○ ○ ○
○ ○ ● ○ ○ ○ ○ ○ ○
○ ○ ○ ● ○ ○ ○ ○ ○
○ ○ ○ ○ ● ○ ○ ○ ○
○ ○ ○ ○ ○ ● ○ ○ ●
○ ○ ○ ○ ○ ○ ○ ○ ●
```

# 目录约定
src目录下存放字体源码，子文件夹遵循以下规范：

```src/字体大小/字体编码/实际编码id...```

比如8px的gb2312编码的字体"、"，其在gb2312编码中，是01区的第02号字，故它的源码位于:

```src/8/gb2312/01/02.pbm```

其他目录的约定：
- lib 字体构建脚本依赖的部分函数库
- build 字体构建输出目录
- git-hook git钩子函数，确保提交的字体源码都是文本格式的pbm文件
- src 构建脚本以及字体源码

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

# 设计规范
字形实际可用像素为 字体大小-1，比如8px的字体，实际上字的大小是7x7。

这样可以保证字和字之间有间隔，不会连在一起。

由于字体较小，为了提高可读性，宁可缺少笔画，也要减少"黑块"的数量。

# Additional License
Using [Source Han Serif](https://github.com/adobe-fonts/source-han-serif/) font as base image, it using SIL Open Font License 1.1.
使用[思源字体](https://github.com/adobe-fonts/source-han-serif/)初始化了字体源码，本项目是在此基础上修改的，故生成的字体本身遵循SIL Open Font协议。
