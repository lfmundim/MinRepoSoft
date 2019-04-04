import argparse
import GitPyService as gps
import ComplexCalc as cc
from git import Repo
import io
import os

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
complexCalc = cc.ComplexCalc()

# complexidade por indent dos arquivos do ultimo commit
if args.option == "1":
    repo = Repo(args.folder)
    commits = repo.iter_commits()
    commit = next(commits)
    repo.git.checkout(commit)
    craDic = {}
    ctaDic = {}
    mcaDic = {}

    for root, directory, files in os.walk(args.folder):
        for file in files:
            cta = 0
            cra = 0
            mca = 0
            if(file.endswith(args.fileType)):
                craDic[file] = complexCalc.GetCRAByIndent(os.path.join(root, file))
                ctaDic[file] = complexCalc.GetCTAByIndent(os.path.join(root, file))
                mcaDic[file] = complexCalc.GetMCAByIndent(os.path.join(root, file))

    # Ordenar desc -> [0]
    print('CRA:\n', craDic, '\n')
    print('CTA:\n', ctaDic, '\n')
    print('MCA:\n', mcaDic, '\n')

# qtd de arquivos da extensao no primeiro e ultimo commits
elif args.option == "2":
    gitPyService.GetCountFilesFirstAndLastCommits(args.fileType)

# qtd de arquivos em cada commit
elif args.option == "3":
    gitPyService.GetCountFilesByCommit()

# qtd de arquivos da extensao em cada commit
elif args.option == "4":
    gitPyService.GetCountFilesByCommit(fileType=args.fileType)

# numero de linha de codigo da extensao em cada commit
elif args.option == "5":
    gitPyService.GetLinesByFile(fileType=args.fileType)