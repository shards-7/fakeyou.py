from uuid import uuid4

"""
Objects to return data in a dynmic way, no i won"t explain it all
and no comments should be here

its just objects
"""


class UserRatings:
    def __init__(self, json):
        self.positiveCount = json.get("positive_count")
        self.negativeCount = json.get("negative_count")
        self.totalCount = json.get("total_count")


class ListVoice:
    def __init__(self, json: dict, size):
        voices = json["models"]
        self.modelTokens = []
        self.ttsModelType = []
        self.creatorToken = []
        self.creatorUsername = []
        self.creatorDisplayName = []
        self.creatorGravatarHash = []
        self.title = []
        self.langTag = []
        self.isFrontPageFeatured = []
        self.isTwitchFeatured = []
        self.categoryTokens = []
        self.created = []
        self.lastUpdate = []
        self.user_ratings = []
        self.json = []

        for i in range(size):
            self.modelTokens.append(voices[i]["model_token"])
            self.ttsModelType.append(voices[i]["tts_model_type"])
            self.creatorToken.append(voices[i]["creator_user_token"])
            self.creatorUsername.append(voices[i]["creator_username"])
            self.creatorDisplayName.append(voices[i]["creator_display_name"])
            self.creatorGravatarHash.append(voices[i]["creator_gravatar_hash"])
            self.title.append(voices[i]["title"])
            self.langTag.append(voices[i]["ietf_language_tag"])
            self.isFrontPageFeatured.append(voices[i]["is_front_page_featured"])
            self.isTwitchFeatured.append(voices[i]["is_twitch_featured"])
            self.categoryTokens.append(voices[i]["category_tokens"])
            self.created.append(voices[i]["created_at"])
            self.lastUpdate.append(voices[i]["updated_at"])
            self.json.append(voices[i])
            self.user_ratings.append(UserRatings(voices[i].get("UserRatings", {})))

        else:
            for voice in voices:
                self.modelTokens.append(voice["model_token"])
                self.ttsModelType.append(voice["tts_model_type"])
                self.creatorToken.append(voice["creator_user_token"])
                self.creatorUsername.append(voice["creator_username"])
                self.creatorDisplayName.append(voice["creator_display_name"])
                self.creatorGravatarHash.append(voice["creator_gravatar_hash"])
                self.title.append(voice["title"])
                self.langTag.append(voice["ietf_language_tag"])
                self.isFrontPageFeatured.append(voice["is_front_page_featured"])
                self.isTwitchFeatured.append(voice["is_twitch_featured"])
                self.categoryTokens.append(voice["category_tokens"])
                self.created.append(voice["created_at"])
                self.lastUpdate.append(voice["updated_at"])
                self.json.append(voice)
                self.user_ratings.append(UserRatings(voice.get("UserRatings", {})))


class Categories:
    def __init__(self, json, size):
        categorizes = json["categories"]
        self.categoryToken = []
        self.modelType = []
        self.maybeSuperCategoryToken = []
        self.canDirectlyHaveModels = []
        self.canHaveSubCategories = []
        self.onlyModsApply = []
        self.name = []
        self.dropDownName = []
        self.isModApproved = []
        self.created = []
        self.lastUpdate = []
        self.deleted = []
        self.json = []

        if size != 0:
            for i in range(size):
                self.categoryToken.append(categorizes[i]["category_token"])
                self.modelType.append(categorizes[i]["model_type"])
                self.maybeSuperCategoryToken.append(categorizes[i]["maybe_super_category_token"])
                self.canDirectlyHaveModels.append(categorizes[i]["can_directly_have_models"])
                self.canHaveSubCategories.append(categorizes[i]["can_have_subcategories"])
                self.onlyModsApply.append(categorizes[i]["can_only_mods_apply"])
                self.name.append(categorizes[i]["name"])
                self.dropDownName.append(categorizes[i]["name_for_dropdown"])
                self.isModApproved.append(categorizes[i]["is_mod_approved"])
                self.created.append(categorizes[i]["created_at"])
                self.lastUpdate.append(categorizes[i]["updated_at"])
                self.deleted.append(categorizes[i]["deleted_at"])
                self.json.append(categorizes[i])
        else:
            for category in categorizes:
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


class Wav:
    def __init__(self, hjson, content=None):
        json = hjson["state"]
        self.json = json
        self.jobToken = json["job_token"]
        self.status = json["status"]
        self.resultToken = json["maybe_result_token"]

        if json["maybe_public_bucket_wav_audio_path"]:
            self.link = self.link = "https://storage.googleapis.com/vocodes-public" + str(
                json["maybe_public_bucket_wav_audio_path"])
        else:
            self.link = None

        self.title = json["title"]
        self.text = json["raw_inference_text"]
        if content:
            self.content = content

    def save(self, path=None):
        file_name = path or f"fakeyou_{self.title}_{str(uuid4()).replace('-', '_')}.wav"

        with open(file_name, "wb") as f:
            f.write(self.content if isinstance(self.content, bytes) else bytes(self.content, "utf-8"))

        return file_name


