

async def event_friend_add(self, Friend):
    if self.mainID == Friend.id:
        return
    try:
        await Friend.send(f'If you want your own bot follow @LupusLeaks on Twitter or join this discord: https://discord.gg/jxgZH6Z')
    except:
        pass
    
    if not self.Settings.Control.Public_Bot:
        if not Friend.id in self.Settings.Control.FullAccessIDs:
            return
    
    try:
        await Friend.invite()
    except:
        pass

async def event_friend_remove(self, Friend):
    if self.RemovingFriends:
        return

    if not self.Settings.Control.Public_Bot:
        if not Friend.id in self.Settings.Control.FullAccessIDs:
            return

    try:
        await self.add_friend(Friend.id)
    except:
        pass

async def event_friend_request(self, Friend):
    if not self.Settings.Control.Public_Bot:
        if not Friend.id in self.Settings.Control.FullAccessIDs:
            try:
                await Friend.decline()
            except:
                pass

    try:
        await Friend.accept()
    except:
        pass