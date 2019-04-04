import io

class ComplexCalc:
	def GetComplexByIndent(file):
		maxIndent = 0
		with open(file, 'rU') as f:
			for line in f:
				currentIndent = 0
				caracterCount = 0
				for caracter in line:
					if caracter == ' ':
						currentIndent+= 1
						caracterCount+= 1
					else:
						caracterCount+= 1
						break
				if caracterCount == currentIndent: #ignore; empty line
					continue
				elif (int(currentIndent / 4) > maxIndent):
					maxIndent = int(currentIndent / 4)
		return maxIndent;
					 



