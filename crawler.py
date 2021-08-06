""" Crawl image urls from image search engine. """
# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from __future__ import print_function

import re
import time
import sys
import os
import json
import codecs

from urllib import parse
from urllib.parse import unquote, quote
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import requests
from concurrent import futures

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

if sys.platform.startswith("win"):
    phantomjs_path = os.path.join(bundle_dir + "/bin/phantomjs.exe")
else:
    phantomjs_path = "phantomjs"

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap[
    "phantomjs.page.settings.userAgent"
] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100"


headers = {
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept - Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
    'Cookie': 'BDqhfp=%E6%B2%99%E6%BC%A0%E6%9D%A8%E6%A0%91%26%26NaN%26%260%26%261; BAIDUID=3C6861D723C65E43343BA6C92F5E7C3C:FG=1; BIDUPSID=3C6861D723C65E43343BA6C92F5E7C3C; PSTM=1562135321; BDUSS=GtMLVdpSTUxQzdGbFVMWnR1MGJLaHloZUJrRVhteE5jbHV-b1QwcEdIdXlWWVpmSVFBQUFBJCQAAAAAAAAAAAEAAAC6gvQcc2h0YW8yMDExAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALLIXl-yyF5fU; BDUSS_BFESS=GtMLVdpSTUxQzdGbFVMWnR1MGJLaHloZUJrRVhteE5jbHV-b1QwcEdIdXlWWVpmSVFBQUFBJCQAAAAAAAAAAAEAAAC6gvQcc2h0YW8yMDExAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALLIXl-yyF5fU; MCITY=-224%3A; BAIDUID_BFESS=273B8D42F9E24E2F7F7FB461492EE7DF:FG=1; ZD_ENTRY=bing; BDRCVFR[S_ukKV6dOkf]=rmMloD7ZnT3Xh9GpZR8mvqV; delPer=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; __yjs_duid=1_7fd4b381a6550d8579ba6fcbdc4bf6151618466051897; H_PS_PSSID=31660_33848_33772_33855_33607_26350; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; cleanHistoryStatus=0; indexPageSugList=%5B%22%E6%B2%99%E6%BC%A0%E6%9D%A8%E6%A0%91%22%2C%22%E6%B2%99%E6%BC%A0%E5%B0%8F%E6%A0%91%22%2C%22%E6%88%88%E5%A3%81%E5%B0%8F%E6%A0%91%22%2C%22%E8%8D%92%E6%BC%A0%20%E6%A0%91%22%2C%22%E6%88%88%E5%A3%81%20%E6%A0%91%22%2C%22%E7%BB%BF%E6%B4%B2%20%E6%A0%91%22%2C%22%E6%B2%99%E6%BC%A0%20%E6%A0%91%22%2C%22%E6%88%88%E5%A3%81%E6%A0%91%E6%9C%A8%22%2C%22%E6%88%88%E5%A3%81%E6%A0%91%22%5D; ab_sr=1.0.1_N2IzMmNkNzE2ZmZhZmJkY2YwZGUwMzU3ZTgyMDFmZjlhMTg1NDc4MmE1YjljNDA0YjA1OTc5NjdiZmZhNDNjNDhmZTBmZjBlMDQ1NzFlOWQ4ZDQzYmZhNGNlYTEwN2UwZWZlYTAwYzBjNDBmMDgyYjgzYmYxYzFjZDc5MzkyMTRlOTc0YWM3ZjRiN2I5MzU5Y2QyZjM4YmVjNWU0YWY3OTBjMWQ5NTQ2YzhkN2QwMmEyODFkNjJhOWI4MGJhZmFh',
}


def my_print(msg, quiet=False):
    if not quiet:
        print(msg)


def google_gen_query_url(keywords, face_only=False, safe_mode=False):
    base_url = "https://www.google.com/search?tbm=isch&hl=en"
    keywords_str = "&q=" + quote(keywords)
    query_url = base_url + keywords_str
    if face_only is True:
        query_url += "&tbs=itp:face"
    if safe_mode is True:
        query_url += "&safe=on"
    else:
        query_url += "&safe=off"
    return query_url


