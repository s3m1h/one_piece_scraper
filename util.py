import json
import re
def json_save(data,path):
    with open(path + '.json','w',encoding='utf8') as f:
        json.dump(data, f,indent=4,ensure_ascii=False)
        f.write('\n')
    