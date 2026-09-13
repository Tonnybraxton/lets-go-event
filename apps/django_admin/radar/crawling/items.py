import scrapy


class RadarObservationItem(scrapy.Item):
    source_url = scrapy.Field()
    source_event_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    start_raw = scrapy.Field()
    end_raw = scrapy.Field()
    venue_raw = scrapy.Field()
    address_raw = scrapy.Field()
    city_raw = scrapy.Field()
    county_raw = scrapy.Field()
    organizer_raw = scrapy.Field()
    category_raw = scrapy.Field()
    price_raw = scrapy.Field()
    currency_raw = scrapy.Field()
    ticket_url = scrapy.Field()
    image_url = scrapy.Field()
    metadata = scrapy.Field()
