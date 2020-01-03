import time,requests,zipfile,json,os,io

def CheckVersion():
    while True:
        Settings = json.loads(open("Settings.json").read())

        Github = requests.get("https://raw.githubusercontent.com/LupusLeaks/EasyFNBotGlitch/master/Settings.json").json()
        if Github["Bot Version"] != Settings["Bot Version"]:
            print("Restarting...")
            for Value,Key in Settings.items():
                if Value in Github and Value != "Bot Version":
                    Github[Value] = Key

            with open("Settings.json","w+") as f:
                f.write(json.dumps(Github,indent=2))
            r = requests.get("https://github.com/LupusLeaks/EasyFNBotGlitch/releases/download/EasyFNBot/EasyFNBot.zip")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            for fileName in z.namelist():
                if not "Settings.json" in fileName:
                    z.extract(fileName, '')
            os.system("python3 main.py")
        else:
            time.sleep(1800)

def CheckItems():
    while True:
        Settings = json.loads(open("Settings.json").read())
        Cosmetics = requests.get("https://fortnite-api.com/cosmetics/br?language=en",headers={"x-api-key": Settings["fortnite-api Key"],"User-Agent": f'EasyFNBot/{Settings["Bot Version"]}'}).json()

        if Cosmetics["status"] == 200:
            StoredEnglishCosmetics = json.loads(open("Itemsen.json").read())
            if StoredEnglishCosmetics != Cosmetics["data"]:
                print("Cosmetic list update started")
                open("Itemsen.json","w+").write(json.dumps(Cosmetics["data"]))
                Items = []
                ItemCount = len(Cosmetics["data"])

                for Cosmetic in Cosmetics["data"]:
                    Items.append({"Names" : {"en" : Cosmetic["name"]},"id" : Cosmetic["id"],"type" : Cosmetic["type"],"backendType" : Cosmetic["backendType"],"rarity" : Cosmetic["rarity"],"backendRarity" : Cosmetic["backendRarity"],"variants" : {"en" : Cosmetic["variants"]},"path" : Cosmetic["path"]})
            
                for lang in ["ar","de","es-419","es","fr","it","ja","ko","pl","pt-BR","ru","tr","zh-CN","zh-Hant"]:
                    r = requests.get(f"https://fortnite-api.com/cosmetics/br?language={lang}",headers={"x-api-key": Settings["fortnite-api Key"],"User-Agent": f'EasyFNBot/{Settings["Bot Version"]}'}).json()["data"]
                    if ItemCount == len(r):
                        for idx,item in enumerate(r):
                            Items[idx]["Names"][lang] = item["name"]
                            Items[idx]["variants"][lang] = item["variants"]

                open("Items.json","w+").write(json.dumps(Items))
                print("Updated Cosmetic list, big thanks to https://fortnite.com")
        
        time.sleep(600)