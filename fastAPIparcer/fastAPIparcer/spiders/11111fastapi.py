import json
import scrapy
from scrapy.http import JsonRequest


class FastapiSpider(scrapy.Spider):
    name = "fastapi"
    allowed_domains = ['127.0.0.1']
    start_urls = ['http://127.0.0.1:8000/docs']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'fastapi_docs.json',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def parse(self, response):
        # The OpenAPI/Swagger JSON is typically available at /openapi.json
        openapi_url = 'http://127.0.0.1:8000/openapi.json'
        yield JsonRequest(openapi_url, callback=self.parse_openapi)

    def parse_openapi(self, response):
        data = json.loads(response.text)

        # Extract basic API information
        api_info = {
            'title': data.get('info', {}).get('title'),
            'description': data.get('info', {}).get('description'),
            'version': data.get('info', {}).get('version'),
            'endpoints': []
        }

        # Extract paths and methods
        for path, methods in data.get('paths', {}).items():
            for method, details in methods.items():
                endpoint = {
                    'path': path,
                    'method': method.upper(),
                    'summary': details.get('summary'),
                    'description': details.get('description'),
                    'parameters': details.get('parameters', []),
                    'responses': details.get('responses', {})
                }
                api_info['endpoints'].append(endpoint)

        yield api_info
