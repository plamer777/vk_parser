"""The file serves to store class instances used in the application"""
from managers import VKGroupManager, GoogleTableManager, ChatGPTManager
from services import VKGroupService, GPTChatVKGroupService, GoogleTableService
from controllers import VkGroupParseController
from constants import (
    TABLE_NAME, VK_TOKEN, GOOGLE_AUTH_FILE, GPT_API_KEY, GPT_MODEL)
# --------------------------------------------------------------------------

vk_manager = VKGroupManager(VK_TOKEN)
google_table_manager = GoogleTableManager(GOOGLE_AUTH_FILE, TABLE_NAME)
chat_gpt_manager = ChatGPTManager(GPT_API_KEY, GPT_MODEL)

vk_group_service = VKGroupService(vk_manager)
gpt_group_service = GPTChatVKGroupService(chat_gpt_manager)
google_table_service = GoogleTableService(google_table_manager)

vk_group_parse_controller = VkGroupParseController(
    vk_group_service, google_table_service, gpt_group_service)
