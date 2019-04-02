from graa.graaClasses import graaPageGen, graaMetaParser
from graa.functions import *


import yaml

buildDir = getBuildDir()
static_dir = "%s/static/" % buildDir

# Load yaml metadata
with open(buildDir + '/meta/graa.yaml') as f:
  site_config = yaml.safe_load(f)['site_config']

print site_config

# grab template files
main_template = getFileContent( "%s/templates/page.template" % buildDir )
article_template = getFileContent( "%s/templates/article.template" % buildDir )
menuitem_template = getFileContent( "%s/templates/menuitem.template" % buildDir )
rss_template = getFileContent( "%s/templates/rss.xml.template" % buildDir )
rss_item_template = getFileContent( "%s/templates/rss.xml.item.template" % buildDir )

# Add config data to index page
index_page = main_template
index_page = index_page.replace('[SITE_TITLE]', site_config['site_title'])
index_page = index_page.replace('[SITE_DESCRIPTION]', site_config['site_desc'])
index_page = index_page.replace('[MENU_ITEMS]','''
  <li><a href = "/index.html" class = "selected">Blog</a></li>
  <li><a href = "/about.html" >About</a></li>''')

# load articles
articles_metafiles = getFilesFromPath("%s/templates/articles/" % buildDir)
articles = []
article_ids = []
for metafile in articles_metafiles:
  if 'yaml' not in metafile or metafile == 'template.yaml':
    continue

  article_meta = yaml.safe_load(articles_metafiles[metafile])
  article_ids.append(article_meta['id'])
  articles.append(article_meta)

# loop through sorted articles (O^2 for now)
articles_index = ""
article_ids.sort()
for article_id in reversed(article_ids):
  for article in articles:
    if article['id'] == article_id:
      print article

      # generate index page entry
      tmp_article = article_template
      if article['type'] == 'link':
        tmp_article = tmp_article.replace('[ARTICLE_LINK]', article['link'])
      else:
        tmp_article = tmp_article.replace('[ARTICLE_LINK]', '/articles/%s.html' % article['id'])

      tmp_article = tmp_article.replace('[ARTICLE_HEADER]', article['title'])
      tmp_article = tmp_article.replace('[ARTICLE_DESCRIPTION]', article['desc'])
      tmp_article = tmp_article.replace('[ARTICLE_YEAR]', '%s' % article['year'])
      tmp_article = tmp_article.replace('[ARTICLE_KEYWORDS]', article['keywords'])

      articles_index += tmp_article

      # generate article page
      if article['type'] == 'article':
        article_content = getFileContent( "%s/templates/articles/%s" % (buildDir, article['content_file'] ))
        writeFileContent('%s/articles/%s.html' % (static_dir, article['id']), index_page.replace("[ARTICLES]", article_content))


# generate index.html
for line in articles_index.split("\n"):
  try:
    line.encode('ascii')
    continue
  except:
    print line
writeFileContent('%s/test_index.html' % static_dir, index_page.replace("[ARTICLES]", articles_index))


# generate RSS feed

# generate about






# metaParser = graaMetaParser(buildDir + "")
# metaParser.parseMeta()


# pageGenerator = graaPageGen(buildDir, metaParser.metaDict)
# pageGenerator.loadTemplates()
# pageGenerator.generatePages()
