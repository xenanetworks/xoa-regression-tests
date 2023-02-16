import argparse


# to override default dev branch requirement when invoke actions
parser = argparse.ArgumentParser()
parser.add_argument('--repo', dest='repo', type=str, help='repo name of current actions')
parser.add_argument('--branch', dest='branch', type=str, help='repo branch of current actions')
args = parser.parse_args()


ALL_REPO = (
    'open-automation-python-api',
    'open-automation-core',
    'open-automation-config-converter',
)

lines = []
for repo in ALL_REPO:
    if repo == args.repo:
        branch = args.branch
    else:
        branch = 'dev'
    lines.append(f"git+https://github.com/xenanetworks/{repo}.git@{branch}")

with open('git-requires.txt', 'w') as fp:
    fp.write('\n'.join(lines))
