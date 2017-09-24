# Terminal Printer

输出字符图片到终端

### 安装

```bash
$ pip install terminalprinter --upgrade
# or
$ sudo install terminalprinter --upgrade
# if permission issue happened on mac os
$ pip install terminalprinter --user --upgrade
```

### 使用

```bash
$ terminalprint
```

以上命令，将输出默认的字符图到终端(命令太长？为什么不用<tab>)

![](https://static.hellflame.net/resource/de5ca9cf5320673dc43b526e3d737f05)

#### i. 帮助信息

```bash
$ terminalprint -h
```

得到类似输出:

```bash
usage: run.py [-h] [-i] [-t TEXT] [-l l] [-g] [-kr] [-c i] [-f i]
              [--width WIDTH] [--height HEIGHT] [-F path] [-r] [-v]
              [picture]

Terminal Printer

positional arguments:
  picture               可选的图片

optional arguments:
  -h, --help            show this help message and exit
  -i, --init            初始化程序，下载字体
  -t TEXT, --text TEXT  设置将要处理的文本内容，默认为 HellFlame
  -g, --gray            图像转换为灰度图(若指定图)
  -kr, --keep-ratio     保持图片比例
  -c i, --color i       设置颜色
  -f i, --filter i      设置打印填充方式
  --width WIDTH         设置输出宽度，需要与高度一起设置
  --height HEIGHT       设置输出高度，需要与宽度一起设置
  -F path, --font path  设置书写字体
  -r, --reverse         反色(对彩色输出无效)
  -v, --version         输出版本信息

初次使用，需要初始化字体下载
执行 terminalprint -i 初始化
更多帮助信息请访问: https://github.com/hellflame/terminal_printer
```

#### ii. 版本信息

```bash
$ terminalprint -v # terminalprint --version
```

#### iii. 初始化字体库

> 由于程序用到了5个大多数系统没有的三方字体，所以把这5个字体放在了用户目录下的一个隐藏文件目录，`~/.terminal_fonts/` ，3个字体的下载路径分别为：(可以手动下载保存在指定路径)

```
http://7xqh1q.dl1.z0.glb.clouddn.com/Haibaoyuanyuan.ttf
http://7xqh1q.dl1.z0.glb.clouddn.com/fengyun.ttf
http://7xqh1q.dl1.z0.glb.clouddn.com/huakangbold.otf
http://7xqh1q.dl1.z0.glb.clouddn.com/letter.ttf
http://7xqh1q.dl1.z0.glb.clouddn.com/shuyan.ttf
```

当然，可以直接通过以下命令初始化字体库:

```bash
$ terminalprint -i # terminalprint --init
```

#### iv. 设置文本内容

```bash
$ terminalprint -t '文字'
```

默认情况下应该得到用默认字体写的用`i`填充的`文字`两个字:

![](https://static.hellflame.net/resource/7776e7aa8f58a83b8ec19457fb22bdd2)

#### v. 设置输出文字的格式

(1) 填充字符

```bash
$ terminalprint -f [filt char]
```

可以设置的值范围1～223，覆盖ANSI可打印字符

(2) 渲染颜色

> 这需要彩色终端支持

```bash
$ terminalprint -c [color]
```

color值范围30～50，覆盖终端基本的16色

也可以使用随机颜色，只要颜色值是一个非数字字符串即可

```bash
$ terminalprint -c auto
```


(3) 输出宽度与高度

> 高度与宽度需要同时指定，否则尝试使用终端显示区域大小，若获取失败，则使用默认值

```bash
$ terminalprint --width 100 --height 20
```

当然，高宽过小，会导致输出的内容难以辨识出原来的样子，高宽过大，会导致终端中的换行出现，更难辨认

(4) 字体选择

> 部分Linux操作系统可能会因为选择truetype字体lib问题出错，需要自己手动处理。之所以使用下载字体的方式来渲染文字，是因为PIL默认使用的字体基本上只支持ANSI字符，中文字符什么的就变成了小框框=。=，可以自己设置一个不支持中文的字体，然后设置字体中用中文，就可以看到了。

输入数字，选择初始化时的字体，也可以输入字体路径，使用外部字体

```bash
$ terminalprint -F [index|font]
```

内部字体通过一个大于等于0的数字索引

外部字体通过给本地路径来获取

__对了，只绘制图片的话，并不需要字体支持__

(5) 反色

背景与文字填充字符互换

```bash
$ terminalprint -r
```

*最后，可以把以上这些命令交叉使用，获得混合效果，至于可读性，就不好说了*

#### vi. 渲染图片

> 这里需要256色终端支持！以下测试终端为 iterm

可以通过给定有效图片位置来将图片渲染到终端中

```bash
$ terminalprint [pic path]
```

理想的话，可能得到类似下面的输出:

![](https://static.hellflame.net/resource/691d8fddc0dbd019da384b5a2d65bfa2)

但是，实际情况很可能是这样:

![](https://static.hellflame.net/resource/8d2f71ec32ad99cdbeb12471e00d8ae6)

只有把终端字体设置的很小，才有可能看到很多细节，但是此时终端的背景色(黑色)也会更加影响视觉效果，在这里显得更暗了。

设置文字格式中的大部分命令可用，比如强制图片使用灰度图，并且控制填充字符索引不要太高，可能得到以下结果

```bash
# terminalprint [pic] -g -c 34 -f 4
```

![](https://static.hellflame.net/resource/999e9694b20653135555a14a2a1b69ec)

这里的填充字符索引会多义为使用不超过ANSI中可打印字符码值不超过4的字符来表示不同的灰度级别，索引值越大，灰度的符号越多，看上去也会更杂乱。实际上，如果将索引调到最大的话，还是依稀可以看到原图的影子的，不过实际效果嘛，，，灰阶较少的图片也没有问题。

嗯，以上，Just For Fun!

