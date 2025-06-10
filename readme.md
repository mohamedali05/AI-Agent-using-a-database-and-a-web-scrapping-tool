# Project Setup Guide

This project utilizes [n8n](https://n8n.io), a powerful workflow automation tool. It creates an AI agent capable of scrapping data from a sample faq website and accessing a Postgres database through an MCP server.
## Prerequisites

Before getting started, ensure you have the following installed on your system:

- **Docker**: [Download and install Docker](https://docs.docker.com/get-docker/)
- **Git**: For cloning the repository

## Getting Started

### Step 1: Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone <repository-url>
cd <project-directory>
```

### Step 2: Launch the n8n Container

In a terminal, run the official n8n Docker container:

```bash
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

This command will:
- Start n8n on port 5678
- Create a persistent data volume for your workflows
- Run the container interactively

### Step 3: Start the MCP Server

In a **second terminal**, navigate to your project directory and start the MCP server using Docker Compose:

```bash
docker-compose up --build
```

This will run the MCP server that exposes the tools to access to the sample database so that the AI agent can read through it 

## Configuration

### Step 4: Configure OpenAI Credentials

To integrate with OpenAI services:

1. Access your n8n instance at `http://localhost:5678`
2. Follow the [official n8n OpenAI credentials documentation](https://docs.n8n.io/integrations/builtin/credentials/openai/)
3. Add your OpenAI API key to establish the connection

### Step 5: Configure Supabase Credentials

Set up your Supabase database connection using the following credentials:

- **Host**: `https://cpvqgnhjzfzdtyiozrjq.supabase.co`
- **Service Role Key**: 
  ```
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNwdnFnbmhqemZ6ZHR5aW96cmpxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODkzNjkwOCwiZXhwIjoyMDY0NTEyOTA4fQ.nuQNiT43OWzvdsvHRfxOORds1v-t8XmXsV1F5Pszgec
  ```



### step 6 : 
Chat and play with the AI Agent 