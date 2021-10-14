import re
import os


def datasheetFormat(emojis,name,description='',url1='',url2=''):
    if url2:
        urls=f'\n   - 英文：{url1}\n   - 中文：{url2}'
    else:
        urls=url1
    if description or urls:
        return f'{emojis}**{name}**：{description}{" "if description and urls else ""}{urls}'
    else:
        return f'{emojis}**{name}**'

def parsedatasheet(path,defaultemoji=''):
    txt=open(path,encoding="utf-8").read()
    return parseinlinedatasheet(txt,defaultemoji)
    

def parseinlinedatasheet(txt,defaultemoji=''):
    lines=txt.splitlines()
    out=''
    counter=0
    if not defaultemoji:
        for line in lines:
            items=list(map(lambda x:x.strip(),line.split(',')))
            if len(items)>1:
                counter+=1
                out+=f'{counter}. '+datasheetFormat(*items)+"\n"
    else:
        for line in lines:
            items=list(map(lambda x:x.strip(),line.split(',')))
            if len(items)>0:
                counter+=1
                out+=f'{counter}. '+datasheetFormat(defaultemoji,*items)+"\n"
    return out

def parsefile(path):
    dir=os.path.dirname(path)
    t=open(path,encoding="utf-8").read()
    t=re.sub(r'{{#datasheet *: *([^)}{\n ]*?) *\n(.*?)}}',lambda x:parseinlinedatasheet(x[2],x[1]),t,flags=re.M|re.DOTALL)
    t=re.sub(r'{{#includedatasheet *: *([a-zA-Z0-9_\-\\//.]+)(?:| *\| *([^)}{\n ]+?)) *}}',lambda x:parsedatasheet(os.path.join(dir,x[1]),x[2]),t,flags=re.M)
    t=re.sub(r'{{#include *: *([a-zA-Z0-9_\-\\//.]+) *}}',lambda x:parsefile(os.path.join(dir,x[1])),t,flags=re.M)
    return t

if __name__=="__main__":
    t=parsefile("./toolbox/index.md")
    open("./README.md","w",encoding="utf-8").write(t)