import requests

url = "https://www.etsy.com/blog/category/home-and-living?ref=blog"

payload={}
headers = {
  'user-agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
  'Cookie': 'exp_hangover=iVcUUs0wAjRcCr1_U6q_QCjMEkZjZACCpK2G9TC6WqkgtSgtRr88NSk-sagkMy0zOTMxJz4nsSQ1L7kyvtAw3sjAyEjJKi0xpzi1lgEA; fve=1655976127.0; uaid=tm-e9QiZn3WDHL_b-UPa0wUVUMVjZACCpC0G-2F0tVJpYmaKkpVSlbtxuU-ZhblZRXC5mV-gZbCFkW5OZVCKd6ZxuVItAwA.; user_prefs=qTiGlnZew3nO5fe3g2B1GynFfyVjZACCpC0G-2F0tFJosIuSTl5pTo6OUmqebmiwko4SiACLGEEoXEQsAwA.'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
