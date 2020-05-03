import Config
import fortnitepy

from Fortnite import fortniteAPI
from functools import partial

async def Cosmetics(Settings):
    default_party_member = []
    default_party = {}

    #Default language
    if not Settings.DefaultSearchLang.lower() in Config.Languages:
        print(f'ERROR: Couldn\'t find {Settings.DefaultSearchLang.lower()} as a language')
        Settings.DefaultSearchLang = "en"

    #Banner
    if not type(Settings.Party.Cosmetics.Banner.Level) == int:
        print(f'ERROR: {Settings.Party.Cosmetics.Banner.Level} is invaild, make sure you only use numbers')
        Settings.Party.Cosmetics.Banner.Level = 1000

    if not Settings.Party.Privacy.upper() in fortnitepy.PartyPrivacy.__members__:
        Settings.Party.Privacy = "PUBLIC"

    if not Settings.Party.Platfrom in fortnitepy.Platform.__members__:
        Settings.Party.Platfrom = "Windows"

    default_party["privacy"] = fortnitepy.PartyPrivacy[Settings.Party.Privacy.upper()]
    default_party_member.append(partial(fortnitepy.ClientPartyMember.set_banner,season_level=Settings.Party.Cosmetics.Banner.Level,icon=Settings.Party.Cosmetics.Banner.Name,color=Settings.Party.Cosmetics.Banner.Color))

    #Cosmetics
    #Backpack
    if Settings.Party.Cosmetics.Backpack and not Settings.Party.Cosmetics.Pet:
        Backpack = await fortniteAPI.GetBackpack(Settings.Party.Cosmetics.Backpack,Settings.DefaultSearchLang)
        if Backpack:
            v = Settings.Party.Cosmetics.Backpack_Variants
            default_party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=f'{str(Backpack["path"]).replace("FortniteGame/Content","/Game")}.{Backpack["id"]}',variants=v))

    #Skin
    if Settings.Party.Cosmetics.Skin:
        Skin = await fortniteAPI.GetSkin(Settings.Party.Cosmetics.Skin,Settings.DefaultSearchLang)
        if Skin:
            v = Settings.Party.Cosmetics.Skin_Variants
        
            default_party_member.append(partial(fortnitepy.ClientPartyMember.set_outfit,asset=f'{str(Skin["path"]).replace("FortniteGame/Content","/Game")}.{Skin["id"]}',variants=v))

    #Pickaxe
    if Settings.Party.Cosmetics.Pickaxe:
        Pickaxe = await fortniteAPI.GetPickaxe(Settings.Party.Cosmetics.Pickaxe,Settings.DefaultSearchLang)
        if Pickaxe:
            default_party_member.append(partial(fortnitepy.ClientPartyMember.set_pickaxe,asset=f'{str(Pickaxe["path"]).replace("FortniteGame/Content","/Game")}.{Pickaxe["id"]}'))

    #Pet
    if Settings.Party.Cosmetics.Pet:
        Pet = await fortniteAPI.GetPet(Settings.Party.Cosmetics.Pet,Settings.DefaultSearchLang)
        if Pet:
            v = Settings.Party.Cosmetics.Pet_Variants
        
            default_party_member.append(partial(fortnitepy.ClientPartyMember.set_backpack,asset=f'{str(Pet["path"]).replace("FortniteGame/Content","/Game")}.{Pet["id"]}',variants=v))

    return default_party_member,default_party
