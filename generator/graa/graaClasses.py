from functions import *


class graaArticleAutoFormatter(object):
	""" Class for automatically formatting articles with HTML """

	def __init__(self):
		pass


	def isDate(self, v):
		''' Simple check for date line in the format "month, year" '''

		parts = v.split(",")
		if len(parts) == 2:
			if len(parts[0]) <= 10:
				try:
					test = int(parts[-1])
					return True
				except:
					return False

		return False


	def autoFormatArticle(self, content):
		''' Automatically format article '''

		paragraphs = content.split("\n\n")

		# first line is always a header
		paragraphs[0] = "<h2>%s</h2>" % paragraphs[0]

		for i,v in enumerate(paragraphs[1:]):
			index = i+1
			
			if len(v) < 3:
				continue

			# is it a date? make it small
			if self.isDate(v):
				paragraphs[index] = "<small>%s</small>" % v
				continue

			# is it a heading?
			if len(paragraphs[index].split(" ")) < 8 and paragraphs[index][-1] not in ['.',':']:
				paragraphs[index] = "<br><h3>%s</h3>" % v
				continue

			# surround normal paragraphs with <p>
			paragraphs[index] = "<p>%s</p>" % v.replace("\n","<br>")

		return "\n\n".join(paragraphs)



class graaPageGen(object):
	""" Class for generating static pages for graa.nl """

	def __init__(self, graaDir, configuration):
		self.graaDir = graaDir
		self.configuration = configuration
		self.articleAutoFormatter = graaArticleAutoFormatter()
		
		# webroot
		self.webroot = graaDir + "/static/"
		self.articleWebroot = self.webroot + "/articles/"
		self.mainPageFile = self.webroot + "index.html"

		# templates
		self.templateDir = graaDir + "/templates/"


	def loadTemplates(self):
		''' Load templates for pages and articles '''

		# load stuff
		self.pageTemplate = getFileContent( "%s/page.template" % self.templateDir )
		self.linkTemplate = getFileContent( "%s/articleLink.template" % self.templateDir )

		self.publicArticleTemplates = getFilesFromPath("%s/articlesPub/" % self.templateDir)
		self.sortedArticleNames = self.getSortedArticleNames()


	def getReadableArticleType(self, articleName):
		''' Return readable version of article name '''

		articleTypeIdentifier = articleName.split('-')[1]
		return self.configuration['articleTypes'][articleTypeIdentifier]


	def getSortedArticleNames(self):
		''' Sort names of articles (Descending) '''

		sortedArticleNames = [articleName for articleName in self.publicArticleTemplates]
		sortedArticleNames.sort()

		return [i for i in reversed(sortedArticleNames)]


	def generatePages(self):
		''' Generate main page and articles '''

		self.genMainPage()
		self.genArticles()


	def genMainPage(self):
		''' Generate and write graa.nl main page '''

		mainContent = []

		for articleName in self.sortedArticleNames:

			parts = self.publicArticleTemplates[articleName].split("\n")
			headLine = parts[0]
			URLTest = parts[1]

			tmpLink = self.linkTemplate[:]
			
			if len(URLTest) > 5 and URLTest[:4] == 'http':
				tmpLink = tmpLink.replace('[LINK]', URLTest)
			else:
				tmpLink = tmpLink.replace('[LINK]','/articles/%s.html' % articleName)

			tmpLink = tmpLink.replace('[DESCRIPTION]', headLine)
			articleType = self.getReadableArticleType(articleName)
			tmpLink = tmpLink.replace('[TYPE]', articleType)

			mainContent.append(tmpLink)

		writeFileContent(self.mainPageFile, self.pageTemplate.replace('[CONTENT]', "<table>%s</table>" % ''.join(mainContent)))


	def genArticles(self):
		''' Generate and autoformat article files '''

		for articleName in self.sortedArticleNames:
			fullPath = "%s/%s.html" % (self.articleWebroot, articleName)
			articleContent = self.articleAutoFormatter.autoFormatArticle( self.publicArticleTemplates[articleName] )
			writeFileContent(fullPath, self.pageTemplate.replace('[CONTENT]',articleContent))



class graaMetaParser(object):
	""" Class for parsing meta data (configuration) for graa.nl """

	def __init__(self, metaFilePath):
		self.metaFilePath = metaFilePath
		self.metaDict = {}


	def parseMeta(self):
		''' Parse meta data from file, store in dictionary '''

		content = getFileContent(self.metaFilePath)

		lastKey = 'none'
 
		for line in content.split("\n"):
			if line == '' or len(line) < 3:
				continue

			if line[0] == '\t' or line[0] == ' ':
				try:
					key, value = line.replace(' ','').replace('\t','').split(',')
				except:
					continue
				self.metaDict[lastKey][key] = value

			else:
				lastKey = line
				self.metaDict[lastKey] = {}

