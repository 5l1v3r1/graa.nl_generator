import os


def getFilesFromPath(path):
	''' Return files from path in dictionary '''

	fileList = {}
	for f in os.listdir(path):
		fileName = os.path.join(path, f)
		if os.path.isfile(fileName):
			fileList[f] = getFileContent(fileName)

	return fileList


def getFileContent(fileName):
	''' Return the content of some file '''
			
	with open(fileName,'r') as fin:
		content = fin.read()

	return content


def writeFileContent(filename, content):
	''' Write content to a file '''

	with open(filename,'w') as fout:
		fout.write(content)


def getGraaBuildDir():
	''' Return home directory for graa.nl build dir '''

	return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../../")