def google_image_url_from_webpage(driver):
    # time.sleep(10)
    try:
        show_more = driver.find_element_by_id("smb")
        show_more.click()
        time.sleep(5)
    except Exception as e:
        pass
    image_elements = driver.find_elements_by_class_name("rg_l")
    image_urls = list()
    url_pattern = "imgurl=\S*&amp;imgrefurl"

    for image_element in image_elements:
        outer_html = image_element.get_attribute("outerHTML")
        re_group = re.search(url_pattern, outer_html)
        if re_group is not None:
            image_url = unquote(re_group.group()[7:-14])
            image_urls.append(image_url)
    return image_urls


def bing_gen_query_url(keywords, face_only=False, safe_mode=False):
    base_url = "https://www.bing.com/images/search?"
    keywords_str = "&q=" + quote(keywords)
    query_url = base_url + keywords_str
    if face_only is True:
        query_url += "&qft=+filterui:face-face"

    return query_url


def bing_image_url_from_webpage(driver):
    image_urls = list()

    time.sleep(10)
    img_count = 0

    while True:
        image_elements = driver.find_elements_by_class_name("iusc")
        if len(image_elements) > img_count:
            img_count = len(image_elements)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            smb = driver.find_elements_by_class_name("btn_seemore")
            if len(smb) > 0 and smb[0].is_displayed():
                smb[0].click()
            else:
                break
        time.sleep(3)
    for image_element in image_elements:
        m_json_str = image_element.get_attribute("m")
        m_json = json.loads(m_json_str)
        image_urls.append(m_json["murl"])
    return image_urls


def baidu_gen_query_url(keywords, face_only=False, safe_mode=False):
    base_url = "https://image.baidu.com/search/index?tn=baiduimage"
    keywords_str = "&word=" + quote(keywords)
    query_url = base_url + keywords_str
    if face_only is True:
        query_url += "&face=1"
    return query_url


def baidu_image_url_from_webpage(driver):
    time.sleep(10)
    image_elements = driver.find_elements_by_class_name("imgitem")
    image_urls = list()

    for image_element in image_elements:
        image_url = image_element.get_attribute("data-objurl")
        image_urls.append(image_url)
    return image_urls


def baidu_get_image_url_using_api(
    keywords, max_number=10000, face_only=False, proxy=None, proxy_type=None
):
    def decode_url(url):
        in_table = '0123456789abcdefghijklmnopqrstuvw'
        out_table = '7dgjmoru140852vsnkheb963wtqplifca'
        translate_table = str.maketrans(in_table, out_table)
        mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
        for k, v in mapping.items():
            url = url.replace(k, v)
        return url.translate(translate_table)

    base_url = (
        "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592"
        "&lm=7&fp=result&ie=utf-8&oe=utf-8&st=-1"
    )
    keywords_str = "&word={}&queryWord={}".format(quote(keywords), quote(keywords))
    query_url = base_url + keywords_str
    query_url += "&face={}".format(1 if face_only else 0)

    init_url = query_url + "&pn=0&rn=30"

    proxies = None
    if proxy and proxy_type:
        proxies = {
            "http": "{}://{}".format(proxy_type, proxy),
            "https": "{}://{}".format(proxy_type, proxy),
        }

    res = requests.get(init_url, proxies=proxies, headers=headers)
    init_json = json.loads(res.text.replace(r"\'", ""), encoding='utf-8', strict=False)
    total_num = init_json['listNum']

    target_num = min(max_number, total_num)
    crawl_num = min(target_num * 2, total_num)

    crawled_urls = list()
    batch_size = 30

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list = list()

        def process_batch(batch_no, batch_size):
            image_urls = list()
            url = query_url + "&pn={}&rn={}".format(batch_no * batch_size, batch_size)
            try_time = 0
            while True:
                try:
                    response = requests.get(url, proxies=proxies, headers=headers)
                    break
                except Exception as e:
                    try_time += 1
                    if try_time > 3:
                        print(e)
                        return image_urls
            response.encoding = 'utf-8'
            res_json = json.loads(response.text.replace(r"\'", ""), encoding='utf-8', strict=False)
            for data in res_json['data']:
                if 'objURL' in data.keys():
                    image_urls.append(decode_url(data['objURL']))
                elif 'replaceUrl' in data.keys() and len(data['replaceUrl']) == 2:
                    image_urls.append(data['replaceUrl'][1]['ObjURL'])

            return image_urls

        for i in range(0, int((crawl_num + batch_size - 1) / batch_size)):
            future_list.append(executor.submit(process_batch, i, batch_size))
        for future in futures.as_completed(future_list):
            if future.exception() is None:
                crawled_urls += future.result()
            else:
                print(future.exception())

    return crawled_urls[: min(len(crawled_urls), target_num)]


