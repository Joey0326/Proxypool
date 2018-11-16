import json
import re
#from .utils import get_page
from pyquery import PyQuery as pq
import time
import requests

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    # def crawl_daxiang(self):
    #     url = 'http://vtp.daxiangdaili.com/ip/?tid=559363191592228&num=50&filter=on'
    #     html = get_page(url)
    #     if html:
    #         urls = html.split('\n')
    #         for url in urls:
    #             yield url

    def crawl_kxdaili(self):
        #开心代理
        for i in range(1, 11):
            start_url = 'http://ip.kxdaili.com/ipList/{}.html#ip'.format(i)

            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Cache-Control': 'max-age=0',
                       'Connection': 'keep-alive',
                       'Cookie': 'ASPSESSIONIDSQCSDBSA=EAMODKKCIOICBJIKEEHDFICO; __51cke__=; __tins__17751595=%7B%22sid%22%3A%201541757052974%2C%20%22vd%22%3A%2011%2C%20%22expires%22%3A%201541759356875%7D; __51laig__=11',
                       'Host': 'ip.kxdaili.com',
                       'Referer': 'http://ip.kxdaili.com/ipList/.html',
                       'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.108 Safari / 537.36'
                       }

            html = requests.get(start_url,headers=headers)
            if html.status_code == 200:
                print('Crawling: ',html.url)
                ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                # \s* 匹配空格，起到换行作用
                re_ip_address = ip_address.findall(html.text)
                for address, port in re_ip_address:
                    result = address + ':' + port
                    yield result.replace(' ', '')



    def crawl_kuaidaili(self):
        #该代理控制访问速度，所以必须使用time休眠一段时间再访问
        for i in range(1, 5):
            start_url = 'http://www.kuaidaili.com/free/inha/{page}/'.format(page=i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                #'Cookie': 'channelid=0; sid=1541758831215199; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1541758836; _ga=GA1.2.1958916142.1541758836; _gid=GA1.2.1593926403.1541758836; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1541759737',
                'Host': 'www.kuaidaili.com',
                #'If-None-Match': 'W/"2968a967c8b57591fb9139a8d6cc4157"',
                #'Referer': 'https://www.kuaidaili.com/free/inha/1/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.108 Safari / 537.36'
                }
            html = requests.get(start_url,headers=headers)
            time.sleep(0.5)
            if html.status_code == 200:
                print('Crawling: ',html.url)
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html.text)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html.text)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')
            else:
                print(html.status_code,html.url)

    def crawl_xicidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.xicidaili.com/nn/{page}'.format(page=i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTgxMTk5NTRlM2QyMjI0M2I2ZTBlMzRlNGE3MzM5OTg3BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVJNb3VHNG1RN1IxN2tTUW11c1JkQmczZUhRWXBiS283MlJPL2paTkFJbEE9BjsARg%3D%3D--9626232140e86302f1491dc93a31dc66b243c741; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1541757985; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1541758224',
                'Host': 'www.xicidaili.com',
                'If-None-Match': 'W/"2968a967c8b57591fb9139a8d6cc4157"',
                'Referer': 'http://www.ip3366.net/fetch/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.108 Safari / 537.36'
                }
            html = requests.get(start_url, headers=headers)

            if html.status_code == 200:
                print('Crawling: ',html.url)
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html.text)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')


    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Cookie': 'channelid=0; sid=1541758831215199; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1541758836; _ga=GA1.2.1958916142.1541758836; _gid=GA1.2.1593926403.1541758836; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1541759737',
            'Host': 'www.iphai.com',
            #'If-None-Match': 'W/"2968a967c8b57591fb9139a8d6cc4157"',
            'Referer': 'http://www.iphai.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.108 Safari / 537.36'
            }
        html = requests.get(start_url,headers=headers)
        if html.status_code == 200:
            print('Crawling: ',html.url)
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html.text)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')
        else:
            print(html.status_code,html.url)

    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn/index_{page}.html'
        urls = [start_url.format(page=page) for page in range(1,5)]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Cookie': 'channelid=0; sid=1541758831215199; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1541758836; _ga=GA1.2.1958916142.1541758836; _gid=GA1.2.1593926403.1541758836; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1541759737',
            'Host': 'www.89ip.cn',
            #'If-None-Match': 'W/"2968a967c8b57591fb9139a8d6cc4157"',
            'Referer': 'http://www.89ip.cn/api.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.108 Safari / 537.36'
            }
        for url in urls:
            html = requests.get(url,headers = headers)
            if html.status_code == 200:
                print('Crawling: ',html.url)
                doc = pq(html.text)
                trs = doc('.layui-table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:first-child').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])
            else:
                print(html.status_code,html.url)

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = requests.get(start_url, headers=headers)
        if html.status_code == 200:
            print('Crawling: ',html.url)
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html.text)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

        else:
            print(html.status_code,html.url)


    def crawl_swei360(self,page_count=7):

        start_url = 'http://www.swei360.com/free/?page={page}'
        urls = [start_url.format(page=page) for page in range(1,page_count + 1)]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'ASPSESSIONIDQQCSTQQQ = DGFJIAKCMMEBHIPCMFEHGEAA; UM_distinctid = 166f7880be31e0 - 0da756ec4f569d - 346a7809 - 13c680 - 166f7880be4225; CNZZDATA1000194460 = 149791577 - 1541751179 - null % 7C1541751179',
            'Host': 'www.swei360.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.108 Safari / 537.36'
            }
        for url in urls:
            print('Crawling: ',url)
            html = requests.get(url=url,headers = headers)
            if html.status_code == 200:
                doc = pq(html.text)
                trs = doc('#list tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:first-child').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])
            else:
                print(html.status_code,html.url)

    def crawl_ip3366(self,stype_count=5,page_count=7):

        start_url = 'http://www.ip3366.net/?stype={stype}&page={page}'

        urls = [start_url.format(stype=stype,page=page) for stype in range(1,stype_count+1) for page in range(1,page_count + 1)]

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'Cookie': 'UM_distinctid=166f7cba5961ea-0cc3df6220f2af-346a7809-13c680-166f7cba597b2a; CNZZDATA1256284042=343791865-1541751624-%7C1541751624; ASPSESSIONIDQACBQQRC=MFOPGCJCOCFPBPIMDFKAOOHN',
                   'Host': 'www.ip3366.net',
                   'Referer': 'http://www.ip3366.net/fetch/',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.108 Safari / 537.36'
                   }

        for url in urls:
            print('Crawling: ',url)
            html = requests.get(url=url,headers = headers)
            if html.status_code == 200:
                doc = pq(html.text)
                trs = doc('#list tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:first-child').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])
            else:
                print(html.status_code,html.url)


    def crawl_xroxy(self):

        for i in ['CN','US']:
            start_url = 'https://www.xroxy.com/free-proxy-lists/?port=&type=All_http&ssl=&country={country}&latency=&reliability='.format(country=i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                #'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
                'Host': 'www.xroxy.com',
                #'Referer': 'http://www.data5u.com/free/index.shtml',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            }
            html = requests.get(start_url,headers=headers)
            if html.status_code == 200:
                print('Crawling: ',html.url)
                doc = pq(html.text)
                trs = doc('.dttable tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:first-child').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])
            else:
                print(html.status_code,html.url)

    def crawl_goubanjia(self):
        '''
        获取Goubanjia
        :return: 代理
        '''
        start_url = 'http://www.goubanjia.com/'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.goubanjia.com',
            #'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = requests.get(start_url,headers =headers)
        if html.status_code == 200:
            print('Crawling: ',html.url)
            doc = pq(html.text)
            trs = doc('table.table tbody tr').items()
            for tr in trs:
                #print(tr.find('td:nth-child(2)').text())
                if tr.find('td:nth-child(2)').text() == '高匿':
                    td = tr.find('td:nth-child(1)')
                    td.find('p').remove()
                    yield td.text().replace('\n','')

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = requests.get(url)
            if html.status_code ==  200:
                doc = pq(html.text)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    """
    def crawl_proxy360(self):
        '''
        获取Proxy360
        :return: 代理
        '''
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])
    """

    """
    def crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_page(start_url)
        ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        # \s* 匹配空格，起到换行作用
        re_ip_address = ip_address.findall(html)
        for address,port in re_ip_address:
            result = address + ':' + port
            yield result.replace(' ', '')
    """

    """
    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':'+ port
                yield result.replace(' ', '')
    """

    """
    def crawl_premproxy(self):
        for i in ['China-01','China-02','China-03','China-04','Taiwan-01']:
            start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                for address_port in re_ip_address:
                    yield address_port.replace(' ','')

    """
