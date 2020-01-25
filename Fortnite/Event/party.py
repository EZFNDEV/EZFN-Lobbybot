import datetime,asyncio,Config

from Fortnite import fortniteAPI

async def event_party_invite(self, invitation):
    if not self.Settings.Control.Public_Bot:
        if not invitation.sender.id in self.Settings.Control.FullAccessIDs:
            try:
                await invitation.decline()
            except:
                pass

    try:
        await self.user.party.me.set_emote('EID_Wave')
        await asyncio.sleep(2)
    except:
        pass
    
    await invitation.accept()

async def event_party_member_promote(self, old_leader, new_leader):
    if new_leader.id == self.user.id:
        await self.user.party.send(f"Thanks {old_leader.display_name} for promoting me ♥")
        await self.user.party.me.set_emote("EID_TrueLove")

async def event_party_member_join(self, Member):
    if Member.id == self.user.id:
        #Emote
        if self.Settings.Party.Cosmetics.Emote:
            Emote = await fortniteAPI.GetEmote(self.Settings.Party.Cosmetics.Emote,self.Settings.DefaultSearchLang)
            if Emote:
                await self.user.party.me.set_emote(asset=f'{str(Emote["path"]).replace("FortniteGame/Content","/Game")}.{Emote["id"]}')

        #Emoji
        if self.Settings.Party.Cosmetics.Emoji:
            Emoji = await fortniteAPI.GetEmoji(self.Settings.Party.Cosmetics.Emoji,self.Settings.DefaultSearchLang)
            if Emoji:
                await self.user.party.me.set_emote(asset=f'{str(Emoji["path"]).replace("FortniteGame/Content","/Game")}.{Emoji["id"]}')
    else:
        await self.user.party.send(f"Welcome {Member.display_name}, join my Discord: https://discord.gg/jxgZH6Z or follow me on Twitter: @LupusLeaks if you need any help or want your own bot")