# wikisource-scripts
Scripts I use for wikisource

Dependency: python3,pywikibot

##Usage
###Generating links
In the python shell:
```
> import gen
> #gen.genLinks(<סימן>)
> gen.genLinks('שולחן ערוך יורה דעה ב')
```
###Generating sub pages
In the python shell:
```
> import gen
> #gen.genPages(<book name>, <num of the סימן>, <num of סעיפים>)
> bookName = 'שולחן ערוך יורה דעה'
> gen.genPages(bookName, 2, 14)
```
