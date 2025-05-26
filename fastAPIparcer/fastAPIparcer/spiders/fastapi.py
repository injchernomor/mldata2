# fastapi_docs/spiders/docs_spider.py
import json
import scrapy
from scrapy.http import JsonRequest


class FastAPIDocsSpider(scrapy.Spider):
    name = 'fastapi_docs'
    allowed_domains = ['127.0.0.1']
    start_urls = ['http://127.0.0.1:8000/docs']
    
    custom_settings = {
        'FEED_FORMAT': 'csv',  # Changed from json to csv
        'FEED_URI': 'fastapi_docs.csv',
        'FEED_EXPORT_FIELDS': [  # Define column order
            'path',
            'method',
            'summary',
            'description',
            'parameters_count',
            'success_response'
        ],
        'USER_AGENT': 'Mozilla/5.0...'
    }

    def parse(self, response):
        openapi_url = 'http://127.0.0.1:8000/openapi.json'
        yield JsonRequest(openapi_url, callback=self.parse_openapi)

    def parse_openapi(self, response):
        data = json.loads(response.text)
        
        for path, methods in data.get('paths', {}).items():
            for method, details in methods.items():
                # Count parameters
                params_count = len(details.get('parameters', []))
                
                # Get success response description
                success_response = details.get('responses', {}).get('200', {}).get('description', '')
                
                yield {
                    'path': path,
                    'method': method.upper(),
                    'summary': details.get('summary', ''),
                    'description': details.get('description', ''),
                    'parameters_count': params_count,
                    'success_response': success_response
                }