def baidu_get_image_url_from_shitu_api(
    keywords, max_number=10000, face_only=False, proxy=None, proxy_type=None
):
    def decode_url(url):
        urldata = parse.urlparse(url)
        querys = dict(parse.parse_qsl(urldata.query))
        image = querys.get('image')
        if image:
            image = parse.unquote(image)
        return image

    base_url = (
        "https://graph.baidu.com/ajax/pcsimi?tn=pc&idctag=tc&entrance=general"
        "&sids=10004_10803_10600_10916_10912_11004_10924_10905_10018_10901_10942_10907_11012_10971_10968_10974_11032_"
        "12201_17851_17071_18001_18100_19102_17200_17202_18301_18310_18332_18412_19111_19121_19130_19300_19132_19190_"
        "19162_19171_19220_19180_19200_19210_19212_19215_19217_19219_19230_19241_19250"
        "&tpl_from=pc&pageFrom=graph_upload_pcshitu"
    )
    keywords_str = "&sign={}".format(quote(keywords))
    query_url = base_url + keywords_str

    init_url = query_url + "&page=1"

    proxies = None
    if proxy and proxy_type:
        proxies = {
            "http": "{}://{}".format(proxy_type, proxy),
            "https": "{}://{}".format(proxy_type, proxy),
        }

    crawl_num = max_number * 2

    crawled_urls = list()
    batch_size = 30

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list = list()

        def process_batch(batch_no, batch_size):
            image_urls = list()
            url = query_url + "&page={}".format(batch_no + 1)
            my_print(url)
            try_time = 0
            while True:
                try:
                    response = requests.get(url, proxies=proxies, headers=headers)
                    break
                except Exception as e:
                    try_time += 1
                    if try_time > 3:
                        print(e)
                        return image_urls
            response.encoding = 'utf-8'
            res_json = json.loads(response.text.replace(r"\'", ""), encoding='utf-8', strict=False)
            for data in res_json['data']['list']:
                if 'objUrl' in data.keys():
                    image_urls.append(decode_url(data['objUrl']))
                # elif 'replaceUrl' in data.keys() and len(data['replaceUrl']) == 2:
                #     image_urls.append(data['replaceUrl'][1]['ObjURL'])

            return image_urls

        for i in range(0, int((crawl_num + batch_size - 1) / batch_size)):
            future_list.append(executor.submit(process_batch, i, batch_size))
        for future in futures.as_completed(future_list):
            if future.exception() is None:
                crawled_urls += future.result()
            else:
                print(future.exception())

    return crawled_urls[: min(len(crawled_urls), max_number)]


