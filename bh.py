import urllib.request
from lxml import etree

def getBHlist(page):
    tree = etree.HTML(urllib.request.urlopen(page).read().decode('windows-1255'))
    return tree.xpath("//span[@style='font-size:32px; '] | //span[@style='font-size:70%;']")

def formatBH(elemL):
    from re import findall, sub
    txt = ''
    for i in elemL.itertext():
        txt += i
    l = findall('\(.*?\).*?: ', txt)
    ret = ''
    for i in l:
        ret += sub(r'\((.*)\) (.*?)\. (.*): ',
                   r'{{משע|בהט|\1|\2:}} \3.',
                   i).replace("''",'"')
        ret += '\n\n'
        
    return ret.strip()#, l[0].startswith('(א)')
    
def check(s):
    tmp = ''
    for i in s.itertext():
        tmp += i
    return tmp.strip().startswith('א')
def getBH(page, startN = 1):
    """get the paragraphs of BH from page.
    The paragraphs will be seperated by a header.
    Use startN for pages that don't start on siman א"""
    import gim
    h1t = '==סימן {}=='
    h2t = '===סעיף {0}===\n<קטע התחלה={0}/>'
    close = '<קטע סוף={}/>'
    currentS = startN - 1
    res = []
    l = getBHlist(page)
    i = 0
    for s in l:
        if s.get('style') == 'font-size:32px; ':
            i = i + 1
            restart = check(s)
            if restart:
                i = 1
                currentS += 1
                res.append(h1t.format(gim.toGStr(currentS)))
        else:
            text = formatBH(s)
            res.append(h2t.format(gim.toGStr(i)))
            res.append(text)
            res.append(close.format(gim.toGStr(i)))
    return '\n'.join(res)
