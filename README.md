

1. Crawl toàn bộ url có trong toàn bộ category / topic và lưu vào file `urls.txt`

```
scrapy crawl voizfm 

```


2. Chạy lệnh crawl thông tin và lưu vào data.csv

```
scrapy crawl content -o data.csv
```