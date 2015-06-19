from urllib2    import urlopen
from json       import load as json_load
from markdown   import markdown 
from csv        import writer as csv_writer, QUOTE_ALL
from re         import compile


#_root_url = 'https://api.github.com/repos/aa989190f363e46d/zhernochemistry/issues?state=all&per_page=100'
_root_url = 'https://api.github.com/repositories/28739378/issues?state=all&per_page=100'

url = _root_url
issues = []

while True:
  fd = urlopen(url)
  links = fd.headers.dict['link']  
  pagination = {link[-5:-1]:url[1:-1] for url, link in [l.split('; ') for l in links.split(', ')]}
  issues.extend(json_load(fd))  
  if not pagination.has_key('last'):
    break
  url = pagination['next']

bodies =  bb = [i['body'].split('\r\n') for i in issues]
titles = [i['title'] for i in issues]

rslt = {}
splt_re = compile('^(\S+?): *(.*)')
#for n,iss_flds in enumerate([[fld.split(': ') for fld in iss] for iss in bodies]):
for n,iss_flds in enumerate([[splt_re.split(fld)[1:3] for fld in iss] for iss in bodies]):  
  try:
    for k,v in iss_flds:
      if not rslt.has_key(k):
        rslt[k] = [v.encode('utf-8')]
      else:
        rslt[k].append(v.encode('utf-8'))
  except:
    print n,k

if not all([len(rslt[k]) for k in rslt.keys()]):
  BaseException("Categories length not equal")

rslt[rslt.keys()[2]] = [markdown(k.decode('utf-8')).encode('utf-8') for k in rslt[rslt.keys()[2]]]

with open('iss-cards.csv', 'wb') as csvfile:
  writer = csv_writer(csvfile, delimiter=';', quotechar="'", quoting=QUOTE_ALL)
  writer.writerows(zip(titles
    ,[u'<img src="%s.png">' % (name,) for name in titles]
    ,*rslt.values()))

#=========================

from pygithub3 import Github
from markdown  import markdown 

_repo = 'zhernochemistry'
_author = 'aa989190f363e46d'
_splitter_re = u'\n*(МНН|Синонимы|Класс|ИЮПАК|Применение):\s*'
_p_cleaner_re = "^<p>|</p>$"

def body_formatter(body_text):
  body_parts = re.split(_splitter_re,body_text)[2:11:2]
  return [re.sub(_p_cleaner_re,'',markdown(p).encode('utf-8')) for p in body_parts]

issues = [[i.title, u'<img src="%s.png">' % (i.title,)] + body_formatter(i.body) for i in gh.issues.list_by_repo(_author, _repo).all() if i.state == 'open']

with open('iss-cards.csv', 'wb') as csvfile:
  writer = csv_writer(csvfile, delimiter=';', quotechar="'", quoting=QUOTE_ALL)
  writer.writerows(issues)