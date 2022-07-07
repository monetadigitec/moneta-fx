import requests

#url="https://api.apilayer.com/exchangerates_data/latest?symbols=EUR%2C&base=USD"
payload = {}
Headers = {"apikey":"JujvukNl0q9rNPLyPg9LoXYrLZV73tcS"}
get_exch = requests.request("GET",url="https://api.apilayer.com/exchangerates_data/latest?symbols=EUR%2CGBP%2CCNY%2CJPY%2CCHF&base=USD", headers = Headers,data=payload)
#get_exch = requests.request("GET",url, headers = Headers,data=payload)
print(get_exch.status_code)
print(get_exch.text)