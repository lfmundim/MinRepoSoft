import argparse
import GitPyService as gps

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

gitPyService = gps.GitPyService(args.folder, args.repo)

if args.option == "1":
    gitPyService.GetCountFilesFirstAndLastCommits()

elif args.option == "2":
    gitPyService.GetCountFilesFirstAndLastCommits(args.fileType)

elif args.option == "3":
    gitPyService.GetCountFilesByCommit()

elif args.option == "4":
    gitPyService.GetCountFilesByCommit(args.fileType)

# if args.option == "5":
#     allCommits = repo.iter_commits()
#     git = repo.git
#     git.checkout()