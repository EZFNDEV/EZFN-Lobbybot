import json,fortniteAPI,functions,MultipleClients,os,UpdateCheck
from functools import partial
from Events import ready,friends,party,message
from threading import Thread

try:
    import fortnitepy,asyncio,aiofiles
    from termcolor import colored
    from flask import Flask
except:
    os.system("pip3 install --user -r requirements.txt")

Settings = json.loads(open("Settings.json").read())
Languages = ["ar","de","es-419","es","en","fr","it","ja","ko","pl","pt-BR","ru","tr","zh-CN","zh-Hant"]
fortniteClient = fortnitepy.Client(email=Settings["Email"],password=Settings["Password"],status="Join my Discord\nIf you want your own bot\nhttps://discord.gg/jxgZH6Z\nOr Follow me on Twitter\n@LupusLeaks")
fortniteClient.Settings = Settings
fortniteClient.Clients = {}
fortniteClient.RemovingFriends = False
default_party_member = []
default_party = {}

#Default language
if Settings["Default item search language"] in Languages:
    fortniteClient.DefaultLang = Settings["Default item search language"].lower()
else:
    print(f'ERROR: Couldn\'t find {Settings["DefaultItemSearchLanguage"]} as a language')
    fortniteClient.DefaultLang = "en"

#Banner
SeasonLevel=1000
if Settings["Default season level"] and type(Settings["Default season level"]) == int:
    SeasonLevel = Settings["Default season level"]
else:
    print(f'ERROR: {Settings["Default season level"]} is invaild, make sure you only use numbers')
default_party_member.append(partial(fortnitepy.ClientPartyMember.set_banner,season_level=SeasonLevel,icon=Settings["Default banner"],color=Settings["Default banner color"]))

#Platform + Privacy
if Settings["Platform"].upper() in fortnitepy.Platform.__members__:
    fortniteClient.platform = fortnitepy.Platform[Settings["Platform"].upper()]
if Settings["Privacy"].upper() in fortnitepy.PartyPrivacy.__members__:
    default_party["privacy"] = fortnitepy.PartyPrivacy[Settings["Privacy"].upper()]

#Cosmetics
#Backpack
if Settings["Default backpack"] and not Settings["Default pet"]:
    Backpack = fortniteAPI.SGetBackpack(Settings["Default backpack"],fortniteClient.DefaultLang)
    if not "status" in Backpack:
        v = []
        if Settings["Default backpack varaint channel name"] and Settings["Default backpack varaint name"] and Backpack["variants"]["en"]:
            VariantChannelName = Settings["Default backpack varaint channel name"].upper()
            Variant = Settings["Default backpack varaint name"].upper()
            
            for variant in Backpack["variants"]["en"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaBackpack"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=f'{str(Backpack["path"]).replace("FortniteGame/Content","/Game")}.{Backpack["id"]}',variants=v))
#Skin
if Settings["Default skin"]:
    Skin = fortniteAPI.SGetSkin(Settings["Default skin"],fortniteClient.DefaultLang)
    if not "status" in Skin:
        v = []
        if Settings["Default skin varaint channel name"] and Settings["Default skin varaint name"] and Skin["variants"]["en"]:
            VariantChannelName = Settings["Default skin varaint channel name"].upper()
            Variant = Settings["Default skin varaint name"].upper()
            
            for variant in Skin["variants"]["en"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaCharacter"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_outfit,asset=f'{str(Skin["path"]).replace("FortniteGame/Content","/Game")}.{Skin["id"]}',variants=v))
#Pickaxe
if Settings["Default pickaxe"]:
    Pickaxe = fortniteAPI.SGetPickaxe(Settings["Default pickaxe"],fortniteClient.DefaultLang)
    if not "status" in Pickaxe:
        v = []
        if Settings["Default pickaxe varaint channel name"] and Settings["Default pickaxe varaint name"] and Pickaxe["variants"]["en"]:
            VariantChannelName = Settings["Default pickaxe varaint channel name"].upper()
            Variant = Settings["Default pickaxe varaint name"].upper()
            
            for variant in Pickaxe["variants"]["en"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaPickaxe"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_pickaxe,asset=f'{str(Pickaxe["path"]).replace("FortniteGame/Content","/Game")}.{Pickaxe["id"]}',variants=v))

#Pet
if Settings["Default pet"]:
    Pet = fortniteAPI.SGetPet(Settings["Default pet"],fortniteClient.DefaultLang)
    if not "status" in Pet:
        v = []
        if Settings["Default pet varaint channel name"] and Settings["Default pet varaint name"] and Pet["variants"]["en"]:
            VariantChannelName = Settings["Default pet varaint channel name"].upper()
            Variant = Settings["Default pet varaint name"].upper()
            
            for variant in Pickaxe["variants"]["en"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaPetCarrier"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=f'{str(Pet["path"]).replace("FortniteGame/Content","/Game")}.{Pet["id"]}',variants=v))

fortniteClient.default_party_config = default_party
fortniteClient.default_party_member_config = default_party_member

@fortniteClient.event
async def event_ready():
    fortniteClient.starting = True
    fortniteClient.mainID = fortniteClient.user.id
    tasks = []
    for email,password in Settings["SubAccounts"].items():
        if "@" in email:
            tasks.append(MultipleClients.LoadAccount(fortniteClient,email,password))
    if len(tasks) > 0:
        print("Starting sub accounts!")
        await asyncio.wait(tasks)
    
    for Client in fortniteClient.Clients.values():
        Friends = fortniteClient.has_friend(Client.user.id)
        if not Friends:
            try:
                await fortniteClient.add_friend(Client.user.id)
            except:
                pass
        Client.starting = False

    await ready.Ready(fortniteClient)
    fortniteClient.starting = False

@fortniteClient.event
async def event_friend_add(friend):
    await friends.event_friend_add(fortniteClient, friend)
    
@fortniteClient.event
async def event_friend_remove(friend):
    await friends.event_friend_remove(fortniteClient, friend)

@fortniteClient.event
async def event_friend_request(friend):
    await friends.event_friend_request(fortniteClient, friend)

@fortniteClient.event
async def event_party_invite(invitation):
    await party.event_party_invite(fortniteClient, invitation)

@fortniteClient.event
async def event_party_member_join(Member):
    await party.event_party_member_join(fortniteClient,Member)

@fortniteClient.event
async def event_party_member_promote(old_leader, new_leader):
    await party.event_party_member_promote(fortniteClient, old_leader,new_leader)

@fortniteClient.event
async def event_party_message(Message):
    await message.Command(fortniteClient, Message)

@fortniteClient.event
async def event_friend_message(Message):
    await message.Command(fortniteClient, Message)

app = Flask(__name__)
@app.route('/')
def Home():
    return "Follow @LupusLeaks on Twitter"
Thread(target=app.run).start()
Thread(target=UpdateCheck.CheckVersion).start()
Thread(target=UpdateCheck.CheckItems).start()

try:
    fortniteClient.run()
except fortnitepy.errors.AuthException:
    print(colored("Invalid account credentials!","red"))
