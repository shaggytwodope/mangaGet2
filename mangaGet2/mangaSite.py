import re
try:
    import mangaGet2.util as util
except:
    import util

# Aliases
time = util.time
memorize, Util, webpage = util.memorize, util.Util, util.webpage
mktime, strptime, localtime = time.mktime, time.strptime, time.localtime

class mangaSite():
    class Series(webpage):
        siteTemplate = NotImplemented
        seriesTemplate  = NotImplemented    
        soupArgs = NotImplemented
        
        def __init__(self, series, extras='None'):
            self.extras = extras
            self.series = series
            self.title = series
            if self.extras:
                self.runExtras()
        
        @property
        @memorize
        def chapters(self):
            return [self.Chapter(link['href'], self) for link in self.soup.findAll(**self.soupArgs)[::-1]]
        @property
        @memorize
        def url(self):
            return self.seriesTemplate.format(self.series)
        
        class Chapter(webpage):
            listThem = NotImplemented
            
            def __init__(self, link, series):
                self.link = link
                self.series = series
                
            #def pages(self):
                #yield self.Page(self.link, self)
                #for i in self.listThem:
                    #yield self.Page(i['href'], self)
            @property
            @memorize
            def pages(self):
                hold = [self.Page(self.link, self)]
                for i in self.listThem:
                    hold.append(self.page(i['href'], self))
                return hold
            @property
            def pages_len(self):
                return len(self.listThem)+1
            @property
            def title(self):
                return 
            @property
            @memorize
            def url(self):
                return self.series.siteTemplate.format(self.link)
            
            class Page(webpage):
                picCompile = NotImplemented
            
                def __init__(self, page, chapter):
                    self.chapter = chapter
                    self.cookie  = chapter.cookie
                    self.page    = page
                    
                @property
                def image(self):
                    return self.chapter.Image(self.imgUrl, self.name)
                @property
                def name(self):
                    return
                @property
                @memorize
                def url(self):
                    return self.chapter.series.siteTemplate.format(self.page)
                
            class Image():
                
                def __init__(self, url, nameIt=None):
                    self.nameIt=nameIt
                    self.url = url
                    self.urlObj = Util.getUrl(self.url)
                    self.meta = self.urlObj.info()
                    self.data = self.dataGen
                    
                @property
                def dataGen(self):
                    while True:
                        data = self.urlObj.read()
                        contentLen = self.meta.getheader('Content-Length')
                        if len(data) == int(contentLen):
                            break
                        else:
                            del self.urlObj
                            self.urlObj = Util.getUrl(self.url)
                    return data
                