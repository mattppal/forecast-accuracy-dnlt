import scrapy
from forecastadvisor.items import AccuracyItem

class ForecastSpider(scrapy.Spider):
    name = 'forecasts'
    start_urls = ['https://www.forecastadvisor.com/browse/']

    def parse(self, response):
        self.logger.info('get state urls')
        state_hrefs = response.xpath('//div[@id="main-box"]//a//@href').getall()

        for state_href in state_hrefs:
            # state_name = state_href.split('/')[-1]
            yield response.follow(state_href, callback=self.parse_state)
    
    def parse_state(self, response):
        city_hrefs = response.xpath('//div[@id="main-box"]//li//a//@href').getall()
        multiple_hrefs = [city_href for city_href in city_hrefs if 'browse' in city_href]
        
        single_hrefs = set(city_hrefs).difference(set(multiple_hrefs))

        for multiple_href in multiple_hrefs:
            yield response.follow(multiple_href, callback=self.parse_multi_city)

        for single_href in single_hrefs:
            yield response.follow(single_href, callback=self.parse_city)

    def parse_multi_city(self, response):
        single_hrefs = response.xpath('//div[@id="main-box"]//li//a//@href').getall()
        
        for single_href in single_hrefs:
            yield response.follow(single_href, callback=self.parse_city)

    def parse_city(self, response):
        further_analysis_hrefs = response.xpath('//div[@class="further-analysis"]//a//@href').getall()
        for further_analysis_href in further_analysis_hrefs:
            
            cb_kwargs = {'sort_zip': further_analysis_href.split('/')[-2]
                         , 'sort_city': further_analysis_href.split('/')[-3]
                         , 'sort_state':further_analysis_href.split('/')[-4]
                         }

            yield response.follow(further_analysis_href, callback=self.parse_further_analysis, cb_kwargs=cb_kwargs)
    
    def parse_further_analysis(self, response, sort_zip, sort_city, sort_state):
        detail_year_table = response.xpath('//div[@class="centered narrow"]//table[@class="accuracy-data detail"][@id="year"]//tbody/tr')
        
        sort_zip = sort_zip
        sort_city = sort_city
        sort_state = sort_state

        for line in detail_year_table:
            accuracy_item = AccuracyItem()

            provider = line.xpath('td[@headers="provider"]/@title').get()
            hi = line.xpath('td[@headers="hi"]/text()').get()
            low = line.xpath('td[@headers="low"]/text()').get()
            icon = line.xpath('td[@headers="icon"]/text()').get()
            text = line.xpath('td[@headers="text"]/text()').get()
            overall = line.xpath('td[@headers="overall"]/text()').getall()
            

            accuracy_item['provider'] = provider
            accuracy_item['hi'] = hi
            accuracy_item['low'] = low
            accuracy_item['icon'] = icon
            accuracy_item['text'] = text
            accuracy_item['overall'] = overall[0]
            accuracy_item['sort_zip'] = sort_zip
            accuracy_item['sort_city'] = sort_city
            accuracy_item['sort_state'] = sort_state
            
            yield accuracy_item
            
