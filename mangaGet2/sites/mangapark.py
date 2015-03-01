import re
from mangaGet2.mangaSite import mangaSite
from mangaGet2.util import memorize

class mangapark(mangaSite):
    tags = ['mp', 'mangapark']
    class Series(mangaSite.Series):
        siteTemplate = 'http://www.mangapark.com{}'
        seriesTemplate = siteTemplate.format('/manga/{}/')
        soupArgs = {'name': 'div', 'class_': 'stream'}
        version = 0
        
        @property
        @memorize
        def chapters(self):
            return [self.Chapter(tag.find(text='all').parent['href'], self) 
                    for tag in self.soup.findAll(**self.soupArgs)[self.version].findAll('em')[::-1]]
        def runExtras(self):
            #if type(self.extras) == type(''):
                #self.extras = [self.extras]
            for i in self.extras.split(','):
                if 'ver' in i:
                    self.version = int(i.split('=')[-1])-1
        
        class Chapter(mangaSite.Series.Chapter):
            @property
            @memorize
            def listThem(self):
                return self.soup.findAll('img', class_='img')
            @property
            @memorize
            def pages(self):
                return [self.Page(i['src'].split('?')[0], self) for i in self.listThem]
            @property
            def title(self):
                hold = self.url.split('/')[-2:]
                hold[0] = ''.join(['v', '{:0>2}'.format(hold[0].strip('v'))])
                hold[-1] = hold[-1].strip('c')                                                                                                                                            
                if '.' in hold[-1]:
                    hold[-1] = '{:0>3}.{:0>2}'.format(*hold[-1].split('.'))
                else:
                    hold[-1] = '{:0>3}'.format(hold[-1])
                if not 's' in hold[0]:
                    return '_'.join(hold)
                return hold[-1]
            
            class Page(mangaSite.Series.Chapter.Page):
                @property
                def imgUrl(self):
                    return self.page
                @property
                def name(self):
                    hold = self.imgUrl.split('/')[-1].split('.')
                    return '.'.join(['{:0>3}'.format(hold[0]), hold[1]])
