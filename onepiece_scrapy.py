from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import requests
import re
import time
###
from util import json_save
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69"}
URL = {
    'characters':{
        'strawhatpirates': 'https://onepiece.fandom.com/wiki/Straw_Hat_Pirates',
        # List of Canon Characters
        'lncanon': 'https://onepiece.fandom.com/wiki/List_of_Canon_Characters',
        # List_of_Non-Canon_Characters
        'noncanon': 'https://onepiece.fandom.com/wiki/List_of_Non-Canon_Characters'
    },
    'organizations':{
        'marines': 'https://onepiece.fandom.com/wiki/Marines',
        'pirate_crews':'https://onepiece.fandom.com/wiki/Category:Pirate_Crews',
        'shichibukai':'https://onepiece.fandom.com/wiki/Seven_Warlords_of_the_Sea',
        'yonko':'https://onepiece.fandom.com/wiki/Four_Emperors',
        'word_government':'https://onepiece.fandom.com/wiki/World_Government',
        'revolutionary_army':'https://onepiece.fandom.com/wiki/Revolutionary_Army'
    }  
}
### Characters
def straw_hat_prites_scrapy(url_key):
    url = URL['characters'][url_key]
    req = requests.get(url, header=HEADERS)
    soup = bs(req.content, 'html.parser')
    table = soup('table',class_='sortable')
    items = {}
    for i in range(1,len(table[0]('tr')),2):
        name = table[0]('tr')[i].td.text.strip()
        unvan = table[0]('tr')[i]('td')[5]
        item = {
            'wiki_url':'https://onepiece.fandom.com' + table[0]('tr')[i].td.a.get('href'),
            'profession': table[0]('tr')[i]('td')[1].text.lower().strip(),
            'capabilities':table[0]('tr')[i]('td')[2].text.strip().lower().replace("",'').split('\n'),
            'epithet':[unvan.b.text.replace('"','') if unvan.b else unvan.text][0].lower()
        }
        view_url = requests.get(item['wiki_url'])
        view_soup = bs(view_url.content, 'html.parser')
        aside = view_soup('aside')[0]
        try:
            apt = aside('figure',class_="pi-image")[0].a.get('href')
            aprt = aside('figure',class_="pi-image")[1].a.get('href')
            mpt = aside('figure',class_="pi-image")[2].a.get('href')
            mprt = aside('figure',class_="pi-image")[3].a.get('href')
        except:
            apt = None
            aprt = None
            mpt = None
            mprt = None
        item['image_url'] ={
            'anime-post-timeskip': apt,
            'anime-pre-timeskip':aprt,
            'manga-post-timeskip':mpt,
            'manga-pre-timeskip':mprt
        }
        #pattern = re.compile(r'\[\d{1,}\]')
        f = aside.find('section',class_='pi-item')('div',class_='pi-item')
        age = f[11]('div')[0].text
        fiyat = f[14]('div')[0].text
        print(fiyat.split(re.search(r'\[\d{1,}\]',fiyat).group())[0])
        # for i in aside.find('section',class_='pi-item'):
        #     if i('h3')[0].text.replace(':','').lower().replace(' ','_') in liste:
        #         item[i('h3')[0].text.replace(':','').lower().replace(' ','_')] = i.find('div').text
        #items[name] = item
    #json_save(items,'mugiwara')
def straw_hat_prites_galery_scrapy(name, path):
    session = HTMLSession()
    req = session.get(f'https://onepiece.fandom.com/wiki/{name}/Gallery') 
    titles = bs(req.html.find('#toc')[0].html,'html.parser')
    items = {}
    a = 0
    for x in range(2,len(titles('li')) *2 -1, 2):
        image_table = req.html.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr/td/div[{x}]')
        soup = bs(image_table[0].html,'html.parser')
        liste = []
        for i in soup('span'):
            data = {
                'explanation':i('div')[0].text.lower().replace('\"','').replace('\n',''),
                'img_url':i('td')[0].a.get('href')
            }
            liste.append(data)
        items[req.html.find('.mw-headline')[a].text.lower().replace('&','-').replace(' (','_').replace(')','')] = liste
        a += 1
    json_save(items, path)
    
