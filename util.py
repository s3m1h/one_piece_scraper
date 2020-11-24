import json
import re

def sup_cite_parser2(tag):
    odul2 =""
    for i in tag:
        if i == '[' or i =='(':
            break
        else:
            odul2 += i
    return odul2
def sup_cite_parser(tag):
    a =  re.search(r'\[\d{1,}\]',tag)
    if a is not None:
        return tag.replace(a.group(),'')
    return 
    
def json_save(data,path):
    with open(path + '.json','w',encoding='utf8') as f:
        json.dump(data, f,indent=4,ensure_ascii=False)
        f.write('\n')
    