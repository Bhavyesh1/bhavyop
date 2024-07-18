import requests
from googletrans import Translator
from highrise import BaseBot, __main__
from highrise.models import (AnchorPosition, Item, Position, User,)
from highrise import BaseBot
from collections import UserDict
from highrise.models import SessionMetadata, User
from highrise.models import Position
from highrise.models import SessionMetadata, User, CurrencyItem, Item, AnchorPosition, Reaction, ModerateRoomRequest, Position
import random
import asyncio
from highrise import *
from highrise.models import *
from asyncio import Task
from highrise.__main__ import *
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from highrise import BaseBot, __main__
from highrise.models import (
    AnchorPosition,
    CurrencyItem,
    Item,
    Position,
    SessionMetadata,
    User,
)
from highrise.webapi import *
from highrise.models_webapi import *


emote_list : list[tuple[str, str]] = [("Sit", "idle-loop-sitfloor"),
("Enthused", "idle-enthusiastic"),
("Yes", "emote-yes"),
("The Wave", "emote-wave"),
("Tired", "emote-tired"),
("Snowball Fight!", "emote-snowball"),
("Snow Angel", "emote-snowangel"),
("Shy", "emote-shy"),
("Sad", "emote-sad"),
("No", "emote-no"),
("Model", "emote-model"),
("Flirty Wave", "emote-lust"),
("Laugh", "emote-laughing"),
("Kiss", "emote-kiss"),
("Sweating", "emote-hot"),
("Hello", "emote-hello"),
("Greedy Emote", "emote-greedy"),
("Face Palm", "emote-exasperatedb"),
("Curtsy", "emote-curtsy"),
("Confusion", "emote-confused"),
("Charging", "emote-charging"),
("Bow", "emote-bow"),
("Thumbs Up", "emoji-thumbsup"),
("Tummy Ache", "emoji-gagging"),
("Flex", "emoji-flex"),
("Cursing Emote", "emoji-cursing"),
("Raise The Roof", "emoji-celebrate"),
("Angry", "emoji-angry"),("Rest", "sit-idle-cute"),
("Savage Dance", "dance-tiktok8"),
("Don't Start Now", "dance-tiktok2"),
("Let's Go Shopping", "dance-shoppingcart"),  ("Relaxing", "idle-floorsleeping2"),
("Russian Dance", "dance-russian"),
("Penny's Dance", "dance-pennywise"),
("Macarena", "dance-macarena"),
("K-Pop Dance", "dance-blackpink"),
("Hyped", "emote-hyped"),
("Jinglebell", "dance-jinglebell"),
("Nervous", "idle-nervous"),
("Toilet", "idle-toilet"),
("Astronaut", "emote-astronaut"),
("Dance Zombie", "dance-zombie"),
("Heart Eyes", "emote-hearteyes"),
("Swordfight", "emote-swordfight"),
("TimeJump", "emote-timejump"),
("Snake", "emote-snake"),
("Heart Fingers", "emote-heartfingers"),
("Float", "emote-float"),
("Telekinesis", "emote-telekinesis"),
("Penguin dance", "dance-pinguin"),
("Creepy puppet", "dance-creepypuppet"),
("Sleigh", "emote-sleigh"),
("Maniac", "emote-maniac"),
("Energy Ball", "emote-energyball"),
("Singing", "idle_singing"),
("Frog", "emote-frog"),
("Superpose", "emote-superpose"),
("Cute", "emote-cute"),
("TikTok Dance 9", "dance-tiktok9"),
("Weird Dance", "dance-weird"),
("TikTok Dance 10", "dance-tiktok10"),
("Pose 7", "emote-pose7"),
("Pose 8", "emote-pose8"),
("Casual Dance", "idle-dance-casual"),
("Pose 1", "emote-pose1"),
("Pose 3", "emote-pose3"),
("Pose 5", "emote-pose5"),
("Cutey", "emote-cutey"),
("Punk Guitar", "emote-punkguitar"),
("Fashionista", "emote-fashionista"),
("Gravity", "emote-gravity"),
("Ice Cream Dance", "dance-icecream"),
("Wrong Dance", "dance-wrong"),
("UwU", "idle-uwu"),
("TikTok Dance 4", "idle-dance-tiktok4"),
("Advanced Shy", "emote-shy2"),
("Anime Dance", "dance-anime"),
("Kawaii", "dance-kawai"),
("Scritchy", "idle-wild"),
("Ice Skating", "emote-iceskating"),
("SurpriseBig", "emote-pose6"),
("Celebration Step", "emote-celebrationstep"),
("Creepycute", "emote-creepycute"),
("Pose 10", "emote-pose10"),
("Boxer", "emote-boxer"),
("Head Blowup", "emote-headblowup"),
('Ditzy Pose', 'emote-pose9'),
('Teleporting', 'emote-teleporting'),
('Touch', 'dance-touch'),
('Air Guitar','idle-guitar'),
("This Is For You", "emote-gift"),
("Push it", "dance-employee")]

