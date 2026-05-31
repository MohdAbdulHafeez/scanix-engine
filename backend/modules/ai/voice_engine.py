import os
import uuid
import asyncio
import tempfile

import whisper
import edge_tts


class VoiceEngine:

    def __init__(self):

        self.whisper_model = whisper.load_model(

            os.getenv(

                "WHISPER_MODEL",

                "base"

            )

        )

        self.voice_name = os.getenv(

            "VOICE_NAME",

            "en-US-JennyNeural"

        )

    # ===================================
    # Speech → Text
    # ===================================

    def speech_to_text(

        self,

        audio_path

    ):

        result = (

            self.whisper_model.transcribe(

                audio_path

            )

        )

        return {

            "transcript":

            result.get(

                "text",

                ""

            ).strip(),

            "language":

            result.get(

                "language",

                "unknown"

            )

        }

    # ===================================
    # Internal TTS
    # ===================================

    async def _tts(

        self,

        text,

        output_path

    ):

        communicate = (

            edge_tts.Communicate(

                text=text,

                voice=self.voice_name

            )

        )

        await communicate.save(

            output_path

        )

    # ===================================
    # Text → Speech
    # ===================================

    def text_to_speech(

        self,

        text

    ):

        output_path = os.path.join(

            tempfile.gettempdir(),

            f"{uuid.uuid4()}.mp3"

        )

        try:

            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:

                future = executor.submit(

                    lambda: asyncio.run(

                        self._tts(

                            text,

                            output_path

                        )

                    )

                )

                future.result(

                    timeout=30

                )

            if os.path.exists(

                output_path

            ):

                return output_path

        except Exception as e:

            print(

                f"TTS Error: {e}"

            )

        return None
    # ===================================
    # Voice Chat
    # ===================================

    def voice_chat(

        self,

        audio_path,

        nutrition_agent,

        ingredients_result,

        nutrition_result,

        trust_result,

        food_explainer=None,

        image_analysis=None

    ):

        speech = (

            self.speech_to_text(

                audio_path

            )

        )

        transcript = (

            speech.get(

                "transcript",

                ""

            )

        )

        if not transcript:

            return {

                "error":

                "VOICE_NOT_RECOGNIZED",

                "transcript": "",

                "answer":

                "Unable to understand audio."

            }

        response = (

            nutrition_agent.ask_voice(

                transcript=
                transcript,

                ingredients_result=
                ingredients_result,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result,

                food_explainer=
                food_explainer,

                image_analysis=
                image_analysis

            )

        )

        answer = (

            response.get(

                "answer",

                ""

            )

        )

        audio_file = None

        tts_status = "disabled"

        try:

            audio_file = (

                self.text_to_speech(

                    answer

                )

            )

            if audio_file:

                tts_status = "success"

            else:

                tts_status = "failed"

        except Exception:

            tts_status = "failed"
            
        return {

            "transcript":
            transcript,

            "answer":
            answer,

            "audio_file":
            audio_file,

            "tts_status":
            tts_status,

            "language":

            speech.get(

                "language",

                "unknown"

            ),

            "agent_response":
            response

        }

    # ===================================
    # Voice Profiles
    # ===================================

    AVAILABLE_VOICES = {

        "female":

        "en-US-JennyNeural",

        "male":

        "en-US-GuyNeural"

    }

    def set_voice(

        self,

        profile

    ):

        if profile in self.AVAILABLE_VOICES:

            self.voice_name = (

                self.AVAILABLE_VOICES[

                    profile

                ]

            )

            return True

        return False
    

    def tts_available(

        self

    ):

        try:

            test_voice = (

                edge_tts.list_voices

            )

            return True

        except Exception:

            return False
    
    def supported_formats(

        self

    ):

        return [

            ".wav",

            ".mp3",

            ".m4a",

            ".ogg",

            ".flac"

        ]