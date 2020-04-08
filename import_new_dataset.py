import requests

response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")

print(response)