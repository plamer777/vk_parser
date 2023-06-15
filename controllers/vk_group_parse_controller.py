"""This file contains a VkGroupParseController processing parsing process"""
from typing import Iterable
from constants import (
    GPT_REQUEST_TEMPLATE, UPLOAD_FIELDS, GROUP_DATA_TEMPLATE, VK_GROUP_FIELDS,
    MAX_GPT_ATTEMPTS, SYSTEM_ROLE, DATA_COLUMNS_TEMPLATE)
from classes.group_classes import Group
from utils import create_group_info
from services.vk_group_service import VKGroupService
from services.google_table_service import GoogleTableService
from services.gpt_chat_service import GPTChatVKGroupService
# ---------------------------------------------------------------------------


class VkGroupParseController:
    """The VkGroupParseController class contains a logic to get data from
    Google sheet by provided name and column, process uploaded data and send
    necessary data to the Google sheet"""
    def __init__(
            self, vk_service: VKGroupService, table_service: GoogleTableService,
            gpt_service: GPTChatVKGroupService, group_model: type[Group] = Group
    ) -> None:
        """Initialize the VkGroupParseController class
        :param vk_service: an instance of VKGroupService class
        :param table_service: an instance of GoogleTableService class
        :param gpt_service: an instance of GPTChatVKGroupService class
        :param group_model: a class representing a model of VK group
        """
        self._vk_service = vk_service
        self._table_service = table_service
        self._gpt_service = gpt_service
        self._model = group_model

    async def add_tags_to_group_data(
            self, groups: list[Group],
            gpt_chat_request_template: str = GPT_REQUEST_TEMPLATE,
            group_info_template: str = GROUP_DATA_TEMPLATE,
            fields: list[str] = VK_GROUP_FIELDS,
            additional_role: dict[str, str] = SYSTEM_ROLE
    ) -> list[Group]:
        """This method serves to generate tags by group data such as name,
        description, fixed post and add the tags to the group models
        :param groups: a list of Group instances containing VK group data
        :param gpt_chat_request_template: a string representing the template
        for GPT chat request
        :param group_info_template: A template to create a string
        representing multiple groups data
        :param additional_role: a dictionary with additional role of GPT such
        as system or assistant to change GPT chat behavior
        :param fields: a list of strings representing fields that should be
        added to group_info_template
        :return: a list of dictionaries containing VK group data with added
        tags
        """
        for _ in range(MAX_GPT_ATTEMPTS):
            try:
                request = gpt_chat_request_template.format(
                    create_group_info(groups, group_info_template, fields))
                result = await self._gpt_service.fill_group_tags_by_request(
                    groups, request, additional_role)

                return result

            except Exception as e:
                print(f'The was an error during creating tags: {e}. One more '
                      f'attempt')
        return groups

    def get_vk_ids(
            self, offset: int = 0, limit: int = None, start_num: int = 1
    ) -> list[Group]:
        """This method returns a list of VK ids extracted from urls
        downloaded from the provided Google sheet
        :param limit: the maximum number of ids to return
        :param offset: the offset from the start of the ids list
        :param start_num: the first sheet row number to start enumeration with
        :return: a list of GroupId instances
        """
        ids = self._table_service.get_vk_ids_from_sheet()

        if not limit:
            limit = len(ids)

        models = [
            self._model(column_num=num, id=group_id)
            for num, group_id in enumerate(ids, start_num)]
        models = models[offset:offset + limit]

        return models

    def get_groups_by_ids(
            self, groups: list[Group]) -> list[Group] | None:
        """This method serves to get VK groups from official VK API by 
        provided groups filled with ids
        :param groups: a list of strings representing VK group ids
        :return: a list of dictionaries representing VK group data
        """
        result = self._vk_service.get_groups_by_ids(groups)
        return result

    def send_groups_to_google_table(
            self, groups: list[list[Group]],
            col_template: str = DATA_COLUMNS_TEMPLATE,
            fields: Iterable[str] = UPLOAD_FIELDS
    ) -> None:
        """This method serves to send provided group data to Google sheet
        :param groups: a list of Group instances representing the group data
        :param col_template: the string representing the template of columns to
         update data in (for instance 'A{0}:B{1}')
        :param fields: An iterable containing field names that should be sent
        to the Google sheet (the order is important)
        """
        prepared_groups = []
        [prepared_groups.extend(item) for item in groups]

        col_range = col_template.format(
            prepared_groups[0].column_num, prepared_groups[-1].column_num)

        self._table_service.send_groups_to_sheet(
            prepared_groups, col_range, fields)

        print(f'{prepared_groups}\nSent to Google sheet successfully')
