import time,requests,zipfile,json,os,io

def CheckVersion():
    while True:
        Settings = json.loads(open("Settings.json").read())

        GithubT = requests.get("https://raw.githubusercontent.com/LupusLeaks/EasyFNBotGlitch/master/Settings.json").text
        Github = json.loads(GithubT)
        if Github["Bot Version"] != Settings["Bot Version"]:
            print("Restarting...")
            for Value,Key in Settings.items():
                if Value in Github and Value != "Bot Version":
                    GithubT = GithubT.replace(str(json.dumps(Github[Value])),str(json.dumps(Settings[Value])))

            with open("Settings.json","w+") as f:
                f.write(Github)
            r = requests.get("https://github.com/LupusLeaks/EasyFNBotGlitch/releases/download/EasyFNBot/EasyFNBot.zip")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            for fileName in z.namelist():
                if not "Settings.json" in fileName:
                    z.extract(fileName, '')
            os.system("python3 main.py")
        else:
            time.sleep(1800)