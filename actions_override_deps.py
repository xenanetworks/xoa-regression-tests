import argparse
from typing import List


# to override default dev branch requirement when invoke actions
parser = argparse.ArgumentParser()
parser.add_argument('--event_name', dest='event_name', type=str, help='github event name')
parser.add_argument('--event_branch', dest='event_branch', type=str, help='branch of event')
parser.add_argument('--event_repo', dest='event_repo', type=str, help='repo of event')
parser.add_argument('--core_branch', dest='core_branch', type=str, help='branch of core')
parser.add_argument('--converter_branch', dest='converter_branch', type=str, help='branch of converter')
parser.add_argument('--driver_branch', dest='driver_branch', type=str, help='branch of driver')
args = parser.parse_args()


def replace_all_repo() -> List[str]:
    repo_base = "git+https://github.com/xenanetworks"
    lines = [
        f"{repo_base}/open-automation-python-api.git@{args.driver_branch}",
        f"{repo_base}/open-automation-core.git@{args.core_branch}",
        f"{repo_base}/open-automation-config-converter.git@{args.converter_branch}",
    ]
    return lines

def replace_single_repo() -> List[str]:
    ALL_REPO = (
        'open-automation-python-api',
        'open-automation-core',
        'open-automation-config-converter',
    )
    lines = []
    for repo in ALL_REPO:
        if repo == args.event_repo:
            branch = args.event_branch
        else:
            branch = 'dev'
        lines.append(f"git+https://github.com/xenanetworks/{repo}.git@{branch}")
    return lines

def main() -> None:
    if args.event_name == 'push':
        lines = replace_single_repo()
    else: # manual testing
        lines = replace_all_repo()
    with open('git-requires.txt', 'w') as fp:
        fp.write('\n'.join(lines))

if __name__ == "__main__":
    main()
