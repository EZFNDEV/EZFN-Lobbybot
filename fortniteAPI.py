import aiohttp,requests
FNAPI = "https://fortnite-api.com"

def SetItem(self,Item):
    self.id = Item["id"]
    self.type = Item["type"]
    self.backendType = Item["backendType"]
    self.rarity = Item["rarity"]
    self.backendRarity = Item["backendRarity"]
    self.name = Item["name"]
    self.shortDescription = Item["shortDescription"]
    self.description = Item["description"]
    self.set = Item["set"]
    self.series = Item["series"]
    self.backendSeries = Item["backendSeries"]
    self.images = Item["images"]
    self.variants = Item["variants"]
    self.gameplayTags = Item["gameplayTags"]
    self.displayAssetPath = Item["displayAssetPath"]
    self.definition = Item["definition"]
    self.builtInEmoteId = Item["builtInEmoteId"]
    self.requiredItemId = Item["requiredItemId"]
    self.path = Item["path"]
    self.lastUpdate = Item["lastUpdate"]
    self.added = Item["added"]

async def getCosmetic(params,apikey):
    async with aiohttp.ClientSession() as session:
        NameID = params["NameorId"]
        del params["NameorId"]
        params["id"] = NameID
        Cosmetics = await (await session.get(f"{FNAPI}/cosmetics/br/search/ids", params=params, headers={"x-api-key" : apikey})).json()
        if Cosmetics["status"] != 200:
            del params["id"]
            params["name"] = NameID
            Cosmetics = await (await session.get(f"{FNAPI}/cosmetics/br/search", params=params, headers={"x-api-key" : apikey})).json()

        return Cosmetics

def SgetCosmetic(params,apikey):
    NameID = params["NameorId"]
    del params["NameorId"]
    params["id"] = NameID
    Cosmetics = (requests.get(f"{FNAPI}/cosmetics/br/search/ids",params=params,headers={"x-api-key" : apikey})).json()
    if Cosmetics["status"] != 200:
        del params["id"]
        params["name"] = NameID
        Cosmetics = (requests.get(f"{FNAPI}/cosmetics/br/search", params=params, headers={"x-api-key" : apikey})).json()
    return Cosmetics

async def GetSkin(apikey,**kwargs):
    params = {"backendType" : "AthenaCharacter"}
    for key, value in kwargs.items():
        params[key] = value

    return (await getCosmetic(params,apikey))

async def GetBackpack(apikey,**kwargs):
    params = {"backendType" : "AthenaBackpack"}
    for key, value in kwargs.items():
        params[key] = value

    return (await getCosmetic(params,apikey))

async def GetPickaxe(apikey,**kwargs):
    params = {"backendType" : "AthenaPickaxe"}
    for key, value in kwargs.items():
        params[key] = value

    return (await getCosmetic(params,apikey))

async def GetEmote(apikey,**kwargs):
    params = {"backendType" : "AthenaDance"}
    for key, value in kwargs.items():
        params[key] = value

    return (await getCosmetic(params,apikey))

async def GetEmoji(apikey,**kwargs):
    params = {"backendType" : "AthenaEmoji"}
    for key, value in kwargs.items():
        params[key] = value

    return (await getCosmetic(params,apikey))

async def GetPet(apikey,**kwargs):
    params = {"backendType" : "AthenaPetCarrier"}
    for key, value in kwargs.items():
        params[key] = value



def SGetSkin(apikey,**kwargs):
    params = {"backendType" : "AthenaCharacter"}
    for key, value in kwargs.items():
        params[key] = value

    return SgetCosmetic(params,apikey)

def SGetBackpack(apikey,**kwargs):
    params = {"backendType" : "AthenaBackpack"}
    for key, value in kwargs.items():
        params[key] = value

    return SgetCosmetic(params,apikey)

def SGetPickaxe(apikey,**kwargs):
    params = {"backendType" : "AthenaPickaxe"}
    for key, value in kwargs.items():
        params[key] = value

    return SgetCosmetic(params,apikey)

def SGetPet(apikey,**kwargs):
    params = {"backendType" : "AthenaPetCarrier"}
    for key, value in kwargs.items():
        params[key] = value

    return SgetCosmetic(params,apikey)