import fakeyou,asyncio

async def main():
	afy=fakeyou.AsyncFakeYou()
	#defining the class

	session= await afy.login("EMAIL/USERNAME","PASSWORD")
	#login (optional)

	print(session.displayName)
	#getting the display name from session info

	leaderboard=await afy.get_tts_leaderboard()
	#getting tts leaderboard 
	for name,uplaods in zip(leaderboard.displayName,leaderboard.uploadedCount):
		print(f"user {name} uploaded {uplaods} times tts models")
		#sorting and getting data in simple way

	voices=await afy.list_voices(size=3)
	#getting voices (3 only)

	for token,titles in zip(voices.modelTokens,voices.title):
		#getting token and titles
		await afy.say("Hello World",token,filename=titles+".wav",cooldown=2)
		#getting tts "Hello World" for the first 3 voices


asyncio.run(main())