import fortnitepy,json,functions

from Events import ready,friends,party,message

async def LoadAccount(fortniteClient,Email,Password,Platform,default_party_member_config,Settings):
    client = fortnitepy.Client(email=Email,password=Password,platform=Platform,default_party_member_config=default_party_member_config,status="Join my Discord\nIf you want your own bot\nhttps://discord.gg/jxgZH6Z\nOr Follow me on Twitter\n@LupusLeaks")
    client.Settings = Settings
    client.fnkey = fortniteClient.fnkey

    @client.event
    async def event_ready():
        await ready.Ready(client)

    @client.event
    async def event_friend_add(friend):
        await friends.event_friend_add(client, friend)

    @client.event
    async def event_friend_remove(friend):
        await friends.event_friend_remove(client, friend)

    @client.event
    async def event_friend_request(friend):
        await friends.event_friend_request(client, friend)

    @client.event
    async def event_party_invite(invitation):
        await party.event_party_invite(client, invitation)

    @client.event
    async def event_party_member_promote(old_leader, new_leader):
        await party.event_party_member_promote(client, old_leader,new_leader)

    @client.event
    async def event_friend_message(Message):
        await message.Command(client, Message)

    @client.event
    async def event_party_message(Message):
        await message.Command(client, Message)

    await client.start()
    await client.wait_until_ready()