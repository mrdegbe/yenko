import requests
import certifi

url = "https://api.sandbox.africastalking.com/version1/messaging"

try:

    response = requests.get(url, verify=certifi.where(), timeout=10)

    print(response.status_code)
    print(response.text)

except Exception as e:
    print(e)
