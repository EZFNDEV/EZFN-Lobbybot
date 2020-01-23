import sanic,json,requests,zipfile,io,os,sys
from sanic import response

async def CheckPassword(ClientSettings,request):
    if request.headers.get('X-Secret-Password'):
        if ClientSettings.HeaderPassword:
            if not ClientSettings.HeaderPassword == request.headers.get('X-Secret-Password'):
                return response.json({"error":"Unauthorized"},status=401)
        else:
            return response.json({"error":"No secret password is set!"},status=200)
    else:
        return response.json({"error":"Bad request!"},status=400)

async def Update(ClientSettings,request):
    #Check for auth
    Passwd = await CheckPassword(ClientSettings,request)
    if isinstance(Passwd, sanic.response.HTTPResponse): return Passwd

    try:
        Update = json.loads(request.body)
    except:
        return response.json({"error":"Bad request!"},status=400)

    if "UpdateURL" in Update and "SettingsURL" in Update:
        CurrentSettings = json.loads(open("Settings.json").read())
        try:
            os.system('rm -r -f -d *')
        except:
            pass
        NewSettings = requests.get(Update["SettingsURL"]).json()

        for Key,Value in NewSettings.items():
            if Key in CurrentSettings and Key != "Bot Version":
                NewSettings[Key] = CurrentSettings[Key]

        z = zipfile.ZipFile(io.BytesIO((requests.get(Update["UpdateURL"])).content))
        for fileName in z.namelist():
            if not "Settings.json" in fileName:
                z.extract(fileName, '')
        open("Settings.json","w+").write(json.dumps(NewSettings,indent=2))
        sys.exit()
    else:
        return response.json({"error":"Bad request!"},status=400)