class Login:
    def __init__(self, sjson: dict):
        json = sjson["user"]

        self.json = json
        self.userToken = json.get("user_token")
        self.username = json.get("username")
        self.displayName = json.get("display_name")
        self.emailGravatarHash = json.get("email_gravatar_hash")
        self.plan = json.get("fakeyou_plan")
        self.canUseTTS = json.get("can_use_tts")
        self.canUseW2l = json.get("can_use_w2l")
        self.canDeleteOwnTtsResults = json.get("can_delete_own_tts_results")
        self.canDeleteOwnW2lResults = json.get("can_delete_own_w2l_results")
        self.canDeleteOwnAccount = json.get("can_delete_own_account")
        self.canUploadTtsModel = json.get("can_upload_tts_models")
        self.canUploadW2lTemp = json.get("can_upload_w2l_templates")
        self.canDeleteOwnTtsModels = json.get("can_delete_own_tts_models")
        self.canDeleteOwnW2lTemp = json.get("can_delete_own_w2l_templates")
        self.canApproveW2lTemp = json.get("can_approve_w2l_templates")
        self.canEditOtherUsersProfiles = json.get("can_edit_other_users_profiles")
        self.canEditUsersTts = json.get("can_edit_other_users_tts_models")
        self.canEditUsersW2l = json.get("can_edit_other_users_w2l_templates")
        self.canDeleteUsersTts = json.get("can_delete_other_users_tts_models")
        self.canDeleteUsersTtsResults = json.get("can_delete_other_users_tts_results")
        self.canDeleteUsersW2lTemp = json.get("can_delete_other_users_w2l_templates")
        self.canBanUsers = json.get("can_ban_users")
        self.canDeleteUsers = json.get("can_delete_users")


class TTSLeaderboard:

    def __init__(self, ljson):
        ls = ljson["tts_leaderboard"]
        self.json = []
        self.username = []
        self.displayName = []
        self.gravatarHash = []
        self.userToken = []
        self.uploadedCount = []

        for json in ls:
            self.json.append(json)
            self.username.append(json["username"])
            self.displayName.append(json["display_name"])
            self.gravatarHash.append(json["gravatar_hash"])
            self.userToken.append(json["creator_user_token"])
            self.uploadedCount.append(json["uploaded_count"])


class W2lLeaderboard:

    def __init__(self, ljson):
        ls = ljson["w2l_leaderboard"]
        self.json = []
        self.username = []
        self.displayName = []
        self.gravatarHash = []
        self.userToken = []
        self.uploadedCount = []

        for json in ls:
            self.json.append(json)
            self.username.append(json["username"])
            self.displayName.append(json["display_name"])
            self.gravatarHash.append(json["gravatar_hash"])
            self.userToken.append(json["creator_user_token"])
            self.uploadedCount.append(json["uploaded_count"])


class Events:

    def __init__(self, ejson):
        ls = ejson["Events"]
        self.json = []
        self.eventType = []
        self.maybeUserToken = []
        self.maybeUsername = []
        self.maybeDisplayName = []
        self.maybeGravatarHash = []
        self.maybeEntityToken = []
        self.created = []
        self.updated = []

        for json in ls:
            self.json.append(json)
            self.eventType.append(json["event_type"])
            self.maybeUserToken.append(json["maybe_target_user_token"])
            self.maybeUsername.append(json["maybe_target_username"])
            self.maybeDisplayName.append(json["maybe_target_display_name"])
            self.maybeGravatarHash.append(json["maybe_target_user_gravatar_hash"])
            self.maybeEntityToken.append(json["maybe_target_entity_token"])
            self.created.append(json["created_at"])
            self.updated.append(json["updated_at"])


class TTSResults:
    def __init__(self, tts_json):
        self.json = tts_json["results"]
        self.ttsResultToken = []
        self.ttsModelToken = []
        self.ttsModelTitle = []
        self.text = []
        self.maybeCreatorUserToken = []
        self.maybeCreatorUsername = []
        self.maybeCreatorName = []
        self.maybeCreatorResultId = []
        self.fileSize = []
        self.duration = []
        self.visibility = []
        self.created_date = []
        self.update_date = []
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


