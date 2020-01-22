import datetime,asyncio,Config

from Fortnite import fortniteAPI

TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')

async def event_party_invite(self, invitation):
    if self.starting:
        return
    if self.Settings.Party.JoinOnInvite or (str(invitation.sender.id) in str(self.Settings.Control.FullAccessIDs)) or (str(invitation.sender.id) in str(self.Settings.Control.OwnerIDs)) or str(self.mainBotID) == str(invitation.sender.id):
        try:
            await self.user.party.me.set_emote('EID_Wave')
            await asyncio.sleep(2)
        except:
            pass
        await invitation.accept()
    else:
        try:
            await decline.accept()
        except:
            pass

async def event_party_member_promote(self, old_leader, new_leader):
    if new_leader.id == self.user.id:
        await self.user.party.send(f"Thanks {old_leader.display_name} for promoting me ♥")
        await self.user.party.me.set_emote("EID_TrueLove")

async def event_party_member_join(self, Member):
    if Member.id == self.user.id:
        if any(Oli in [member[1] for member in self.user.party.members] for Oli in Config.OlisBots): await self.user.party.me.leave()

        #Emote
        if self.Settings.Party.Cosmetics.Emote:
            Emote = await fortniteAPI.GetEmote(self.Settings.Party.Cosmetics.Emote)
            if Emote:
                await self.user.party.me.set_emote(asset=f'{str(Emote["path"]).replace("FortniteGame/Content","/Game")}.{Emote["id"]}')

        #Emoji
        if self.Settings.Party.Cosmetics.Emoji:
            Emoji = await fortniteAPI.GetEmoji(self.Settings.Party.Cosmetics.Emoji)
            if Emoji:
                await self.user.party.me.set_emote(asset=f'{str(Emoji["path"]).replace("FortniteGame/Content","/Game")}.{Emoji["id"]}')
    else:
        await self.user.party.send(f"Welcome {Member.display_name}, join my Discord: https://discord.gg/jxgZH6Z or follow me on Twitter: @LupusLeaks if you need any help or want your own bot")