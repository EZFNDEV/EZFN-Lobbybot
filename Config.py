Languages = ["ar","de","es-419","es","en","fr","it","ja","ko","pl","pt-BR","ru","tr","zh-CN","zh-Hant"]
Status = "Join my Discord\nIf you want your own bot\nhttps://discord.gg/jxgZH6Z\nOr Follow me on Twitter\n@LupusLeaks"

class ConfigReader():
    def __init__(self,Settings):
        class Account():
            Email = Settings["Account"]["Email"]
            Password = Settings["Account"]["Password"]
            Sub_Accounts = Settings["Account"]["Sub Accounts"]
        class Control():
            FullAccessIDs = Settings["Control"]["Give full access to"]
            Public_Bot = Settings["Control"]["Public Bot"]
        class Party():
            JoinOnInvite = Settings["Party"]["Join party on invitation"]
            Platfrom = Settings["Party"]["Platform"]
            Privacy = Settings["Party"]["Privacy"]
            class Cosmetics():
                Skin = Settings["Party"]["Cosmetics"]["Skin"]
                #Skin_Variants = Settings["Party"]["Cosmetics"]["Skin Variants"]
                Backpack = Settings["Party"]["Cosmetics"]["Backpack"]
                #Backpack_Variants = Settings["Party"]["Cosmetics"]["Backpack Variants"]
                Pet = Settings["Party"]["Cosmetics"]["Pet"]
                #Pet_Variants = Settings["Party"]["Cosmetics"]["Pet Variants"]
                Pickaxe = Settings["Party"]["Cosmetics"]["Pickaxe"]
                Emote = Settings["Party"]["Cosmetics"]["Emote"]
                Emoji = Settings["Party"]["Cosmetics"]["Emoji"]
                class Banner():
                    Color = Settings["Party"]["Cosmetics"]["Banner"]["Banner Color"]
                    Level = Settings["Party"]["Cosmetics"]["Banner"]["Season Level"]
                    Name = Settings["Party"]["Cosmetics"]["Banner"]["Banner Name"]
                Banner = Banner()
            Cosmetics = Cosmetics()
        class Friends():
            AcceptAllR = Settings["Friends"]["Accept all friend requests"]
            #RemoveAllR = Settings["Friends"]["Remove all friend requests"]
            AcceptIncoming = Settings["Friends"]["Accept incoming friend requests"]
            #RemoveIncoming = Settings["Friends"]["Remove incoming friend requests"]
            InviteOnAdd = Settings["Friends"]["Invite friend on friend added"]
            SendOnRemove = Settings["Friends"]["Send friend request on friend removed"]

        self.Bot_Version = Settings["Bot Version"]
        self.DefaultSearchLang = Settings["Default item search language"]
        self.HeaderPassword = Settings["Secret Password"]
        self.Control = Control()
        self.Party = Party()
        self.Friends = Friends()
        self.Account = Account()