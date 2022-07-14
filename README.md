![GitHub top language](https://img.shields.io/github/languages/top/Fraccs/youtooler)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Fraccs/youtooler/youtooler)
![GitHub](https://img.shields.io/github/license/Fraccs/youtooler)
![GitHub issues](https://img.shields.io/github/issues/Fraccs/youtooler)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Fraccs/youtooler)

# Docker Youtooler

> Multithreaded YouTube viewer BOT based on TOR.

## Disclaimer

***Developers assume no liability and are NOT RESPONSIBLE for any misuse or damage caused by this program.***

***This is just an experiment, the usage of this program is NOT RECCOMENDED.***

## Requirements

- **Docker**

- **Docker Compose**

- **High end** machine

- **High speed** internet connection

## Youtooler Installation

```bash
git clone --single-branch --branch docker-latest https://github.com/Fraccs/youtooler.git
```

```bash
cd youtooler
```

## Usage

- Open the Dockefile in the root directory and enter the url of the video between the empty quotation marks in the following line.

> Make sure that the URL is in the correct format: ```https://www.youtube.com/watch?v=<video_id>```

```Dockerfile
>>>>> CMD ["python3", "-u", "src/youtooler.py", "--url", ""] <<<<<
```

- Then build and run the containers with the following command.

```bash
docker-compose up --build -d
```
