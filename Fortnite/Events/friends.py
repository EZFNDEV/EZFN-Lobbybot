import datetime,fortnitepy

from termcolor import colored
TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')

async def event_friend_add(self, Friend):
    if self.Settings.Friends.InviteOnAdd or str(Friend.id) in str(self.Settings.Control.OwnerIDs) or str(Friend.id) in str(self.Settings.Control.FullAccessIDs):
        try:
            await Friend.invite()
        except:
            pass

async def event_friend_remove(self, Friend):
    if self.RemovingFriends:
        return
    if self.Settings.Friends.SendOnRemove or str(Friend.id) in str(self.Settings.Control.OwnerIDs) or str(Friend.id) in str(self.Settings.Control.FullAccessIDs):
        try:
            await self.add_friend(Friend.id)
        except:
            pass

async def event_friend_request(self, Friend):
    if self.Settings.Friends.AcceptIncoming or str(Friend.id) in str(self.Settings.Control.OwnerIDs) or str(Friend.id) in str(self.Settings.Control.FullAccessIDs) or str(Friend.id) == str(self.mainBotID):
        await Friend.accept()
    else:
        await Friend.decline()