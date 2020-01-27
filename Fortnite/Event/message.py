import os,fortnitepy,datetime,asyncio,sys,json,random

from termcolor import colored
from random import shuffle
from Fortnite.Event import SetCosmetics

async def SwitchSkins(fnClient,Skins):
    for Skin in Skins:
        await fnClient.user.party.me.set_outfit(Skin["id"])

async def Command(self, message):
    msg = message.content.upper().strip()
    args = msg.split(" ")

    HasFullAccess = False
    if not self.Settings.Control.Public_Bot:
        if not message.author.id in self.Settings.Control.FullAccessIDs:
            return
    
    if message.author.id in self.Settings.Control.FullAccessIDs:
        HasFullAccess = True
    

    if any(CosmeticCommand in msg for CosmeticCommand in ["!SKIN","!BACKPACK","!PICKAXE","!EMOJI","!EMOTE"]):
        await SetCosmetics.SetCosmeticMSG(self,message)
    elif args[0] == "!SAY" and HasFullAccess:
        try:
            await self.user.party.send(msg[5:])
            await message.reply('Message sent')
        except:
            await message.reply('Something went wrong while sending the message...')
    elif args[0] == "!MESSAGEALLBOTS" and HasFullAccess:
        for Client in self.Clients.values():
            if Client.user.id != self.user.id:
                try:
                    Friend = self.get_friend(Client.user.id)
                    if Friend:
                        await Friend.send(msg[16:])
                except:
                    pass
    elif msg == "!BOTS JOIN" and HasFullAccess:
        if self.user.id == self.mainID:
            for Client in self.Clients.values():
                Friend = self.get_friend(Client.user.id)
                if Friend:
                    await message.reply(f'Invited {Client.user.display_name}')
                    await Friend.invite()
        else:
            User = await self.fetch_profile(self.mainID,cache=False,raw=False)
            await message.reply(f"Sorry this isn't the main bot please write that to : {User.display_name}")

    elif msg == "!REMOVE ALL FRIENDS" and HasFullAccess:
        self.RemovingFriends = True
        Friends = list(self.friends.values())

        for Friend in Friends:
            if Friend.id not in self.Settings.Control.OwnerIDs or Friend.id not in self.Settings.Control.FullAccessIDs:
                try:
                    Friend.remove()
                except:
                    pass
                
        self.RemovingFriends = False
        await message.reply("Removed all friends which doesn't have full access")
    elif msg == "?FULLACCESS":
        await message.reply(f'You have full access : {str(HasFullAccess)}')
    elif args[0] == "!RANDOMIZE" and args[1] == "SKIN" and HasFullAccess:
        if self.randomizing == True: return await message.reply('Sorry, this client is already randomizing...')
        self.randomizing = True
        Skins = [Skin for Skin in json.loads(open("Items.json").read()) if Skin["type"] == "outfit"]
        shuffle(Skins) #Make it random
        await message.reply("Starting!")
        try:
            await asyncio.wait_for(SwitchSkins(self,Skins),60,loop=self.loop)
        except:
            await message.reply("Stopped randomizing")
            self.randomizing = False
    elif args[0] == "!PRIVACY" and len(args) > 1:
        if self.user.party.leader.id == self.user.id:
            if msg[9:] in fortnitepy.PartyPrivacy.__members__:
                await self.user.party.set_privacy(fortnitepy.PartyPrivacy[msg[9:]])
                await message.reply(f'Privacy set to {msg[9:].capitalize()}')
            else:
                await message.reply("Invaild Privacy, follow @LupusLeaks on Twitter or join my Discord: https://discord.gg/jxgZH6Z to get help")
        else:
            await message.reply(f"Can't set privacy to {msg[9:].capitalize()}. I am not the leader of the party.")
    elif "!BP" == args[0] and len(args) > 1:
        try:
            await self.user.party.me.set_battlepass_info(has_purchased=bool(args[1]), level=int(args[2]), self_boost_xp=int(args[3]), friend_boost_xp=int(args[4]))
            await message.reply("New Battle Pass Info set")
        except:
            await message.reply("Command : !BP <True/False> <Level> <Self XP Boost> <Friend XP Boost>")
    elif msg == "!RESTART" and HasFullAccess:
        await message.reply("Restarting...")
        await self.restart()
    elif args[0] == "!BANNER" and len(args) > 1:
        if "--LEVEL=" in msg:
            msg = msg + " "
            Level = SetCosmetics.GetValue(msg,"--LEVEL="," ")
            try:
                Level = int(Level)
            except:
                await message.reply("Sorry you can only use numbers as level")
                return
            msg = msg.replace("--LEVEL=" + str(Level), "").strip()
            await self.user.party.me.set_banner(icon=msg[8:], season_level=Level)
            await message.reply(f"Banner set to {msg[8:].capitalize()} and Level set to {Level}")
        else:
            await self.user.party.me.set_banner(icon=msg[8:])
            await message.reply(f'Banner set to {msg[8:].capitalize()}')
    elif msg == "!REMOVE":
        await message.reply('Are you sure that I should delete you as my friend? Please write "Yes delete me"')

        def isYes(message):
            return (message.author.id == message.author.id) and (message.content.upper() == "YES DELETE ME")
        
        try:
            DeleteMe = await self.wait_for('message', check=isYes, timeout=60)
            if DeleteMe:
                try:
                    await self.remove_friend(message.author.id)
                    await message.reply("Removed you as my friend")
                except fortnitepy.errors.HTTPException as Error:
                    Error2Send = Error.message
                    for message_var in Error.message_vars:
                        if self.is_id(Error.message_vars):
                            UserName = (self.fetch_profile(message_var, cache=False, raw=False)).display_name
                            Error2Send = Error2Send.replace(message_var, UserName)
                    await message.reply(Error2Send)
        except asyncio.TimeoutError:
            await message.reply("You took too long, canceled removing you as a friend ♥")
    elif "!PLATFORM" == args[0] and len(args) > 1:
        if msg[10:] in fortnitepy.Platform.__members__:
            self.platform = fortnitepy.Platform[msg[10:]]
        else:
            await message.reply("Can't find the Platform! Join this Discord for help : https://discord.gg/jxgZH6Z")
            return

        Members = [Member for Member in self.user.party.members if self.get_friend(Member)]
        partyID = self.user.party.id
        await self.user.party.me.leave()
        await message.reply(f"Successfuly changed Platform to {(str((self.platform))[9:]).lower().capitalize()}")
        try:
            await self.join_to_party(partyID, check_private=True)
        except fortnitepy.Forbidden:
            if len(Members) == 0:
                await message.reply("Can't join your party")
            else:
                for Member in Members:
                    if Member != self.user.id:
                        if self.get_friend(Member):
                            await self.get_friend(Member).join_party()
      
    elif args[0] == "!KICK" and HasFullAccess and len(args) > 1:
        UserToKick = await self.fetch_profile(msg[6:],cache=False, raw=False)
        if UserToKick is None:
            await message.reply("Can't find this Username")
            return
        if UserToKick.id == self.user.id:
            await message.reply('Can\'t kick myself. Use "!Leave Party" instead')
            return
        if UserToKick.id in self.user.party.members:
            User = self.user.party.members.get(UserToKick.id)
            try:
                await User.kick()
                await message.reply(f"Kicked {User.display_name}")
            except fortnitepy.Forbidden:
                await message.reply(f"Can't kick {User.display_name}. I am not the leader of the party.")
        else:
            await message.reply("User isn't in my party")

    elif args[0] == "!PROMOTE" and HasFullAccess:
        if msg == "!PROMOTE":
            UserToPromote = await self.fetch_profile(message.author.id,cache=False, raw=False)
        else:
            UserToPromote = await self.fetch_profile(msg[9:],cache=False, raw=False)
        if UserToPromote is None:
            await message.reply(f"Can't invite {message.content[8:]}, the user isn't my friend")
            return
        if UserToPromote.id in self.user.party.members:
            User = self.user.party.members.get(UserToPromote.id)
            try:
                await User.promote()
                await message.reply(f"Promoted {User.display_name}")
            except fortnitepy.Forbidden:
                await message.reply(f"Can't Promote {User.display_name}, I am not the party leader")
        else:
            await message.reply("User isnt in my party")

    elif args[0] == "!INVITE":
        if msg == "!INVITE":
            User = await self.fetch_profile(message.author.id, cache=True, raw=False)
        else:
            User = await self.fetch_profile(msg[8:], cache=True, raw=False)
        if User is None:
            await message.reply(f"Can't invite {message.content[8:]}, the user isn't my friend")
            return
        try:
            if User.id in self.user.party.members:
                await message.reply(f"{User.display_name} is already member of the party")
                return
            else:
                Friend = self.get_friend(User.id)
                await Friend.invite()
                await message.reply(f"Invited {Friend.display_name}")
        except fortnitepy.errors.PartyError:
            await message.reply(f"Can't invite {User.display_name}, the party is full.")

    elif "!ADD" == args[0] and len(args) > 1:
        User = await self.fetch_profile(msg[5:], cache=False, raw=False)
        if User is None:
            await message.reply(f"Can't find user {message.content[5:]}")
            return
        try:
            await self.add_friend(User.id)
            await message.reply(f"Friend request send to {User.display_name}")
        except fortnitepy.errors.HTTPException as Error:
            Error2Send = Error.message
            for message_var in Error.message_vars:
                if self.is_id(message_var):
                    UserName = (await self.fetch_profile(message_var, cache=False, raw=False)).display_name
                    Error2Send = Error2Send.replace(message_var, UserName)
            await message.reply(Error2Send)

    elif "!REMOVE" == args[0] and len(args) > 1 and HasFullAccess:
        User = await self.fetch_profile(msg[8:], cache=False, raw=False)
        if User is None:
            await message.reply("Can't find user")
            return
        if self.get_friend(User.id) is not None:
            try:
                await self.remove_friend(User.id)
                await message.reply(f"Removed {User.display_name} as my friend")
            except fortnitepy.errors.HTTPException as Error:
                Error2Send = Error.message
                for message_var in Error.message_vars:
                    if self.is_id(Error.message_vars):
                        UserName = (self.fetch_profile(message_var, cache=False, raw=False)).display_name
                        Error2Send = Error2Send.replace(message_var, UserName)
                await message.reply(Error2Send)
        else:
            await message.reply("Can't find user in my friend list")
    elif msg == "!JOIN" :
        if self.Settings.Party.JoinOnInvite or HasFullAccess:
            if self.get_friend(message.author.id):
                try:
                    await self.get_friend(message.author.id).join_party()
                except:
                    await message.reply("Can't join your Party")
            else:
                await message.reply("You aren't my friend")
        else:
            await message.reply("You are not allowed to use this command!")
    elif msg == "!LOGOUT" and HasFullAccess:
        await message.reply("Logged out")
        await self.logout()
        sys.exit()
    elif msg == "!LEAVE PARTY" and HasFullAccess:
        try:
            await self.user.party.me.set_emote('EID_Wave')
            await asyncio.sleep(2)
        except:
            pass
        await self.user.party.me.leave()
        await message.reply("Successfuly left Party.")
    elif msg == "!READY":
        await self.user.party.me.set_ready(True)
        await message.reply("Successfuly set my readiness to ready")

    elif msg == "!NOT READY":
        await self.user.party.me.set_ready(False)
        await message.reply("Successfuly set my readiness to not ready")
        
    elif msg == "!STOP EMOTE":
        await self.user.party.me.set_emote("EID_InvaildEmoteToStopDancing")
        await message.reply("Stopped Dancing!")

    elif msg == "!NO SKIN":
        await self.user.party.me.set_outfit("CID_InvaildOutfit")
        await message.reply("I am now invisible")
    elif msg == "?FRIENDS":
        Friend_count = len(self.friends.items())
        if Friend_count == 0:
            await message.reply("I dont have Friends")
        elif Friend_count == 1:
            await message.reply("I have one Friend")
        elif Friend_count > 1:
            await message.reply(f"I have {str(Friend_count)} friends")
    elif msg == "?BLOCKED":
        Blocked_count = len(await self.fetch_blocklist())
        if Blocked_count == 0:
            await message.reply("I dont have Blocked anyone")
        elif Blocked_count == 1:
            await message.reply("I have blocked one user")
        elif Blocked_count > 1:
            await message.reply(f"I have blocked {str(Blocked_count)} users")
    elif msg == "?BANNER":
        await message.reply(f"Current Banner Name : {str(self.user.party.me.banner[0]).capitalize()}")
    elif args[0] == "?ID":
        if msg == "?ID":
            await message.reply(f"Your ID is : {message.author.id}")
        elif len(args) > 1:
            User = await self.fetch_profile(msg[4:],cache=False,raw=False)
            if User:
                await message.reply(f"ID : {User.id}")
            else:
                await message.reply("Can't find this User")
    elif msg == "?PARTY LEADER":
        PartyLeaderName = str(self.user.party.leader.display_name)
        await message.reply(f"Current Party Leader : {PartyLeaderName}")

    elif msg == "?JOINED":
        delta_time = datetime.datetime.utcnow() - self.user.party.me.joined_at
        Time = datetime.timedelta(seconds=delta_time.seconds)
        await message.reply(f"Joined {Time} ago")

    elif msg == "?PARTY":
        PartyLeader = str(self.user.party.leader.display_name)
        Members = str(self.user.party.member_count)
        PlayList = self.user.party.playlist_info[0]
        Privacy = str(self.user.party.privacy)[13:]
        Fill = str(self.user.party.squad_fill)
        await message.reply(f"Party leader : {PartyLeader} \n Members : {Members} \n Playlist : {PlayList} \n Privacy : {Privacy} \n Fill : {Fill}")
    elif msg == "?PICKAXE":
        await self.user.party.me.set_emote("EID_IceKing")

    elif msg == "!PURPLESKULL":
        await self.user.party.me.set_outfit("CID_030_Athena_Commando_M_Halloween",variants=self.user.party.me.create_variants(clothing_color=1))
        await message.reply('Skin set to Skull Trooper with Purple Glow variant!')

    elif msg == "!PINKGHOUL":
        await self.user.party.me.set_outfit("CID_029_Athena_Commando_F_Halloween",variants=self.user.party.me.create_variants(material=3))
        await message.reply('Skin set to Ghoul Trooper with Pink variant!')

    elif msg == "!MINTYELF":
        await self.user.party.me.set_outfit("CID_051_Athena_Commando_M_HolidayElf",variants=self.user.party.me.create_variants(material=2))
        await message.reply('Skin set to Elf with Minty variant!')

    
    