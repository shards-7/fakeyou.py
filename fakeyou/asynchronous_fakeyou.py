import aiohttp,json,time,asyncio
from uuid import uuid4
from .objects import *
from .exception import *

"""
Hey devs, i know you're looking throug the code
its messy, i'll comment it later.
"""


class AsyncFakeYou():
	
	def __init__(self,verbose:bool=False):
		self.v=verbose
		self.baseurl="https://api.fakeyou.com/"
		self.headers={"accept":"application/json","content-Type": "application/json"}
		
		self.session=aiohttp.ClientSession(headers=self.headers)
		
		if self.v:
			print("Session Ready...")
	
	def __del__(self):
		try:
			loop=asyncio.get_event_loop()
			loop.create_task(self._close())
		except:
			loop=asyncio.new_event_loop()
			loop.run_until_complete(self._close())
	
	async def _close(self):
		if not self.session.closed:
			await self.session.close()
	
			
	
	async def login(self,username,password):
		ljson={"username_or_email":username,"password":password}
		async with self.session.post(self.baseurl+"login",json=ljson) as loginHandler:
			lrjson=await loginHandler.json()
			if loginHandler.status == 200:
				if lrjson["success"] == True:
					if self.v: print("Login succsess")
					sjsonResponse = await self.session.get(self.baseurl+"session")
					sjson=await sjsonResponse.json()
					if self.v: print(sjson)
					return login(sjson=sjson)
				
				elif lrjson["success"]==False and lrjson["error_type"]=="InvalidCredentials":
					raise InvalidCredentials("check username or password")
			elif loginHandler.status == 429:
				raise TooManyRequests("Too many requests, try again later or use a proxy.")
			
			
	async def list_voices(self,size:int=25):
		if self.v:
			print("Getting voice list")
		async with self.session.get(url=self.baseurl+"tts/list") as handler:
		
			if self.v:
				print("Got all voices, sorting...")
			
			if handler.status==429:raise TooManyRequests("Too many requests, try again later or use a proxy.")
			hjson=await handler.json()
			if handler.status==200:return list_voice(hjson,size=size)
	
	async def list_voice_categories(self,size:int=25):
		if self.v:
			print("Getting voice categories")
		async with self.session.get(self.baseurl+"category/list/tts") as handler:
		
			if self.v:
				print("Got all categories, sorting...")
			if handler.status==429:raise TooManyRequests("Too many requests, try again later or use a proxy.")
			hjson=await handler.json()
			if handler.status==200:return categories(hjson,size=size)
	
	async def get_voices_by_category(self,categoryToken:str):
		voices= await self.list_voices(size=0)
		found={"models":[]}
		if self.v:
			print("Looping through")
		for tokens,vjson in zip(voices.categoryTokens,voices.json):
			for token in tokens:
				if token==categoryToken:
					found["models"].append(vjson)
		
		return list_voice(json=found,size=0)
	
	async def search(self,query:str):
		cjson={"categories":[]}
		vjson={"models":[]}
		found_voices=vjson["models"]
		found_categories=cjson["categories"]
		voices= await self.list_voices(size=0)
		categories= await self.list_voice_categories(size=0)
		
		for categoryName,categoryJson in zip(categories.name,categories.json):
			if query.lower() in categoryName.lower():
				found_categories.append(categoryJson)
		
		for voiceName,voiceJson in zip(voices.title,voices.json):
			if query.lower() in voiceName.lower():
				found_voices.append(voiceJson)
		
		return search(vjson=vjson,cjson=cjson)
		
	async def generate_ijt(self,text:str,ttsModelToken:str,filename:str="fakeyou.wav"):
		if self.v:
			print("getting job token")
		payload={"uuid_idempotency_token":str(uuid4()),"tts_model_token":ttsModelToken,"inference_text":text}
		async with self.session.post(url=self.baseurl+"tts/inference",data=json.dumps(payload)) as handler:
			
			if handler.status==200:
				aijt=await handler.json()
				ijt= aijt["inference_job_token"]
				return ijt
			elif handler.status==400:
				raise RequestError("check token and text, or contact the developer IG:@thedemonicat")
			elif handler.status==429:
				raise TooManyRequests("Too many requests, try again later or use a proxy.")
	
	async def get_wav(self,ijt:str,cooldown:int,filename:str="fakeyou.wav"):
		while True:
			async with self.session.get(url=self.baseurl+f"tts/job/{ijt}") as handler:
				if handler.status==200:
					hjson=await handler.json()
					wavo=wav(hjson)
					if self.v:
						print("WAV STATUS :",wavo.status)
				
					if wavo.status=="started":
						continue
					elif "pending" in wavo.status:
						time.sleep(cooldown)
						continue
					elif "attempt_failed" in wavo.status:
						raise TtsAttemptFailed("check token and text, or contact the developer IG:@thedemonicat")
					elif "complete_success":
						async with self.session.get("https://storage.googleapis.com/vocodes-public"+wavo.maybePublicWavPath) as rcontent:
							with open(filename,"wb") as wavfile:
								content = await rcontent.read()
								wavfile.write(content)
								wavfile.close()
								content=None
						return wav
				elif handler.status==429:
					raise TooManyRequests("Too many requests, try again later or use a proxy.")
	
	async def say(self,text:str,ttsModelToken:str,filename:str="fakeyou.wav",cooldown:int=3):
		ijt=await self.generate_ijt(text=text,ttsModelToken=ttsModelToken,filename=filename)
		return await self.get_wav(ijt,cooldown=cooldown)
	
	async def get_tts_leaderboard(self):
		async with self.session.get(self.baseurl+"leaderboard") as handler:
			if handler.status == 200:
				ljson= await handler.json()
				return ttsleaderboard(ljson)
			if handler.status==429:raise TooManyRequests("Too many requests, try again later or use a proxy.")
	
	async def get_w2l_leaderboard(self):
		async with self.session.get(self.baseurl+"leaderboard") as handler:
			if handler.status == 200:
				ljson= await handler.json()
				return w2lleaderboard(ljson)
			if handler.status==429:raise TooManyRequests("Too many requests, try again later or use a proxy.")
	
	async def get_last_events(self):
		async with self.session.get(self.baseurl+"events") as handler:
			if handler.status == 200:
				ejson=await handler.json()
				return events(ejson)
			if handler.status==429:raise TooManyRequests("Too many requests, try again later or use a proxy.")