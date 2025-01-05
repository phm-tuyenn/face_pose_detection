import os, requests, json

def loop():
    print("start upload log")
    filename = os.path.join("C:", "Users", "Public", "detect_log.json")
    prevLog = open(filename, "r", encoding="utf-8").read()
    while True:
        log = open(filename, "r", encoding="utf-8").read()
        if prevLog != log:
            requests.get('https://giamsathoctap.vercel.app/api/setLog?code=0913', json=json.loads(log))
        prevLog = log