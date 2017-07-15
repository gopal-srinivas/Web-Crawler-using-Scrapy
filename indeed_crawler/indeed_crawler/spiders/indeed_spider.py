import scrapy

class IndeedSpider(scrapy.Spider):
	name = "jobs"
	start_urls = [
		'https://www.indeed.com/jobs?q=&l=Hillsboro%2C+OR',
	]

	def parse(self, response):
		for jobentry in response.css("div.row.result"):
			if(jobentry.css("h2.jobtitle a.turnstileLink::text").extract_first() != None):
				yield {
					'job': jobentry.css("h2.jobtitle a.turnstileLink::text").extract_first(),
					'company': jobentry.css("span.company span a::text").extract_first(),
					'location': jobentry.css("span.location span::text").extract_first(),
					'salary': jobentry.css("td.snip span.no-wrap::text").extract_first()
				}

			next_page = response.css('div.pagination a::attr(href)').extract()

			next_page = next_page[len(next_page) - 1]

			if next_page is not None:
				next_page = response.urljoin(next_page)
				yield scrapy.Request(next_page, callback=self.parse)
	
			
				
					
				
			