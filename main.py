
import json
import asyncio
import fortnitepy
import sys
import os

import Config
import MultipleClients
from Webserver import Check
from Fortnite import DefaultCosmetics
from Fortnite.Events import party,friends,message

import sanic
from sanic import Sanic,response,request

OldSettings = json.loads(open("Settings.json").read())
New = {}
if not "Account" in OldSettings:
    New["Bot Version"] = "1.0.4"
    New["Default item search language"] = OldSettings["Default item search language"]
    New["Secret Password"] = OldSettings["Password"]

    New["Account"] = {}
    New["Account"]["Email"] = OldSettings["Email"]
    New["Account"]["Password"] = OldSettings["Password"]
    New["Account"]["Sub Accounts"] = OldSettings["SubAccounts"]

    New["Control"] = {}
    New["Control"]["Give full access to"] = OldSettings["Give full access to"]
    New["Control"]["Bot owner IDs"] = OldSettings["Bot owner IDs"]

    New["Party"] = {"Cosmetics":{"Banner":{}}}
    New["Party"]["Cosmetics"]["Skin"] = OldSettings["Default skin"]
    New["Party"]["Cosmetics"]["Backpack"] = OldSettings["Default backpack"]
    New["Party"]["Cosmetics"]["Pet"] = OldSettings["Default pet"]
    New["Party"]["Cosmetics"]["Pickaxe"] = OldSettings["Default pickaxe"]
    New["Party"]["Cosmetics"]["Emote"] = OldSettings["Default emote"]
    New["Party"]["Cosmetics"]["Emoji"] = OldSettings["Default emoji"]
    New["Party"]["Cosmetics"]["Banner"]["Banner Color"] = OldSettings["Default banner color"]
    New["Party"]["Cosmetics"]["Banner"]["Banner Name"] = OldSettings["Default banner"]
    New["Party"]["Cosmetics"]["Banner"]["Season Level"] = OldSettings["Default season level"]
    New["Party"]["Privacy"] = OldSettings["Privacy"]
    New["Party"]["Platform"] = OldSettings["Platform"]
    New["Party"]["Join party on invitation"] = OldSettings["Join party on invitation"]

    New["Friends"] = {}
    New["Friends"]["Accept all friend requests"] = OldSettings["Accept all friend requests"]
    New["Friends"]["Accept incoming friend requests"] = OldSettings["Accept incoming friend request"]
    New["Friends"]["Invite friend on friend added"] = OldSettings["Invite friend on friend added"]
    New["Friends"]["Send friend request on friend removed"] = OldSettings["Send friend request on friend removed"]
    open("Settings.json","w+").write(json.dumps(New,indent=2))

ClientSettings = Config.ConfigReader(json.loads(open("Settings.json").read()))

app = Sanic('EasyFNBot')
fnClient = fortnitepy.Client(email=None,password=None)
fnClient.Clients = {}
fnClient.tasks = []
fnClient.Randomizing = False
fnClient.starting = True
fnClient.RemovingFriends = False

@fnClient.event
async def event_friend_add(friend):
    await friends.event_friend_add(fnClient, friend)
    
@fnClient.event
async def event_friend_remove(friend):
    await friends.event_friend_remove(fnClient, friend)

@fnClient.event
async def event_friend_request(friend):
    await friends.event_friend_request(fnClient, friend)

@fnClient.event
async def event_party_invite(invitation):
    await party.event_party_invite(fnClient, invitation)

@fnClient.event
async def event_party_member_join(Member):
    await party.event_party_member_join(fnClient,Member)

@fnClient.event
async def event_party_member_promote(old_leader, new_leader):
    await party.event_party_member_promote(fnClient, old_leader,new_leader)

@fnClient.event
async def event_party_message(Message):
    await message.Command(fnClient, Message)

@fnClient.event
async def event_friend_message(Message):
    await message.Command(fnClient, Message)

@app.route('/')
async def Home(req):
    return response.text('Follow @LupusLeaks on Twitter')

@app.post('/settings')
async def patch_settings(request):
    #Check for auth
    if request.headers.get('X-Secret-Password'):
        if ClientSettings.HeaderPassword:
            if not ClientSettings.HeaderPassword == request.headers.get('X-Secret-Password'):
                return response.json({"error":"Unauthorized"},status=401)
    else:
        return response.json({"error":"Bad request!"},status=400)

    try:
        NewSettings = json.loads(request.body)
    except:
        return response.json({"error":"Bad request!"},status=400)

    try:
        Settings = json.loads(open("Settings.json").read())
        for Key,Value in NewSettings.items():
            if Key in Settings:
                Settings[Key] = Value
        open("Settings.json","w+").write(json.dumps(Settings,indent=2))
    except:
        return response.json({"error":"Can't read the Settings file!"})
    
    return response.json(Settings)

