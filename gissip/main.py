#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import argparse
import requests
from datetime import datetime, timedelta
import yaml

log = logging.getLogger('critical_peering')
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


def get_commits_within_window(api, headers, owner, repo, days):
    req_response = requests.get(api + "/repos/{}/{}/commits".format(owner, repo), headers=headers)

    if req_response.status_code == 404:
        raise ValueError("Owner or Repo not found")
    elif req_response.status_code == 403:
        raise ValueError("Rate Limit error: {}. Current value "
                         "of access per hour: {}".format(req_response.json()['message'],
                                                         req_response.headers['X-RateLimit-Limit']))
    elif req_response.status_code == 401:
        raise ValueError("Failed Authorization")

    result_commits = []
    all_commits = req_response.json()
    for commit in all_commits:
        commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        if commit_date > datetime.now() - timedelta(days=days):
            result_commits.append(commit)

    return result_commits


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

    if args.token:
        headers = {'Authorization': 'token ' + args.token}
        req_response = requests.get(args.api, headers=headers)
        if req_response.status_code == 401:
            log.info("Authorization error: {}".format(req_response.json()['message']))
        else:
            log.info("INFO: Successfully authenticated")
    else:
        headers = None

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
                            results[owner][repo].add(get_commits_within_window(args.api, headers, owner,
                                                                               repo, args.days))
                        else:
                            results[owner][repo] = get_commits_within_window(args.api, headers, owner, repo, args.days)
                    except ValueError as e:
                        log.error("{}, Owner: {}, Repo: {}".format(e, owner, repo))
    elif args.repo and args.owner:
        results[args.owner] = {}
        try:
            results[args.owner][args.repo] = get_commits_within_window(args.api, headers, args.owner,
                                                                       args.repo, args.days)
        except ValueError as e:
            log.error("{}, Owner: {}, Repo: {}".format(e, args.owner, args.repo))
    else:
        print("pass me something")

    # pprint.pprint(results)
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
