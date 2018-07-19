import discord, urllib3, certifi
from bs4 import BeautifulSoup
from settings import *

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('define'):
        print(message.content)
        word = message.content.replace('define ', '')
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
        response = http.request('GET', 'https://en.oxforddictionaries.com/definition/' + word)
        soup = BeautifulSoup(response.data, 'html.parser')
        
        description_box = soup.find('span',{'class': 'ind'})
        try:
            description = description_box.text.strip()
            msg = word + ': ' + description
            await client.send_message(message.channel, msg)
        except AttributeError:
            await client.send_message(message.channel, "Could not find definition for the word " + word + ", sorry!")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)