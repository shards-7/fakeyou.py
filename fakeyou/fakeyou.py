import requests,json,time,logging,re
from uuid import uuid4
from .objects import *
from .exception import *
"""
Hey devs, i know you're looking throug the code
its messy, i'll comment it later.
"""


class FakeYou():
	
	def __init__(self,verbose:bool=False):
		self.baseurl="https://api.fakeyou.com/"
		
		#the base api url, every method will be called using
		#this url, <url+method name>
		
		self.headers={"accept":"application/json","content-Type": "application/json"}
		#general headers needed for almost every request
		
		self.session=requests.Session()
		#our session
		
		self.session.headers=self.headers
		#including our headers in
		
		logging.debug("Session created")
			
	
	def login(self,username,password):
		
		ljson={"username_or_email":username,"password":password}
		#login payload
		
		logging.debug("Sending Login request")
		
		loginHandler=self.session.post(self.baseurl+"login",json=ljson)
		#sending the login request, this will return cookies and status
		logging.debug("Login request sent")
		
		lrjson=loginHandler.json()
		#our response from 'login request'
		if loginHandler.status_code == 200:
			#this means we're in without 'ERRORS'
			
			logging.debug("Processing the response (login)")
			if lrjson["success"] == True:
				#login success
				logging.debug("Login has been done successfully")
				sjson=self.session.get(self.baseurl+"session").json()
				return login(sjson=sjson)
				
			elif lrjson["success"]==False and lrjson["error_type"]=="InvalidCredentials":
				#login failed
				logging.critical("FALSE email/password, raising error.")
				raise InvalidCredentials()
		
		elif loginHandler.status_code == 429:
			#ip ban !
			logging.critical("IP IS BANNED (caused by login request)")
			raise TooManyRequests()
			
			
	def list_voices(self,size:int=25):
		#this function will list every single voice that can be used
		logging.debug("fetching voice models")
		handler=self.session.get(self.baseurl+"tts/list")
		logging.debug("Voice models fetched")
		if handler.status_code==429:
			#ip ban
			logging.critical("Your ip is banned, raising error")
			raise TooManyRequests()
			
		if handler.status_code==200:
			#success
			hjson=handler.json()
			#getting voices json
			logging.debug("processing data.")
			return list_voice(hjson,size=size)
	
	def list_voice_categories(self,size:int=25):
		#this function will return voice categories
		#categories can be used in other functions, like :
			#func : get_voices_by_category
		
		logging.debug("Fetching categories")
		handler=self.session.get(self.baseurl+"category/list/tts")
		logging.debug("Categories fetched!")
		
			
		if handler.status_code==429:
			#ip ban
			logging.error("Your ip is banned");raise TooManyRequests()
		
		if handler.status_code==200:
			hjson=handler.json()
			return categories(hjson,size=size)
	
	def get_voices_by_category(self,categoryToken:str):
		#this function gets all voices by category
		#does it by filtering !
		
		voices=self.list_voices(size=0)
		#to get all voices
		
		found={"models":[]}
		#this var will be parsed as list_voice object
		
		
			
		for tokens,vjson in zip(voices.categoryTokens,voices.json):
			#we get tokens to filter it all using tokens
			#then we append json to 'found' then 
			#we parse it
			for token in tokens:
				if token==categoryToken:
					found["models"].append(vjson)
		
		return list_voice(json=found,size=0)
	
	
	def make_tts_job(self,text:str,ttsModelToken:str):
		
			
		payload={"uuid_idempotency_token":str(uuid4()),"tts_model_token":ttsModelToken,"inference_text":text}
		handler=self.session.post(url=self.baseurl+"tts/inference",data=json.dumps(payload))
		if handler.status_code==200:
			ijt=handler.json()["inference_job_token"]
			return ijt
		elif handler.status_code==400:
			raise RequestError("check token and text, or contact the developer IG:@thedemonicat")
		elif handler.status_code==429:
			raise TooManyRequests()
	
	def tts_poll(self,ijt:str):
		while True:
			handler=self.session.get(url=self.baseurl+f"tts/job/{ijt}")
			if handler.status_code==200:
				hjson=handler.json()
				wavo=wav(hjson)
				
					
				if wavo.status=="started":
					continue
				elif "pending" == wavo.status:
					
					continue
				elif "attempt_failed" == wavo.status:
					raise Failed()
				elif "dead" == wavo.status:
					raise Dead()
				elif "complete_success" == wavo.status:
					if wavo.link!=None:
						content=self.session.get(wavo.link).content
						del wavo
						#for RAM
						return wav(hjson,content)
					else:
						raise PathNullError()
					
					
			elif handler.status_code==429:
				raise TooManyRequests()
	

	def say(self,text:str,ttsModelToken:str):
		
		return self.tts_poll(self.make_tts_job(text=text,ttsModelToken=ttsModelToken))
	
	def tts_status(self,ijt:str):
		handler=self.session.get(url=self.baseurl+f"tts/job/{ijt}")
		if handler.status_code==200:
			hjson=handler.json()
			return hjson["state"]["status"]
		else:
			raise RequestError("Something went wrong, content:",handler.content)

	def get_tts_leaderboard(self):
		handler=self.session.get(self.baseurl+"leaderboard")
		if handler.status_code == 200:
			ljson=handler.json()
			return ttsleaderboard(ljson)
		if handler.status_code==429:raise TooManyRequests()
	
	def get_w2l_leaderboard(self):
		handler=self.session.get(self.baseurl+"leaderboard")
		if handler.status_code == 200:
			ljson=handler.json()
			return w2lleaderboard(ljson)
		if handler.status_code==429:raise TooManyRequests()
	
	def get_last_events(self):
		handler=self.session.get(self.baseurl+"events")
		if handler.status_code == 200:
			ejson=handler.json()
			return events(ejson)
		if handler.status_code==429:raise TooManyRequests()
	
	def get_user(self,username:str,limit:int=25):
		try:
			profile_handler=self.session.get(self.baseurl+f"user/{username}/profile")
			if profile_handler.status_code==404:
				raise UserNotFound(username)
			tts_results=self.session.get(self.baseurl+f"user/{username}/tts_results?limit={limit}")
			w2l_results=self.session.get(self.baseurl+f"user/{username}/w2l_results?limit={limit}")
			tts_models=self.session.get(self.baseurl+f"user/{username}/tts_models?limit={limit}")
			w2l_models=self.session.get(self.baseurl+f"user/{username}/w2l_templates?limit={limit}")
			
			if profile_handler.status_code==429 or w2l_models.status_code==429:
				raise TooManyRequests()
			
			
			else:
				return profileo(
				profile_json=profile_handler.json(),
				w2l_temps_json=w2l_models.json(),
				tts_result_json=tts_results.json(),
				tts_models_json=tts_models.json(),
				w2l_result_json=w2l_results.json())
				
		except:raise RequestError("Something went wrong, Try again")
	
	def get_queue(self):
		try:
			queue=self.session.get("https://api.fakeyou.com/tts/queue_length").json()["pending_job_count"]
			return queue
		except:
			raise RequestError("Something went wrong, please try again or check your internet connection")
			
	def create_account(self,username:str,password:str,email:str):
		if len(username) < 3 :
			raise UsernameTooShort()
		
		if len(password) < 8:
			raise PasswordTooShort()
		
		if re.match("^[\w]+@([\w-]+\.)+[\w]+",email) == None:
			raise EmailInvalid()
		
		data={"username":username,"email_address":email,"password":password,"password_confirmation":password}
		
		handler=self.session.post(url="https://api.fakeyou.com/create_account",json=data)
		
		if handler.status_code == 400:
			error=handler.json()["error_type"]
			
			if error=="UsernameTaken" or error=="UsernameReserved":
				raise UsernameTaken()
			elif error=="EmailTaken":
				raise EmailTaken()
		elif handler.status_code==200:
				return "OK"
	
	def make_w2l_job(self,file:open,template_token):
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
			handler=self.session.post(url="https://api.fakeyou.com/w2l/inference",files=form)
			print("Done, sent")
			try:
				w2lJson=handler.json()
				print(w2lJson)
			except:
				raise RequestError("Please try again later")
			
			if handler.status_code==400:
				if w2lJson["error_reason"] == "Template does not exist":
					raise W2lTemplateTokenWrong()
				
			elif handler.status_code==429:
				raise TooManyRequests()
			
			elif handler.status_code==200:
				print("return")
				return w2lJson["inference_job_token"]
	def w2l_poll(self,ijt:str):
		while True:
			
			polling_handler=self.session.get(f"https://api.fakeyou.com/w2l/job/{ijt}")
			
			if polling_handler.status_code==200:
				try:pjs=polling_handler.json()
				except:raise RequestError("Something went wrong.","REQUEST CONTENT:",polling_handler.content)
				state=pjs["state"]["status"]
				if state == "complete_success":
					content=self.session.get("https://storage.googleapis.com/vocodes-public"+str(pjs["state"]["maybe_public_bucket_video_path"])).content
					return w2lo(pjs,content)
				if state == "Started":
					continue
				if state == "pending":
					continue
				if state == "dead" or state=="attempt_failed":
					raise Failed()
	
	def w2l(self,file:open,template_token:str) :
		ijt=self.make_w2l_job(file,template_token)
		w2l_polling = self.w2l_poll(ijt)
		return w2l_polling
	
	def delete_tts_result(self,result_token):
		data={"set_delete":True,"as_mod":True}
		handler=self.session.post(f"https://api.fakeyou.com/tts/result/{result_token}/delete",json=data)
		
		stats=handler.status_code
		
		if stats==200:
			return "DONE"
		elif stats==401:
			raise UnAuthorized(f"You're not authorized to delete tts result {result_token}")
		elif stats==404:
			raise TtsResultNotFound(result_token)
	
	def delete_w2l_result(self,result_token):
		data={"set_delete":True,"as_mod":False}
		handler=self.session.post(f"https://api.fakeyou.com/w2l/result/{result_token}/delete",json=data)
		
		stats=handler.status_code
		
		if stats==200:
			return "DONE"
		elif stats==401:
			raise UnAuthorized(f"You're not authorized to delete tts result {result_token}")
		elif stats==404:
			raise TtsResultNotFound(result_token)
	
	
	def logout(self):
		self.session.cookies.clear()
	
	