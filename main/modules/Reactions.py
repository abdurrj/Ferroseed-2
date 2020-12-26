from discord.ext.commands import Cog
import discord


#######################################################################################

class Reactions(Cog):
    def __init__(self, client):
        self.client = client
        

        
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        guild = self.client.get_guild(guild_id)
        message_id = payload.message_id
        if message_id == 756051702200664115:
            if payload.emoji.name == 'martin': # :name: for custom, but 😂 for unicode
                role = discord.utils.get(guild.roles, name ='Martin') # Can use (id = int) as well, In case role name changes
            elif payload.emoji.name == '😈':
                role = discord.utils.get(guild.roles, name='Uniwinkle')
            elif payload.emoji.name == '🌸':
                role = discord.utils.get(guild.roles, name='Cherry')
            elif payload.emoji.name == 'ditto':
                role = discord.utils.get(guild.roles, name='Violet')
            elif payload.emoji.name == '💜':
                role = discord.utils.get(guild.roles, name='Lavender')
            elif payload.emoji.name == '🐤':
                role = discord.utils.get(guild.roles, name='Goldenrod')
            elif payload.emoji.name == '🌧️':
                role = discord.utils.get(guild.roles, name='Rain')
            elif payload.emoji.name == '💙':
                role = discord.utils.get(guild.roles, name='Forget-Me-Not')
            elif payload.emoji.name == '🌵':
                role = discord.utils.get(guild.roles, name='Saguaro')
            elif payload.emoji.name == '🌲':
                role = discord.utils.get(guild.roles, name='Evergreen')
            elif payload.emoji.name == '🍀':
                role = discord.utils.get(guild.roles, name='Mint')
            elif payload.emoji.name == '🌹':
                role = discord.utils.get(guild.roles, name='Rose')
            elif payload.emoji.name == '🍞':
                role = discord.utils.get(guild.roles, name='Cinnamon')
            # else:
            #     role = discord.utils.get(guild.roles, name=payload.emoji.name)    Use this if if emoji name = role names

            if role is not None:
                print(role.name)
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                print(member)
                if member is not None:
                    await member.add_roles(role)
                    print("done")
                else:
                    print("member not found")
            else:
                print("role not found")


        # Reaction role start
        if message_id == 757997437213212826: # Reaction role
            print("Reaction role message")
            if payload.emoji.name == 'pogo': # :name: for custom, but 😂 for unicode
                role = discord.utils.get(guild.roles, id=757995249091084440) # Pogo raiders
            elif payload.emoji.name == '⛑️':
                role = discord.utils.get(guild.roles, id=771463405239926835) # Dynamax adventurers
            elif payload.emoji.name == '📎':
                role = discord.utils.get(guild.roles, id=774424262173261927) # She/her
            elif payload.emoji.name == '🛋️':
                role = discord.utils.get(guild.roles, id=774424406923149312) # He/Him
            elif payload.emoji.name == '🖍️':
                role = discord.utils.get(guild.roles, id=774424474790920192) # They/Them
            elif payload.emoji.name == '🛩️':
                role = discord.utils.get(guild.roles, id=774424521260269568) # Any pronouns
            elif payload.emoji.name == '📓':
                role = discord.utils.get(guild.roles, id=774424567283712043) # Other pronouns           
            # elif payload.emoji.name == '😈':
            #     role = discord.utils.get(guild.roles, name='Uniwinkle')

            if role is not None:
                print(role.name)
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                print(member)
                if member is not None:
                    await member.add_roles(role)
                    print("done")
                else:
                    print("member not found")
            else:
                print("role not found")


        # react to pin start
        if payload.emoji.name == "📌":
            pin_channel = self.client.get_channel(payload.channel_id)
            pin_msg = payload.message_id
            pin_msg = await pin_channel.fetch_message(payload.message_id)
            # pin_msg_user = [pin_msg.author.id]
            # pin_reactor = discord.utils.find(lambda m : m.id == payload.user_id, pin_guild.members)
            # pin_reactor_id = int(pin_reactor.id)
            # valid_users = pin_msg_user + admin_users_id
            # valid_users_test = all(user != pin_reactor_id for user in valid_users)
            # if valid_users_test == False:
            await pin_msg.pin()


        # Create voice channel
        if message_id == 770315723464638484:
            voice_category = self.client.get_channel(739139545202950161)
            channel_list = guild.channels
            channel_name_list = []
            for i in range(0, len(channel_list)):
                channel_name = channel_list[i].name
                channel_name_list.append(channel_name)
            if payload.emoji.name == '🟥':
                channel_name = "a-red-voice-channel"
                if channel_name in channel_name_list:
                    print("Channel already created")
                else:
                    await guild.create_voice_channel(channel_name, category=voice_category)
            elif payload.emoji.name == '🟩':
                channel_name = "a-green-voice-channel"
                if channel_name in channel_name_list:
                    print("Channel already created")
                else:
                    await guild.create_voice_channel(channel_name, category=voice_category)
            elif payload.emoji.name == '🟦':
                channel_name = "a-blue-voice-channel"
                if channel_name in channel_name_list:
                    print("Channel already created")
                else:
                    await guild.create_voice_channel(channel_name, category=voice_category)




    """
    ####################################################################
    """



