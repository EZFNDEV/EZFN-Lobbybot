import datetime,asyncio,fortniteAPI

from termcolor import colored
TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')

async def event_party_invite(self, invitation):
    if (self.Settings["Join party on invitation"]) or (invitation.sender.id in self.Settings["Give full access to"]):
        await self.user.party.me.set_emote('EID_Wave')
        await asyncio.sleep(2)
        await invitation.accept()

async def event_party_member_promote(self, old_leader, new_leader):
    if new_leader.id == self.user.id:
        await self.user.party.send(f"Thanks {old_leader.display_name} for promoting me ♥")
        await self.user.party.me.set_emote("EID_TrueLove")

async def event_party_member_join(self, Member):
    if Member.id == self.user.id:
        if (self.user.party.leader.id == Member.id) and self.user.party.member_count == 1:
            print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] Created Party', "green"))
        else:
            print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] Joined Party', "green"))
            
        #Emote
        if self.Settings["Default emote"]:
            Emote = await fortniteAPI.GetEmote(NameorId=self.Settings["Default emote"],matchMethod="starts",searchLanguage="en",Language="en")
            if Emote.status == 200:
                await self.user.party.me.set_emote(Emote.id)

        #Emoji
        if self.Settings["Default emoji"]:
            Emoji = await fortniteAPI.GetEmoji(NameorId=self.Settings["Default emoji"],matchMethod="starts",searchLanguage="en",Language="en")
            if Emoji.status == 200:
                await self.user.party.me.set_emote(asset=f'{str(Emoji.path).replace("FortniteGame/Content","/Game")}.{Emoji.id}')
    else:
        print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Member.display_name} Joined the Party', "green"))
        await self.user.party.send(f"Welcome {Member.display_name}, join my Discord: https://discord.gg/jxgZH6Z or follow me on Twitter: @LupusLeaks if you need any help or want your own bot")