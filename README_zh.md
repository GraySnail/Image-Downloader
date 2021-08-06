# Image Downloader

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## 1. 简介

- 从图片搜索引擎，爬取关键字搜索的原图 URL 并下载
- 开发语言 python，采用 Requests、Selenium、Phantomjs 等库进行开发

## 2. 功能

- 支持的搜索引擎: Google, 必应, 百度
- 提供 GUI 及 CMD 版本
- GUI 版本支持关键词键入，以及通过关键词列表文件（行分隔,**使用 UTF-8 编码**）输入进行批处理爬图下载
- 可配置线程数进行并发下载，提高下载速度
- 支持搜索引擎的条件查询（如 :site）
- 支持 Google 的安全模式开启和关闭
- 支持 socks5 和 http 代理的配置，方便科学上网用户
- **提供预编译的 windows 单文件可执行 exe 下载, 推荐非开发者用户使用。[点此下载](https://github.com/sczhengyabin/Google-Image-Downloader/releases)**
- 命令行添加“百度识图”图片下载

## 3. 解决依赖

### 3.1 Windows 环境

#### 3.1.1 下载并安装 python3.5

- [下载地址](https://www.python.org/ftp/python/3.5.3/python-3.5.3.exe)
- 安装时请注意勾选"add to PATH"

#### 3.1.2 下载并安装 PyQt5

- [下载地址](https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.6/PyQt5-5.6-gpl-Py3.5-Qt5.6.0-x32-2.exe/download)

#### 3.1.3 下载 phantomjs 并配置

- [下载地址](https://bitbucket.org/ariya/phantomjs/downloads)
- 选择最新的 windows 版本下载即可
- 下载完成后将 phantomjs.exe 拷贝到 "本项目文件夹/bin/"

#### 3.1.4 安装相关 python 库

```
pip3.exe install -r requirements.txt
```

#### 3.1.5 [可选] 打包成单个可执行文件

确保 3.1.3 步骤完成后，CMD 进到项目文件夹，执行如下命令：

```
pip3.exe install pyinstaller
pyinstaller image_downloader_gui.spec
```

命令完成后，exe 文件在 ./dist 文件夹中

### 3.2 Linux 环境（debian 系列）

#### 3.2.1 安装依赖库

```
apt-get install python3-pip python3-pyqt5 pyqt5-dev-tools
```

#### 3.2.2 下载 Phantomjs 并配置

- [x86 PC 用户下载地址](https://bitbucket.org/ariya/phantomjs/downloads) （官方）
- [树莓派用户下载地址](https://github.com/fg2it/phantomjs-on-raspberry/releases)（无官方版本，第三方通过源码编译）

**[警告]: 通过 apt-get 安装的 phantomjs 为非完整版，无法在本项目中使用.**

下载完成后，将 phantomjs 文件路径添加至 PATH 环境变量，或者将其拷贝到/usr/local/bin 文件夹。

## 4. 如何使用

### 4.1 图形界面

```
image_downloader_gui.py
```

![](/GUI.png)

### 4.2 命令行

```
usage: image_downloader.py [-h] [--engine {Google,Bing,Baidu}]
                           [--max-number MAX_NUMBER]
                           [--num-threads NUM_THREADS] [--timeout TIMEOUT]
                           [--output OUTPUT] [--safe-mode] [--face-only]
                           [--proxy_http PROXY_HTTP]
                           [--proxy_socks5 PROXY_SOCKS5]
                           keywords
```

#### 4.2.1 百度识图

在浏览器打开 [百度识图](https://graph.baidu.com/pcpage/index?tpl_from=pc),上传本地或使用网络图片，在列表页中，`F12`开发根据查看 `https://graph.baidu.com/ajax/pcsimi`请求，获取其中的 `sign` 参数值，作为关键字使用。例如：

```bash
python image_downloader.py --engine=BaiduShitu --max-number=10 --num-threads=50 --output=./images/test2 --safe-mode 122edc2c6ef4a7048501101628227246
```

## 许可

- MIT License
- 996ICU License
