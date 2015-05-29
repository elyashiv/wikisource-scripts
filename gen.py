import gim
import pywikibot

template = '''{{{{סעיף שולחן ערוך|{}|{}|{}|הקודם={}|הבא={}}}}}

<sub>[[#שולחן ערוך|▲ חזור לראש]]</sub>
'''

def genPage(page, siman, seif, last = False):
    siman = gim.toGStr(siman)
    Cseif = gim.toGStr(seif)
    Pseif = gim.toGStr(seif - 1) if seif > 1 else ''
    Nseif = gim.toGStr(seif + 1) if not last else ''
    book  = ' '.join(page.title().split(' ')[2:4])
    txt = template.format(book,siman, Cseif, Pseif, Nseif)
    page.text = txt
    page.save(comment = "הוספת סעיף בשולחן ערוך, בוצע על ידי בוט", async=True)


def genPages(siman, m, n):
    site = pywikibot.getSite('he', 'wikisource')
    siman = siman + ' ' + gim.toGStr(m)
    for i in range(n):
        pageName = siman + ' ' + gim.toGStr(i + 1)
        page = pywikibot.Page(site, pageName)
        if not page.exists():
            genPage(page, m, i + 1, i + 1 == n)

def genLinks(pageName):
    secbeg = '\n<קטע התחלה={}/>\n'
    secend = '\n<קטע סוף={}/>\n'
    link   = '[[{} {}|{}]]'
    site = pywikibot.getSite('he', 'wikisource')
    page = pywikibot.Page(site, pageName)
    text = page.text.split('==')
    start = text.pop(0)
    headers = text[::2]
    data    = text[1::2]
    res = [start]
    for h,d in zip(headers, data):
        s = h.split(' ')[-1]
        if s.endswith(']]'): s = s[:-2]
        if not h.startswith('[['):
            h = link.format(pageName, s, h)
        if not d.strip().startswith('<'):
            d = secbeg.format(s) + d.strip() + secend.format(s)
        res += [h,d]
    text = '=='.join(res)
    page.text = text
    page.save(comment = 'הוספת קישורים לסעיפים, נעשה על ידי בוט')

def getN(t):
  l = t.split('\n')[0].split('|')[-1][:-2]
  return int(l)

def genAll(nameT, iterator):
  site = pywikibot.getSite()
  for i in iterator:
    page = pywikibot.Page(site, nameT + gim.toGStr(i))
    if page.exists():
      n = getN(page.text)
      genPages(nameT, i, n)
      genLinks(nameT + gim.toGStr(i))
