import requests

class HTTP:
    def __init__(self):
        pass
    
    def send_http(self,url, method, headers, data):
        response = requests.request(method,url, headers=headers, data=data)
        return response