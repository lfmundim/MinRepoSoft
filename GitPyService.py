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

	def GetNumberOfEdits(self, add=True, searchString='List<', yearFrom='1969', yearTo='2020'):
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
				if(self.IsInYearInterval(yearFrom, yearTo, setYear)):
					nextCommit = next(allCommits)
					diff = self.repo.git.diff(element, nextCommit)
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

	def GetCountFilesFirstAndLastCommits(self, fileType=""):
		allCommits = self.repo.iter_commits()
		element = next(allCommits)
		count = 0
		for file in element.stats.files:
			if fileType == "" or file.endswith(fileType):
				count += 1
		print('Number of files on latest commit: ', count)
		while True:
			try:
				element = next(allCommits)
			except StopIteration:
				break
		count = 0
		for file in element.stats.files:
			if fileType == "" or file.endswith(fileType):
				count += 1
		print('Number of files on first commit: ', count)

	def GetCountFilesByCommit(self, fileType="All"):
		allCommits = self.repo.iter_commits()
		fileCountList = []
		while True:
			try:
				element = next(allCommits)
				if fileType=="All":
					fileCountList.append(len(element.stats.files))
				else:
					fileCount = 0
					for file in element.stats.files:
						if file.endswith(fileType):
							fileCount += 1
					fileCountList.append(fileCount)
			except StopIteration:
				break
		print(fileType, 'Files per commit: ')
		print(fileCountList)

	def GetLinesByFile(self, fileType='.cs'):
		allCommits = self.repo.iter_commits()
		while True:
			try:
				commit = next(allCommits)
				print('Commit ', commit)
				files = commit.stats.files
				for file in files:
					if not file.endswith(fileType):
						continue
					try:
						targetfile = commit.tree / file
					# files not found
					except KeyError:
						continue
					with io.BytesIO(targetfile.data_stream.read()) as f:
						num_lines = sum(1 for line in f)
						print('\t',file, "Line Count: ", num_lines)
			except StopIteration:
				break

	def GetCountFilesByYear(self, fileType="All"):
		allCommits = self.repo.iter_commits()
		latestCommit = next(allCommits)
		dictionary = {}
		lastYear = self.GetCommitYear(latestCommit)
		allCommits = self.repo.iter_commits()
		while True:
			try:
				element = next(allCommits)
				year = self.GetCommitYear(element)
				if lastYear != year:
					print(lastYear, ':', len(dictionary))
					lastYear = year
					dictionary = {}
				for file in element.stats.files:
					if fileType != "All":
						if file not in dictionary and file.endswith(fileType):
							dictionary[file] = 1
						elif file in dictionary and file.endswith(fileType):
							dictionary[file] = dictionary[file] + 1	
					else:
						if file not in dictionary:
							dictionary[file] = 1
						else:
							dictionary[file] = dictionary[file] + 1
			except StopIteration:
				break

	def GetFilesByYear(self, fileType):
		allCommits = self.repo.iter_commits()
		dictionary = {}
		while True:
			try:
				element = next(allCommits)
				year = self.GetCommitYear(element)
				for file in element.stats.files:
					if not file.endswith(fileType):
						continue
					try:
						targetfile = element.tree / file
					# files not found
					except KeyError:
						continue
					with io.BytesIO(targetfile.data_stream.read()) as f:
						num_lines = sum(1 for line in f)
					if year not in dictionary and file.endswith(fileType):
							dictionary[year] = num_lines
					elif year in dictionary and file.endswith(fileType):
						dictionary[year] = dictionary[year] + num_lines
			except StopIteration:
				break
		print (dictionary)

