# Container Security Paper

## How to run:

### Install Dependencies
Ensure you have the necessary dependencies installed. Use the `requirements.txt` file to set up your environment:
```
pip install -r requirements.txt
```

The entry point to the application is the server.py file. you can run it using "python3 server.py" command.

The Application runs in the 5050 port by default.

All the framework configurations related to policy,posture,etc can be setup using the files in the configuration folder.

The scan_docker_image.py file is the continuos monitoring module of the container framework and it scans the docker image periodically.You can run the script using the "python3 scan_docker_image.py" command.


