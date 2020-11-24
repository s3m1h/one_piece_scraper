from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import requests
import re
import time
###
from util import (
    json_save,
    sup_cite_parser,
    sup_cite_parser2
)
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69"}
URL = {
    'strawhatpirates':'https://onepiece.fandom.com/wiki/Straw_Hat_Pirates',
    'pirate_crews':{
        'strawhatpirates':'https://onepiece.fandom.com/wiki/Straw_Hat_Pirates',
        'bigmom':'https://onepiece.fandom.com/wiki/Big_Mom_Pirates',
        'beasts':'https://onepiece.fandom.com/wiki/Beasts_Pirates',
        'redhair':'https://onepiece.fandom.com/wiki/Red_Hair_Pirates',
        'blacbeard':'https://onepiece.fandom.com/wiki/Blackbeard_Pirates',
        'whitebeard':'https://onepiece.fandom.com/wiki/Whitebeard_Pirates',
        'sun':'https://onepiece.fandom.com/wiki/Sun_Pirates',
        'buggys':'https://onepiece.fandom.com/wiki/Buggy%27s_Delivery',
        'heart':'https://onepiece.fandom.com/wiki/Heart_Pirates',
        'baroque':'https://onepiece.fandom.com/wiki/Baroque_Works',
        'donquixote':'https://onepiece.fandom.com/wiki/Donquixote_Pirates',
        'thriller_bark':'https://onepiece.fandom.com/wiki/Thriller_Bark_Pirates',
    },
    'characters':{
        # List of Canon Characters
        'lncanon': 'https://onepiece.fandom.com/wiki/List_of_Canon_Characters',
        # List_of_Non-Canon_Characters
        'noncanon': 'https://onepiece.fandom.com/wiki/List_of_Non-Canon_Characters'
    },
    'organizations':{
        'pirates': 'https://onepiece.fandom.com/wiki/Marines',
        'pirate_crews':'https://onepiece.fandom.com/wiki/Category:Pirate_Crews',
        'shichibukai':'https://onepiece.fandom.com/wiki/Seven_Warlords_of_the_Sea',
        'yonko':'https://onepiece.fandom.com/wiki/Four_Emperors',
        'word_government':'https://onepiece.fandom.com/wiki/World_Government',
        'revolutionary_army':'https://onepiece.fandom.com/wiki/Revolutionary_Army'
    },
    'impeldown': 'https://onepiece.fandom.com/wiki/Impel_Down'
    
}
### Characters
def straw_hat_prites_scrapy(path): #https://onepiece.fandom.com/wiki/Straw_Hat_Pirates --> table
    url = URL['strawhatpirates']
    req = requests.get(url, headers=HEADERS)
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
        items[name] = item
    json_save(items, path)
def pirate_crews_scrapy():
    req = requests.get(URL['pirate_crews']['whitebeard'], headers = HEADERS)
    soup = bs(req.content, 'html.parser')
    items = {}
    liste = ['status','age','birthday','height','bounty', 'occupations','epithet','japanese_name','devil_fruit','fruit']
    #print(soup('table',class_='cs')[0]('th')[0].text)
    for j in soup('div',class_='Gallery-pic')[:-2]:
        name = j.a.get('title')
        name_url = 'https://onepiece.fandom.com' + j.a.get('href')
        rq = requests.get(name_url, headers = HEADERS)
        view_soup = bs(rq.content, 'html.parser')
        aside = view_soup('aside')[0]
        # data verisinin içinde önce listedeki elemanları none olarak atıyoruz sebebi ise bazı karakterlerin bazı özellikleri yok 
        data = {}
        for li in liste:
            data[li] = None
        try:
            section0 = aside('section',class_='pi-item')[0]
            section1 = aside('section',class_='pi-item')[1]
        except:
            section1 = ''
        for i in section0('div')[:-2]:
            if i('h3') != []:
                h3 = i('h3')[0].text.lower().replace(':','').replace(' ','')
                for h3_name in liste:
                    if h3 == h3_name:
                        print(h3_name , i('div')[0].text)
                        data[h3_name] = sup_cite_parser2(i('div')[0].text.replace('\"','')).strip()
                        if section1 == '':
                            data['devil_fruit'] = None
                        else:
                            data['devil_fruit'] = 'yes'
                            data['fruit'] = sup_cite_parser2(section1('div')[0].find('div').text)
        items[name] = data
    json_save(items,'whitebeard') 
pirate_crews_scrapy()
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

def organizations_shichibukai_scrapy():
    req = requests.get(URL['organizations']['shichibukai'], headers = HEADERS)
    soup = bs(req.content, 'html.parser')
    items = {}
    for i in soup('table', class_='sortable')[0]('tr')[1:]:
        name = i('td')[0].a.get('title').lower()
        data = {
            'age': i('td')[1].text.strip().replace('\n',''),
            'height':i('td')[2].text[:5],
            'birthday':sup_cite_parser(i('td')[3].text.replace('\n','')),
            'bounty': sup_cite_parser(i('td')[4].text.replace('\n','')),
            'epithet':[i('td')[6].b.text if i('td')[6].b is not None else ''][0].lower()    
        }
        for powers in i('td')[5]('li'):
            data['abilities_and_powers'] = powers.text
        items[name] = data
    print(items)
    #json_save(items, 'shichibukai')
def organizations_yonko_scrapy():
    req = requests.get(URL['organizations']['yonko'], headers = HEADERS)
    soup = bs(req.content, 'html.parser')
    
if __name__=='__main__':
    # straw_hat_prites_scrapy('mugivara no lufi')
    pass
    #pirate_crews_scrapy()
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
    #organizations_shichibukai_scrapy()