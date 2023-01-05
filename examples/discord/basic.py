import discord,fakeyou

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.afy=fakeyou.AsyncFakeYou()
        self.runningSay=False

    async def on_message(self, message):
        if message.author == self.user:
            return

        if "!marioSay" in message.content:
            if self.runningSay:return
            else:self.runningSay==True
            toSay=message.content.replace("!marioSay ","")
            #TM:7wbtjphx8h8v is the one which used in docs, so imma use it
            try:
           	 await self.afy.say(toSay,"TM:7wbtjphx8h8v")
            except fakeyou.exception.TtsAttemptFailed:
            	await message.channel.send("Sorry, something went wrong")
            	return
            await message.channel.send(file=discord.File("fakeyou.wav"))
            self.runningSay==False
client = MyClient()
client.run('TOKEN HERE')
