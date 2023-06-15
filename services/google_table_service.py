from typing import Iterable
from classes.group_classes import Group
from managers import GoogleTableManager
from utils import get_ids_from_urls
# --------------------------------------------------------------------------


class GoogleTableService:

    def __init__(
            self, table_manager: GoogleTableManager, model: type[Group] = Group
    ) -> None:
        self._table_manager = table_manager
        self._model = model

    def get_vk_ids_from_sheet(self) -> list[str] | None:
        """This method returns a list of vk_ids extracted from the provided
        urls
        :return: a list of vk_ids or None if there was any error during
        extracting vk ids from the given sheet
        """
        ids = get_ids_from_urls(
            self._table_manager.get_by_column())

        return ids

    def send_groups_to_sheet(
            self, groups: list[Group], col_range: str, fields: Iterable[str]
    ) -> None:
        """This method serves to send provided group data to Google sheet
        :param groups: a list of Group instances representing the group data
        :param col_range: the range of columns to update data in (for
        instance 'A3:B8')
        :param fields: An iterable containing field names that should be sent
        to the Google sheet (the order is important)
        """
        group_list = list(
            map(lambda x: [getattr(x, key, None) for key in fields], groups))
        self._table_manager.upload_to_sheet(col_range, group_list)
