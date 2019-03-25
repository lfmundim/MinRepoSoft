import argparse
import time
import re as regex
from git import Repo

def GetCommitYear(element):
	return time.strftime("%Y", time.gmtime(element.committed_date))

def IsInYearInterval(yearFrom, yearTo, setYear):
	return (yearFrom=="1969" and yearTo=="2020") or (setYear>=yearFrom and setYear<=yearTo)

def GetTotalCommits(repo, yearFrom="1969", yearTo="2020", message=""):
	allCommits = repo.iter_commits()
	count = 0
	while True:
		try:
			element = next(allCommits)
			setYear = GetCommitYear(element)
			if(((yearFrom=="1969" and yearTo=="2020") or (setYear>=yearFrom and setYear<=yearTo)) and (message == "" or element.message.find(message)>=0)):
				count = count + 1
		except StopIteration:
			break
	print ('Total number of commits: {}'.format(count))

def GetTopCommiters(repo, yearFrom="1969", yearTo="2020", max=10):
	allCommits = repo.iter_commits()
	dictionary = {}
	count = 0
	while True:
		try:
			element = next(allCommits)
			setYear = GetCommitYear(element)
			if (IsInYearInterval(yearFrom, yearTo, setYear)):
				if element.author.name in dictionary:
					dictionary[element.author.name] = dictionary[element.author.name] + 1
				else:
					dictionary[element.author.name] = 1
		except StopIteration:
			break
	print('Top %d Committers (from %s to %s):' % (max, yearFrom, yearTo))
	for key, value in sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True):
		print (key, value)
		count = count + 1
		if count == max:
			break

def GetNumberOfEdits(repo, add=True, searchString='List<'):
	allCommits = repo.iter_commits()
	total = 0
	if(add):
		searchRegex = r"\+.*" + regex.escape(searchString) + r".*\n"
	else:
		searchRegex = r"\-.*" + regex.escape(searchString) + r".*\n"
	while True:
		try:
			element = next(allCommits)
			setYear = GetCommitYear(element)
			if(IsInYearInterval(args.yearFrom, args.yearTo, setYear)):
				nextCommit = next(allCommits)
				diff = repo.git.diff(element, nextCommit)
				allLists = regex.findall(searchRegex, diff)
				total = total + len(allLists)
		except StopIteration:
			print("Number of \'%s\' Edits: %d %s" % (searchString, total, "adds" if add else "removes"))
			break

def GetMostModifiedFiles(repo, yearFrom="1969", yearTo="2020", extension=".cs", max=5):
	allCommits = repo.iter_commits()
	dictionary = {}
	count = 0
	while True:
		try:
			element = next(allCommits)
			setYear = GetCommitYear(element)
			if(IsInYearInterval(yearFrom, yearTo, setYear)):
				for key in element.stats.files:
					if key.endswith(extension): 
						if key in dictionary:
							dictionary[key] = dictionary[key] + 1
						else:
							dictionary[key] = 1
		except StopIteration:
			break
	print("Top %d modified files with extension %s (from %s to %s):" % (max, extension, yearFrom, yearTo))
	for key, value in sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True):
		print (key, value)
		count = count + 1
		if count == max:
			break

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

#1. Quantos commits possui o projeto? 
if args.option == "1":
	GetTotalCommits(repo)

#2. Quantos commits foram realizados em 2019? Em 2018? Em 2017 
elif args.option == "2":
	GetTotalCommits(repo, args.yearFrom, args.yearTo)

#3. Quantos commits incluem a string “feature”? E a string “fix”? 
elif args.option == "3":
	GetTotalCommits(repo, message=args.searchString)

#4. Quais os 5 arquivos <extensao> mais modificados? 
#5. Quais os 5 arquivos <extensao> mais modificados desde 2018? 
#6. Quais os 5 arquivos <extensao> mais modificados em 2017? 
elif args.option == "4" or args.option == "5" or args.option == "6":
	print ("This might take a while if the selected repository has a big number of commits")
	GetMostModifiedFiles(repo, args.yearFrom, args.yearTo, args.fileType, int(args.count))

#7. Quais os 3 desenvolvedores mais ativos? 
# Obs: Serão printados por default os top10, pois o repositório de exemplo tem múltiplos committers que são o mesmo usuário
elif args.option == "7":
	GetTopCommiters(repo, max=int(args.count))

#8. Quais 3 desenvolvedores mais ativos em 2019? 
elif args.option == "8":
	GetTopCommiters(repo, args.yearFrom, args.yearTo, int(args.count))

#9. Quantas vezes List foi adicionado no código? 
elif args.option == "9":
	GetNumberOfEdits(repo, True, args.searchString)

#10. Quantas vezes Dictionary foi removido do código? 
elif args.option == "10":
	GetNumberOfEdits(repo, False, args.searchString)
