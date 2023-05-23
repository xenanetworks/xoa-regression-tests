import argparse


# to override default dev branch requirement when invoke actions
parser = argparse.ArgumentParser()
parser.add_argument('--core_branch', dest='core_branch', type=str, help='branch of core')
parser.add_argument('--converter_branch', dest='converter_branch', type=str, help='branch of converter')
parser.add_argument('--driver_branch', dest='driver_branch', type=str, help='branch of driver')
args = parser.parse_args()

repo_base = "git+https://github.com/xenanetworks"
lines = [
    f"{repo_base}/'open-automation-python-api'.git@{driver_branch}",
    f"{repo_base}/'open-automation-core'.git@{core_branch}",
    f"{repo_base}/'open-automation-config-converter'.git@{converter_branch}",
]
with open('git-requires.txt', 'w') as fp:
    fp.write('\n'.join(lines))
