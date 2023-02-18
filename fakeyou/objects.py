from uuid import uuid4
"""
Objects to return data in a dynmic way, no i won't explain it all
and no comments should be here

its just objects
"""
class list_voice():
	def __init__(self,json:dict,size):
		voicels=json["models"]
		self.modelTokens=[]
		self.ttsModelType=[]
		self.creatorToken=[]
		self.creatorUsername=[]
		self.creatorDisplayName=[]
		self.creatorGavatarHash=[]
		self.title=[]
		self.langTag=[]
		self.isFrontPageFeatured=[]
		self.isTwitchFeatured=[]
		self.categoryTokens=[]
		self.created=[]
		self.lastUpdate=[]
		self.json=[]
		if size!=0:
			for i in range(size):
				self.modelTokens.append(voicels[i]["model_token"])
				self.ttsModelType.append(voicels[i]["tts_model_type"])
				self.creatorToken.append(voicels[i]["creator_user_token"])
				self.creatorUsername.append(voicels[i]["creator_username"])
				self.creatorDisplayName.append(voicels[i]["creator_display_name"])
				self.creatorGavatarHash.append(voicels[i]["creator_gravatar_hash"])
				self.title.append(voicels[i]["title"])
				self.langTag.append(voicels[i]["ietf_language_tag"])
				self.isFrontPageFeatured.append(voicels[i]["is_front_page_featured"])
				self.isTwitchFeatured.append(voicels[i]["is_twitch_featured"])
				self.categoryTokens.append(voicels[i]["category_tokens"])
				self.created.append(voicels[i]["created_at"])
				self.lastUpdate.append(voicels[i]["updated_at"])
				self.json.append(voicels[i])
		else:
			for voice in voicels:
				self.modelTokens.append(voice["model_token"])
				self.ttsModelType.append(voice["tts_model_type"])
				self.creatorToken.append(voice["creator_user_token"])
				self.creatorUsername.append(voice["creator_username"])
				self.creatorDisplayName.append(voice["creator_display_name"])
				self.creatorGavatarHash.append(voice["creator_gravatar_hash"])
				self.title.append(voice["title"])
				self.langTag.append(voice["ietf_language_tag"])
				self.isFrontPageFeatured.append(voice["is_front_page_featured"])
				self.isTwitchFeatured.append(voice["is_twitch_featured"])
				self.categoryTokens.append(voice["category_tokens"])
				self.created.append(voice["created_at"])
				self.lastUpdate.append(voice["updated_at"])
				self.json.append(voice)
		
class categories():
	def __init__(self,json,size):
		categoriesls=json["categories"]
		self.categoryToken=[]
		self.modelType=[]
		self.maybeSuperCategoryToken=[]
		self.canDirectlyHaveModels=[]
		self.canHaveSubCategories=[]
		self.onlyModsApply=[]
		self.name=[]
		self.dropDownName=[]
		self.isModApproved=[]
		self.created=[]
		self.lastUpdate=[]
		self.deleted=[]
		self.json=[]
		if size!=0:
			for i in range(size):
				self.categoryToken.append(categoriesls[i]["category_token"])
				self.modelType.append(categoriesls[i]["model_type"])
				self.maybeSuperCategoryToken.append(categoriesls[i]["maybe_super_category_token"])
				self.canDirectlyHaveModels.append(categoriesls[i]["can_directly_have_models"])
				self.canHaveSubCategories.append(categoriesls[i]["can_have_subcategories"])
				self.onlyModsApply.append(categoriesls[i]["can_only_mods_apply"])
				self.name.append(categoriesls[i]["name"])
				self.dropDownName.append(categoriesls[i]["name_for_dropdown"])
				self.isModApproved.append(categoriesls[i]["is_mod_approved"])
				self.created.append(categoriesls[i]["created_at"])
				self.lastUpdate.append(categoriesls[i]["updated_at"])
				self.deleted.append(categoriesls[i]["deleted_at"])
				self.json.append(categoriesls[i])
		else:
			for category in categoriesls:
				self.categoryToken.append(category["category_token"])
				self.modelType.append(category["model_type"])
				self.maybeSuperCategoryToken.append(category["maybe_super_category_token"])
				self.canDirectlyHaveModels.append(category["can_directly_have_models"])
				self.canHaveSubCategories.append(category["can_have_subcategories"])
				self.onlyModsApply.append(category["can_only_mods_apply"])
				self.name.append(category["name"])
				self.dropDownName.append(category["name_for_dropdown"])
				self.isModApproved.append(category["is_mod_approved"])
				self.created.append(category["created_at"])
				self.lastUpdate.append(category["updated_at"])
				self.deleted.append(category["deleted_at"])
				self.json.append(category)

