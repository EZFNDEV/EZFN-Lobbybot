import fortnitepy,fortniteAPI

async def SetCosmeticMSG(self,message):
    msg = message.content.upper().strip()
    args = msg.split(" ")

    Lang = self.DefaultLang
    if "--LANG=" in msg:
        msg = msg + " "
        Lang = GetValue(msg,"--LANG="," ")
        msg = msg.replace("--LANG=" + Lang, "").strip()
        Lang = Lang.lower()

    if args[0] == "!SKIN":
        Item = GetName("!SKIN",msg)
        Item = await fortniteAPI.GetSkin(Item,Lang)
    elif args[0] == "!BACKPACK":
        Item = GetName("!BACKPACK",msg)
        Item = await fortniteAPI.GetBackpack(Item,Lang)
    elif args[0] == "!PICKAXE":
        Item = GetName("!PICKAXE",msg)
        Item = await fortniteAPI.GetPickaxe(Item,Lang)
    elif args[0] == "!EMOJI":
        Item = GetName("!EMOJI",msg)
        Item = await fortniteAPI.GetEmoji(Item,Lang)
    elif args[0] == "!EMOTE":
        Item = GetName("!EMOTE",msg)
        Item = await fortniteAPI.GetEmote(Item,Lang)
           
    if "status" in Item:
        await message.reply("Can't find this item")
        return
    else:
        v = []
        if msg.count("--") != 0:
            if Item["variants"][Lang]: #Make sure that the item has variants
                for Variant in GetValues(msg):
                    VariantChannelName = (Variant.split("=")[0])[2:]
                    Variant = Variant.split("=")[1]
                        
                    for variant in Item["variants"][Lang]:
                        if variant["type"].upper() == VariantChannelName:
                            for tag in variant["options"]:
                                if tag["name"].upper() == Variant:
                                    v.append(create_variant(variant["channel"],tag["tag"],item=Item["backendType"]))
            else: #The item has no variants
                await message.reply("Can't find any variants for this item")
            
        asset=f'{str(Item["path"]).replace("FortniteGame/Content","/Game")}.{Item["id"]}'
        if args[0] == "!SKIN":
            await self.user.party.me.set_outfit(asset=asset,variants=v)
        elif args[0] == "!BACKPACK":
            await self.user.party.me.set_backpack(asset=asset,variants=v)
        elif args[0] == "!PICKAXE":
            await self.user.party.me.set_pickaxe(asset=asset,variants=v)
        elif args[0] == "!EMOJI":
            await self.user.party.me.set_emote(asset=asset)
        elif args[0] == "!EMOTE":
            await self.user.party.me.set_emote(asset=asset)

        await message.reply(f'{Item["type"].capitalize()} set to {Item["Names"][Lang]}')

def GetName(Name,Message):
    if Message.count("--") != 0:
        Item = GetValue(Message,f'{Name} ',"--")
    else:
        Item = Message[(len(Name) + 1):]

    return Item.strip()

def create_variant(VariantChannelName,Variant,item="AthenaCharacter"):
    return {'item': item,'channel': VariantChannelName,'variant': Variant}

def GetValue(fullLine,startWith,endWith):
    startIndex = fullLine.index(startWith) + len(startWith)
    endIndex = fullLine[startIndex:].index(endWith) + startIndex
    return fullLine[startIndex:endIndex]

def GetValues(fullLine):
    Variants = []
    for Variant in range(0,fullLine.count("--")):
        try:
            startIndex = fullLine.index("--")
            ValueStartIndex = fullLine[startIndex:].index("=") + startIndex + 1
        
            try:
                endIndex = fullLine[ValueStartIndex:].index("--") + ValueStartIndex
            except:
                endIndex = len(fullLine)
            Variants.append(fullLine[startIndex:endIndex])
            fullLine = fullLine.replace(fullLine[startIndex:endIndex],"")
        except:
            return None
    return Variants