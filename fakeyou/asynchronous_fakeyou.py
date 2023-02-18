import aiohttp,json,time,asyncio,re
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
	
	
	async def make_tts_job(self,text:str,ttsModelToken:str,filename:str="fakeyou.wav"):
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
	
	async def tts_poll(self,ijt:str):
		while True:
			async with self.session.get(url=self.baseurl+f"tts/job/{ijt}") as handler:
				if handler.status==200:
					hjson=await handler.json()
					wavo=wav(hjson)
					if self.v:
						print("WAV STATUS :",wavo.status)
				
					if wavo.status=="started":
						continue
					elif "pending" == wavo.status:
						continue
					elif "attempt_failed" == wavo.status:
						raise Failed()
					
					elif "dead" == wavo.status:
						raise Dead()
					
					elif "complete_success" == wavo.status:
						if wavo.link != None:
							async with self.session.get(wavo.link) as rcontent:
								del wavo
								#for RAM
								
								return wav(hjson,rcontent)
						else:
							raise PathNullError()
				elif handler.status==429:
					raise TooManyRequests("Too many requests, try again later")
	
	async def say(self,text:str,ttsModelToken:str,filename:str="fakeyou.wav"):
		ijt=await self.make_tts_job(text=text,ttsModelToken=ttsModelToken,filename=filename)
		return await self.tts_poll(ijt)
	
	async def get_tts_leaderboard(self):
		async with self.session.get(self.baseurl+"leaderboard") as handler:
			if handler.status == 200:
				ljson= await handler.json()
				return ttsleaderboard(ljson)
			if handler.status==429:raise TooManyRequests("Too many requests, try again later")
	
	async def get_w2l_leaderboard(self):
		async with self.session.get(self.baseurl+"leaderboard") as handler:
			if handler.status == 200:
				ljson= await handler.json()
				return w2lleaderboard(ljson)
			if handler.status==429:raise TooManyRequests("Too many requests, try again later")
	
	async def get_last_events(self):
		async with self.session.get(self.baseurl+"events") as handler:
			if handler.status == 200:
				ejson=await handler.json()
				return events(ejson)
			if handler.status==429:raise TooManyRequests("Too many requests, try again later")
	
	async def get_user(self,username:str,limit:int=25):
		try:
			profile_handler=await self.session.get(self.baseurl+f"user/{username}/profile")
			if profile_handler.status==404:
				raise UserNotFound(username)
			tts_results=await self.session.get(self.baseurl+f"user/{username}/tts_results?limit={limit}")
			w2l_results=await self.session.get(self.baseurl+f"user/{username}/w2l_results?limit={limit}")
			tts_models=await self.session.get(self.baseurl+f"user/{username}/tts_models?limit={limit}")
			w2l_models=await self.session.get(self.baseurl+f"user/{username}/w2l_templates?limit={limit}")
			
			if profile_handler.status==429 or w2l_models.status==429:
				raise TooManyRequests()
			
			
			else:
				return profileo(
				profile_json=await profile_handler.json(),
				w2l_temps_json=await w2l_models.json(),
				tts_result_json=await tts_results.json(),
				tts_models_json=await tts_models.json(),
				w2l_result_json=await w2l_results.json())
				
		except:
			raise RequestError("Something went wrong, Try again")
	
	async def get_queue(self):
		try:
			handler=await self.session.get("https://api.fakeyou.com/tts/queue_length")
			queue=await handler.json()
			
			return queue["pending_job_count"]
		except:
			raise RequestError("Something went wrong, please try again or check your internet connection")
			
	async def create_account(self,username:str,password:str,email:str):
		if len(username) < 3 :
			raise UsernameTooShort()
		
		if len(password) < 8:
			raise PasswordTooShort()
		
		if re.match("^[\w]+@([\w-]+\.)+[\w]+",email) == None:
			raise EmailInvalid()
		
		data={"username":username,"email_address":email,"password":password,"password_confirmation":password}
		
		handler=await self.session.post(url="https://api.fakeyou.com/create_account",json=data)
		
		if handler.status == 400:
			error=handler.json()["error_type"]
			
			if error=="UsernameTaken" or error=="UsernameReserved":
				raise UsernameTaken()
			elif error=="EmailTaken":
				raise EmailTaken()
		elif handler.status==200:
				return "OK"
	
	async def make_w2l_job(self,file:open,template_token):
			file_name=file.name
			if "/" in file_name:
				name=file_name.split("/").pop()
			else:
				name=file_name
			form={
			"template_token":template_token,
			"uuid_idempotency_token":str(uuid4()),
			"audio":(name,file.read(),"audio/mpeg")
		}
			handler=await self.session.post(url="https://api.fakeyou.com/w2l/inference",files=form)
			try:
				w2lJson=handler.json()
			except:
				raise RequestError("Please try again later")
			
			if handler.status==400:
				if w2lJson["error_reason"] == "Template does not exist":
					raise W2lTemplateTokenWrong()
				
			elif handler.status==429:
				raise TooManyRequests()
			
			elif handler.status==200:
				return w2lJson["inference_job_token"]
	
	async def w2l_poll(self,ijt:str):
		while True:
			polling_handler=await self.session.get(f"https://api.fakeyou.com/w2l/job/{ijt}")
			if polling_handler.status==200:
				try:pjs=polling_handler.json()
				except:raise RequestError("Something went wrong.","REQUEST CONTENT:",polling_handler.content)
				state=pjs["state"]["status"]
				if state == "complete_success":
					get_w2l_content=await self.session.get("https://storage.googleapis.com/vocodes-public"+str(pjs["state"]["maybe_public_bucket_video_path"]))
					content=get_w2l_content.content
					return w2lo(pjs,content)
				if state == "Started":
					continue
				if state == "pending":
					continue
	
	async def w2l(self,file:open,template_token:str) :
		ijt=await self.make_w2l_job(file,template_token)
		w2l_polling = await self.w2l_poll(ijt)
		return w2l_polling
		
	async def delete_tts_result(self,result_token):
		data={"set_delete":True,"as_mod":True}
		handler=await self.session.post(f"https://api.fakeyou.com/tts/result/{result_token}/delete",json=data)
		
		stats=handler.status
		
		if stats==200:
			return "DONE"
		elif stats==401:
			raise UnAuthorized(f"You're not authorized to delete tts result {result_token}")
		elif stats==404:
			raise TtsResultNotFound(result_token)
	
	async def delete_w2l_result(self,result_token):
		data={"set_delete":True,"as_mod":False}
		handler=await self.session.post(f"https://api.fakeyou.com/w2l/result/{result_token}/delete",json=data)
		
		stats=handler.status
		
		if stats==200:
			return "DONE"
		elif stats==401:
			raise UnAuthorized(f"You're not authorized to delete tts result {result_token}")
		elif stats==404:
			raise TtsResultNotFound(result_token)
	
	
	def logout(self):
		
		self.session.cookie_jar.clear()
	
	