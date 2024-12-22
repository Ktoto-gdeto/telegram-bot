import requests

TOKEN = "7992162373:AAFSKzAq4-OP6roCFzpDlD6k8kWQkrnu60c"
url = f"https://api.telegram.org/bot{TOKEN}/getMe"

response = requests.get(url)
print(response.json())
