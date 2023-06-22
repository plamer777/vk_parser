"""This file contains utility functions"""
import re
from classes.group_classes import Group
# ------------------------------------------------------------------------


def get_ids_from_urls(urls: list[str]) -> list[str]:
    """This function serves to extract the group ids from the URLs
    :param urls: list of strings representing the URLs
    :return: list of strings representing the group ids
    """
    result = []
    for url in urls:
        uid = url.split('/')[-1].replace('club', '')
        result.append(uid)

    return result


def split_data_list(data_list: list, count: int) -> list[list]:
    """This function splits a list of any objects into a list of lists
    :param data_list: list of objects to split
    :param count: number of elements in each nested list to split
    :return: list of lists of objects
    """
    result = []
    while data_list:
        part = data_list[:count]
        result.append(part)
        del data_list[:count]
    return result


def create_group_info(
        groups: list[Group], template: str, fields: list[str]) -> str:
    """This function creates a string representing the group information from
    provided template and group fields
    :param groups: list of Group instances
    :param template: string representing the template to render
    :param fields: list of fields to be included in the template
    """
    result = ''
    for num, item in enumerate(groups, 1):
        result += template.format(
            num, *[getattr(item, field, None) for field in fields])

    return result


def clean_digits(data: str) -> str:
    try:
        pattern = re.compile(r'[^-0-9]*')
        result = pattern.sub('', data)
    except (ValueError, TypeError):
        result = data

    return result
