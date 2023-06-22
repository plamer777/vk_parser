"""This file contains a VKGroupService provides a business logic to work with
VK groups"""
from classes.group_classes import Group
from managers import VKGroupManager
# -------------------------------------------------------------------------


class VKGroupService:
    """VKGroupService class has all necessary methods to get VK groups data"""
    def __init__(self, vk_manager: VKGroupManager) -> None:
        """Initialization of the class
        :param vk_manager: an instance of VKGroupManager class provides group
        data from VK API
        """
        self._vk_manager = vk_manager

    def get_groups_by_ids(
            self, groups: list[Group], get_post_text: bool = True) -> list[Group]:
        """This method serves to get VK groups from official VK API by
        the provided ids
        :param groups: a list of Group instances with their ids
        :param get_post_text: a boolean indicating if you need to turn VK
        post ids into its text
        :return: a list of models representing VK groups
        """
        try:
            ids = [group.id for group in groups]
            result = self._vk_manager.get_groups_by_ids(ids)
            if get_post_text:
                result = self._change_fixed_post_ids_to_text(result)

            for group in groups:
                if result and group.id == str(result[0].get('id')):
                    [setattr(group, key, value)
                     for key, value in result.pop(0).items()
                     if key in group.__dict__]

        except Exception as e:
            print(f'Failed to load VK groups, error: {e}')
            groups = None

        return groups

    def _change_fixed_post_ids_to_text(self, groups: list[dict]) -> list[dict]:
        """This method serves to change the fixed post ids into its text.
        If there is not a fixed post or fixed post was deleted then the fixed
        post field will be created and filled by the text of first post on
        the group's wall
        :param groups: a list of dicts representing the VK groups
        :return: a list of dicts representing the groups with the post texts
        """
        post_ids = self._create_fixed_post_ids_list(groups)
        fixed_posts = self._vk_manager.get_fixed_posts(post_ids)

        for group in groups:
            try:
                if fixed_posts and group.get('id') == -fixed_posts[0].get(
                        'owner_id'):
                    group['fixed_post'] = fixed_posts.pop(0)['text'][:500]

                if (not group.get('fixed_post') or
                        str(group.get('fixed_post')).strip() == 'Post deleted'):

                    group['fixed_post'] = (
                        self._vk_manager.get_post_text_by_group_id(
                            group.get('id'))[0]['text'][:500]
                    )

            except Exception as e:
                print(f'Failed to get post data from VK API, error: {e}')

        return groups

    @staticmethod
    def _create_fixed_post_ids_list(groups_list: list[dict]) -> list[str]:
        """This method serves to create a list of ids from group ids and post
        ids (for instance 51545154_2342) to use to get info about these posts
        :param groups_list: a list of dicts representing the VK groups
        :return: a list of strings with concatenated ids
        """
        groups_with_fixed_post = [
            group for group in groups_list if group.get('fixed_post')]
        posts_data = map(
            lambda x: f"-{x['id']}_{x['fixed_post']}", groups_with_fixed_post)

        return list(posts_data)
