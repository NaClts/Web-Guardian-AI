# Web Guardian AI
Enhancing web security of home lab through AI-based web application firewall (WAF)

## Overview

This repository contains the source code for **Web Guardian AI**, deployed using **Docker Compose**.

👉 **For the full project description and system architecture, please visit:**
**https://wp2025.cs.hku.hk/fyp25100/**

---

## Installation & Setup (Docker Compose)

### Prerequisites

- **Docker**
- **Docker Compose**
- Git

Verify installation:
```bash
docker --version
docker compose version
```

***

## Steps (Quick Start)

### Step 1: Clone the Repository

```bash
git clone https://github.com/NaClts/Web-Guardian-AI.git
```

### Step 2: Enter the Project Directory

```bash
cd Web-Guardian-AI
```

***

### Step 3: Download Required SLM to the Specific Path

A required SLM file must be downloaded and placed in a specific directory before building the containers.

Use the provided link:

**https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_M.gguf**

... to download the file and save it to the following path:

```bash
./auth-service-py/app/models/
````

Example:

```bash
wget https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_M.gguf -O auth-service-py/app/models/Phi-3.5-mini-instruct-Q4_K_M.gguf
```

Or using `curl`:

```bash
curl -L https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_M.gguf -o auth-service-py/app/models/Phi-3.5-mini-instruct-Q4_K_M.gguf
```

> **Important:**
>
> *   The file **must** be placed in the exact path shown above.

***

### Step 4: Configure the Upstream Web Application

Edit the `docker-compose.yml` file and update the environment variables for the **Envoy** service.

Example:

```yaml
services:
  envoy:
    build: ./envoy
    ports:
      - "80:80"
      - "443:443"
    environment:
      WEB_APP_HOST: www.example.com
      WEB_APP_PORT: 80
    depends_on:
      - auth-service-py

  auth-service-py:
    build: ./auth-service-py
```

#### Configuration Explanation

*   `WEB_APP_HOST`  
    Set this to the **hostname or IP address** of the upstream web application you want to protect.
    *   Examples:
        *   `www.example.com`
        *   `192.168.1.100`
        *   `my-internal-app`

*   `WEB_APP_PORT`  
    Set this to the **HTTP port number** the upstream web application listens on.
    *   Examples:
        *   `80`
        *   `8080`

This allows Envoy to forward traffic to the specified upstream service.

***

### Step 5: Build and Start All Services

```bash
docker compose up -d
```

***

### Step 6: Access the Protected Application

Once running, access the application via:

    http://localhost

***

## Managing the Services

### Stop the Containers

```bash
docker compose down
```

***

## License

This project is licensed under the **GPL-3.0 license**.
