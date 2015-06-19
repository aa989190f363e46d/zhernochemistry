from pygithub3 import Github
from time import sleep

_repo = 'zhernochemistry'
#_repo = 'quizCensor'
_author = 'aa989190f363e46d'

template = u"""МНН: %s
Синонимы: 
Класс: 
ИЮПАК: 
Применение: . [ru:w:](), [en:w:](), [ru:lm:]()"""

#['cards_page_{0:0>2}_{1}_{2}'.format(*i) for i in list(product(range(1,57),range(1,3),range(1,4)))]

with open('card-names') as source:
  rows = [re.split('\t{2,2}',i.strip()) for i in source.readlines()]

auth = dict(login='aa989190f363e46d@googlemail.com',\
            password='p8Uwyy*J')
gh = Github(**auth)

for e,card in enumerate(rows):

  print '%02.0d. %s' % (e,card[0])

  data_dict = dict(title       = '%s' % card[0],
                    body       = template % card[1].decode('utf-8'),
                    #assignee   = 'aa989190f363e46d',
                    assignee   = 'kate-b',
                    labels     = ['bug', 'wontfix', 'invalid'])

  gh.issues.create(data_dict, _author, _repo)
  sleep(1)