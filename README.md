# Container Security Framework

A comprehensive framework for monitoring and securing container deployments.

## Overview

This framework provides tools and configurations for container security scanning, policy enforcement, and posture management.

## Prerequisites

- Python 3.x
- Docker
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-repo/container-security.git
cd container-security
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
container-security/
├── server.py
├── scan_docker_image.py
├── requirements.txt
└── configuration/
    ├── policy/
    └── posture/
```

## Usage

### Main Application Server

The main application server handles the core functionality of the framework.

## **1. Build the Docker Image**
Run the following command to build the Docker image:
```sh
docker build -t flask-zt-server .

## **2. Run the Container with Environment Variables**
To run the container and pass an environment variable (`TEST_SCENARIO`), use:
```sh
docker run -d -e TEST_SCENARIO=all_pass -p 5050:5050 --name flask-zt-server flask-zt-server
```
- `-d` → Runs in detached mode (background)
- `-e TEST_SCENARIO=all_pass` → Passes the environment variable
- `-p 5050:5050` → Maps container port 5050 to host port 5050
- `--name flask-zt-server` → Names the container

2. Access the application:
- Default port: 5050
- URL: `https://localhost:5050/get_resource`

### Container Image Scanner

The framework includes a continuous monitoring module for scanning Docker images.

1. Run the scanner:
```bash
python3 scan_docker_image.py
```

## Configuration

All framework configurations can be customized using the files in the `configuration` directory:

- `configuration/policy/`: Security policy definitions
- `configuration/posture/`: Security posture settings



