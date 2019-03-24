import argparse
import time
from git import Repo

def GetTotalCommits(repo, year="1969", message=""):
	allCommits = repo.iter_commits()
	count = 0
	while True:
		try:
			element = next(allCommits)
			#date = time.asctime(time.gmtime(element.committed_date))
			setYear = time.strftime("%Y", time.gmtime(element.committed_date))
			if((year=="1969" or year==setYear) and (message == "" or element.message.find(message)>=0)):
				count = count + 1
		except StopIteration:
			break
	print ('Total number of commits: {}'.format(count))

parser = argparse.ArgumentParser(description="Arguments Description")
parser.add_argument('--repo', nargs='?', default='Z:\MinRepoSoft\lime-csharp', help='Repo to use')
parser.add_argument('--option', nargs='?', default=1, help='Option selected from list')
parser.add_argument('--year', nargs='?', default="2019", help='Year to check')
parser.add_argument('--searchString', nargs='?', default=1, help='String to search for')
parser.add_argument('--count', nargs='?', default=5, help='Positions returned')
parser.add_argument('--fileType', nargs='?', default='cs', help='File extension to search for')

args = parser.parse_args()
repo = Repo(args.repo)


if args.option == "1":
	GetTotalCommits(repo)

elif args.option == "2":
	GetTotalCommits(repo, args.year)

elif args.option == "3":
	GetTotalCommits(repo, "1969", args.searchString)

elif args.option == "4" or args.option == "5" or args.option == "6":
	file = repo.commit('9bf513720b9f4019ef9fc4836bfab9608d817224').stats.files[0]
	print(file)
	#print(repo.commit('9bf513720b9f4019ef9fc4836bfab9608d817224').stats.files)

#elif args.option == 7

#elif args.option == 8

#elif args.option == 9

#elif args.option == 10