class wav():
	
	def __init__(self,hjson,content=None):
		json=hjson["state"]
		self.json=json
		self.jobToken=json["job_token"]
		self.status=json["status"]
		self.resultToken=json["maybe_result_token"]
		if json["maybe_public_bucket_wav_audio_path"] != None:
			self.link=self.link="https://storage.googleapis.com/vocodes-public"+str(json["maybe_public_bucket_wav_audio_path"])
		else:
			self.link=None
		self.title=json["title"]
		self.text=json["raw_inference_text"]
		if content:
			self.content=content
	
	def save(self,path=None):
		if path==None:
			
			with open(path,"wb") as f:
				f.write(self.content)
				f.close()
		else:
			file_name=f"fakeyou_{self.title}_{str(uuid4()).replace('-','_')}.wav"
			with open(f"", "wb") as f:
				f.write(bytes(self.content,"utf-8"))
				f.close()
			return file_name

class login():
	
	def __init__(self,sjson:dict):
		json=sjson["user"]
		
		self.json=json
		self.userToken=json["user_token"]
		self.username=json["username"]
		self.displayName=json['display_name']
		self.emailGravatarHash=json['email_gravatar_hash']
		self.plan=json['fakeyou_plan']
		self.canUseTTS=json['can_use_tts']
		self.canUseW2l=json['can_use_w2l']
		self.canDeleteOwnTtsResults=json['can_delete_own_tts_results']
		self.canDeleteOwnW2lResults=json['can_delete_own_w2l_results']
		self.canDeleteOwnAccount=json['can_delete_own_account']
		self.canUploadTtsModel=json['can_upload_tts_models']
		self.canUploadW2lTemp=json['can_upload_w2l_templates']
		self.canDeleteOwnTtsModels=json['can_delete_own_tts_models']
		self.canDeleteOwnW2lTemp=json['can_delete_own_w2l_templates']
		self.canApproveW2lTemp=json['can_approve_w2l_templates']
		self.canEditOtherUsersProfiles=json['can_edit_other_users_profiles']
		self.canEditUsersTts=json['can_edit_other_users_tts_models']
		self.canEditUsersW2l=json['can_edit_other_users_w2l_templates']
		self.canDeleteUsersTts=json['can_delete_other_users_tts_models']
		self.canDeleteUsersTtsResults=json['can_delete_other_users_tts_results']
		self.canDeleteUsersW2lTemp=json['can_delete_other_users_w2l_templates']
		self.canBanUsers=json['can_ban_users']
		self.canDeleteUsers=['can_delete_users']
		


class ttsleaderboard():
	
	def __init__(self,ljson):
		ls=ljson['tts_leaderboard']
		self.json=[]
		self.username=[]
		self.displayName=[]
		self.gravatarHash=[]
		self.userToken=[]
		self.uploadedCount=[]
		
		for json in ls:
			self.json.append(json)
			self.username.append(json['username'])
			self.displayName.append(json['display_name'])
			self.gravatarHash.append(json["gravatar_hash"])
			self.userToken.append(json["creator_user_token"])
			self.uploadedCount.append(json["uploaded_count"])

class w2lleaderboard():
	
	def __init__(self,ljson):
		ls=ljson['w2l_leaderboard']
		self.json=[]
		self.username=[]
		self.displayName=[]
		self.gravatarHash=[]
		self.userToken=[]
		self.uploadedCount=[]
		
		for json in ls:
			self.json.append(json)
			self.username.append(json['username'])
			self.displayName.append(json['display_name'])
			self.gravatarHash.append(json["gravatar_hash"])
			self.userToken.append(json["creator_user_token"])
			self.uploadedCount.append(json["uploaded_count"])

class events():
	
	def __init__(self,ejson):
		ls=ejson["events"]
		self.json=[]
		self.eventType=[]
		self.maybeUserToken=[]
		self.maybeUsername=[]
		self.maybeDisplayName=[]
		self.maybeGavatarHash=[]
		self.maybeEntityToken=[]
		self.created=[]
		self.updated=[]
		
		for json in ls:
			self.json.append(json)
			self.eventType.append(json['event_type'])
			self.maybeUserToken.append(json["maybe_target_user_token"])
			self.maybeUsername.append(json['maybe_target_username'])
			self.maybeDisplayName.append(json["maybe_target_display_name"])
			self.maybeGavatarHash.append(json["maybe_target_user_gravatar_hash"])
			self.maybeEntityToken.append(json["maybe_target_entity_token"])
			self.created.append(json["created_at"])
			self.updated.append(json["updated_at"])

