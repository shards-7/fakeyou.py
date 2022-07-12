import requests,json,time
from uuid import uuid4
from .objects import *
from .exception import *
"""
Hey devs, i know you're looking throug the code
its messy, i'll comment it later.
"""


class FakeYou():
	
	def __init__(self,proxies:dict=None,verbose:bool=False):
		self.v=verbose
		self.baseurl="https://api.fakeyou.com/"
		self.headers={"accept":"application/json","content-Type": "application/json"}
		
		self.session=requests.Session()
		if proxies!=None:
			self.session.proxies=proxies
		self.session.headers=self.headers
		if self.v:
			print("Session Ready...")
	
	def list_voices(self,size:int=25):
		if self.v:
			print("Getting voice list")
		handler=self.session.get(self.baseurl+"tts/list")
		
		if self.v:
			print("Got all voices, sorting...")
		
		if handler.status_code==429:raise TooManyRequests("Too many requests, try again later or use a proxy.")
		hjson=handler.json()
		if handler.status_code==200:return list_voice(hjson,size=size)
	
	def list_voice_categories(self,size:int=25):
		if self.v:
			print("Getting voice categories")
		handler=self.session.get(self.baseurl+"category/list/tts")
		
		if self.v:
			print("Got all categories, sorting...")
		if handler.status_code==429:raise TooManyRequests("Too many requests, try again later or use a proxy.")
		hjson=handler.json()
		if handler.status_code==200:return categories(hjson,size=size)
	
	def get_voices_by_category(self,categoryToken:str):
		voices=self.list_voices(size=0)
		found={"models":[]}
		if self.v:
			print("Looping through")
		for tokens,vjson in zip(voices.categoryTokens,voices.json):
			for token in tokens:
				if token==categoryToken:
					found["models"].append(vjson)
		
		return list_voice(json=found,size=0)
	
	def search(self,query:str):
		cjson={"categories":[]}
		vjson={"models":[]}
		found_voices=vjson["models"]
		found_categories=cjson["categories"]
		voices=self.list_voices(size=0)
		categories=self.list_voice_categories(size=0)
		
		for categoryName,categoryJson in zip(categories.name,categories.json):
			if query.lower() in categoryName.lower():
				found_categories.append(categoryJson)
		
		for voiceName,voiceJson in zip(voices.title,voices.json):
			if query.lower() in voiceName.lower():
				found_voices.append(voiceJson)
		
		return search(vjson=vjson,cjson=cjson)
		
	def generate_ijt(self,text:str,ttsModelToken:str,filename:str="fakeyou.wav"):
		if self.v:
			print("getting job token")
		payload={"uuid_idempotency_token":str(uuid4()),"tts_model_token":ttsModelToken,"inference_text":text}
		handler=self.session.post(url=self.baseurl+"tts/inference",data=json.dumps(payload))
		if handler.status_code==200:
			ijt=handler.json()["inference_job_token"]
			return ijt
		elif handler.status_code==400:
			raise RequestError("check token and text, or contact the developer IG:@thedemonicat")
		elif handler.status_code==429:
			raise TooManyRequests("Too many requests, try again later or use a proxy.")
	
	def get_wav(self,ijt:str,filename:str="fakeyou.wav"):
		while True:
			handler=self.session.get(url=self.baseurl+f"tts/job/{ijt}")
			if handler.status_code==200:
				hjson=handler.json()
				wavo=wav(hjson)
				if self.v:
					print("WAV STATUS :",wavo.status)
				
				if wavo.status=="started":
					continue
				elif "pending" in wavo.status:
					continue
				elif "attempt_failed" in wavo.status:
					raise TtsAttemptFailed("check token and text, or contact the developer IG:@thedemonicat")
				elif "complete_success":
					content=self.session.get("https://storage.googleapis.com/vocodes-public"+wavo.maybePublicWavPath).content
					with open(filename,"wb") as wavfile:
						wavfile.write(content)
						wavfile.close()
					return wav
			elif handler.status_code==429:
				raise TooManyRequests("Too many requests, try again later or use a proxy.")
	
	def say(self,text:str,ttsModelToken:str,filename:str="fakeyou.wav"):
		ijt=self.generate_ijt(text=text,ttsModelToken=ttsModelToken,filename=filename)
		return self.get_wav(ijt)
	
	
	
	
	