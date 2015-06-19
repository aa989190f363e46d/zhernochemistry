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