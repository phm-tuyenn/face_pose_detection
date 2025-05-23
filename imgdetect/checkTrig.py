import requests, os, json

def loop():
    atStart = json.loads(open(os.path.join("C:/", "Users", "Public", "setting.json"), "r").read())["runAtStartup"]
    code = json.loads(open(os.path.join("C:/", "Users", "Public", "setting.json"), "r").read())["code"]
    open(os.path.join("C:/", "Users", "Public", "open.json"), "w").write(json.dumps({
            "open": atStart
        }))
    _out = "false"
    if atStart: _out = "true"
    requests.get('https://giamsathoctap.vercel.app/api/setEnable?code=' + code + '&enable='+_out)
    prevState = atStart
    print("wait for start")
    while True:
        state = requests.get('https://giamsathoctap.vercel.app/api/getEnable?code=' + code).json()["enable"]
        if state != prevState:
            open(os.path.join("C:/", "Users", "Public", "open.json"), "w").write(json.dumps({
                "open": state
            }))
        prevState = state