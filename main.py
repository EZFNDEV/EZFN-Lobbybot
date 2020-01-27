import asyncio
import Config
import json
import MultipleClients
import fortnitepy
import sys
import io
import zipfile
import requests
from sanic import Sanic,response
from Fortnite import DefaultCosmetics
from Fortnite.Event import friends,party,message

app = Sanic('EasyFNLobbyBot')
fnClient = fortnitepy.Client(email=None,password=None)
ClientSettings = Config.ConfigReader(json.loads(open("Settings.json").read()))
fnClient.Clients = {}
fnClient.randomizing = False
fnClient.RemovingFriends = False

@fnClient.event
async def event_ready():
    print("Fortnite Client is now ready!")
    fnClient.mainID = fnClient.user.id
    fnClient.SubAccountCount = len([Email for Email in fnClient.Settings.Account.Sub_Accounts if "@" in Email])

    if fnClient.SubAccountCount > 0:
        tasks = []
        for email,password in fnClient.Settings.Account.Sub_Accounts.items():
            if "@" in email and len(tasks) < 10:
                tasks.append(MultipleClients.LoadAccount(fnClient,email,password))
        
        try:
            await asyncio.wait(tasks)
        except:
            pass

        for Client in fnClient.Clients.values():
            Friends = fnClient.has_friend(Client.user.id)
            if not Friends:
                try:
                    await fnClient.add_friend(Client.user.id)
                except:
                    pass

#Friends
@fnClient.event
async def event_friend_add(friend):
    await friends.event_friend_add(fnClient, friend)
    
@fnClient.event
async def event_friend_remove(friend):
    await friends.event_friend_remove(fnClient, friend)

@fnClient.event
async def event_friend_request(friend):
    await friends.event_friend_request(fnClient, friend)
#Party
@fnClient.event
async def event_party_invite(invitation):
    await party.event_party_invite(fnClient, invitation)

@fnClient.event
async def event_party_member_join(Member):
    await party.event_party_member_join(fnClient,Member)

@fnClient.event
async def event_party_member_promote(old_leader, new_leader):
    await party.event_party_member_promote(fnClient, old_leader,new_leader)
#message
@fnClient.event
async def event_party_message(Message):
    await message.Command(fnClient, Message)

@fnClient.event
async def event_friend_message(Message):
    await message.Command(fnClient, Message)

async def StartFNClient():
    ClientSettings = Config.ConfigReader(json.loads(open("Settings.json").read()))
    fnClient.email = ClientSettings.Account.Email
    fnClient.password = ClientSettings.Account.Password
    fnClient.Settings = ClientSettings
    fnClient.status = Config.Status
    DC = await DefaultCosmetics.Cosmetics(ClientSettings)
    fnClient.default_party_member_config = DC[0]
    fnClient.default_party_config = DC[1]

    try:
        await fnClient.start()
        await fnClient.wait_until_ready()
    except fortnitepy.AuthException as e:
        if "errors.com.epicgames.accountportal.captcha_invalid" in str(e):
            return response.json({"error":"errors.com.epicgames.accountportal.captcha_invalid"})
        return response.json({"error":"Wrong Epic Games Account Credentials!"})
    except Exception as e:
        return response.json({"error":"Something went wrong while logging in!","errorMessage":e})

async def Authenticate(request):
    ClientSettings = Config.ConfigReader(json.loads(open("Settings.json").read()))
    if request.headers.get('X-Secret-Password'):
        if ClientSettings.HeaderPassword:
            if not ClientSettings.HeaderPassword == request.headers.get('X-Secret-Password'):
                return response.json({"error":"Unauthorized"},status=401)
        else:
            return response.json({"error":"No secret password is set!"},status=200)
    else:
        return response.json({"error":"Bad request!"},status=400)

@app.route('/')
async def Home(request):
    return response.text('Follow @LupusLeaks on Twitter')

@app.route('/update')
async def Update(request):
    update = await Authenticate(request)
    if isinstance(update, response.HTTPResponse): return update
    
    CurrentSettings = json.loads(open("Settings.json").read())
    try:
        os.system('rm -r -f -d *')
    except:
        pass

    NewSettings = requests.get('https://raw.githubusercontent.com/LupusLeaks/EasyFNBotGlitch/master/Settings.json').json()
    for Key,Value in NewSettings.items():
        if Key in CurrentSettings and Key != "Bot Version":
            NewSettings[Key] = CurrentSettings[Key]

    z = zipfile.ZipFile(io.BytesIO((requests.get('https://github.com/LupusLeaks/EasyFNBotGlitch/releases/download/EasyFNBot/EasyFNBot.zip')).content))
    for fileName in z.namelist():
        if not "Settings.json" in fileName:
            z.extract(fileName, '')
    open("Settings.json","w+").write(json.dumps(NewSettings,indent=2))
    sys.exit()

@app.route('/settings')
async def settings(request):
    settings = await Authenticate(request)
    if isinstance(settings, response.HTTPResponse): return settings
    Settings = json.loads(open("Settings.json").read())

    if request.body:
        try:
            newbody = json.loads(request.body)
        except:
            return response.json({"error":"Bad request!"})
        open("Settings.json","w+").write(json.dumps(newbody,indent=2))
        sys.exit()
    else:
        return response.json(Settings)

@app.route('/status')
async def status(request):
    Status = await Authenticate(request)
    if isinstance(Status, response.HTTPResponse): return Status

    data = {"mainClient":{"is_ready":fnClient.is_ready(),"displayName":fnClient.user.display_name,"friends":len(fnClient.friends)}}
    if len(fnClient.Clients) > 0:
        data["SubClients"] = {}
        for Client in fnClient.Clients.values():
            data["SubClients"][Client.user.display_name] = {"friends":len(Client.friends),"is_ready":Client.is_ready()}

    return response.json(data)

@app.route('/start')
async def start(request):
    Start = await Authenticate(request)
    if isinstance(Start, response.HTTPResponse): return Start

    if fnClient.is_ready():
        return response.json({"error":"The client is already ready!"},status=200)

    return await StartFNClient()

@app.route('/restart')
async def restart(request):
    ReStart = await Authenticate(request)
    if isinstance(ReStart, response.HTTPResponse): return ReStart

    for client in fnClient.Clients.values():
        await client.logout()
    await fnClient.logout()
    await asyncio.sleep(0.5)

    return await StartFNClient()

@app.route('/restartall')
async def restartall(request):
    Restart = await Authenticate(request)
    if isinstance(Restart, response.HTTPResponse): return Restart

    sys.exit()

@app.route('/stop')
async def stop(request):
    Stop = await Authenticate(request)
    if isinstance(Stop, response.HTTPResponse): return Stop

    for client in fnClient.Clients.values():
        await client.logout()
    await fnClient.logout()
    return response.json({"success":"Logged out!"})

#Start Server
loop = asyncio.get_event_loop()
loop.create_task(app.create_server(host="127.0.0.1", port=8000, return_asyncio_server=True))
if ClientSettings.AutoStart:
    loop.create_task(StartFNClient())
try:
    loop.run_forever()
finally:
    loop.stop()