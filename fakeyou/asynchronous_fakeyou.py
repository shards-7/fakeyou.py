import json
import re

import aiohttp

from .util import *


# Hey devs, I know you're looking through the code
# its messy, I'll comment it later.


class AsyncFakeYou:

    def __init__(self, verbose=False):
        self.session = None
        self.verbose = verbose
        self.base_url = "https://api.fakeyou.com/"
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get_session(self) -> aiohttp.ClientSession:
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(headers=self.headers)
        return self.session

    async def login(self, username, password):
        login_data = {"username_or_email": username, "password": password}

        async with await self.get_session() as session:
            async with session.post(self.base_url + "login", json=login_data) as response:
                data = await response.json()
                if response.status == 200 and data.get("success"):
                    if self.verbose:
                        print("Login success")
                    session_response = await session.get(self.base_url + "session")
                    session_data = await session_response.json()
                    if self.verbose:
                        print(session_data)
                    return Login(session_data)
                elif data.get("error_type") == "InvalidCredentials":
                    raise InvalidCredentials("check username or password")
                elif response.status == 429:
                    raise TooManyRequests("Too many requests, try again later or use a proxy.")

    async def list_voices(self, size: int = 25) -> ListVoice:
        if self.verbose:
            print("Getting voice list")
        async with await self.get_session() as session:
            async with session.get(url=self.base_url + "tts/list") as handler:

                if self.verbose:
                    print("Got all voices, sorting...")

                if handler.status == 429:
                    raise TooManyRequests("Too many requests, try again later or use a proxy.")

                hjson = await handler.json()

                if handler.status == 200:
                    return ListVoice(hjson, size=size)

    async def list_voice_categories(self, size: int = 25):
        if self.verbose:
            print("Getting voice categories")

        async with await self.get_session() as session:
            async with session.get(self.base_url + "category/list/tts") as handler:

                if self.verbose:
                    print("Got all categories, sorting...")

                if handler.status == 429:
                    raise TooManyRequests("Too many requests, try again later or use a proxy.")

                hjson = await handler.json()

                if handler.status == 200:
                    return Categories(hjson, size=size)

    async def get_voices_by_category(self, categoryToken: str):
        voices = await self.list_voices(size=0)
        found = {"models": []}
        if self.verbose:
            print("Looping through")
        for tokens, vjson in zip(voices.categoryTokens, voices.json):
            for token in tokens:
                if token == categoryToken:
                    found["models"].append(vjson)

        return ListVoice(json=found, size=0)

    async def make_tts_job(self, text: str, ttsModelToken: str, filename: str = "fakeyou.wav"):
        if self.verbose:
            print("getting job token")
        payload = {"uuid_idempotency_token": str(uuid4()), "tts_model_token": ttsModelToken, "inference_text": text}
        async with await self.get_session() as session:
            async with session.post(url=self.base_url + "tts/inference", data=json.dumps(payload)) as handler:

                if handler.status == 200:
                    aijt = await handler.json()
                    ijt = aijt["inference_job_token"]
                    return ijt
                elif handler.status == 400:
                    raise RequestError("check token and text, or contact the developer IG:@thedemonicat")
                elif handler.status == 429:
                    raise TooManyRequests("Too many requests, try again later or use a proxy.")

    async def tts_poll(self, ijt: str):
        while True:
            async with await self.get_session() as session:
                async with session.get(url=self.base_url + f"tts/job/{ijt}") as handler:
                    if handler.status == 200:
                        hjson = await handler.json()
                        wavo = Wav(hjson)
                        if self.verbose:
                            print("WAV STATUS :", wavo.status)

                        if wavo.status == "started":
                            continue
                        elif "pending" == wavo.status:
                            continue
                        elif "attempt_failed" == wavo.status:
                            raise Failed()

                        elif "dead" == wavo.status:
                            raise Dead()

                        elif "complete_success" == wavo.status:
                            if wavo.link:
                                async with session.get(wavo.link) as rcontent:
                                    del wavo
                                    return Wav(hjson, rcontent)
                            else:
                                raise PathNullError()
                    elif handler.status == 429:
                        raise TooManyRequests("Too many requests, try again later")

    async def say(self, text: str, ttsModelToken: str, filename: str = "fakeyou.wav"):
        ijt = await self.make_tts_job(text=text, ttsModelToken=ttsModelToken, filename=filename)
        return await self.tts_poll(ijt)

    async def get_tts_leaderboard(self):
        async with await self.get_session() as session:
            async with session.get(self.base_url + "leaderboard") as handler:
                if handler.status == 200:
                    ljson = await handler.json()
                    return TTSLeaderboard(ljson)

                if handler.status == 429:
                    raise TooManyRequests("Too many requests, try again later")

    async def get_w2l_leaderboard(self):
        async with await self.get_session() as session:
            async with session.get(self.base_url + "leaderboard") as handler:
                if handler.status == 200:
                    ljson = await handler.json()
                    return W2lLeaderboard(ljson)

                if handler.status == 429:
                    raise TooManyRequests("Too many requests, try again later")

    async def get_last_events(self):
        async with await self.get_session() as session:
            async with session.get(self.base_url + "events") as handler:
                if handler.status == 200:
                    ejson = await handler.json()
                    return Events(ejson)

                if handler.status == 429:
                    raise TooManyRequests("Too many requests, try again later")

    async def get_user(self, username: str, limit: int = 25):
        async with await self.get_session() as session:
            profile_handler = await session.get(self.base_url + f"user/{username}/profile")

            if profile_handler.status == 404:
                raise UserNotFound(username)

            tts_results = await session.get(self.base_url + f"user/{username}/tts_results?limit={limit}")
            w2l_results = await session.get(self.base_url + f"user/{username}/w2l_results?limit={limit}")
            tts_models = await session.get(self.base_url + f"user/{username}/tts_models?limit={limit}")
            w2l_models = await session.get(self.base_url + f"user/{username}/w2l_templates?limit={limit}")

            if profile_handler.status == 429 or w2l_models.status == 429:
                raise TooManyRequests()

            else:
                return Profile(
                    profile_json=await profile_handler.json(),
                    w2l_temps_json=await w2l_models.json(),
                    tts_result_json=await tts_results.json(),
                    tts_models_json=await tts_models.json(),
                    w2l_result_json=await w2l_results.json())

    async def get_queue(self):
        async with await self.get_session() as session:
            handler = await session.get("https://api.fakeyou.com/tts/queue_length")
            queue = await handler.json()

        return queue["pending_job_count"]

    async def create_account(self, username: str, password: str, email: str):
        if len(username) < 3:
            raise UsernameTooShort()

        if len(password) < 8:
            raise PasswordTooShort()

        if not re.match("^\w+@([\w-]+\.)+\w+", email):
            raise EmailInvalid()

        data = {"username": username, "email_address": email, "password": password, "password_confirmation": password}

        async with await self.get_session() as session:
            async with session.post(url="https://api.fakeyou.com/create_account", json=data) as handler:
                if handler.status == 400:
                    error = handler.json()["error_type"]

                    if error == "UsernameTaken" or error == "UsernameReserved":
                        raise UsernameTaken()
                    elif error == "EmailTaken":
                        raise EmailTaken()
                elif handler.status == 200:
                    return "OK"

    async def make_w2l_job(self, file: open, template_token):
        file_name = file.name.split("/").pop() if "/" in file.name else file.name
        form = {
            "template_token": template_token,
            "uuid_idempotency_token": str(uuid4()),
            "audio": (file_name, file.read(), "audio/mpeg")
        }
        async with await self.get_session() as session:
            async with session.post(url="https://api.fakeyou.com/w2l/inference", files=form) as handler:
                try:
                    w2lJson = handler.json()
                except:
                    raise RequestError("Please try again later")

                if handler.status == 400:
                    if w2lJson["error_reason"] == "Template does not exist":
                        raise W2lTemplateTokenWrong()

                elif handler.status == 429:
                    raise TooManyRequests()

                elif handler.status == 200:
                    return w2lJson["inference_job_token"]

    async def w2l_poll(self, ijt: str):
        async with await self.get_session() as session:
            while True:
                polling_handler = await session.get(f"https://api.fakeyou.com/w2l/job/{ijt}")
                if polling_handler.status == 200:
                    try:
                        pjs = polling_handler.json()
                    except:
                        raise RequestError("Something went wrong.", "REQUEST CONTENT:", polling_handler.content)

                    state = pjs["state"]["status"]

                    if state == "complete_success":
                        get_w2l_content = await session.get(
                            "https://storage.googleapis.com/vocodes-public" +
                            str(pjs["state"]["maybe_public_bucket_video_path"])
                        )
                        content = get_w2l_content.content
                        return W2Lo(pjs, content)

                    if state == "Started" or state == "pending":
                        continue

    async def w2l(self, file: open, template_token: str):
        ijt = await self.make_w2l_job(file, template_token)
        w2l_polling = await self.w2l_poll(ijt)
        return w2l_polling

    async def delete_tts_result(self, result_token):
        async with await self.get_session() as session:
            data = {"set_delete": True, "as_mod": True}
            handler = await session.post(f"https://api.fakeyou.com/tts/result/{result_token}/delete", json=data)

            stats = handler.status

            if stats == 200:
                return "DONE"
            elif stats == 401:
                raise UnAuthorized(f"You're not authorized to delete tts result {result_token}")
            elif stats == 404:
                raise TtsResultNotFound(result_token)

    async def delete_w2l_result(self, result_token):
        async with await self.get_session() as session:
            data = {"set_delete": True, "as_mod": False}
            handler = await session.post(f"https://api.fakeyou.com/w2l/result/{result_token}/delete", json=data)

            stats = handler.status

            if stats == 200:
                return "DONE"
            elif stats == 401:
                raise UnAuthorized(f"You're not authorized to delete tts result {result_token}")
            elif stats == 404:
                raise TtsResultNotFound(result_token)

    async def logout(self):
        async with await self.get_session() as session:
            session.cookie_jar.clear()
