# News AI-based Chat Delivery Project

This project is designed to deliver news in a chat format based on data and themes.

## Installation

### Step 1: Create a .env File

Add a `.env` file to the root directory of the project with the following content:

```bash
# Embedder settings
EMBEDDER_PORT=
SPECIFIC_MODEL="" #will be chosen default model
CUDA_VISIBLE_DEVICES_EMB=

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

## Project Description

(Coming soon...)

## Usage

(Coming soon...)
