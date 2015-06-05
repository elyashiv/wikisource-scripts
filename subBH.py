import re
import pywikibot
import gim

r = re.compile('^={2}[^=]*={2}$', re.MULTILINE)
site = pywikibot.getSite()

def doIt(pname, i, override=False):
    page = pywikibot.Page(site, pname)
    t = page.text
    l = re.split(r, t)
    l.pop(0)
    sub('באר היטב על אבן העזר {}',
        '{{{{פרשן על שו"ע|באר היטב|אבן העזר|{}|{}|{}}}}}', i, l, override)

def sub(nameTmp, hTmp, i, l, override=False):
    for b in l:
        p = pywikibot.Page(site, nameTmp.format(gim.toGStr(i)))
        s = hTmp.format(gim.toGStr(i-1), gim.toGStr(i), gim.toGStr(i+1))
        s += b
        if override or not p.exists():
            p.text = s
            p.save()
        i += 1
