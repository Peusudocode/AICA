import requests


if __name__ == '__main__':
    response = requests.get('https://7d9e-2001-b400-e732-85cb-388d-f27b-2b1-eca8.ngrok.io/door1?status=start')
    print(response)