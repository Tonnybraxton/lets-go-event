# Radar spiders and extractors

Use the simplest authorized acquisition path: partner API, public API, RSS, ICS, JSON-LD, sitemap, static HTML, then Playwright only when JavaScript is required.

`JsonLdExtractor` handles schema.org event variants. `SelectorExtractor` accepts constrained CSS or `xpath:` field expressions. The Scrapy `radar_jsonld` spider demonstrates the adapter boundary. Spiders only emit raw observations; they never publish canonical events.

Run the spider with a reviewed public URL:

```powershell
scrapy runspider radar\crawling\spiders\generic_jsonld.py -a start_url=https://example.org/events
```