class _tts_results():
	def __init__(self,ttsJson):
		self.json=ttsJson["results"]
		self.ttsResultToken=[]
		self.ttsModelToken=[]
		self.ttsModelTitle=[]
		self.text=[]
		self.maybeCreatorUserToken=[]
		self.maybeCreatorUsername=[]
		self.maybeCreatorName=[]
		self.maybeCreatorResultId=[]
		self.fileSize=[]
		self.duration=[]
		self.visibility=[]
		self.created_date=[]
		self.update_date=[]
		for data in self.json:
			self.ttsResultToken.append(data["tts_result_token"])
			self.ttsModelToken.append(data["tts_model_token"])
			self.ttsModelTitle.append(data["tts_model_title"])
			self.text.append(data["raw_inference_text"])
			self.maybeCreatorUserToken.append(data["maybe_creator_user_token"])
			self.maybeCreatorUsername.append(data["maybe_creator_username"])
			self.maybeCreatorName.append(data["maybe_creator_display_name"])
			self.maybeCreatorResultId.append(data["maybe_creator_result_id"])
			self.fileSize.append(data["file_size_bytes"])
			self.duration.append(data["duration_millis"])
			self.visibility.append(data["visibility"])
			self.created_date.append(data["updated_at"])

class _w2l_results():
	def __init__(self,w2lJson):
		self.json=w2lJson["results"]
		self.w2lResultToken=[]
		self.maybeW2lTemplateToken=[]
		self.maybeTtsInferenceResultToken=[]
		self.templateType=[]
		self.templateTitle=[]
		self.maybeCreatorUserToken=[]
		self.maybeCreatorUsername=[]
		self.maybeCreatorName=[]
		self.maybeCreatorResultId=[]
		self.fileSize=[]
		self.width=[]
		self.height=[]
		self.duration=[]
		self.visibility=[]
		self.created_date=[]
		self.update_date=[]
		
		for data in self.json:
			self.w2lResultToken.append(data["w2l_result_token"])
			self.maybeW2lTemplateToken.append(data["maybe_w2l_template_token"])
			self.maybeTtsInferenceResultToken.append(data["maybe_tts_inference_result_token"])
			self.templateType.append(data["template_type"])
			self.templateTitle.append(data["template_title"])
			self.maybeCreatorUserToken.append(data["maybe_creator_user_token"])
			self.maybeCreatorUsername.append(data["maybe_creator_username"])
			self.maybeCreatorName.append(data["maybe_creator_display_name"])
			self.maybeCreatorResultId.append(data["maybe_creator_result_id"])
			self.fileSize.append(data["file_size_bytes"])
			self.width.append(data["frame_width"])
			self.height.append(data["frame_height"])
			self.duration.append(data["duration_millis"])
			self.visibility.append(data["visibility"])
			self.created_date.append(data["created_at"])
			self.update_date.append(data["updated_at"])

class _tts_models():
	def __init__(self,modelsJson):
		self.json=modelsJson["models"]
		self.modelToken=[]
		self.ttsModelType=[]
		self.title=[]
		self.ietfLanguageTag=[]
		self.ietfPrimaryLanguagTag=[]
		self.creatorUserToken=[]
		self.creatorUsername=[]
		self.creatorName=[]
		self.gravatarHash=[]
		self.isLockedFromUse=[]
		self.isFrontPageFeatured=[]
		self.isTwitchFeatured=[]
		self.suggestedUniqeBotCommand=[]
		self.created_date=[]
		self.update_date=[]
		
		for data in self.json:
			self.modelToken.append(data["model_token"])
			self.ttsModelType.append(data["tts_model_type"])
			self.title.append(data["title"])
			self.ietfLanguageTag.append(data["ietf_language_tag"])
			self.ietfPrimaryLanguagTag.append(data["ietf_primary_language_subtag"])
			self.creatorUserToken.append(data["creator_user_token"])
			self.creatorUsername.append(data["creator_username"])
			self.creatorName.append(data["creator_display_name"])
			self.gravatarHash.append(data["creator_gravatar_hash"])
			self.isLockedFromUse.append(data["is_locked_from_use"])
			self.isFrontPageFeatured.append(data["is_front_page_featured":])
			self.isTwitchFeatured.append(data["is_twitch_featured"])
			self.suggestedUniqeBotCommand.append(data["maybe_suggested_unique_bot_command"])
			self.created_date.append(data["created_at"])
			self.update_date.append(data["updated_at"])
