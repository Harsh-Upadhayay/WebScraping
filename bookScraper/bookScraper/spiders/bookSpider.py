import scrapy
from bookScraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookSpider"

    # To Scrape within a website only.
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books =  response.css("article.product_pod")

        for book in books:
            url = book.css("a").attrib['href']

            if 'catalogue/' in url:
                bookUrl = 'https://books.toscrape.com/' + url
            else:
                bookUrl = 'https://books.toscrape.com/catalogue/' + url

            yield response.follow(bookUrl, callback=self.parseBookPage)
        
        
        # Url for next page
        nextPageUrl = response.css("li.next a::attr(href)").get()
        
        if nextPageUrl is not None:
            if 'catalogue/' in nextPageUrl:
                nextPageUrl = 'https://books.toscrape.com/' + nextPageUrl
            else:
                nextPageUrl = 'https://books.toscrape.com/catalogue/' + nextPageUrl

            yield response.follow(nextPageUrl, callback=self.parse)

    def parseBookPage(self, response):

        # yield {

        #     'url': response.url,
        #     'title': response.css('.product_main h1::text').get(),
        #     'description': response.xpath("/html/body/div[1]/div/div[2]/div[2]/article/p").get(),
        #     'price': response.xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[1]/div[2]/p[1]").css("p::text").get(),
        #     'rating': response.xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[1]/div[2]/p[3]").css("p::attr('class')").get(),

        # }
        

        bookItem = BookItem()
        bookItem['url'] = response.url
        bookItem['title'] = response.css('.product_main h1::text').get()
        bookItem['description'] = response.xpath("/html/body/div[1]/div/div[2]/div[2]/article/p").get()
        bookItem['price'] = response.xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[1]/div[2]/p[1]").css("p::text").get()
        bookItem['rating'] = response.xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[1]/div[2]/p[3]").css("p::attr('class')").get()

        yield bookItem