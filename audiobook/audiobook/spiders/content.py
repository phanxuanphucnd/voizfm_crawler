import json
from scrapy import Spider
from scrapy import Request
from audiobook.items import AudiobookItem


class VoizfmContentSpider(Spider):
    """VoizFM"""
    name = 'content'
    allowed_domains = ['voiz.vn/']
    with open('./urls.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    start_urls = list(set([line.strip() for line in lines]))

    OUTPUT_DIRECTORY = './data.jsonl'
    order_number = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url, callback=self.parse)

    def parse(self, response):
        print(f">>>>> Processing url {response.url}...")
        item = AudiobookItem()
        title = response.xpath('//*[@class="audio__title"]/text()').get().strip()
        author = response.xpath('//*[@class="info__item--border-sm"]/text()').get().strip()
        item['title'] = title
        item['author'] = author

        with open(self.OUTPUT_DIRECTORY, 'a', encoding='utf-8') as f:
            f.write(json.dumps(
                {'stt': self.order_number, 'title': title, 'author': author},
                indent=4,
                ensure_ascii=False
            ))
            f.write('\n')

        self.order_number += 1

        yield item
