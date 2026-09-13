import scrapy

from radar.extraction import JsonLdExtractor


class GenericJsonLdSpider(scrapy.Spider):
    name = "radar_jsonld"
    custom_settings = {"ROBOTSTXT_OBEY": True}

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("start_url is required")
        self.start_urls = [start_url]

    def parse(self, response):
        for observation in JsonLdExtractor().extract(response.text, response.url):
            yield observation.as_dict()
