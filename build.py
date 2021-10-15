import re
import os


def datasheetFormat(emojis,name,description='',url1='',url2='',*args):
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
    defaultemoji=defaultemoji or ""
    lines=txt.splitlines()
    out=''
    counter=0
    for line in lines:
        items=list(map(lambda x:x.strip(),line.split(',')))
        if len(items)>1:
            counter+=1
            out+=f'{counter}. {defaultemoji}'+datasheetFormat(*items)+"\n"
    return out

def parsefile(path):
    dir=os.path.dirname(path)
    t=open(path,encoding="utf-8").read()
    t=re.sub(r'{{#datasheet *: *([^)}{\n ]*?) *\n(.*?)}}',lambda x:parseinlinedatasheet(x[2],x[1]),t,flags=re.M|re.DOTALL)
    t=re.sub(r'{{#includedatasheet *: *([a-zA-Z0-9_\-\\//.]+)(?:| *\| *([^)}{\n ]+?)) *}}',lambda x:parsedatasheet(os.path.join(dir,x[1]),x[2]),t,flags=re.M)
    t=re.sub(r'{{#include *: *([a-zA-Z0-9_\-\\//.]+) *}}',lambda x:parsefile(os.path.join(dir,x[1])),t,flags=re.M)
    t=re.sub(r'{{#([^}{]+?)}}',lambda x:f'<!--{x[1]}-->',t,flags=re.M|re.DOTALL)
    return t

if __name__=="__main__":
    INPUT_FILE="./toolbox/index.md"
    OUTPUT_FILE="README.md"

    with open(OUTPUT_FILE,"w",encoding="utf-8") as f:
        f.write(parsefile(INPUT_FILE))
    print("Program finished.")