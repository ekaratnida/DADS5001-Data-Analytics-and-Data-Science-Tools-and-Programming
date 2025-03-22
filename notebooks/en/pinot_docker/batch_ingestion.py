import requests

upload_url = "http://localhost:9000/tables/batch"
files = {
    'file': ('movies.csv', open('movies.csv', 'rb')),
}
response = requests.post(upload_url, files=files)
print(response.status_code, response.text)