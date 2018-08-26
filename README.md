# GISSIP: Git Gossip 

[![Build Status](https://travis-ci.org/chadell/gissip.svg?branch=master)](https://travis-ci.org/chadell/gissip)

Have you ever wondered if any change has happened to one of your loved GitHub repos?

This simple tool give you a simple way to track them and get links to the merge commits that have happened on the last X days.

Some GitHub APIs need authorization (others as the public GitHub.com impose rate limit, so you can authenticate yourself)
To create a GitHub token do:
* Your profile -> Settings -> Developer Settings -> Personal Access Tokens (Repo scope is enough)

```bash
$ python -m gissip.main  -h
usage: main.py [-h] [-v] [-a API] [-o OWNER] [-r REPO] [-d DAYS] [-y YAML]
               [-t TOKEN]

Get merge commits of your favourite repos

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -a API, --api API     Github API URL
  -o OWNER, --owner OWNER
                        Github owner
  -r REPO, --repo REPO  Repository you are checking
  -d DAYS, --days DAYS  How many days you want to observe
  -y YAML, --yaml YAML  Path to YAML file where you define you loved repos
  -t TOKEN, --token TOKEN
                        Github Access Token to get better rate access to API
```

## Examples

```bash
$ python -m gissip.main  -d 7 -y my_loved_repos.yml
$ python -m gissip.main  -d 7 -y my_loved_repos.yml -t xxx -a "my own GitHub API"
$ python -m gissip.main -o chadell -r gissip
```

### YAML file

You can also define a YAML file containing several repos from several owners, follow the below format and pass to the script:
```yaml
---
- chadell:
  - chadell.github.io
  - gissip

- dachad:
  - tcpgoon
```

## TODO

* Testing, CI, CD
* Upload PIP packages
