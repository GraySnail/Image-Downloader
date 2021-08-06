# Image Downloader

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## 1. 简介

- 从图片搜索引擎，爬取关键字搜索的原图 URL 并下载
- 开发语言 python，采用 Requests、Selenium 等库进行开发

## 2. 功能

- 支持的搜索引擎: Google, 必应, 百度
- 提供 GUI 及 CMD 版本
- GUI 版本支持关键词键入，以及通过关键词列表文件（行分隔,**使用 UTF-8 编码**）输入进行批处理爬图下载
- 可配置线程数进行并发下载，提高下载速度
- 支持搜索引擎的条件查询（如 :site）
- 支持 Google 的安全模式开启和关闭
- 支持 socks5 和 http 代理的配置，方便科学上网用户

* 命令行添加“百度识图”图片下载

## 3. 安装

### 3.1 下载并安装 python3.5+

- [下载地址](https://www.python.org/downloads/)

### 3.2 下载 chromedriver 并配置[推荐]

- [下载地址](https://chromedriver.chromium.org/downloads)
- 选择对应系统、chrome 浏览器的版本
- 下载完成后将`chromedriver`拷贝到 "本项目文件夹/bin/"，或者其他文件夹后添加到 PATH 中

### 3.3 下载 phantomjs 并配置[过时]

- [下载地址](https://bitbucket.org/ariya/phantomjs/downloads)
- 选择最新的 windows 版本下载即可
- 下载完成后将 phantomjs.exe 拷贝到 "本项目文件夹/bin/"，或者其他文件夹后添加到 PATH 中

### 3.4 安装相关 python 库

```bash
pip3 install -r requirements.txt
```

## 4. 如何使用

### 4.1 图形界面

运行`image_downloader_gui.py`脚本以启动 GUI 界面

```bash
python image_downloader_gui.py
```

![GUI](/GUI.png)

### 4.2 命令行

```bash
usage: image_downloader.py [-h] [--engine {Google,Bing,Baidu}]
                           [--driver {chrome_headless,chrome,phantomjs}]
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

## 备注

由于 Google 修改了前端页面，无法直接从单个页面获取全部图片的原始链接，所以需要通过模拟人工点击操作遍历所有图片，因此使用 Google 引擎来爬取图片时间较长，如需加速可以减少单个关键字的最大图片数量。

## 许可

- MIT License
- 996ICU License
