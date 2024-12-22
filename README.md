<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">

<img src="images/bot_logo.jpg" height=200 align = "center"/>

<h3 align="center">AI News Bot</h3>

</div>

# News AI-based Chat Delivery Project

This project is designed to deliver news in a chat format based on data and themes.

## Our mission
(what is good for)

## About the project
(structure and services description)

## Architecture
(.png and description) 

## Telegram bot example
(.png)

## UI example
(.png)

## API example
(.png)

## Technology steck
(description with hrefs)

## Data description
 - You can download data via YandexDisk from [here](https://disk.yandex.ru/d/Tz5hsycHYzRJKg)
 - Original data consists of `7516 rows`
 - There are monthly news from 5 thematic Telegram channels:
   1. Economics
   2. Sport
   3. AI
   4. IT
   5. Sciense
 - Columns: `message_id`, `chat_id`, `message_date`, `content`, `theme`

## Installation

### Step 1: Create a .env File

Add a `.env` file to the root directory of the project with the following content:

```bash
# Embedder settings
EMBEDDER_PORT=
SPECIFIC_MODEL="" # will be chosen default model
CUDA_VISIBLE_DEVICES_EMB=all

#DB settings
DB_SERVICE_PORT=
DB_HOST=mysql
DB_PORT=3306
DB_NAME=mydatabase
DB_USER=root
DB_ROOT_PASSWORD=123
CSV_PATH="/db_service/news_data/news.csv" # could be downloaded from yandex disk

# RAG settings
RAG_MANAGER_PORT=

# Neural GPT worker settings
WORKER_PORT=
GPT_TOKEN=""
BASE_GPT_URL="https://*********/openai/v1" 

#Bot settings
BOT_API_TOKEN=""

#Parser settings
USE_PARSER=0 # 0 or 1
API_ID=
API_HASH=''
PHONE='+7**********'

#Gradio settings
GRADIO_PORT=
```

Fill in the variables with the appropriate values.

### Step 2: Build and Start Containers

1. **Build Containers**

   Run the following command to build the Docker containers:

   ```bash
   docker-compose build
   ```

2. **Start Containers**

   Start the containers in detached mode:

   ```bash
   docker-compose up -d
   ```

## Authors
