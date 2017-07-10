import requests
from lxml import html
import time, random, json

__author__ = 'jesee'


class Model(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        return '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))


class Mogu(Model):
    def __init__(self):
        self.href = ''


def rewrite(ip):
    return {'http': 'http://' + ip}


def choice_ip():
    with open("ips.txt", "r", encoding='utf-8') as f:
        ips = f.read().strip('\n')
    l = [ip.strip() for ip in ips]
    ips = list(map(rewrite, l))
    proxy = random.choice(ips)
    return proxy


def write_message(mogus, path, method):
    d = dict(
        default=lambda o: o.__dict__,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
    )
    json_m = json.dumps(mogus, **d)
    with open(path, method, encoding='utf-8') as f:
        f.write(json_m)


def url_from_div(div):
    m = Mogu()
    mogu_url = 'http://www.mgzf.com'
    m.href = mogu_url + div.xpath('.//a/@href')[0]
    return m


def cached_url(url):
    import os
    filename = url.split('=')[-1] + '.html'
    path = os.path.join('mogu_page', filename)
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
        s.proxies = choice_ip()
        r = s.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(r.content)
    return r.content


def mogu_from_url(url):
    page = cached_url(url)
    root = html.fromstring(page)
    # // 从根开始找
    mogu_divs = root.xpath('//div[@class="inner"]')
    mogus = [url_from_div(div) for div in mogu_divs]
    return mogus


def main():
    m = []
    method = 'a'
    path = 'txt/mogu_href.txt'
    for i in range(51):
        time.sleep(random.randint(5, 8))
        url = 'http://www.mgzf.com/list?order=8&mogu_info_page={}'.format(i)
        mogus = mogu_from_url(url)
        m.extend(mogus)
    write_message(m, path, method)


if __name__ == '__main__':
    main()
