import requests
from lxml import html
from mogu_href import Model, write_message, choice_ip
import random, json, time

__author__ = 'jesee'


class HouseInfo(Model):
    def __init__(self):
        self.name = ''
        self.phone = ''
        self.address = ''
        self.status = ''


def load_message(path):
    l = list()
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        r = json.loads(s)
    for i in r:
        if i not in l:
            l.append(i)
    return l


def house_from_div(div):
    h = HouseInfo()
    h.phone = div.xpath('.//span[@class="tel_phone"]/p/text()')[0]
    h.name = div.xpath('.//div[@class="person-wrap"]/div/span/text()')[0]
    h.address = div.xpath('.//li[@class="move-title"]/h1/span/text()')[0].strip()
    return h


def cached_url(url):
    import os
    filename = url.split('/')[-1].split('.')[0] + '.html'
    path = os.path.join('mogu_info_page', filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    else:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, compress',
            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
        }
        s = requests.session()
        proxies = choice_ip()
        print(proxies)
        r = s.get(url, headers=headers, proxies=proxies)
        with open(path, 'wb') as f:
            f.write(r.content)
    return r.content


def house_from_url(url):
    page = cached_url(url)
    root = html.fromstring(page)
    house_divs = root.xpath('//ul[@class="room-info-wrap"]')
    if house_divs:
        houses = [house_from_div(div) for div in house_divs]
    else:
        house_divs = root.xpath('//div[@class="my-container nopadding"]')
        houses = []
        for div in house_divs:
            h = HouseInfo()
            h.status = div.xpath('.//div[@class="f18 white"]/text()')[0]
            houses.append(h)
    return houses


def main():
    path_href = 'txt/mogu_href.txt'
    path_info = 'txt/mogu_info.txt'
    method = 'a'
    m = []
    l = load_message(path_href)
    for i, e in enumerate(l):
        time.sleep(random.randint(5, 8))
        url = e.get('href')
        house = house_from_url(url)
        m.extend(house)
    write_message(m, path_info, method)


if __name__ == '__main__':
    main()
