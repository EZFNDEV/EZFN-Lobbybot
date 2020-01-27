import fortnitepy,json,Config

from Fortnite.Event import friends,party,message

async def LoadAccount(fnClient,Email,Password):
    client = fortnitepy.Client(email=Email,password=Password,platform=fnClient.platform,default_party_member_config=fnClient.default_party_member_config,status='Discord: https://discord.gg/jxgZH6Z\nTwitter: @LupusLeaks\nGET YOUR OWN BOT FOR FREE!',loop=fnClient.loop)
    
    client.Settings = fnClient.Settings
    client.mainID = fnClient.mainID
    client.randomizing = False
    client.RemovingFriends = False

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
    async def event_party_member_join(Member):
        await party.event_party_member_join(client,Member)

    @client.event
    async def event_party_member_promote(old_leader, new_leader):
        await party.event_party_member_promote(client, old_leader,new_leader)

    @client.event
    async def event_party_message(Message):
        await message.Command(client, Message)

    @client.event
    async def event_friend_message(Message):
        await message.Command(client, Message)

    try:
        fnClient.loop.create_task(client.start())
        await client.wait_until_ready()
        fnClient.Clients[client.user.id] = client
    except:
        pass