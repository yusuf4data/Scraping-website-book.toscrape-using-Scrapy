import scrapy


class ScrapeBookSpider(scrapy.Spider):
    name = 'scrape_book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    base_url = 'http://books.toscrape.com/'

    def parse(self, response):
        # link of all books in the page 1
        all_book_in_page = response.xpath('//article')
        for book in all_book_in_page:
            book_partial_url = book.xpath('h3/a/@href').extract_first()
            if 'catalogue/' not in book_partial_url:
                book_partial_url = 'catalogue/' + book_partial_url
            book_url = self.base_url + book_partial_url
            yield scrapy.Request(book_url, callback=self.book_parse)
        # check if there is a next page if yes it will fix the link and parse data again
        next_page=response.xpath("//li[@class='next']/a/@href").extract_first()

        if next_page:
            if 'catalogue/' not in next_page:
                next_page='catalogue/'+next_page
            next_page=self.base_url+next_page
            yield scrapy.Request(next_page,callback=self.parse)


    def book_parse(self,response):

        # extract details of the book
        # the title
        title=response.xpath("//div/h1/text()").extract_first()
        # the price
        price=response.xpath("//p[@class='price_color']/text()").extract_first()
        # In stock
        availablety=response.xpath("//p[@class='instock availability']/text()").extract()[1].strip().replace('In stock','')
        # image source //div[@class='item active']/img/@src
        img_url=response.xpath("//div[@class='item active']/img/@src").extract_first().replace('../..','')
        final_img_url=self.base_url+img_url
        # Product Description
        Description=response.xpath('//*[@id="content_inner"]/article/p/text()').extract_first()
        # Product Information
        UPC=response.xpath('//table//tr[1]/td/text()').extract_first()
        # Product Type
        Product_Type=response.xpath('//table//tr[2]/td/text()').extract_first()
        # Price (excl. tax)
        Price_excl_tax = response.xpath('//table//tr[3]/td/text()').extract_first()
        # Price (incl. tax)
        Price_incl_tax = response.xpath('//table//tr[4]/td/text()').extract_first()
        # Tax
        Tax = response.xpath('//table//tr[5]/td/text()').extract_first()
        # Number of reviews
        Number_of_reviews = response.xpath('//table//tr[7]/td/text()').extract_first()

        yield {
            'title':title,
            'price':price,
            'availablety':availablety,
            'final_img_url':final_img_url,
            'Description':Description,
            'UPC':UPC,
            'Product_Type':Product_Type,
            'Price_excl_tax':Price_excl_tax,
            'Price_incl_tax':Price_incl_tax,
            'Tax':Tax,
            'Number_of_reviews':Number_of_reviews

        }

