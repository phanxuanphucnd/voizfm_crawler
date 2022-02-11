import json
from scrapy import Spider
from scrapy import Request
from audiobook.items import AudiobookItem

from selenium import webdriver
# from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException


class VoizfmSpider(Spider):
    """VoizFM"""
    name = 'voizfm'
    allowed_domains = ['voiz.vn/']
    start_urls = [
        # 'https://voiz.vn/audio-book/lanh_dao',
        # 'https://voiz.vn/audio-book/ky_nang',
        # 'https://voiz.vn/audio-book/lua_doi',
        # 'https://voiz.vn/audio-book/lich_su',
        # 'https://voiz.vn/audio-book/thanh_cong',
        # 'https://voiz.vn/audio-book/coming_soon',
        # 'https://voiz.vn/audio-book/hanh_phuc',
        # 'https://voiz.vn/audio-book/cong_nghe',
        # 'https://voiz.vn/audio-book/marketing',
        # 'https://voiz.vn/audio-book/suc_khoe',
        # 'https://voiz.vn/audio-book/tam_ly',
        # 'https://voiz.vn/audio-book/tam_linh',
        # 'https://voiz.vn/audio-book/kinh_doanh',
        # 'https://voiz.vn/audio-book/con_cai',
        # 'https://voiz.vn/audio-book/danh_nhan',
        # 'https://voiz.vn/podcast/phap_thoai',
        # 'https://voiz.vn/podcast/tam_su',
        # 'https://voiz.vn/podcast/tin_tuc',
        # 'https://voiz.vn/podcast/kien_thuc',
        # 'https://voiz.vn/podcast/kinh_di',
        # 'https://voiz.vn/podcast/hoc_ngoai_ngu',
        # 'https://voiz.vn/podcast/giai_tri',
        # 'https://voiz.vn/podcast/van_hoa',
        # 'https://voiz.vn/podcast/ngu_ngon',
        # 'https://voiz.vn/podcast/thien_tinh_tam'
    ]
    order_number = 0
    OUTPUT_DIRECTORY = './urls.txt'
    driver_path ='./drivers/chromedriver'

    chromeOptions = Options()
    chromeOptions.headless = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_driver = webdriver.Chrome(executable_path=self.driver_path,
                                            options=self.chromeOptions,
                                            service_log_path='NUL')
        # self.display = Display(visible=0, size=(800, 600))
        # self.display.start()

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url, callback=self.parse)

    def parse(self, response):
        self.main_driver.implicitly_wait(5)
        self.main_driver.get(response.url)
        more_flag = True
        while more_flag == True:
            button_more = None
            self.main_driver.implicitly_wait(3)
            button_more = self.main_driver.find_element_by_xpath(
                '//*[@class="btn load-more__button js-load-mord-item"]')
            try:
                button_more.click()
            except:
                print("Buttom `Xem thêm` not existed !")
                more_flag = False

        self.main_driver.implicitly_wait(5)
        entries = self.main_driver.find_elements_by_xpath('//*[@class="category-item__link"]')
        links = [entry.get_attribute('href') for entry in entries]
        print(f"\n>>> URLs : {links}\n")
        for link in links:
            with open(self.OUTPUT_DIRECTORY, 'a', encoding='utf-8') as f:
                f.writelines(link + '\n')
            # yield Request(url=link, callback=self.parse_content)

        self.main_driver.close()
        # self.display.close()

    # def parse_content(self, response):
    #     print(f">>>>> Processing url {response.url}...")
    #     item = AudiobookItem()
    #     title = response.xpath('//*[@class="audio__title"]/text()').get()
    #     author = response.xpath('//*[@class="info__item--border-sm"]/text()').get()
    #     item['title'] = title
    #     item['author'] = author
    #
    #     with open(self.OUTPUT_DIRECTORY, 'a', encoding='utf-8') as f:
    #         f.write(json.dumps(
    #             {
    #                 'stt': self.order_number,
    #                 'title': title,
    #                 'author': author
    #             }, indent=4, ensure_ascii=False
    #         ))
    #     self.order_number += 1
    #
    #     yield  item