def lncanon_characters_scrapy():
    req = requests.get(URL['characters']['lncanon'], headers= HEADERS)
    soup = bs(req.content, 'html.parser')
    items = {}
    for x in range(2):
        for tr in soup('table',class_='wikitable')[x]('tr')[1:]:
            name = tr('td')[1].text
            data = {
                'name_url': 'https://onepiece.fandom.com'+ tr('td')[1].a.get('href'),
                'chapter_no': tr('td')[2].text.replace('\n',''),
                'chapter_no_url':['https://onepiece.fandom.com' + tr('td')[2].a.get('href') if tr('td')[2].a is not None else None][0],
                'epsido_no':tr('td')[3].text.replace('\n',''),
                'epsido_no_url':['https://onepiece.fandom.com'+ tr('td')[3].a.get('href') if tr('td')[3].a is not None else None][0],
                'year':tr('td')[4].text.replace('\n',''),
                'note':tr('td')[5].text.replace('\n','')
            }
            items[name.lower().replace(' ','_').replace('\n','')] = data
    json_save(items, 'lncanon')
    
def non_canon_characters_scrapy(): 
    req = requests.get(URL['characters']['noncanon'], headers=HEADERS)
    soup = bs(req.content, 'html.parser')
    items = {}
    for tr in soup('table',class_='wikitable')[0]('tr')[1:]:
        name = tr('td')[1].text
        data = {
            'name_url':'https://onepiece.fandom.com'+ tr('td')[1].a.get('href'),
            'type':tr('td')[2].text,
            'number':tr('td')[3].text,
            'year':tr('td')[4].text,
            'appears_in':tr('td')[5].text.replace('\n',''),
            'appears_in_url':['https://onepiece.fandom.com' + tr('td')[5].a.get('href') if tr('td')[5].a is not None else None][0]
        }
        items[name.lower()] = data
    json_save(items, 'noncanon1')
    
### Organizations
def organizations_marines_scrapy():
    req = requests.get(URL['organizations']['marines'], headers = HEADERS)
    soup = bs(req.content, 'html.parser')
    items = {}
    for i in soup('div',class_='Gallery-pic'):
        name = i.a.get('title')
        # data = {
        #     'name_url': ,
        #     #'image_url':i.img.get('data-src')
        # }
        items[name.lower()] = 'https://onepiece.fandom.com/' + i.a.get('href')
    json_save(items,'marines')
### TRENDING PAGES
def organizations_pirate_crews_scrapy():
    req = requests.get(URL['organizations']['pirate_crews'], headers = HEADERS)
    soup = bs(req.content, 'html.parser')
    items = {}
    for i in soup('ul',class_='category-page__trending-pages')[0]('li'):
        pirate_crews_name = i.a.text.lower().replace('\n','').strip()
        pirate_crews_url = i.a.get('href')
        rq = requests.get('https://onepiece.fandom.com'+ pirate_crews_url, headers=HEADERS)
        soupp = bs(rq.content, 'html.parser')
        liste = []
        for j in soupp('div',class_='Gallery-pic'):
            name = j.a.get('title')
            if j.a.img is not None:
                data = {
                    'name':j.a.get('title'),
                    'image':j.a.img.get('data-src')  
                }
                liste.append(data)
        items[pirate_crews_name] = liste
    print(items)
def organizations_shichibukai_scrapy():
    req = requests.get(URL['organizations']['shichibukai'], headers = HEADERS)
    soup = bs(req.content, 'html.parser')
    for i in soup('table', class_='sortable')[0]('tr')[1:]:
        name = i('td')[0].a.get('title').lower()
        birthday = re.search(r'\[\d{1,}\]',i('td')[3].text)
        bounty = re.search(r'\[\d{1,}\]',i('td')[4].text)
        data = {
            'age': i('td')[1].text.strip().replace('\n',''),
            'height':i('td')[2].text[:5],
            'birthday':[i('td')[3].text.replace(birthday.group(),'') if birthday is not None else ''][0],
            'bounty':[i('td')[4].text.replace(bounty.group(),'') if bounty is not None else ''][0],
        }
        for powers in i('td')[5]('li'):
            data['abilities_and_powers'] = powers.text
if __name__=='__main__':

    #straw_hat_prites_scrapy('strawhatpirates')
    
    # Straw hat prites galery
    #(Tony_Tony_Chopper, path)
    #straw_hat_prites_galery_scrapy('Monkey_D._Luffy','mdluffy')
    # straw_hat_prites_galerry_scrapy('Roronoa_Zoro')
    # straw_hat_prites_galerry_scrapy('Nami')
    # straw_hat_prites_galerry_scrapy('Sanji')
    # straw_hat_prites_galerry_scrapy('Tony_Tony_Chopper')
    # straw_hat_prites_galerry_scrapy('Nico_Robin')
    # straw_hat_prites_galerry_scrapy('Franky')
    # straw_hat_prites_galerry_scrapy('Brook')
    # straw_hat_prites_galerry_scrapy('Jinbe')

    #non_canon_characters_scrapy()
    #lncanon_characters_scrapy()
    
    #organizations_marines_scrapy()
    organizations_shichibukai_scrapy()