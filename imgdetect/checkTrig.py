import requests, os, json

prevState = requests.get('https://giamsathoctap.vercel.app/api/getEnable?code=0913').json()["enable"]

def loop():
    while True:
        state = requests.get('https://giamsathoctap.vercel.app/api/getEnable?code=0913').json()["enable"]
        if state != prevState:
            open(os.path.join("C:", "Users", "Public", "open.json"), "w").write(json.dumps({
                "open": state
            }))
        prevState = state