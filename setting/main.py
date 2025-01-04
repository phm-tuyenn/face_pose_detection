import os, json
from random import randrange

filename = os.path.join("C:", "Users", "Public", "setting.json")
if not os.path.exists(filename):
    f = open(filename, "w")
    f.write(json.dumps({
        "code": str(randrange(10)) + str(randrange(10)) + str(randrange(10)) + str(randrange(10)),
        "password": "$2b$12$zoHuqo7EpPxE0bTNOTh6LOlvjuJFdgaE/dpUl0.2RemQkdlSoto4u",
        "detectTime": 2,
        "alarmTime": 120
    }))
    f.close()

with open(filename, 'r', encoding="utf-8") as f:
    data = json.loads(f.read()) 
    import login
    if login.show(data):
        import setting
        setting.show(data, filename)