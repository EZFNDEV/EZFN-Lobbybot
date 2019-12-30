import fortnitepy

from threading import Thread
from termcolor import colored
from flask import Flask

async def Ready(self):
    if self.Settings["Accept all friend requests"]:
        Friends = [Friend for Friend in self.friends.items() if Friend[1].direction.upper() == "INBOUND"]
        
        for Friend in Friends:
            try:
                await Friend[1].accept()
                print(f"Accepted {Friend[1].display_name}'s friend request")
            except:
                pass
    FriendsOnline = len([Friend for Friend in self.friends.items() if Friend[1].is_online])
    Inbound = len([Friend for Friend in self.pending_friends.items() if Friend[1].direction.upper() == "OUTGOING" or "OUTBOUND"])
    Outgoing = len([Friend for Friend in self.pending_friends.items() if not Friend[1].direction.upper() == "OUTGOING" or "OUTBOUND"])

    print('----------------')
    print(colored(f"{self.user.display_name} is now online !", "green"))
    print(f"Platform : {(str((self.platform))[9:]).lower().capitalize()}")
    print(f"Bots UserName : {self.user.display_name}")
    print(f"Bots UserID : {self.user.id}")
    try:
        print(f"Blocked Users : {str(len(await self.get_blocklist()))}") #This isn't working atm...
    except:
        pass
    print(f'You have {len(self.friends.items())} friends')
    print(f"Friends Online : {FriendsOnline}")
    print(f"Pending Friends Incoming : {Inbound}")
    print(f"Pending Friends Outgoing : {Outgoing}")
    print('----------------')
