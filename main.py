import discord
import os
from openai import OpenAI

file = input("Enter A or B for loading the chat:\n ")
match(file):
    case "A":
        file = "chatA.txt"
    case "B":
        file = "chatB.txt"
    case _:
        print("Invalid input")
        exit()
with open(file, "r") as f:
    chat = f.read()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
token = os.getenv("SECRET_KEY")
if not token:
    raise ValueError("SECRET_KEY environment variable is not set")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global chat
        chat += f"{message.author}: {message.content}\n"
        print(f'message from {message.author}: {message.content}')
        if self.user != message.author:
            if self.user in message.mentions:
                print(chat)
                channel = message.channel
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": chat},
                        {"role": "user", "content": message.content}
                    ],
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                messageToSend = response.choices[0].message.content
                await channel.send(messageToSend)


intents = discord.Intents.default()
intents.message_content = True

discord_client = MyClient(intents=intents)
discord_client.run(token)