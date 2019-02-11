import tkinter
import sys
import asyncio
import discord
import pafy
import urllib.request
import asyncio

print('Do not play anything just yet')

#add bot token here
TOKEN = '----------------------------------'
client = discord.Client()
player = 0
link = ""
wc = 0
exit = False
playing = 0
play_text = '!yt'
#add channel id for witch channel the bot should listen on 
chatChannelID = '----------------------------------'
#add channel id for witch channel the bot should talk in
voicChannelID = '----------------------------------'
replaying = 0


def stop_playing():
    global player
    print("stopped playing")
    player.stop()

@client.event
async def on_message(message):
    global player, link, wc, replaying
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(play_text):
        replaying = 1
        if player.is_playing():
            stop_playing()
        index = str(message.content).find(' ')
        link = message.content[index + 1:]
        print("link = " + link)
        for it in client.voice_clients:
            wc = it

        if link[0:5] == 'https':
            #player = await wc.create_ytdl_player(link)
            #player.volume = 0.5
            print("started from link = " + link)
            #player.start()
            #print(player)

            #text = ("Playing " + link).format(message)
            #await client.send_message(message.channel, text)
        else:
            link = str(link).replace(" ", "+")
            print("searching for " + link)
            with urllib.request.urlopen(('https://www.youtube.com/results?search_query=' + str(link) + "&page=1")) as response:
                html = response.read()
                index = str(html).find('href="/watch?')
                vid = str(html)[index + 6:index + 26]
                print("vid = " + vid)
                link = 'https://www.youtube.com' + vid
                print("search link = " + link)
                #player = await wc.create_ytdl_player(link)
                #player.volume = 0.5
                print("started")
                #player.start()
                text = ("Playing https://www.youtube.com" + vid).format(message)
                await client.send_message(message.channel, text)
    if message.content.startswith('!close'):
        global exit

        for it in client.voice_clients:
            wc = it
        await wc.disconnect()
        stop_playing()
        exit = True
        await asyncio.sleep(2)
        await client.logout()
        print("closing")
    if message.content.startswith('!pause'):
        replaying = 0
        player.pause()
    if message.content.startswith('!resume'):
        replaying = 1
        player.resume()
    if message.content.startswith('!up'):
        index = str(message.content).find(' ')
        amount = message.content[index + 1:]
        player.volume += float(amount)

    if message.content.startswith('!down'):
        index = str(message.content).find(' ')
        amount = message.content[index + 1:]
        player.volume -= float(amount)


@client.event
async def on_ready():
    global wc, player ,wc
    print('Logged in as ' + client.user.name)
    print('------')

    channel = client.get_channel(voicChannelID)
    wc = await client.join_voice_channel(channel)
    player = await wc.create_ytdl_player('https://www.youtube.com/watch?v=YeaGUfZM5hs')
    player.volume = 0.5
    stop_playing()
    #print(wc)
    print('Ready to play')

async def check():
    global player, link, exit ,wc
    while (True):
        if (exit == True):
            print("exited check")
            return
        try:
            if player.is_done() == True and replaying:
                print("test")
                print(player)
                for it in client.voice_clients:
                    wc = it
                stop_playing()
                print("playing = " + link)
                player = await wc.create_ytdl_player(link,before_options=" -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                player.start()
                print(player)
                player.volume = 0.1
        except:
            v = 1
        await asyncio.sleep(0.5)

client.loop.create_task(check())
client.run(TOKEN)
