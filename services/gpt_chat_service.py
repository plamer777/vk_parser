"""This file contains the GPTChatVKGroupService class provides a business
logic to work with GPT chat"""
import json
from classes.group_classes import Group
from managers import ChatGPTManager
# --------------------------------------------------------------------------


class GPTChatVKGroupService:
    """The GPTChatVKGroupService with necessary methods to send requests and
    get responses from GPR chat"""
    def __init__(self, gpt_manager: ChatGPTManager) -> None:
        """Initialization of the GPTChatVKGroupService class
        :param gpt_manager: an instance of ChatGPTManager class provides
        access to Open AI API
        """
        self._gpt_manager = gpt_manager

    async def fill_group_tags_by_request(
            self, groups: list[Group], request: str,
            additional_role: dict[str, str] = None) -> list[Group]:
        """This method serves to generate tags by group data such as name,
        description, fixed post, etc. and add the tags to the provided group
        model
        :param groups: a list of Group instances containing VK group data
        :param additional_role: a dictionary with additional role of GPT such
        as system or assistant to change GPT chat behavior
        :param request: the string representing the request for GPT chat to
        generate tags
        :return: a list of Group instances containing VK group data with added
        tags
        """
        messages = [
            {'role': 'user', 'content': request}
        ]
        if additional_role:
            messages.insert(0, additional_role)
        response = await self._gpt_manager.get_completion(messages)
        tags: list[list] = json.loads(response)
        for group in groups:
            group.tags = ', '.join(tags.pop(0)) if tags else None

        return groups
