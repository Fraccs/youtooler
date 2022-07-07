![GitHub top language](https://img.shields.io/github/languages/top/Fraccs/youtooler)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Fraccs/youtooler/youtooler)
![GitHub](https://img.shields.io/github/license/Fraccs/youtooler)
![GitHub issues](https://img.shields.io/github/issues/Fraccs/youtooler)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Fraccs/youtooler)

# Youtooler

> Multithreaded YouTube viewer BOT based on TOR.

## Disclaimer

***Developers assume no liability and are NOT RESPONSIBLE for any misuse or damage caused by this program.***

***This is just an experiment, the usage of this program is NOT RECCOMENDED.***

## Requirements

- **Linux** High end machine

- **Python** 3.10.x

- **Firefox**

- **Geckodriver**

- **TOR**

- **High speed** internet connection.

## Firefox Installation (Debian / Ubuntu)

```bash
sudo apt update
```

```bash
sudo apt install firefox-esr
```

## Geckodriver Installation (Debian / Ubuntu)

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
```

```bash
tar -xvzf geckodriver*
```

```bash
chmod +x geckodriver
```

```bash
sudo mv geckodriver /usr/local/bin/
```

## TOR Installation (Debian / Ubuntu)

```bash
sudo apt update
```

```bash
sudo apt install tor
```

## Youtooler Installation (Linux)

```bash
git clone --single-branch --branch python-latest https://github.com/Fraccs/youtooler.git
```

```bash
cd youtooler
```

```bash
pip install -r requirements.txt
```

```bash
pip install .
```

## Usage

> The program binds 5 TOR subprocesses to the ports: ```9050, 9052, 9054, 9056, 9058```, make sure that nothing else is running on those ports.

> Make sure that the URL is in the correct format: ```https://www.youtube.com/watch?v=<video_id>```

```bash
cd src
```

```bash
python3 youtooler.py --url <url_of_video>
```