#     # remove react to remove role
    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild_id = payload.guild_id
        guild = self.client.get_guild(guild_id)
        message_id = payload.message_id
        if message_id == 756051702200664115: # Reaction colour roles
            if payload.emoji.name == 'martin': # :name: for custom, but 😂 for unicode
                role = discord.utils.get(guild.roles, name='Martin')
            elif payload.emoji.name == '😈':
                role = discord.utils.get(guild.roles, name='Uniwinkle')
            elif payload.emoji.name == '🌸':
                role = discord.utils.get(guild.roles, name='Cherry')
            elif payload.emoji.name == 'ditto':
                role = discord.utils.get(guild.roles, name='Violet')
            elif payload.emoji.name == '💜':
                role = discord.utils.get(guild.roles, name='Lavender')
            elif payload.emoji.name == '🐤':
                role = discord.utils.get(guild.roles, name='Goldenrod')
            elif payload.emoji.name == '🌧️':
                role = discord.utils.get(guild.roles, name='Rain')
            elif payload.emoji.name == '💙':
                role = discord.utils.get(guild.roles, name='Forget-Me-Not')
            elif payload.emoji.name == '🌵':
                role = discord.utils.get(guild.roles, name='Saguaro')
            elif payload.emoji.name == '🌲':
                role = discord.utils.get(guild.roles, name='Evergreen')
            elif payload.emoji.name == '🍀':
                role = discord.utils.get(guild.roles, name='Mint')
            elif payload.emoji.name == '🌹':
                role = discord.utils.get(guild.roles, name='Rose')
            elif payload.emoji.name == '🍞':
                role = discord.utils.get(guild.roles, name='Cinnamon')
            # else:
            #     role = discord.utils.get(guild.roles, name=payload.emoji.name)
            if role is not None:
                print(role.name)
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print("done")
                else:
                    print("member not found")
            else:
                print("role not found")
        

        # Remove react to remove role start
        if message_id == 757997437213212826: # Reaction roles
            if payload.emoji.name == 'pogo': # :name: for custom, but 😂 for unicode
                role = discord.utils.get(guild.roles, id=757995249091084440) # Pogo raiders
            elif payload.emoji.name == '⛑️':
                role = discord.utils.get(guild.roles, id=771463405239926835) # Dynamax adventurers
            elif payload.emoji.name == '📎':
                role = discord.utils.get(guild.roles, id=774424262173261927) # She/her
            elif payload.emoji.name == '🛋️':
                role = discord.utils.get(guild.roles, id=774424406923149312) # He/Him
            elif payload.emoji.name == '🖍️':
                role = discord.utils.get(guild.roles, id=774424474790920192) # They/Them
            elif payload.emoji.name == '🛩️':
                role = discord.utils.get(guild.roles, id=774424521260269568) # Any pronouns
            elif payload.emoji.name == '📓':
                role = discord.utils.get(guild.roles, id=774424567283712043) # Other pronouns
            # elif payload.emoji.name == '😈':
                # role = discord.utils.get(guild.roles, name='Uniwinkle')

            if role is not None:
                print(role.name)
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print("done")
                else:
                    print("member not found")
            else:
                print("role not found")
        

        # Remove react to remove pin start
        if payload.emoji.name == "📌": 
            pin_channel = self.client.get_channel(payload.channel_id)
            pin_msg = payload.message_id
            pin_msg = await pin_channel.fetch_message(payload.message_id)
            # pin_msg_user = [pin_msg.author.id]
            # pin_reactor = discord.utils.find(lambda m : m.id == payload.user_id, pin_guild.members)
            # pin_reactor_id = int(pin_reactor.id)
            # valid_users = pin_msg_user + admin_users_id
            # valid_users_test = all(user != pin_reactor_id for user in valid_users)
            # if valid_users_test == False: # use this if you want only message author and admins to be able to unpin
            await pin_msg.unpin()



        if message_id == 770315723464638484:
            # voice_category = client.get_channel(770314988170248222)
            if payload.emoji.name == '🟥':
                channel_name = "a-red-voice-channel"
                channel = discord.utils.get(guild.voice_channels, name=channel_name)
                await discord.VoiceChannel.delete(channel)
            elif payload.emoji.name == '🟩':
                channel_name = "a-green-voice-channel"
                channel = discord.utils.get(guild.voice_channels, name=channel_name)
                await discord.VoiceChannel.delete(channel)
            elif payload.emoji.name == '🟦':
                channel_name = "a-blue-voice-channel"
                channel = discord.utils.get(guild.voice_channels, name=channel_name)
                await discord.VoiceChannel.delete(channel)


#     '''
#     #####################
#     Reaction events end
#     #################
#     '''


def setup(client):
    client.add_cog(Reactions(client))
