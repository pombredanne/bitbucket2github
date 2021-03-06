#!/usr/bin/env python

""" This script backs up all public repos of a BitBucket user to GitHub.
"""

import tempfile
import os

import vault
from scriptine.shell import sh
import bitbucket, github

bitbucket_username = vault.get('bitbucket.org', 'username')
github_username = vault.get('github.com', 'username')
github_api_token = vault.get('github.com', github_username)

bitbucket_url = 'http://bitbucket.org/{0}/{1}'
github_url = 'git+ssh://git@github.com/{0}/{1}.git'
tmp_dir = tempfile.gettempdir()


def backup(repo):
    print "Syncing " + repo + " from BitBucket to GitHub"
    github.create_repo(repo, github_username, github_api_token)

    bitbucket_repo = bitbucket_url.format(bitbucket_username, repo)
    github_repo = github_url.format(github_username, repo)
    local_repo = os.path.join(tmp_dir, repo)

    if os.path.exists(local_repo):
        sh('hg pull {0} -R {1}'.format(bitbucket_repo, local_repo))
    else:
        sh('hg clone {0} {1}'.format(bitbucket_repo, local_repo))

    sh('hg bookmark master -f -R {0}'.format(local_repo))
    sh('hg push {0} -R {1}'.format(github_repo, local_repo))


def main():
    for repo in bitbucket.repos(bitbucket_username):
        backup(repo)


if __name__ == '__main__':
    main()
