from solver import find_position
from icons import match
import requests
import time

def load_image(url):
    response = requests.get(url)
    return response.content

result = requests.post(
	url="https://basiliskcaptcha.com/challenge/create-challenge",
	json={
		"site_key": "a3760bfe5cf4254b2759c19fb2601667",
		"site_domain": "https://faucetpay.io"
	},
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
	}
).json()

captcha_id = result["data"]["captcha_id"]
slide_url = result["data"]["slide_url"]
background_url = result["data"]["background_url"]
slide_y = result["data"]["slide_y"]

_puzzle = load_image(slide_url)
_background = load_image(background_url)

coordinate = find_position(_background, _puzzle)["coordinates"]

trail_x, trail_y = [], []

timestamp = int(time.time() * 1000)

for coord in range(8, coordinate[0] + 1):
	timestamp += 15
	trail_x.append({"timestamp":timestamp,"coord":coord})
	trail_y.append({"timestamp":timestamp,"coord":0})

answer = requests.post(
	url="https://basiliskcaptcha.com/challenge/slide-verify",
	json={
		"site_key":"a3760bfe5cf4254b2759c19fb2601667",
		"site_domain":"https://faucetpay.io",
		"captcha_id":captcha_id,
		"trail_x":trail_x,
		"trail_y":trail_y
	},
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
	}
).json()

print(answer)

response = requests.post(
	url="https://basiliskcaptcha.com/challenge/icons-challenge",
	json={
		"site_key":"a3760bfe5cf4254b2759c19fb2601667",
		"site_domain":"https://faucetpay.io",
		"captcha_id":captcha_id
	},
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
	}
).json()

print(response)

background_url = response["data"]["background_url"]
icons_order = response["data"]["icons_order"]

background_bytef = load_image(background_url)

coords, trail_x, trail_y = match(background_bytef, icons_order)

result = requests.post(
	url="https://basiliskcaptcha.com/challenge/icons-verify",
	json={
		"site_key":"a3760bfe5cf4254b2759c19fb2601667",
		"site_domain":"https://faucetpay.io",
		"captcha_id":captcha_id,
		"coords":coords,
		"trail_x":trail_x,
		"trail_y":trail_y
	},
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
	}
).json()
print(result)


answer = requests.post(
	url="https://api.faucetpay.io/account/login",
	json={
		"user_email":"XXXXXXXXXXXX",
		"password":"XXXXXXXXXXXX",
		"captcha_response":result["data"]["captcha_response"]
	},
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
	}
).json()

print(answer)

token = answer["token"]


url = "https://api.faucetpay.io/limbo/play"

headers = {
	"Authorization":"Bearer {}".format(token)
}

def req(data):
	while 1:
		try:
			res = requests.post(url=url, json=data, headers=headers)
			return res.json()
			break
		except:
			...


number = 0.00074249

data = {
	"client_seed":"eXlP1bc1IDnaZILeegqL6S7FEPmDQB5Dz56J1DUNmzSGa0s9V6d8AN6tY8kunTSS",
	"bet_amt":number,
	"coin":"DGB",
	"target_payout":"2.00"
}

headers["Content-Length"] = str(len(data))

response = req(data)
print(response)
win = response["data"]["win"]
while 1:
	if win:
		number = 0.00074249
		data["bet_amt"] = number
		headers["Content-Length"] = str(len(data))
		response = req(data)
		win = response["data"]["win"]
		print(response["data"]['balance'])
	else:
		number = number * 2
		data["bet_amt"] = number
		headers["Content-Length"] = str(len(data))
		response = req(data)
		win = response["data"]["win"]
		print(response["data"]['balance'])




