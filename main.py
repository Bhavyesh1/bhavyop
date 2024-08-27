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
import os
import google.generativeai as genai # Import for Google Generative AI



emote_list : list[tuple[str, str,float]] = [("1", "idle-loop-sitfloor", 22.321055),
("2", "idle-enthusiastic", 15.941537),

("93", "emote-kissing-bound",6)]

# Set up Google Generative AI
os.environ["GOOGLE_AI_API_KEY"] = "AIzaSyBkz5C5QaTIPYMHblpGkTkef543SOmOotA"  # Replace with your API key
genai.configure(api_key=os.environ['GOOGLE_AI_API_KEY'])


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

            
                          # Combined list of authorized users/moderators
                          self.authorized_users = ["igyouknowme", "DEAD74","lemonadee_","lixxioup","Niks._ ","xx_sanju_xx"] 
                          # List of users who cannot be kicked or banned
                          self.protected_users = ["igyouknowme","DEAD74","bhelpuri_","xx_sanju_xx","Niks._ ","lemonadee_"]
            
        async def on_user_move(self, user: User, pos: Position) -> None:
            self.user_positions[user.username] = pos
            print (f"{user.username} moved to {pos}")
    
        async def on_start(self, session_metadata: SessionMetadata) -> None:
            
            Counter.bot_id = session_metadata.user_id
            print("is booting ...")
            pass
            
            
            
            self.highrise.tg.create_task(self.highrise.walk_to(Position(x=0, y=0.0, z=0, facing='FrontLeft')))
            
            while True:
                await asyncio.sleep(9)
                await self.highrise.send_emote(
                random.choice(['emote-ghost-idle']))

    

        async def run(self, room_id, token):
            definitions = [BotDefinition(self, room_id, token)]
            await __main__.main(definitions)

        async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
            """Handles direct messages from users."""
            response = await self.highrise.get_messages(conversation_id)
            if isinstance(response, GetMessagesRequest.GetMessagesResponse):
                message = response.messages[0].content

            # Process the user's question
            if message.lower().startswith("ai"):
                text = message[3:]  # Remove "ai" from the start of the message
                if len(text) == 0:
                    await self.highrise.send_message(conversation_id, f"Please ask a question.")
                    return

                # Use Google Generative AI to generate a response
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(text)
                response_text = response.text   
                # Split the response into 230-word chunks
                chunks = [response_text[i:i+230] for i in range(0, len(response_text), 230)]
                # Send the chunks to the chat
                for chunk in chunks:
                    await self.highrise.send_message(conversation_id, f"{chunk}")
