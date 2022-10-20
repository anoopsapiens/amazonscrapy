import requests
import scrapy
import time
from bs4 import BeautifulSoup
from selectorlib import Extractor
e = Extractor.from_yaml_file('scrap_criteria.yml')
refererlink = 'https://www.amazon.com'


class AmazonspiderSpider(scrapy.Spider):
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    name = 'amazonspider'
    allowed_domains = ['amazon.com']
    with open('amazon/spiders/keywords.data') as f:
        keywords = f.readlines()
    keywords = [k.strip().replace(' ', '+') for k in keywords]
    start_urls=[]
    # start_urls = [
    #     'https://www.amazon.com/s?k=laptops'
    # ]
    for x in keywords:
        start_urls.append('https://www.amazon.com/s?k='+x)

    def parse(self, response):
        product_count = 1
        data = e.extract(response.text)
        if data:
            for product in data['products']:
                product_url = refererlink+product['url']
                # if product_count <= 5:
                #     product_count += 1
                self.extract(product_url)
                if self.name != "NA":
                    yield {
                        'name'          :   self.name,
                        'price'         :   self.price,
                        'quantity'      :   1,
                        'rating'        :   self.rating,
                        'availablility' :   self.isavailable,
                        'Seller Name'   :   self.seller_name,
                        'product link'  :   product_url,
                        'image link'    :   self.image_link,
                    }
                    break

    def extract(self, product_url):
        time.time(.4)
        # proxies = { 
        #       "http"  : "http://35.193.225.103:80", 
        #       "https" : "http://35.193.225.103:80", 
        #       "ftp"   : "http://35.193.225.103:80"
        #     }
        req = requests.get(product_url, headers=self.HEADERS)#,proxies=proxies)
        html = BeautifulSoup(req.text, "lxml")
        try:
            self.name = html.find("span", attrs={
                "id": 'productTitle'}).string.strip().replace(',', '')
        except:
            try:
                self.name = html.find('span', attrs={
                    "class": 'a-size-large product-title-word-break'}).string.strip().replace(',', '')
            except:
                self.name = "NA"
        try:
            self.price = html.find(
                "span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
            self.price = self.price.strip('$')
            self.price = float(self.price)
        except:
            self.price = "NA"
    #------------------------------retrieving product rating--------------------------------------#
        try:
            self.rating = html.find("i", attrs={
                'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
        except:
            try:
                self.rating = html.find(
                    "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
            except:
                self.rating = "NA"
    #-----------------------------------availablility status----------------------------------------#
        try:
            self.isavailable = html.find("div", attrs={'id': 'availability'}).find(
                "span").string.strip().replace(',', '')
        except:
            self.isavailable = "NA"
    #-----------------------------------Seller Name------------------------------------------------#
        try:
            self.seller_name = html.find(
                "div", attrs={"id": 'merchant-info'}).contents[2].string
        except:
            try:
                self.seller_name = html.find(
                    "a", attrs={"id": 'sellerProfileTriggerId'}).string
            except:
                self.seller_name = "amazon"
    #-----------------------------------------------#
        try:
            # .split()[23].split('=')[1]
            self.image_link = str(
                html.find("div", attrs={"id": 'imgTagWrapperId'}))
            self.image_link = re.search("(?P<url>https?://[^\s]+)", self.image_link).group("url").split('"')[0]
        except:
            try:
                self.image_link = str(html.find("div", attrs={
                    "class": 'imgTagWrapperId'})).split()[23].split('=')[1]
            except:
                self.image_link = "NA"
