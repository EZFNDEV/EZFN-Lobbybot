import datetime,fortnitepy

from termcolor import colored
TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')

async def event_friend_add(self, Friend):
    TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')
    print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} is now your friend', "green"))
    if self.Settings["Invite friend on friend added"] or Friend.id in self.Settings["Give full access to"]:
        try:
            await Friend.invite()
            print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] Invited {Friend.display_name}', "green"))
        except fortnitepy.errors.PartyError:
            await Friend.send("Can't invite you, the party is full")
        await Friend.send("Thanks for adding my bot, if you want to make your own bot or need any help follow @LupusLeaks on Twitter on join my Discord https://discord.gg/jxgZH6Z")

async def event_friend_remove(self, Friend):
    if self.RemovingFriends:
        return
    if self.Settings["Send friend request on friend removed"] or Friend.id in self.Settings["Give full access to"]:
        try:
            await self.add_friend(Friend.id)
            print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} removed you as a friend, bot sent him a friend request', "green"))
        except fortnitepy.errors.HTTPException as Error:
            print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} removed you as a friend', "red"))
    else:
        print(colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} removed you as a friend', "red"))

async def event_friend_request(self, Friend):
    if self.Settings["Accept incoming friend request"] or Friend.id in self.Settings["Give full access to"] or Friend.id == self.mainID:
        await Friend.accept()