@app.get('/restart')
async def refresh(request):
    #Check for auth
    Passwd = await Check.CheckPassword(ClientSettings,request)
    if isinstance(Passwd, sanic.response.HTTPResponse): return Passwd

    if not ClientSettings.Account.Email or not ClientSettings.Account.Password:
        return response.json({"error":"Email adress or password was not found!"},status=404)
    
    fnClient.email = ClientSettings.Account.Email
    fnClient.password = ClientSettings.Account.Password

    try:
        await fnClient.start()
        await fnClient.wait_until_ready()
    except fortnitepy.AuthException:
        return response.json({"error":"Wrong Epic Games Account Credentials!"})
    except:
        return response.json({"error":"Something went wrong while logging in!"})
    return response.json({"success":"Successfully restarted the fortnite client!"})

@app.get('/status')
async def status(request):
    #Check for auth
    Passwd = await Check.CheckPassword(ClientSettings,request)
    if isinstance(Passwd, sanic.response.HTTPResponse): return Passwd

    if not fnClient.is_ready():
        return response.json({"started":fnClient.is_ready()})
    else:
        if len(fnClient.Clients.values()) > 0:
            Friends = 0
            for Client in fnClient.Clients.values():
                Friends += len(Client.friends)
            SubBots = [Client.user.display_name for Client in fnClient.Clients.values()]
            return response.json({"MainBot":fnClient.user.display_name,'Friends':Friends,"Sub Bots":SubBots})
        else:
            return response.json({"started":fnClient.is_ready(),'Friends':len(fnClient.friends)})

@app.get('/update')
async def update(request):
    return await Check.Update(ClientSettings,request)

@app.get('/start')
async def start(request):
    #Check for auth

    if not ClientSettings.Account.Email or not ClientSettings.Account.Password:
        return response.json({"error":"Email adress or password was not found!"},status=404)

    if fnClient.is_ready():
        return response.json({"error":"The client is already ready!"},status=200)
    
    fnClient.email = ClientSettings.Account.Email
    fnClient.password = ClientSettings.Account.Password
    fnClient.Settings = ClientSettings
    DC = await DefaultCosmetics.Cosmetics(ClientSettings)
    fnClient.default_party_member_config = DC[0]
    fnClient.default_party_config = DC[1]

    try:
        await fnClient.start()
        await fnClient.wait_until_ready()
    except fortnitepy.AuthException:
        return response.json({"error":"Wrong Epic Games Account Credentials!"})
    except:
        return response.json({"error":"Something went wrong while logging in!"})
    
    fnClient.mainBotID = fnClient.user.id
    Errors = False

    for email,password in ClientSettings.Account.Sub_Accounts.items():
        if "@" in email:
            fnClient.tasks.append(MultipleClients.LoadAccount(fnClient,email,password))
    if len(fnClient.tasks) > 0:
        try:
            await asyncio.wait(fnClient.tasks)
        except:
            Errors = True
        
        Friends = 0
        for Client in fnClient.Clients.values():
            Friends = fnClient.has_friend(Client.user.id)
            if not Friends:
                try:
                    await fnClient.add_friend(Client.user.id)
                except:
                    pass
            if fnClient.Settings.Control.OwnerIDs:
                fnClient.Settings.Control.OwnerIDs += f',{Client.user.id}'
            else:
                fnClient.Settings.Control.FullAccessIDs += f',{Client.user.id}'
            Client.starting = False
            Friends += len(Client.friends)
        SubBots = [Client.user.display_name for Client in fnClient.Clients.values()]
        fnClient.tasks.clear()
        return response.json({"MainBot":fnClient.user.display_name,'Friends':Friends,"Sub Bots":SubBots,'Errors':Errors})
    
    if fnClient.is_ready():
        return response.json({'MainBot':fnClient.user.display_name,'Friends':len(fnClient.friends)})
    else:
        return response.json({"error":"Unknown"})

loop=asyncio.get_event_loop()
loop.create_task(app.create_server(host="127.0.0.1", port=8000, return_asyncio_server=True))
if ClientSettings.Account.Email:
    fnClient.email = ClientSettings.Account.Email
    fnClient.password = ClientSettings.Account.Password
    loop.create_task(fnClient.start())
try:
    loop.run_forever()
finally:
    loop.stop()