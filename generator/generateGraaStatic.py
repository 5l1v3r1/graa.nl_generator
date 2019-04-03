from graa.functions import *
from xml.sax.saxutils import escape as xmlescape
import yaml

buildDir = getBuildDir()
static_dir = "%s/static/" % buildDir

# Load yaml metadata
with open(buildDir + '/meta/graa.yaml') as f:
  site_config = yaml.safe_load(f)['site_config']

# grab template files
main_template = getFileContent( "%s/templates/page.template" % buildDir )
article_template = getFileContent( "%s/templates/article.template" % buildDir )
menuitem_template = getFileContent( "%s/templates/menuitem.template" % buildDir )
rss_template = getFileContent( "%s/templates/rss.xml.template" % buildDir )
rss_item_template = getFileContent( "%s/templates/rss.xml.item.template" % buildDir )

# Add config data to index page
index_page = main_template

index_page = index_page.replace('[SITE_TITLE]', site_config['site_title'])
rss_template = rss_template.replace('[SITE_TITLE]', site_config['site_title'])

index_page = index_page.replace('[SITE_DESCRIPTION]', site_config['site_desc'])
rss_template = rss_template.replace('[SITE_DESCRIPTION]', site_config['site_desc'])

blog_page = index_page.replace('[MENU_ITEMS]','''
  <li><a href = "/index.html" class = "selected">Blog</a></li>
  <li><a href = "/advisories.html">Advisories</a></li>
  <li><a href = "/programming.html">Programming</a></li>
  <li><a href = "/about.html" >About</a></li>
  <li><a href = "/articles/3099.html">Contact</a></li>
  ''')
advisory_page = index_page.replace('[MENU_ITEMS]','''
  <li><a href = "/index.html">Blog</a></li>
  <li><a href = "/advisories.html" class = "selected">Advisories</a></li>
  <li><a href = "/programming.html">Programming</a></li>
  <li><a href = "/about.html" >About</a></li>
  <li><a href = "/articles/3099.html">Contact</a></li>
  ''')
programming_page = index_page.replace('[MENU_ITEMS]','''
  <li><a href = "/index.html">Blog</a></li>
  <li><a href = "/advisories.html">Advisories</a></li>
  <li><a href = "/programming.html" class = "selected">Programming</a></li>
  <li><a href = "/about.html" >About</a></li>
  <li><a href = "/articles/3099.html">Contact</a></li>
  ''')
about_page = index_page.replace('[MENU_ITEMS]','''
  <li><a href = "/index.html">Blog</a></li>
  <li><a href = "/advisories.html">Advisories</a></li>
  <li><a href = "/programming.html">Programming</a></li>
  <li><a href = "/about.html" class = "selected">About</a></li>
  <li><a href = "/articles/3099.html">Contact</a></li>
  ''')

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
articles_advisories = ""
articles_programming = ""
articles_about = ""

rss_items = []

article_ids.sort()
for article_id in reversed(article_ids):
  for article in articles:
    if article['id'] == article_id:
      # print article

      if article['type'] == 'link':
        new_link = article['link']
      else:
        new_link = '/articles/%s.html' % article['id']

      # generate rss item
      rss_tmp = rss_item_template
      rss_tmp = rss_tmp.replace("[RSS_ITEM_TITLE]", xmlescape(article['title']))
      rss_tmp = rss_tmp.replace("[RSS_ITEM_CATEGORY]", xmlescape(article['section']))
      rss_tmp = rss_tmp.replace("[RSS_ITEM_GUID]", xmlescape(new_link))
      rss_tmp = rss_tmp.replace("[RSS_ITEM_LINK]", xmlescape(new_link))

      rss_items.append(rss_tmp)

      # generate index page entry
      tmp_article = article_template
      tmp_article = tmp_article.replace('[ARTICLE_LINK]', new_link)
      tmp_article = tmp_article.replace('[ARTICLE_HEADER]', article['title'])
      tmp_article = tmp_article.replace('[ARTICLE_DESCRIPTION]', article['desc'])
      tmp_article = tmp_article.replace('[ARTICLE_YEAR]', '%s' % article['year'])
      tmp_article = tmp_article.replace('[ARTICLE_KEYWORDS]', article['keywords'])

      if article['section'] == 'Blog':
        articles_index += tmp_article
      if article['section'] == 'Advisory':
        articles_advisories += tmp_article
      if article['section'] == 'Programming':
        articles_programming += tmp_article
      if article['section'] == 'About':
        articles_about += tmp_article

      # generate article page
      if article['type'] == 'article':
        article_content = getFileContent( "%s/templates/articles/%s" % (buildDir, article['content_file'] ))
        if article['section'] == 'Blog':
          writeFileContent('%s/articles/%s.html' % (static_dir, article['id']), blog_page.replace("[ARTICLES]", article_content))
        if article['section'] == 'Advisory':
          writeFileContent('%s/articles/%s.html' % (static_dir, article['id']), advisory_page.replace("[ARTICLES]", article_content))
        if article['section'] == 'Programming':
          writeFileContent('%s/articles/%s.html' % (static_dir, article['id']), programming_page.replace("[ARTICLES]", article_content))
        if article['section'] == 'About':
          writeFileContent('%s/articles/%s.html' % (static_dir, article['id']), about_page.replace("[ARTICLES]", article_content))



# generate index.html
writeFileContent('%s/index.html' % static_dir, blog_page.replace("[ARTICLES]", articles_index))
writeFileContent('%s/advisories.html' % static_dir, advisory_page.replace("[ARTICLES]", articles_advisories))
writeFileContent('%s/programming.html' % static_dir, programming_page.replace("[ARTICLES]", articles_programming))
writeFileContent('%s/about.html' % static_dir, about_page.replace("[ARTICLES]", articles_about))


# generate RSS feed
fullRSS = rss_template.replace("[RSS_ITEMS]", "\n".join(rss_items))
writeFileContent("%s/rss.xml" % static_dir, fullRSS )
