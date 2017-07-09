from graa.graaClasses import graaPageGen, graaMetaParser
from graa.functions import *

buildDir = getGraaBuildDir()

metaParser = graaMetaParser(buildDir + "/meta/graa.meta")
metaParser.parseMeta()


pageGenerator = graaPageGen(buildDir, metaParser.metaDict)
pageGenerator.loadTemplates()
pageGenerator.generatePages()
