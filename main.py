try:
    import fortnitepy,json,fortniteAPI,functions,MultipleClients,asyncio,os,UpdateCheck
    from functools import partial
    from termcolor import colored
    from Events import ready,friends,party,message
    from threading import Thread
    from flask import Flask
except:
    os.system("pip3 install --user -r requirements.txt")

Settings = json.loads(open("Settings.json").read())
Languages = ["ar","de","es-419","es","en","fr","it","ja","ko","pl","pt-BR","ru","tr","zh-CN","zh-Hant"]
fortniteClient = fortnitepy.Client(email=Settings["Email"],password=Settings["Password"],status="Join my Discord\nIf you want your own bot\nhttps://discord.gg/jxgZH6Z\nOr Follow me on Twitter\n@LupusLeaks")
fortniteClient.Settings = Settings
default_party_member = []
default_party = {}
fortniteClient.fnkey = Settings["fortnite-api Key"] #Set the fortnite-api.com api key

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
    default_party["Privacy"] = fortnitepy.PartyPrivacy[Settings["Privacy"].upper()]

#Cosmetics
#Backpack
if Settings["Default backpack"] and not Settings["Default pet"]:
    Backpack = fortniteAPI.SGetBackpack(NameorId=Settings["Default backpack"],matchMethod="starts",searchLanguage=fortniteClient.DefaultLang,Language=fortniteClient.DefaultLang,apikey=fortniteClient.fnkey)
    if Backpack["status"] == 200:
        v = []
        if Settings["Default backpack varaint channel name"] and Settings["Default backpack varaint name"] and Backpack["data"]["variants"]:
            VariantChannelName = Settings["Default backpack varaint channel name"].upper()
            Variant = Settings["Default backpack varaint name"].upper()
            
            for variant in Backpack["data"]["variants"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaBackpack"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=f'{str(Backpack["data"]["path"]).replace("FortniteGame/Content","/Game")}.{Backpack["data"]["id"]}',variants=v))
#Skin
if Settings["Default skin"]:
    Skin = fortniteAPI.SGetSkin(apikey=fortniteClient.fnkey,NameorId=Settings["Default skin"],matchMethod="starts",searchLanguage=fortniteClient.DefaultLang,Language=fortniteClient.DefaultLang)
    if Skin["status"] == 200:
        v = []
        if Settings["Default skin varaint channel name"] and Settings["Default skin varaint name"] and Skin["data"]["variants"]:
            VariantChannelName = Settings["Default skin varaint channel name"].upper()
            Variant = Settings["Default skin varaint name"].upper()
            
            for variant in Skin["data"]["variants"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaCharacter"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_outfit,asset=f'{str(Skin["data"]["path"]).replace("FortniteGame/Content","/Game")}.{Skin["data"]["id"]}',variants=v))
#Pickaxe
if Settings["Default pickaxe"]:
    Pickaxe = fortniteAPI.SGetPickaxe(apikey=fortniteClient.fnkey,NameorId=Settings["Default pickaxe"],matchMethod="starts",searchLanguage=fortniteClient.DefaultLang,Language=fortniteClient.DefaultLang)
    if Pickaxe["status"] == 200:
        v = []
        if Settings["Default pickaxe varaint channel name"] and Settings["Default pickaxe varaint name"] and Pickaxe["data"]["variants"]:
            VariantChannelName = Settings["Default pickaxe varaint channel name"].upper()
            Variant = Settings["Default pickaxe varaint name"].upper()
            
            for variant in Pickaxe["data"]["variants"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaPickaxe"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_pickaxe,asset=f'{str(Pickaxe["data"]["path"]).replace("FortniteGame/Content","/Game")}.{Pickaxe["data"]["id"]}',variants=v))

#Pet
if Settings["Default pet"]:
    Pet = fortniteAPI.SGetPet(apikey=fortniteClient.fnkey,NameorId=Settings["Default pet"],matchMethod="starts",searchLanguage=fortniteClient.DefaultLang,Language=fortniteClient.DefaultLang)
    if Pet["status"] == 200:
        v = []
        if Settings["Default pet varaint channel name"] and Settings["Default pet varaint name"] and Pet["data"]["variants"]:
            VariantChannelName = Settings["Default pet varaint channel name"].upper()
            Variant = Settings["Default pet varaint name"].upper()
            
            for variant in Pickaxe["data"]["variants"]:
                if variant["type"].upper() == VariantChannelName:
                    for tag in variant["options"]:
                        if tag["name"].upper() == Variant:
                            v.append(functions.create_variant(variant["channel"],tag["tag"],item="AthenaPetCarrier"))
        default_party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=f'{str(Pet["data"]["path"]).replace("FortniteGame/Content","/Game")}.{Pet["data"]["id"]}',variants=v))

fortniteClient.default_party_config = default_party
fortniteClient.default_party_member_config = default_party_member

@fortniteClient.event
async def event_ready():
    for email,password in Settings["SubAccounts"].items():
        if "@" in email:
            fortniteClient.loop.create_task(MultipleClients.LoadAccount(fortniteClient,email,password,fortniteClient.platform,fortniteClient.default_party_member_config,Settings))
    await ready.Ready(fortniteClient)

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

try:
    fortniteClient.run()
except fortnitepy.errors.AuthException:
    print(colored("Invalid account credentials!","red"))