# TikStalker
A Python script developed to automate the process of extracting public information from TikTok accounts for OSINT.

## Python library:
```text
pip install beautifulsoup4
pip install requests
pip install argparse
```

## TikStalker Usage:
Help menu:
```
usage: main.py [-h] -u TARGET [-a UAGENT]

TikStalker is a Python script is developed to automate the process of extracting public information from TikTok accounts.

options:
  -h, --help            show this help message and exit
  -u TARGET, --user TARGET
                        The @nickname from your target
  -a UAGENT, --user-agent UAGENT
                        Custom User-Agent <name>

```
```
python3 TikStalker.py -u justinbieber
```
Output result:
![image](https://github.com/P4nD3m1CB0Y0xD/TikStalker/assets/123909611/1282ccaf-3581-4fb7-9466-00351e8b47cc)
