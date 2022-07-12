
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
	
	def __init__(self,hjson):
		json=hjson["state"]
		self.json=json
		self.jobToken=json["job_token"]
		self.status=json["status"]
		self.resultToken=json["maybe_result_token"]
		self.maybePublicWavPath=json["maybe_public_bucket_wav_audio_path"]
		self.title=json["title"]
		self.text=json["raw_inference_text"]

class search():
	
	def __init__(self,vjson,cjson):
		self.voices=list_voice(json=vjson,size=0)
		self.categories=categories(json=cjson,size=0)