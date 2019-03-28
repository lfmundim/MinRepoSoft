import io
import time
import re as regex
from git import Repo

class GitPyService:
	def __init__(self, path, url):
		self.repo = self.InitializeRepo(path, url)

	def InitializeRepo(self, path, url):
		if path != '':
			folder = path
		else:	
			folder = './' + url.split('/')[-1].split('.')[0]
			try:
				Repo.clone_from(url, folder)
			except:
				print("")

		return Repo(folder)

	def GetCommitYear(self, element):
		return time.strftime("%Y", time.gmtime(element.committed_date))

	def IsInYearInterval(self, yearFrom, yearTo, setYear):
		return (yearFrom=="1969" and yearTo=="2020") or (setYear>=yearFrom and setYear<=yearTo)

	def GetTotalCommits(self, yearFrom="1969", yearTo="2020", message=""):
		allCommits = self.repo.iter_commits()
		count = 0
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if(((yearFrom=="1969" and yearTo=="2020") or (setYear>=yearFrom and setYear<=yearTo)) and (message == "" or element.message.find(message)>=0)):
					count = count + 1
			except StopIteration:
				break
		print ('Total number of commits: {}'.format(count))

	def GetTopCommiters(self, yearFrom="1969", yearTo="2020", max=10):
		allCommits = self.repo.iter_commits()
		dictionary = {}
		count = 0
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if (self.IsInYearInterval(yearFrom, yearTo, setYear)):
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

	def GetNumberOfEdits(self, add=True, searchString='List<'):
		allCommits = self.repo.iter_commits()
		total = 0
		if(add):
			searchRegex = r"\+.*" + regex.escape(searchString) + r".*\n"
		else:
			searchRegex = r"\-.*" + regex.escape(searchString) + r".*\n"
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if(self.IsInYearInterval(args.yearFrom, args.yearTo, setYear)):
					nextCommit = next(allCommits)
					diff = repo.git.diff(element, nextCommit)
					allLists = regex.findall(searchRegex, diff)
					total = total + len(allLists)
			except StopIteration:
				print("Number of \'%s\' Edits: %d %s" % (searchString, total, "adds" if add else "removes"))
				break

	def GetMostModifiedFiles(self, yearFrom="1969", yearTo="2020", extension=".cs", max=5):
		allCommits = self.repo.iter_commits()
		dictionary = {}
		count = 0
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if(self.IsInYearInterval(yearFrom, yearTo, setYear)):
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

	def GetLinesByFile(self, commit):
		files = commit.stats.files
		for file in files:
			targetfile = commit.tree / file

			with io.BytesIO(targetfile.data_stream.read()) as f:
				num_lines = sum(1 for line in f)
				print("Count: ", num_lines)