class BotDefinition:
    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token



class MyBot(BaseBot):
        def __init__(self, *args, **kwargs):
                          super().__init__(*args, **kwargs)
                          self.following_user = None 
                          self.banned_users = {} 
                          self.following_username = None
                          super().__init__()
                          self.user_positions = {}
                          self.is_dancing = False 
                          self.sender_position = None           
                          self.is_following = False    




        async def on_user_move(self, user: User, pos: Position) -> None:
            self.user_positions[user.username] = pos
            print (f"{user.username} moved to {pos}")
    
    
        async def loop(self: BaseBot, user: User, message: str) -> None:
                    # Defining the loop_emote method locally so it cann't be accessed from the command handler.
                    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
                        emote_id = ""
                        for emote in emote_list:
                            if emote[0].lower() == emote_name.lower():
                                emote_id = emote[1]
                                break
                        if emote_id == "":
                            await self.highrise.chat("Invalid emote")
                            return
                        user_position = None
                        user_in_room = False
                        room_users = (await self.highrise.get_room_users()).content
                        for room_user, position in room_users:
                            if room_user.id == user.id:
                                user_position = position
                                start_position = position
                                user_in_room = True
                                break
                        if user_position == None:
                            await self.highrise.chat("User not found")
                            return
                        await self.highrise.chat(f"@{user.username} is looping {emote_name}")
                        while start_position == user_position:
                            try:
                                await self.highrise.send_emote(emote_id, user.id)
                            except:
                                await self.highrise.chat(f"Sorry, @{user.username}, this emote isn't free or you don't own it.")
                                return
                            await asyncio.sleep(10)
                            room_users = (await self.highrise.get_room_users()).content
                            user_in_room = False
                            for room_user, position in room_users:
                                if room_user.id == user.id:
                                    user_position = position
                                    user_in_room = True
                                    break
                            if user_in_room == False:
                                break
                    try:
                        splited_message = message.split(" ")
                        # The emote name is every string after the first one
                        emote_name = " ".join(splited_message[1:])
                    except:
                        await self.highrise.chat("Invalid command format. Please use 'loop <emote name>.")
                        return
                    else:   
                        taskgroup = self.highrise.tg
                        task_list : list[Task] = list(taskgroup._tasks)
                        for task in task_list:
                            if task.get_name() == user.username:
                                # Removes the task from the task group
                                task.cancel()

                        room_users = (await self.highrise.get_room_users()).content
                        user_list  = []
                        for room_user, pos in room_users:
                            user_list.append(room_user.username)

                        taskgroup.create_task(coro=loop_emote(self, user, emote_name))
                        task_list : list[Task] = list(taskgroup._tasks)
                        for task in task_list:
                            if task.get_coro().__name__ == "loop_emote" and not (task.get_name() in user_list):
                                task.set_name(user.username)

        async def stop_loop(self: BaseBot, user: User, message: str) -> None:
                    taskgroup = self.highrise.tg
                    task_list : list[Task] = list(taskgroup._tasks)
                    for task in task_list:
                        print(task.get_name())
                        if task.get_name() == user.username:
                            task.cancel()
                            await self.highrise.chat(f"Stopping your emote loop, {user.username}!")
                            return
                    await self.highrise.chat(f"You're not looping any emotes, {user.username}")
                    return

        async def run(self, room_id, token):
                   definitions = [BotDefinition(self, room_id, token)]
                   await __main__.main(definitions)

        async def on_user_leave(self, user: User): 
                print({user.username})
                await self.highrise.chat(f" have a good day 🤍 {user.username}")

        async def on_user_join(self, user: User, position: Position  | AnchorPosition): 
                print(f"{user.username} has joined the room.")
                await self.highrise.chat(f" @{user.username}  Welcome to chill 🇮🇳 ")
                await self.highrise.chat(f" @{user.username}  'Please check my bio or type 'hey cheese' for commands")

        async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
            print(f"{sender.username} tipped {receiver.username} an amount of {tip.amount}")

        async def on_chat(self, user: User, message: str) -> None:

            
            if message == "floor 1":
                await self.highrise.teleport(user.id, Position(10.5 ,0.0 ,7.5))

            if message == "floor 2":
                await self.highrise.teleport(user.id, Position(13.0 ,7.0 ,5.5))

            if message == "floor 3":
                await self.highrise.teleport(user.id, Position(13.5 ,16.0 ,6.05))

            
            if message.lower().startswith("/tipme "):
                parts = message.split(" ")
                if len(parts) != 2:
                    await self.highrise.send_message(user.id, "Invalid command")
                    return
                #checks if the amount is valid
                try:
                    amount = int(parts[1])
                except:
                    await self.highrise.chat("Invalid amount")
                    return
                #checks if the bot has the amount
                bot_wallet = await self.highrise.get_wallet()
                bot_amount = bot_wallet.content[0].amount
                if bot_amount <= amount:
                    await self.highrise.chat("Not enough funds")
                    return
                #converts the amount to a string of bars and calculates the fee
                """Possible values are: "gold_bar_1",
                "gold_bar_5", "gold_bar_10", "gold_bar_50", 
                "gold_bar_100", "gold_bar_500", 
                "gold_bar_1k", "gold_bar_5000", "gold_bar_10k" """
                bars_dictionary = {10000: "gold_bar_10k", 
                                   5000: "gold_bar_5000",
                                   1000: "gold_bar_1k",
                                   500: "gold_bar_500",
                                   100: "gold_bar_100",
                                   50: "gold_bar_50",
                                   10: "gold_bar_10",
                                   5: "gold_bar_5",
                                   1: "gold_bar_1"}
                fees_dictionary = {10000: 1000,
                                   5000: 500,
                                   1000: 100,
                                   500: 50,
                                   100: 10,
                                   50: 5,
                                   10: 1,
                                   5: 1,
                                   1: 1}
                #loop to check the highest bar that can be used and the amount of it needed
                tip = []
                total = 0
                for bar in bars_dictionary:
                    if amount >= bar:
                        bar_amount = amount // bar
                        amount = amount % bar
                        for i in range(bar_amount):
                            tip.append(bars_dictionary[bar])
                            total = bar+fees_dictionary[bar]
                if total > bot_amount:
                    await self.highrise.chat("Not enough funds")
                    return
                for bar in tip:
                    await self.highrise.tip_user(user.id, bar)
            if message.lower().startswith("loop"):
                            await self.loop(user, message)
            elif message.lower().startswith("stop loop"):
                            await self.stop_loop(user, message)

            
            if message.startswith("come") and user.username in ["T9s", "kirrish", "cheese.cake._", "igyouknowme" , "_cheese.cake"]:
                    response = await self.highrise.get_room_users()
                    your_pos = None
                    for content in response.content:
                            if content[0].id == user.id:
                                    if isinstance(content[1], Position):
                                            your_pos = content[1]
                                            break
                    if not your_pos:
                            await self.highrise.send_whisper(user.id, f"invalid command")
                            return
                    await self.highrise.chat("Yes boss!")
                    await self.highrise.walk_to(your_pos)

            
            
            # Flirting Feature
            if message.lower().startswith("flirt"):
                flirty_phrases = [ "Thank god I have life insurance. Because you make my heart stop." , "Hey gurl, wanna play shark attack, i eat u scream!" , "Can I take your picture? I need it to show Santa what I want for Christmas." , "Are you Christmas? Because I want to Merry you" , "Are you a tub of ice cream? Cause I wanna spoon you all night." , "Are you hiring? Because you look like you have a couple openings that need filling." , "You look like the scariest haunted house because I'm going to scream so loud when I'm inside you." , "Are you a magician? Because whenever I look at you, everyone else disappears." , "Are you a bank loan? Because you have my interest." , "Any chance you have an extra heart? Mine's been stolen!" , "Did your license get suspended for driving all these guys crazy?" , "I'd say God bless you, but it looks like he already has!" , "Even in zero gravity, I would still fall for you!" , "You must be made of Copper and Tellurium- because you're CuTe!" , "I'm not a photographer, but I can definitely picture us together." , "Life without you is like a broken pencil...pointless." , "You're so sweet, you're giving me a toothache" , "Was your father an alien? Because on planet Earth, there's no one else like you" , "We're not socks, but I think we'd make a great pair" , "No more ex, no more next, be my last"
                        
                ]
                await self.highrise.chat(f"@{user.username}, {random.choice(flirty_phrases)}")

            # Joke Feature
            if message.lower().startswith("joke") :
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!","I'm reading a book about anti-gravity. It's impossible to put down!",
                    "What do you call a lazy kangaroo? A pouch potato!",
                    "I'm on a seafood diet. I see food, and I eat it!",
                    "What do you call a bear with no teeth? A gummy bear!",
                    "I went to a fight the other night. It was a total knockout!",
                    "I'm afraid of speed bumps. They're always up to something.",
                    "What do you call a cow with no legs? Ground beef!",
                    "Why don't they play poker in the jungle? Too many cheetahs!"
                        
                ]
                await self.highrise.chat(f"@{user.username}, {random.choice(jokes)}")


            
            help_list = [ "         " , "type 'hello' in dm of bot to get emotelist" , "       "  , "flirt" , "          " ,  "joke" , "         ", "roast (@username) to roast someone", "      " , "floor 1/2/3 to teleport to different floors"]  
            if message.startswith("hey cheese"):  
                help_list = "\n".join( help_list)
                await self.highrise.send_whisper(user.id,help_list)
    
            if message.lower().startswith("/userinfo"):
                await self.userinfo(user, message)
            if message.lower().startswith("roast"):
                await self.roast(user, message)
            # Summon command
            if message.lower().startswith("summon"):
                await self.summon(user, message)
            # Dice roll feature
            if message.lower().startswith("roll"):
                await self.dice_roll(user, message)
            # Emote all feature
            if message.lower().startswith("all"):
                await self.emote_all(user, message)

        async def userinfo(self: BaseBot, user: User, message: str) -> None:
            # List of authorized users
            authorized_users = ["T9s", "kirrish", "cheese.cake._", "igyouknowme", "_cheese.cake"] 

            # Check if the user is authorized
            if user.username not in authorized_users:
                await self.highrise.chat(f"You are not authorized to use this command, @{user.username}.")
                return

            # Split the message into parts
            parts = message.split(" ")
            if len(parts) != 2:
                await self.highrise.chat("Incorrect format, please use /userinfo <@username>")
                return
            # Removes the @ from the username if it exists
            if parts[1].startswith("@"):
                username = parts[1][1:]
            else:
                username = parts[1]
            # Get the user id from the username
            user = await self.webapi.get_users(username=username, limit=1)
            if user:
                user_id = user.users[0].user_id
            else:
                await self.highrise.chat("User not found, please specify a valid user")
                return

            # Get the user info
            userinfo = await self.webapi.get_user(user_id)
            number_of_followers = userinfo.user.num_followers
            number_of_friends = userinfo.user.num_friends
            number_of_folowing = userinfo.user.num_following
            joined_at = (userinfo.user.joined_at).strftime("%d/%m/%Y %H:%M:%S")
            try:
                last_login = (userinfo.user.last_online_in).strftime("%d/%m/%Y %H:%M:%S")
            except:
                last_login = "Last login not available"
            # Get the number of posts and the most liked post
            userposts = await self.webapi.get_posts(author_id=user_id)
            number_of_posts = 0
            most_likes_post = 0
            try:
                while userposts.last_id != "":
                    for post in userposts.posts:
                        if post.num_likes > most_likes_post:
                            most_likes_post = post.num_likes
                        number_of_posts += 1
                    userposts = await self.webapi.get_posts(
                        author_id=user_id, starts_after=userposts.last_id
                    )
            except Exception as e:
                print(e)

            # Send the info to the chat
            await self.highrise.chat(
                f"""User: {username}\nNumber of followers: {number_of_followers}\nNumber of friends: {number_of_friends}\nNumber of following: {number_of_folowing}\nJoined at: {joined_at}\nLast login: {last_login}\nNumber of posts: {number_of_posts}\nMost likes in a post: {most_likes_post}"""
            )

        async def wallet(self, user: User, message: str) -> None:
            wallet = (await self.highrise.get_wallet()).content
            await self.highrise.chat(f"The bot wallet contains {wallet[0].amount} {wallet[0].type}")

        async def roast(self: BaseBot, user: User, message: str) -> None:
                
            # Split the message into parts
            parts = message.split(" ")
            if len(parts) != 2:
                await self.highrise.chat("Incorrect format, please use roast <@username>")
                return
            # Removes the @ from the username if it exists
            if parts[1].startswith("@"):
                username = parts[1][1:]
            else:
                username = parts[1]

            roasts = [
                f"You're so basic, even Google can't find you.",
                f"I'm not sure what's more wrinkled, your brain or your forehead.",
                f"You're like a penny, two-faced and not worth much.",
                f"I've seen better-looking mannequins in thrift stores.",
                f"You're the reason they invented dark mode.",
                f"You're so fake, even your hair extensions have extensions.",
                f"You're like a broken pencil...pointless.",
                f"I bet you think the world revolves around you, but it's actually just spinning in circles.",
                f"You're so lost, you couldn't find your way out of a paper bag.",
                f"You're the reason people invented sarcasm."
            ]

            await self.highrise.chat(f"@{username}, {random.choice(roasts)}")

        async def summon(self: BaseBot, user: User, message: str) -> None:
            # List of authorized users
            authorized_users = ["T9s", "kirrish", "cheese.cake._", "igyouknowme", "_cheese.cake"] 

            # Check if the user is authorized
            if user.username not in authorized_users:
                await self.highrise.chat(f"You are not authorized to use this command, @{user.username}.")
                return

            # Split the message into parts
            parts = message.split(" ")
            if len(parts) != 2:
                await self.highrise.chat("Incorrect format, please use summon <@username>")
                return

            # Removes the @ from the username if it exists
            if parts[1].startswith("@"):
                username = parts[1][1:]
            else:
                username = parts[1]

            # Get the user's current position
            response = await self.highrise.get_room_users()
            your_pos = None
            for content in response.content:
                if content[0].id == user.id:
                    if isinstance(content[1], Position):
                        your_pos = content[1]
                        break

            if not your_pos:
                await self.highrise.chat("Invalid command, please specify a valid username.")
                return

            # Teleport the bot to the specified user's position
            await self.highrise.chat(f"Summoning @{username}...")

            # Find the target user's ID
            room_users = (await self.highrise.get_room_users()).content
            target_user_id = None
            for room_user, pos in room_users:
                if room_user.username.lower() == username.lower():
                    target_user_id = room_user.id
                    break

            if target_user_id is None:
                await self.highrise.chat(f"User @{username} not found in the room.")
                return

            # Teleport the target user
            await self.highrise.teleport(target_user_id, your_pos)

            
        async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
            response = await self.highrise.get_messages(conversation_id)
            if isinstance(response, GetMessagesRequest.GetMessagesResponse):
                message = response.messages[0].content
            print (message)
            if message.lower() == "hello":
                loop_list1 = ['Heyya 👋🏻', '      , ''emotelist : ', '              ',  'Sit','Enthused' , 'The Wave', 'Tired', 'Snowball Fight!','Snow Angel', 'shy', 'sad', 'no', 'model', 'flirty Wave', 'laugh', 'kiss', 'sweating', 'hello', 'greedy emote', 'face palm' , 'curtsy', 'confusion', 'charging', 'bow', 'thumbs up', 'tummy ache', 'flex', 'cursing emote', 'raise the roof', 'angry' 
                ]
                loop_list1 = '\n'.join(loop_list1)            
                loop_list2 = ['savage dance', "don't start now", "let's go shopping", 'russian dance', "penny's dance", 'macarena', 'k-pop dance', 'hyped', 'jinglebell', 'nervous', 'toilet', 'astronaut', 'dance zombie', 'heart eyes', 'swordfight', 'timejump', 'snake' , 'heart fingers', 'float', 'telekinesis', 'penguin dance' , 'creepy puppet', 'sleigh' 
                        ]
                loop_list2 = '\n'.join(loop_list2)
                loop_list3 = ['maniac', 'energy ball', 'singing', 'frog', 'superpose', 'cute', 'tiktok dance 9', 'weird dance', 'tiktok dance 10', 'pose 7', 'pose 8', 'casual dance', 'pose 1', 'pose 3', 'pose 5', 'cutey', 'punk guitar', 'fashionista', 'gravity', 'ice cream dance', 'wrong dance', 'uwu', 'tiktok dance 4' ]
                loop_list3 = '\n'.join(loop_list3)
                loop_list4 = ['advanced shy', 'anime dance', 'kawaii', 'scritchy', 'ice skating', 'surprise big', 'celebration step', 'creepycute', 'pose 10', 'boxer', 'head blowup', 'ditzy pose', 'teleporting', 'touch', 'air guitar', 'this is for you', 'push it', '          ' , '           ']
                loop_list4 = '\n'.join(loop_list4)
                loop_list5 = ['commands: ', 'loop (emote name ) to start looping ' , 'loop stop - to stop looping ' , 'emote (emote name) (username) - to perform emote in duo', 'roast (@username)- to roast user' , 'flirt' , 'joke', 'floor 1/2/3 for teleporting ', '             ' , ' pm @cheese.cake._ for Bot / Radio purchase',]
                loop_list5 = '\n'.join(loop_list5)
                loop_list6 = ['invited to ',  'https://high.rs/room?id=665ec2fa0fde57aed29082d9']
                loop_list6 = '\n'.join(loop_list6)
                await self.highrise.send_message(conversation_id, loop_list1)  
                await self.highrise.send_message(conversation_id, loop_list2)
                await self.highrise.send_message(conversation_id, loop_list3) 
                await self.highrise.send_message(conversation_id, loop_list4)                
                await self.highrise.send_message(conversation_id, loop_list5)
                await             self.highrise.send_message(conversation_id, loop_list6)

        async def dice_roll(self: BaseBot, user: User, message: str) -> None:
            """Rolls a dice and sends the result to the chat."""
            try:
                # Check for a custom number of sides
                parts = message.split(" ")
                if len(parts) > 1:
                    sides = int(parts[1])
                    if sides < 1:
                        raise ValueError
                else:
                    sides = 6  # Default to a six-sided die
                result = random.randint(1, sides)
                await self.highrise.chat(f"@{user.username} rolled a {result}!")
            except ValueError:
                await self.highrise.chat(f"Invalid number of sides. Please enter a number greater than 0.")

        async def emote_all(self: BaseBot, user: User, message: str) -> None:
            """Performs an emote on all users in the room."""
            parts = message.split(" ")
            if len(parts) < 2:
                await self.highrise.chat("Invalid command format. Please use 'all <emote name>'.")
                return

            emote_name = " ".join(parts[1:])
            emote_id = ""
            for emote in emote_list:
                if emote[0].lower() == emote_name.lower():
                    emote_id = emote[1]
                    break

            if emote_id == "":
                await self.highrise.chat("Invalid emote.")
                return

            room_users = (await self.highrise.get_room_users()).content
            for room_user, _ in room_users:
                try:
                    await self.highrise.send_emote(emote_id, room_user.id)
                except:
                    await self.highrise.chat(f"Sorry, @{room_user.username}, this emote isn't free or you don't own it.")

            await self.highrise.chat(f"Emote '{emote_name}' performed on all users.")

if __name__== "__main__":
    room_id = "665ec2fa0fde57aed29082d9"
    token = "6cdd36db3568a14e6a1ef37da655f0dc9728442b4c56ada998bb6f94a2587d98"
    arun(MyBot().run(room_id, token))