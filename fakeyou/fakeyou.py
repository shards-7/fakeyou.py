import re

from .util import *


# Hey devs, I know you're looking through the code
# its messy, I'll comment it later.


class FakeYou(Service):
    def __init__(self, proxies: dict = None):
        Service.__init__(self, proxies)

    def login(self, username, password):
        data = {
            "username_or_email": username,
            "password": password
        }
        self.post("/login", data)
        return Login(self.get("/session").json())

    def get_voices(self, size: int = 0) -> ListVoice:
        return ListVoice(self.get("/tts/list").json(), size=size)

    def get_voice_categories(self, size: int = 25) -> Categories:
        return Categories(self.get("/category/list/tts").json(), size=size)

    def get_voices_by_category(self, category_token: str):
        voices = self.get_voices(size=0)
        found = {
            "models": [
                vjson for tokens, vjson in zip(voices.categoryTokens, voices.json) if category_token in tokens
            ]
        }
        return ListVoice(json=found, size=0)

    def make_tts_job(self, text: str, tts_model_token: str):
        data = {
            "uuid_idempotency_token": str(uuid4()),
            "tts_model_token": tts_model_token,
            "inference_text": text
        }
        return self.post("/tts/inference", data).json()["inference_job_token"]

    def tts_poll(self, ijt: str):
        while True:
            ijt_data = self.get(f"/tts/job/{ijt}").json()
            wav = Wav(ijt_data)
            status_cases = {
                "started": None,
                "pending": None,
                "attempt_failed": Failed(),
                "dead": Dead(),
                "complete_success": self.get_wav_content(wav, ijt_data)
            }
            status = status_cases.get(wav.status)

            if not status:
                continue

    def get_wav_content(self, wav, ijt_data):
        if wav.link:
            content = self.get(wav.link).content
            del wav
            return Wav(ijt_data, content)
        else:
            raise PathNullError()

    def say(self, text: str, tts_model_token: str):
        return self.tts_poll(self.make_tts_job(text=text, tts_model_token=tts_model_token))

    def tts_status(self, ijt: str):
        return self.get(f"/tts/job/{ijt}").json()["state"]["status"]

    def get_tts_leaderboard(self):
        return TTSLeaderboard(self.get("/leaderboard").json())

    def get_w2l_leaderboard(self):
        return W2lLeaderboard(self.get("/leaderboard").json())

    def get_last_events(self):
        return Events(self.get("/events").json())

    def get_user(self, username: str, limit: int = 25):
        profile_handler = self.get(f"/user/{username}/profile")
        limit = {"limit": limit}
        tts_results = self.get(f"/user/{username}/tts_results", params=limit)
        w2l_results = self.get(f"/user/{username}/w2l_results", params=limit)
        tts_models = self.get(f"/user/{username}/tts_models", params=limit)
        w2l_models = self.get(f"/user/{username}/w2l_templates", params=limit)

        return Profile(
            profile_json=profile_handler.json(),
            w2l_temps_json=w2l_models.json(),
            tts_result_json=tts_results.json(),
            tts_models_json=tts_models.json(),
            w2l_result_json=w2l_results.json()
        )

    def get_queue_length(self):
        return self.get("/tts/queue_length").json()["pending_job_count"]

    def create_account(self, username: str, email: str, password: str):
        if len(username) < 3:
            raise UsernameTooShort()

        if not re.match(r"^\w+@([\w-]+\.)+\w+$", email):
            raise EmailInvalid()

        if len(password) < 8:
            raise PasswordTooShort()

        data = {
            "username": username,
            "email_address": email,
            "password": password,
            "password_confirmation": password
        }
        return self.post("/create_account", data)

    def get_w2l_inference(self, file: open, template_token):
        file_name = file.name.split("/").pop() if "/" in file.name else file.name

        form = {
            "template_token": template_token,
            "uuid_idempotency_token": str(uuid4()),
            "audio": (file_name, file.read(), "audio/mpeg")
        }

        return self.post("/w2l/inference", files=form).json()["inference_job_token"]

    def w2l_poll(self, ijt: str):
        while True:
            pjs = self.get(f"/w2l/job/{ijt}").json()
            state = pjs["state"]["status"]

            if state == "complete_success":
                bucket_path = str(pjs["state"]["maybe_public_bucket_video_path"])
                content = self.get(f"https://storage.googleapis.com/vocodes-public{bucket_path}").content
                return W2Lo(pjs, content)

    def w2l(self, file: open, template_token: str):
        return self.w2l_poll(self.get_w2l_inference(file, template_token))

    def delete_tts_result(self, result_token):
        data = {"set_delete": True, "as_mod": True}
        return self.post(f"/tts/result/{result_token}/delete", data)

    def delete_w2l_result(self, result_token):
        data = {"set_delete": True, "as_mod": False}
        return self.post(f"/w2l/result/{result_token}/delete", data)

    def logout(self):
        self.clear_cookies()
