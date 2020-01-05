# EasyFNBot

## Introduction

> With EasyFNBot you can easily create you own Fortnite Lobby Bot in less then 5 minutes which will be online forever!

## Installation

Please read everything before you start with this!

[Video Tutorial](https://www.youtube.com/watch?v=7mesWioqolM)

You need an api-key to use the commands which changes the cosmetics of the bot,
just go to https://fortnite-api.com/profile and register with your discord account (it is completly free!) then copy the key

> 1. Join [our](https://discord.gg/jxgZH6Z) Discord Server
> 2. If you want to get the epic id of a user write ?id <UserName> in [bot-commands](https://discordapp.com/channels/629295115751522305/651093620753170432) (Can be used for "Give full access to" or "Bot owner IDs")
> 3. Remix [this](https://glitch.com/edit/#!/easyfnbot) project (Make sure to have an account with Glitch so you'll be able to use the bot in the future)
> 2. Click on your project name (top left) and make it PRIVATE!
> 3. Open "Settings.json" and modify it as you want
> 4. Click on Tools -> Logs -> Console and type "refresh" wait until your Bot started!
> 6. Then go to [bot-commands](https://discordapp.com/channels/629295115751522305/651093620753170432) and type your +Glitch_Project_URL, for example: +https://glitch.com/edit/#!/easyfnbot?path=Readme.md

## Features
- 24/7 Online
- Bot owner is setable
- Auto updating
- ABSOLUTELY FREE

## Settings
```
{
    "Bot Version": "1.0.0",
    "fortnite-api Key": "x-api-key",
    "Email": "YOUR_EMAIL", 
    "Password": "YOUR_PASSWORD",
    "SubAccounts" : {
        "YOUR_EMAIL" : "YOUR_PASSWORD", #If you want multiple bots
        "YOUR_EMAIL2" : "YOUR_PASSWORD2" #You can put as much emails as you want here
    },
    "Give full access to": "", #The Account IDs you want give full access to, split multiple with "," to get the acount ids write ?id AccountName in the bot-commands channel on discord
    "Bot owner IDs": "", #None else as users with the Account IDs here can use the bot!
    "Join party on invitation": true, #If false, the bot won't join others on invitation

    "Platform": "Playstation", #The Platform the bot should be on (Windows,Mac,Playstation,xBox,Switch,iOS,Android)
    "Privacy": "Public", #The bots privacy (Public,Friends_allow_friends_of_friends,Friends,Private_allow_friends_of_friends,Private)

    "Default season level": 1000, #The season level the bot should be on
    "Default banner": "OtherBanner28", #The banner the bot will use if he joins a party
    "Default banner color" : "defaultcolor15", #The banner color the bot will use if he joins a party

    "Default skin": "Ghoul Trooper",  #The Default Skin the bot will wear if he joins a party
    "Default skin varaint channel name" : "Style", #If the Skin has variants you can put the variant channel name in here (example for Ghoul Trooper : Style)
    "Default skin varaint name": "Pink", #If the Skin has variants you can put the variant name in here (example for Ghoul Trooper : Pink)

    "Default backpack": "",
    "Default backpack varaint channel name" : "",
    "Default backpack varaint name": "",

    "Default pet" : "",
    "Default pet varaint channel name" : "",
    "Default pet varaint name" : "",

    "Default pickaxe" : "",
    "Default pickaxe varaint channel name" : "",
    "Default pickaxe varaint name" : "",

    "Default emote": "True Heart", #The bot will use this emote after he joins a party
    "Default emoji" : "", #The bot will use this emoji after he joins a party

    "Accept all friend requests": true, #If true the bot will accept all friend requests
    "Accept incoming friend request": true, #If true the bot will accept all INCOMING friend requests
    "Invite friend on friend added": true, #If true the bot will invite users which just got added as friends
    "Send friend request on friend removed": true, #If true the bot will send a new friend request to the user who remove the bot as a friend

    "Thanks on promote": true, #If true the bot will thank in the chat
    "Default item search language" : "en" #The default language the bot uses to search items
}
```
## Commands
> Notice:  
> "*" means that it is optional  
> You can find everything you need to set variants if you type ?skin <Skin Name> in my Discord [bot-commands](https://discordapp.com/channels/629295115751522305/651093620753170432)  
### Give full access only  
> !Remove all friends  
> All friends which doesn't have Full Access will be removed

> !Bots join  
> If you are running multiple bots, this will invite all bots into your lobby if its public and you write to the main account  
  
> !Fix Lobby  
> The game won't crash anymore if you wrote !Crash Lobby before  
  
> !Logout  
> Logs the bot out  
  
> !Restart  
> The bot will restart  
  
> !leave party  
> The bot will leave his party  
  
> !remove <username>  
> Example: !remove Ninja  
> The bot will remove the user as a friend
  
> !join  
> The bot will try to join your party
### Party  
> `!privacy <Privacy>`  
> Example: !privacy public  
> Extra : Party Owner permission is needed  
> Changes the privacy of the party  
  
> `!Banner <BannerName> *--level=<Level(must be numbers)>` 
> Example: !Banner OtherBanner28 --level=1000  
> Changes the banner of the bot  

> `!bp <True/False> <Level> <Self XP Boost> <Friend XP Boost>`  
> Example: !bp True 1000 1000 1000  
> Changes the battlepass info of the bot  

> `!platform <Platform Name>` 
> Example !platform Playstation  
> Changes the platform the bot is on, the bot need to leave the party but will try to rejoin  

> `!kick <partymember name>`
> Example: !kick Ninja  
> Extra : Party Owner permission is needed  
> Kicks the partymember out of the party  
  
> `!promote <partymember name>`  
> Example: !promote Ninja  
> Extra : Party Owner permission is needed  
> Promotes the partymember  
  
> `!invite <partymember name>` 
> Example: !invite Ninja  
> Invites the user  
  
> !ready  
> The bot will ready up  
  
> !not ready  
> The bot will unready  
  
> !stop emote  
> The bot will stop emoting  
  
> !no skin  
> The bot will be invisible  
  
> ?Pickaxe  
> The bot will play the Ice King emote  
  
> ?Banner  
> The bot will send the current banner name  
  
> ?party leader  
> The bot will write the current party leader's name into the chat  
  
> ?joined  
> The bot will write for how long he is in the party  
  
> ?party  
> The bot will write some info about the party in the chat
#### Cosmetics  
> !purpleskull  
> The bot will set the skin to Skull Trooper with Purple Glow variant  
  
> !pinkghoul  
> The bot will set the skin to Ghoul Trooper with Pink variant  
  
> !mintyelf  
> The bot will set the skin to Elf with Minty variant  
  
> You can change the equipped cosmetics with the following commands :  
>  
> `!emote <Emote Name> *--lang=<Language Code>`  
> `!emoji <Emoji Name> *--lang=<Language Code>` 
>  
> Example: !emote Der Wurm --lang=de  
> Example: !emote floss
##### Variants possible  
> `!skin <Skin Name> *--lang=<Language Code> *--<variant channel name>=<variant name>`  
> `!pickaxe <Pickaxe Name> *--lang=<Language Code> *--<variant channel name>=<variant name>`  
> `!backpack <Backpack Name> *--lang=<Language Code> *--<variant channel name>=<variant name>`  
  
> Example: !skin Skull Trooper --Style=Purple Glow
# Friends 
> `!add <Username>`
> Example: !add Ninja  
> The bot will send a friend request to the user  
  
> !remove  
> The bot will remove you as a friend  
  
> ?friends  
> The bot will write in the chat how many friends he has  
  
> ?blocked  
> The bot will write in the chat how many users he blocked  
