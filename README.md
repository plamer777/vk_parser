# The GPT VK Parser
The application uploads VK group URLs from Google table, extracts ids, parse VK groups data by using 
official API, creates tags and make predictions about user solvency, self-education and progression 
depending on title, description, fixed post and status by using GPT chat and returns result to the Google sheet.

The app provides functionality as follows:
 - To download urls from Google sheet
 - To get group data from VK API
 - To generate 3 tags by using GPT chat
 - To make predictions about user solvency, self-education and progression
 - To send prepared group data to Google sheet
 - To set different parameters such as group batch to parse per request and to send to Google sheet,
batch of groups to send to GPT chat to generate tags and so on
 
---

**Technologies used in the project:**
 
 - VK API
 - Gspread 
 - Asyncio
 - Open AI
 - Pydantic
 - Docker
 - Docker-compose

---

**Project's structure:**
 
 - auth_data - An auth file with Google keys
 - classes - Pydantic classes representing VK group
 - managers - classes to get access to VK API, Google table and Open AI
 - services - objects providing business logic for managers
 - constants.py - constants to configure the application
 - controllers - controller classes to manage different parsing services
 - container.py - manager, service and controller instances
 - Docker-compose.yaml - main file to start the application by using Docker
 - Dockerfile - description of the image to create API container 
 - main.py - a main file to run the application
 - utils.py - utility functions
 - README.md - this file with project description
 - requirements.txt - requirements for the application
---

**How to start the project:**
First of all you have to prepare keys and tokens to get access to the VK API, Open AI API and Google API.
- To get VK API token just use this link and press blue button to continue:
https://oauth.vk.com/authorize?client_id=6478436&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.95
- To get OpenAI API token you can use this tutorial for example:
https://diegoinacio.github.io/machine-learning-notebooks-page/pages/connect_openai_api.html
- To get Google API key I can recommend this amazing tutorial with pictures:
https://dvsemenov.ru/google-tablicy-i-python-podrobnoe-rukovodstvo-s-primerami/#__Google_Api_Console

To start the app just follow the next steps:
 - Clone the repository
 - Prepare .env file by using .env-example file and info provided below
 - Put the Google auth file into auth_data directory (create directory if it doesn't exist)
 - Prepare settings in the constants.py file following the steps provided below
 - Create and activate virtual environment
 - Set up all requirements provided in the requirements.txt file
 - Change main.py file by your needs if you want to generate tags or make predictions or both (new method was added
in the VkGroupParseController in 22 June 2023)
 - Run the application by using the command: `python3 main.py`

---

Settings:
- GOOGLE_AUTH_FILE = path.join('auth_data', env_sets.GOOGLE_KEY_FILE) - path to your Google authentication file
- VK_TOKEN = env_sets.VK_TOKEN - your VK token to get access to VK API

- TABLE_NAME = 'vk parser' - the name of Google table the data is stored in (do not confuse with the sheet name)
- URL_COLUMN = 2 - the number of column the VK group URLs is stored in
- PARSE_SHEET = 'вся база' - the name of the Google sheet with parse data
- MAX_GROUPS_PER_REQUEST = 100 - the maximum number of groups to get from the VK API by single request
- MAX_POST_PER_REQUEST = 50 - the maximum number of posts to get from the VK API by single request
- MAX_GROUPS_TO_SEND = 10 - the maximum number of prepared groups with all requested data to send to the Google sheet 
- DATA_COLUMNS_TEMPLATE = 'D{0}:G{1}' - the template with range of cells to send parsed data to 
- UPLOAD_FIELDS = ('status', 'description', 'fixed_post', 'tags') - the fields to upload to the Google sheet 
(the order is important, and filed amount should be the same as amount of columns in the DATA_COLUMNS_TEMPLATE, 
for example D:G - means D, E, F, G columns will be filled with values of UPLOAD_FIELDS)


- PARSE_OFFSET = 0 - the offset from URLs list to start parsing. Use this parameter if you want to parse data for 
instance from 20 group but not from start position
- PARSE_LIMIT = None - the amount of groups to parse if you don't want parse all your URLs

- GET_POST_ATTEMPTS = 2 - the attempt amount to get first post text. Can be useful because of VK API requests limit

- GPT_API_KEY = env_sets.GPT_API_KEY - your Open AI key (located in the .env file)
- GPT_MODEL = env_sets.GPT_MODEL - GPT model to use (set in the .env file)
- GPT_GROUPS_LIMIT = 2 - the number of groups to process by GPT Chat per single request (I don't recommend to use more
than 5-10 depending on text size of your message to GPT)
- MAX_GPT_ATTEMPTS = 10 - the maximum number of attempts to process request by GPT Chat (Very useful setting 
because of GPT chat can provide different kinds of data per same request)
- SYSTEM_ROLE - additional GPT role to change GPT chat behavior
- GPT_REQUEST_TEMPLATE - a main template request to GPT chat (change it according to your needs)
- GROUP_DATA_TEMPLATE - a VK group data template to inject into GPT chat template
- VK_GROUP_FIELDS - a VK group fields to get from VK API. Read official documentation to see all available fields

New settings added in 22 July 2023:
- GET_POST_TEXT - The boolean parameter indicates whether to include post text from post id or not
- GPT_SOLVENCY_TEMPLATE - very similar to GPT_REQUEST_TEMPLATE but for making predictions about group users' solvency
- GPT_PROGRESSION_TEMPLATE - the same as above but for progression
- GPT_SELF_EDUCATION_TEMPLATE - the same as above but for self-education
- FIELDS_TO_TEMPLATES - a dictionary with Group model fields that have to be sent to Google sheet and templates for 
each field to generate data by GPT chat


Example of .env file:

    GPT_API_KEY=your_open_ai_key
    VK_TOKEN=your_vk_access_token
    GPT_MODEL=gpt-3.5-turbo - the GPT language model
    GOOGLE_KEY_FILE=your_key_file.json

The project was created by Alexey Mavrin in 15 June 2023