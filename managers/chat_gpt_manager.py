"""This file contains ChatGPTManager to get data from OpenAI API"""
import openai
# -------------------------------------------------------------------------


class ChatGPTManager:
    """The ChatGPTManager class provides access to the OpenAI API"""
    def __init__(
            self, api_key: str, gpt_model: str, api_url: str = None) -> None:
        """Initialize the ChatGPTManager class
        :param api_key: The OpenAI secret key to get access to the OpenAI API
        :param gpt_model: The name of the neuro model to work with
        """
        self._init_api(api_key, api_url)
        self._model = gpt_model

    @staticmethod
    def _init_api(api_key: str, api_url: str) -> None:
        """This method provides access to the OpenAI API
        :param api_key: The OpenAI secret key
        """
        openai.api_key = api_key
        if api_url:
            openai.api_base = api_url

    async def get_completion(
            self, messages: list[dict]) -> str | None:
        """This method serves to prepare provided request by GPT chat model
        and to return requested data
        :param messages: a list of dictionaries with GPT roles and content
        :return: the string representing the requested data or None if there
        was any error during the processing of the request
        """
        try:
            completion = await openai.ChatCompletion.acreate(
                model=self._model,
                messages=messages,
            )
            return completion.choices[0].message.content

        except Exception as e:
            print(f"Failed to create completion, the error is {e}")