def crawl_image_urls(
    keywords,
    engine="Google",
    max_number=10000,
    face_only=False,
    safe_mode=False,
    proxy=None,
    proxy_type="http",
    quiet=False,
    browser="phantomjs",
):
    """
    Scrape image urls of keywords from Google Image Search
    :param keywords: keywords you want to search
    :param engine: search engine used to search images
    :param max_number: limit the max number of image urls the function output, equal or less than 0 for unlimited
    :param face_only: image type set to face only, provided by Google
    :param safe_mode: switch for safe mode of Google Search
    :param proxy: proxy address, example: socks5 192.168.0.91:1080
    :param proxy_type: socks5, http
    :return: list of scraped image urls
    """

    my_print("\nScraping From {0} Image Search ...\n".format(engine), quiet)
    my_print("Keywords:  " + keywords, quiet)
    if max_number <= 0:
        my_print("Number:  No limit", quiet)
        max_number = 10000
    else:
        my_print("Number:  {}".format(max_number), quiet)
    my_print("Face Only:  {}".format(str(face_only)), quiet)
    my_print("Safe Mode:  {}".format(str(safe_mode)), quiet)

    if engine == "Google":
        query_url = google_gen_query_url(keywords, face_only, safe_mode)
    elif engine == "Bing":
        query_url = bing_gen_query_url(keywords, face_only, safe_mode)
    elif engine == "Baidu":
        query_url = baidu_gen_query_url(keywords, face_only, safe_mode)
    elif engine == 'BaiduShitu':
        query_url = 'https://graph.baidu.com'
    else:
        return

    my_print("Query URL:  " + query_url, quiet)

    if browser == "chrome":
        chrome_options = webdriver.ChromeOptions()
        if proxy is not None and proxy_type is not None:
            chrome_options.add_argument("--proxy-server={}://{}".format(proxy_type, proxy))
        driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
    else:
        phantomjs_args = []
        if proxy is not None and proxy_type is not None:
            phantomjs_args += [
                "--proxy=" + proxy,
                "--proxy-type=" + proxy_type,
            ]
        driver = webdriver.PhantomJS(
            executable_path=phantomjs_path, service_args=phantomjs_args, desired_capabilities=dcap
        )

    if engine == "Google":
        driver.set_window_size(10000, 7500)
        driver.get(query_url)
        image_urls = google_image_url_from_webpage(driver)
    elif engine == "Bing":
        driver.set_window_size(1920, 1080)
        driver.get(query_url)
        image_urls = bing_image_url_from_webpage(driver)

    elif engine == 'Baidu':  # Baidu
        # driver.set_window_size(10000, 7500)
        # driver.get(query_url)
        # image_urls = baidu_image_url_from_webpage(driver)
        image_urls = baidu_get_image_url_using_api(
            keywords, max_number=max_number, face_only=face_only, proxy=proxy, proxy_type=proxy_type
        )
    elif engine == 'BaiduShitu':
        # 百度识图
        image_urls = baidu_get_image_url_from_shitu_api(
            keywords, max_number=max_number, face_only=face_only, proxy=proxy, proxy_type=proxy_type
        )

    driver.close()

    if max_number > len(image_urls):
        output_num = len(image_urls)
    else:
        output_num = max_number

    my_print(
        "\n== {0} out of {1} crawled images urls will be used.\n".format(
            output_num, len(image_urls)
        ),
        quiet,
    )

    return image_urls[0:output_num]


if __name__ == '__main__':

    def decode_url(url):
        urldata = parse.urlparse(url)
        querys = dict(parse.parse_qsl(urldata.query))
        image = querys.get('image')
        if image:
            image = parse.unquote(image)
        return image

    url = "https://graph.baidu.com/pcpage/similar?originSign=121f96d06cb3885912c3401628147064&srcp=crs_pc_similar&tn=pc&idctag=tc&sids=10007_10803_10600_10914_10913_11006_10920_10905_10018_10901_10942_10907_11013_10971_10968_10974_11032_12201_17851_17071_18013_18101_19101_17200_17202_18300_18311_18332_18412_19114_19123_19131_19300_19132_19196_19162_19170_19220_19180_19200_19210_19212_19214_19217_19218_19230_19242_19250_9999&logid=3233674079&entrance=general&tpl_from=pc&pageFrom=graph_upload_pcshitu&image=https%3A%2F%2Fss2.baidu.com%2F6ON1bjeh1BF3odCf%2Fit%2Fu%3D1824286984%2C1057972425%26fm%3D27%26gp%3D0.jpg&carousel=503&index=2&page=1"

    image = decode_url(url)
    print(image)