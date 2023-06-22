"""This is a main file to run the application"""
from asyncio import run, create_task, gather
from constants import (
    GPT_GROUPS_LIMIT, MAX_GROUPS_TO_SEND, PARSE_OFFSET, PARSE_LIMIT,
    MAX_GROUPS_PER_REQUEST, FIELDS_TO_TEMPLATES, GET_POST_TEXT)
from container import vk_group_parse_controller
# --------------------------------------------------------------------------


async def main():
    """This is a main function to run the application"""
    group_ids = vk_group_parse_controller.get_vk_ids(
        offset=PARSE_OFFSET, limit=PARSE_LIMIT)
    tasks = []
    groups = vk_group_parse_controller.get_groups_by_ids(
        group_ids[:MAX_GROUPS_PER_REQUEST], get_post_text=GET_POST_TEXT)

    while group_ids:
        task = create_task(
            (vk_group_parse_controller
             .add_solvency_progression_education_to_group(
              groups[:GPT_GROUPS_LIMIT])))
        del groups[:GPT_GROUPS_LIMIT]
        del group_ids[:GPT_GROUPS_LIMIT]
        tasks.append(task)

        if (len(tasks) * GPT_GROUPS_LIMIT >= MAX_GROUPS_TO_SEND or
                not groups):
            prepared_data = await gather(*tasks)
            vk_group_parse_controller.send_groups_to_google_table(
                prepared_data, fields=FIELDS_TO_TEMPLATES)
            tasks.clear()

        if not groups:
            groups = vk_group_parse_controller.get_groups_by_ids(
                group_ids[:MAX_GROUPS_PER_REQUEST], get_post_text=GET_POST_TEXT)


if __name__ == '__main__':
    run(main())
