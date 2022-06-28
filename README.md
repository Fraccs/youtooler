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

***Most TOR nodes are blacklisted, this makes the potential gains obtainable with the program close to none, furthermore YouTube could reset the views counter of the video at any time if any suspicious activity is detected.***

## Requirements

- **Linux** Mid-High end machine.

- **Python** 3.10.x

- **Chrome** browser.

- **TOR** (not TOR browser).

- **High speed** internet connection.

## Chrome Installation (Debian / Ubuntu)

### (Skip this if you already have Chrome)

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

```bash
sudo apt install ./google-chrome-stable_current_amd64.deb
```

## TOR Installation (Debian / Ubuntu)

### (Skip this if you already have TOR)

```bash
sudo apt update
```

```bash
sudo apt install tor
```

## Youtooler Installation (Linux)

```bash
git clone https://github.com/Fraccs/youtooler.git
```

```bash
cd youtooler
```

```bash
pip install -r requirements.txt
```

## Usage

> The program binds 5 TOR subprocesses to the ports: ```9050, 9052, 9054, 9056, 9058```, make sure that nothing else is running on those ports.

> Make sure that the URL is in the correct format: ```https://www.youtube.com/watch?v=<video_id>```

```bash
$ python3 youtooler.py --url <url_of_video>
```
