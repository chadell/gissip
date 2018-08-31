import logging
import requests
from datetime import datetime, timedelta


log = logging.getLogger('gissip.api')


class GitAPI:
    def __init__(self, url, token=None):
        self.url = url
        self.token = token
        self.headers = self._get_headers()

    def _get_headers(self):
        if self.token:
            headers = {'Authorization': 'token ' + self.token}
            req_response = requests.get(self.url, headers=headers)
            if req_response.status_code == 401:
                headers = None
                log.warning("Authorization error: {}".format(req_response.json()['message']))
            else:
                log.info("INFO: Successfully authenticated")
        else:
            headers = None

        return headers

    def get_commits_within_window(self, owner, repo, days):
        req_response = requests.get(self.url + "/repos/{}/{}/commits".format(owner, repo), headers=self.headers)

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
