import argparse
import time
import re as regex
from git import Repo

parser = argparse.ArgumentParser(description="Arguments Description")
parser.add_argument('--repo', nargs='?', default='https://github.com/takenet/lime-csharp', help='Repo to use')
parser.add_argument('--folder', nargs='?', default='', help='Folder to use')
parser.add_argument('--option', nargs='?', default=1, help='Option selected from list')
parser.add_argument('--yearTo', nargs='?', default="2019", help='Year to check up to')
parser.add_argument('--yearFrom', nargs='?', default="1969", help='Year to check from')
parser.add_argument('--searchString', nargs='?', default=1, help='String to search for')
parser.add_argument('--count', nargs='?', default=10, help='Positions returned')
parser.add_argument('--fileType', nargs='?', default='.cs', help='File extension to search for')

args = parser.parse_args()

if args.folder != '':
	folder = args.folder
else:	
	repoName = args.repo.split('/')[-1].split('.')[0]
	folder = './'+repoName
	Repo.clone_from(args.repo, folder)
repo = Repo(folder)

if args.option == "1":
    allCommits = repo.iter_commits()
    element = next(allCommits)
    print('Files on latest commit: ', len(element.stats.files))
    print(element.stats.files)
    while True:
        try:
            element = next(allCommits)
        except StopIteration:
            break
    print('Files on first commit: ', len(element.stats.files))
    print(element.stats.files)

if args.option == "2":
    allCommits = repo.iter_commits()
    element = next(allCommits)
    count = 0
    for file in element.stats.files:
        if file.endswith(args.fileType):
            count += 1
    print('Number of files using extension ', args.fileType, 'on latest commit: ', count)
    count = 0
    while True:
        try:
            element = next(allCommits)
        except StopIteration:
            break
    for file in element.stats.files:
        if file.endswith(args.fileType):
            count += 1
    print('Number of files using extension ', args.fileType, 'on first commit: ', count)

if args.option == "3":
    allCommits = repo.iter_commits()
    fileCountList = []
    while True:
        try:
            element = next(allCommits)
            fileCountList.append(len(element.stats.files))
        except StopIteration:
            break
    print('Files per commit: ')
    print(fileCountList)


if args.option == "4":
    allCommits = repo.iter_commits()
    fileCountList = []
    while True:
        try:
            element = next(allCommits)
            fileCount = 0
            for file in element.stats.files:
                if file.endswith(args.fileType):
                    fileCount += 1
            fileCountList.append(fileCount)
        except StopIteration:
            break
    print(args.fileType, 'Files per commit: ')
    print(fileCountList)

if args.option == "5":
    allCommits = repo.iter_commits()
    git = repo.git
    git.checkout()