class W2lResults:
    def __init__(self, w2l_json):
        self.json = w2l_json["results"]
        self.w2lResultToken = []
        self.maybeW2lTemplateToken = []
        self.maybeTtsInferenceResultToken = []
        self.templateType = []
        self.templateTitle = []
        self.maybeCreatorUserToken = []
        self.maybeCreatorUsername = []
        self.maybeCreatorName = []
        self.maybeCreatorResultId = []
        self.fileSize = []
        self.width = []
        self.height = []
        self.duration = []
        self.visibility = []
        self.created_date = []
        self.update_date = []

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


class TTSModels:
    def __init__(self, models_json):
        self.json = models_json["models"]
        self.modelToken = []
        self.ttsModelType = []
        self.title = []
        self.ietfLanguageTag = []
        self.ietfPrimaryLanguagTag = []
        self.creatorUserToken = []
        self.creatorUsername = []
        self.creatorName = []
        self.gravatarHash = []
        self.isLockedFromUse = []
        self.isFrontPageFeatured = []
        self.isTwitchFeatured = []
        self.suggestedUniqeBotCommand = []
        self.created_date = []
        self.update_date = []

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


class W2lTemplates:
    def __init__(self, temp_json):
        self.json = temp_json["templates"]
        self.templateToken = []
        self.templateType = []
        self.creatorUserToken = []
        self.creatorUsername = []
        self.creatorName = []
        self.title = []
        self.width = []
        self.height = []
        self.duration = []
        self.previewUrl = []
        self.isPublicListingApproved = []
        self.created_date = []
        self.updated_date = []

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
                self.previewUrl.append(
                    "https://storage.googleapis.com/vocodes-public" + str(data["maybe_image_object_name"]))
            elif data["maybe_video_object_name"]:
                self.previewUrl.append(
                    "https://storage.googleapis.com/vocodes-public" + data["maybe_video_object_name"])
            self.isPublicListingApproved.append(data["is_public_listing_approved"])
            self.created_date.append(data["created_at"])
            self.updated_date.append(data["updated_at"])


class Badges:
    def __init__(self, badg_list):
        self.json = badg_list
        self.slug = []
        self.title = []
        self.description = []
        self.imageUrl = []
        self.grantedAt = []

        for data in self.json:
            self.slug.append(data["slug"])
            self.title.append(data["title"])
            self.description.append(data["description"])
            self.imageUrl.append(data["image_url"])
            self.grantedAt.append(data["granted_at"])


class User:
    def __init__(self, user_json):
        self.json = user_json
        self.userToken = self.json["user_token"]
        self.username = self.json["username"]
        self.name = self.json["display_name"]
        self.gravatarHash = self.json["email_gravatar_hash"]
        self.profileMarkdown = self.json["profile_markdown"]
        self.role = self.json["user_role_slug"]
        self.is_gravatar_disabled = self.json["disable_gravatar"]
        self.preferredTtsVisibiltiy = self.json["preferred_tts_result_visibility"]
        self.preferredW2lVisibiltiy = self.json["preferred_w2l_result_visibility"]
        self.discordUsername = self.json["discord_username"]
        self.twitchUsername = self.json["twitch_username"]
        self.twitterUsername = self.json["twitter_username"]
        self.patreonUsername = self.json["patreon_username"]
        self.githubUsername = self.json["github_username"]
        self.cashappUsername = self.json["cashapp_username"]
        self.url = self.json["website_url"]
        self.created_at = self.json["created_at"]


class Profile:
    def __init__(self, profile_json, w2l_temps_json, tts_models_json, tts_result_json, w2l_result_json):
        self.w2lTemplates = W2lTemplates(w2l_temps_json)
        self.ttsModels = TTSModels(tts_models_json)
        self.ttsResults = TTSResults(tts_result_json)
        self.w2lResults = W2lResults(w2l_result_json)
        self.badges = Badges(profile_json["user"]["badges"])

        self.json = profile_json
        self.user = User(profile_json["user"])


class W2Lo:

    def __init__(self, state_json, content):
        ij = state_json["state"]
        self.jobToken = ij["job_token"]
        self.status = ij["status"]
        self.maybeStatusDescription = ij["maybe_extra_status_description"]
        self.attemptCount = ij["attempt_count"]
        self.resultToken = ij["maybe_result_token"]
        self.link = "https://storage.googleapis.com/vocodes-public" + str(ij["maybe_public_bucket_video_path"])
        self.maybeW2lTemplateToken = ij["maybe_w2l_template_token"]
        self.w2lTemplateType = ij["w2l_template_type"]
        self.title = ij["title"]
        self.created_date = ij["created_at"]
        self.content = content

    def save(self, path=None):
        path = path or self.link.split("/").pop()

        with open(path, "wb") as f:
            f.write(self.content)
