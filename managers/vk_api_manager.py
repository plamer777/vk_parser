"""This file contains VKAPIManager to get data from VK API"""
import sys
from time import sleep
from vk_api import VkApi
from constants import (
    MAX_GROUPS_PER_REQUEST, MAX_POST_PER_REQUEST, VK_GROUP_FIELDS,
    GET_POST_ATTEMPTS)
from utils import split_data_list
# --------------------------------------------------------------------------


class VKGroupManager:
    """The VKAPIManager class provides access to the VK API"""
    def __init__(self, vk_token: str) -> None:
        """Initialize the VKAPIManager class
        :param vk_token: The token to get access to the VK API
        """
        self._client = VkApi(token=vk_token)

    def get_groups_by_ids(
            self, group_ids: list[str], delay: float = None,
            fields: list[str] = VK_GROUP_FIELDS,
            max_per_request: int = MAX_GROUPS_PER_REQUEST
    ) -> list[dict]:
        """This method returns a list of groups data from VK API found by its
        ids
        :param group_ids: a list of group ids
        :param delay: a float representing the amount of time to wait before
        returning the next part of groups (can be useful because of VK API
        restrictions on the number of requests per second)
        :param fields: a list of fields of groups to return
        :param max_per_request: an integer representing the maximum number of
        groups per single request (500 by default)
        :return: a list of dictionaries containing groups data
        """
        try:
            split_ids_list = split_data_list(
                group_ids, max_per_request)
            result = []
            for ids in split_ids_list:
                response = self._client.method(
                    'groups.getById', values={
                        'fields': ','.join(fields),
                        'group_ids': ','.join(ids)
                    })
                result.extend(response)
                if delay is not None:
                    sleep(delay)

            return result

        except Exception as e:
            sys.exit(f'Failed to get groups data from VK API, error: {e}')

    def get_post_text_by_group_id(
            self, group_id: str | int, count: int = 1, delay: float = 0.5
    ) -> list[dict]:
        """This method returns a list of dictionaries representing the posts
        of provided certain group
        :param group_id: a string or integer representing the group id
        :param count: an integer representing the number of posts to return
        :param delay: a float representing the seconds to wait before the
        next attempt to send request to the VK API. May be useful because of
        the limit of the number of requests per second
        :return: a list of strings representing the post texts
        """
        for _ in range(GET_POST_ATTEMPTS):
            try:
                posts_data = self._client.method(
                    'wall.get', values={
                        'owner_id': f'-{group_id}',
                        'filter': 'owner',
                        'count': count,
                    }
                )
                posts_details = posts_data['items']

                return posts_details

            except Exception as e:
                print(f'Failed to get post data from VK API, error: {e}')
                sleep(delay)

    def get_fixed_posts(self, post_ids: list[str]) -> list[dict]:
        """This method returns a list of dictionaries representing the fixed
        posts found by its ids
        :param post_ids: a list of strings representing the post ids
        :return: a list of strings representing the fixed posts
        """
        fixed_posts = []
        split_post_ids_list = split_data_list(
            list(post_ids), MAX_POST_PER_REQUEST)
        for row in split_post_ids_list:
            response = self._client.method(
                'wall.getById', values={
                    'posts': ','.join(row)
                })
            fixed_posts.extend(response)

        return fixed_posts