class _w2l_templates():
	def __init__(self,tempJson):
		self.json=tempJson["templates"]
		self.templateToken=[]
		self.templateType=[]
		self.creatorUserToken=[]
		self.creatorUsername=[]
		self.creatorName=[]
		self.title=[]
		self.width=[]
		self.height=[]
		self.duration=[]
		self.previewUrl=[]
		self.isPublicListingApproved=[]
		self.created_date=[]
		self.updated_date=[]
		
		for data in self.json:
			self.templateToken.append(data["template_token"])
			self.templateType.append(data["template_type"])
			self.creatorUserToken.append(data["creator_user_token"])
			self.creatorUsername.append(data["creator_username"])
			self.creatorName.append(data["creator_username"])
			self.title.append(data["title"])
			self.width.append(data["frame_width"])
			self.height.append(data["frame_height"])
			self.duration.append(data["duration_millis"])
			if data["maybe_image_object_name"]:
				self.previewUrl.append("https://storage.googleapis.com/vocodes-public"+str(data["maybe_image_object_name"]))
			elif data["maybe_video_object_name"]:
				self.previewUrl.append("https://storage.googleapis.com/vocodes-public"+data["maybe_video_object_name"])
			self.isPublicListingApproved.append(data["is_public_listing_approved"])
			self.created_date.append(data["created_at"])
			self.updated_date.append(data["updated_at"])
class _badges():
	def __init__(self,badgList):
		
		self.json=badgList
		self.slug=[]
		self.title=[]
		self.description=[]
		self.imageUrl=[]
		self.grantedAt=[]
		
		for data in self.json:
			self.slug.append(data["slug"])
			self.title.append(data["title"])
			self.description.append(data["description"])
			self.imageUrl.append(data["image_url"])
			self.grantedAt.append(data["granted_at"])
class _user():
	def __init__(self,userJson):
		self.json=userJson
		self.userToken=userJson["user_token"]
		self.username=userJson["username"]
		self.name=userJson["display_name"]
		self.gravatarHash=userJson["email_gravatar_hash"]
		self.profileMarkdown=userJson["profile_markdown"]
		self.role=userJson["user_role_slug"]
		self.is_gravatar_disabled=userJson["disable_gravatar"]
		self.preferredTtsVisibiltiy=userJson["preferred_tts_result_visibility"]
		self.preferredW2lVisibiltiy=userJson["preferred_w2l_result_visibility"]
		self.discordUsername=userJson["discord_username"]
		self.twitchUsername=userJson["twitch_username"]
		self.twitterUsername=userJson["twitter_username"]
		self.patreonUsername=userJson["patreon_username"]
		self.githubUsername=userJson["github_username"]
		self.cashappUsername=userJson["cashapp_username"]
		self.url=userJson["website_url"]
		self.created_at=userJson["created_at"]
class profileo():
	
	def __init__(self,profile_json,w2l_temps_json,tts_models_json,tts_result_json,w2l_result_json):
		self.w2lTemplates=_w2l_templates(w2l_temps_json)
		self.ttsModels=_tts_models(tts_models_json)
		self.ttsResults=_tts_results(tts_result_json)
		self.w2lResults=_w2l_results(w2l_result_json)
		self.badges=_badges(profile_json["user"]["badges"])
		
		self.json=profile_json
		self.user=_user(profile_json["user"])

class w2lo():
	
	def __init__(self,stateJson,content):
	
		ij=stateJson["state"]
		self.jobToken=ij["job_token"]
		self.status=ij["status"]
		self.maybeStatusDescription=ij["maybe_extra_status_description"]
		self.attemptCount=ij["attempt_count"]
		self.resultToken=ij["maybe_result_token"]
		self.link="https://storage.googleapis.com/vocodes-public"+str(ij["maybe_public_bucket_video_path"])
		self.maybeW2lTemplateToken=ij["maybe_w2l_template_token"]
		self.w2lTemplateType=ij["w2l_template_type"]
		self.title=ij["title"]
		self.created_date=ij["created_at"]
		self.content=content
	
	def save(self,path=None):
		if path==None:
			name=self.link.split("/").pop()
			with open(name,"wb") as f:
				f.write(self.content)
		else:
			with open(path, "wb") as f:
				f.write(self.content)