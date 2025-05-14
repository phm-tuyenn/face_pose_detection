import os, requests, json

def loop():
    print("start upload log")
    filename = os.path.join("C:/", "Users", "Public", "detect_log.json")
    code = json.loads(open(os.path.join("C:/", "Users", "Public", "setting.json"), "r").read())["code"]
    try:
        open(filename, "r").close()
    except:
        open(filename, "w").write("[]")
    prevLog = open(filename, "r", encoding="utf-8").read()
    while True:
        log = open(filename, "r", encoding="utf-8").read()
        if prevLog != log:
            requests.get('https://giamsathoctap.vercel.app/api/setLog?code=' + code, json=json.loads(log))
        prevLog = log