#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import argparse
import yaml
from gissip.github_api import GitAPI


log = logging.getLogger('gissip')
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)


def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


def print_results(results):
    for owner in results:
        for repo in results[owner]:
            print((bordered("Commits submitted for {}/{}\n".format(owner, repo))))
            for commit in results[owner][repo]:
                print(commit['html_url'])


def parse_arguments():
    parser = argparse.ArgumentParser(description='Get merge commits of your favourite repos')

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument('-a', '--api', help='Github API URL', default='https://api.github.com')
    parser.add_argument('-o', '--owner', help='Github owner')
    parser.add_argument('-r', '--repo', help='Repository you are checking')
    parser.add_argument('-d', '--days', help='How many days you want to observe', type=int, default=1)
    parser.add_argument('-y', '--yaml', help='Path to YAML file where you define you loved repos')
    parser.add_argument('-t', '--token', help='Github Access Token to get better rate access to API')

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    results = {}

    git_api = GitAPI(url=args.api,
                     token=args.token)

    if args.yaml:
        with open(args.yaml, 'r') as yaml_file:
            owners_and_repos = yaml.load(yaml_file)
        for owner_and_repos in owners_and_repos:
            owner = list(owner_and_repos.keys())[0]
            for repos in list(owner_and_repos.values()):
                results[owner] = {}
                for repo in repos:
                    try:
                        if repo in list(results[owner].keys()):
                            results[owner][repo].add(git_api.get_commits_within_window(owner, repo, args.days))
                        else:
                            results[owner][repo] = git_api.get_commits_within_window(owner, repo, args.days)
                    except ValueError as e:
                        log.error("{}, Owner: {}, Repo: {}".format(e, owner, repo))
    elif args.repo and args.owner:
        results[args.owner] = {}
        try:
            results[args.owner][args.repo] = git_api.get_commits_within_window(args.owner, args.repo, args.days)
        except ValueError as e:
            log.error("{}, Owner: {}, Repo: {}".format(e, args.owner, args.repo))
    else:
        print("Gissip need either a repo or a YML file to look at")

    print_results(results)


if __name__ == "__main__":

    try:
        main()
        sys.exit(0)
    except Exception as e:
        logging.critical(
            str(e),
            exc_info=True
        )
        sys.exit(1)
