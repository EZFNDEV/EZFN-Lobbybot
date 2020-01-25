

async def event_friend_add(self, Friend):
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
            return

    try:
        await Friend.accept()
    except:
        pass