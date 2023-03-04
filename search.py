import requests
import json

class BingSearch:
    def __init__(self, subscription_key : str, endpoint : str="https://api.bing.microsoft.com/v7.0/search"):
        self.subscription_key = subscription_key
        self.endpoint = endpoint
        
    def query_urls(self, query: str) -> list:
        results = self._get_results_dict(query)
        
        pages = results['webPages']
        values = pages['value']
        urls = [{'title': value['name'], 'url' : value['displayUrl']} for value in values]

        return urls
    
    def _get_results_dict(self, query: str):
        response = self._request(query)
        results = response.json()
    
        return results
        
    def _request(self, query: str) -> dict:
        mkt = 'en-US'
        params = { 'q': query, 'mkt': mkt }
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
        except Exception as ex:
            raise ex
        
        return response
