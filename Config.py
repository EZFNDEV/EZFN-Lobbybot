Languages = ["ar","de","es-419","es","en","fr","it","ja","ko","pl","pt-BR","ru","tr","zh-CN","zh-Hant"]
Status = "Join my Discord\nIf you want your own bot\nhttps://discord.gg/jxgZH6Z\nOr Follow me on Twitter\n@LupusLeaks"
OlisBots = ["ed62aeef963d4fcdb6d732527ae13be7","773f993a56a34b66bb859c8f6814364e","b2222e370ca34a88ad8a45b6a54a7227","06c382dde8dc460c8eeb0e58371f29f6","748ad338f76546b18f510928ea733e61","bc1f8c66865845de8ebbe33b2f0ad1a6","c1b4b01549ac45da82cc4d6e38a33171","7c6e52153961420597d2e5954c1b7ef9"]

class ConfigReader():
    def __init__(self,Settings):
        class Account():
            Email = Settings["Account"]["Email"]
            Password = Settings["Account"]["Password"]
            Sub_Accounts = Settings["Account"]["Sub Accounts"]
        class Control():
            FullAccessIDs = Settings["Control"]["Give full access to"]
            OwnerIDs = Settings["Control"]["Bot owner IDs"]
        class Party():
            JoinOnInvite = Settings["Party"]["Join party on invitation"]
            Platfrom = Settings["Party"]["Platform"]
            Privacy = Settings["Party"]["Privacy"]
            class Cosmetics():
                Skin = Settings["Party"]["Cosmetics"]["Skin"]
                #Skin_Variants = Settings["Party"]["Cosmetics"]["Skin Variants"]
                Backpack = Settings["Party"]["Cosmetics"]["Skin"]
                #Backpack_Variants = Settings["Party"]["Cosmetics"]["Backpack Variants"]
                Pet = Settings["Party"]["Cosmetics"]["Skin"]
                #Pet_Variants = Settings["Party"]["Cosmetics"]["Pet Variants"]
                Pickaxe = Settings["Party"]["Cosmetics"]["Skin"]
                Emote = Settings["Party"]["Cosmetics"]["Skin"]
                Emoji = Settings["Party"]["Cosmetics"]["Skin"]
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