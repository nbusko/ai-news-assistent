# News AI-based Chat Delivery Project

This project is designed to deliver news in a chat format based on data and themes.

## Data description

 - Original data consists of `6561 rows`
 - There are monthly news from 5 thematic Telegram channels:
   1. Economics
   2. Sport
   3. AI
   4. IT
   5. Sciense
 - Columns: `MESSAGE_ID` `CHAT_ID` `MESSAGE_DATE` `MESSAGE_DATA`

## Installation

### Step 1: Create a .env File

Add a `.env` file to the root directory of the project with the following content:

```bash
# Embedder settings
EMBEDDER_PORT=
SPECIFIC_MODEL="" # will be chosen default model
CUDA_VISIBLE_DEVICES_EMB=

# MySQL
DB_NAME=
DB_USER=
EMBEDDER_URL=
DB_HOST=
DB_PORT=
DB_ROOT_PASSWORD=

# RAG
RAG_ENGINE_PORT=

# Neural GPT worker settings
WORKER_PORT=
GPT_TOKEN=""
BASE_GPT_URL="" 
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

## Project Structure

- mysql:
  - MySQL database.
- rag_engine:
  - Service for searching information in the database based on user requests.
- neural_worker:
  - Service for processing user requests using LLM.
- embedder:
  - Service for obtaining text embeddings.

## Usage

(Coming soon...)
