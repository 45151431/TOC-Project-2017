from transitions.extensions import GraphMachine
import urllib.request
from html.parser import HTMLParser

class HTMLParser1(HTMLParser):
    t = 0
    table = 0
    s = ''
    cnt = 0
    def handle_starttag(self, tag, attrs):
        if tag=='td':
            self.t = 1
            self.cnt = self.cnt+1
        if tag=='table':
            self.table = self.table+1
            self.cnt = 0
    def handle_endtag(self, tag):
        if tag=='td':
            self.t = 0
        if tag=='table' and self.table>=3:
            self.cnt = 0
    def handle_data(self, data):
        if self.t==1 and self.table>=3:
            if self.cnt==1:
                self.s = self.s+str(self.table-2)+'.'
                self.s = self.s+data
                self.s = self.s+'\n'

class HTMLParser2(HTMLParser):
    t = 0
    table = 0
    s = ''
    cnt = 0
    movie = []
    def handle_starttag(self, tag, attrs):
        if tag=='td':
            self.t = 1
            self.cnt = self.cnt+1
        if tag=='table':
            self.table = self.table+1
            self.cnt = 0
    def handle_endtag(self, tag):
        if tag=='td':
            self.t = 0
        if tag=='table' and self.table>=3:
            self.movie.append(self.s)
            self.s = ''
            self.cnt = 0
    def handle_data(self, data):
        if self.t==1 and self.table>=3:
            self.s = self.s+data
            if self.cnt==1:
                self.s = self.s+'\n'
            if self.cnt>1 and self.cnt%3==1:
                self.s = self.s+'\n'


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_user(self, update):
        text = update.message.text
        return text == 'back'

    def is_going_to_usererror(self, update):
        text = update.message.text
        return text != 'TN' and text != 'NF' and text != 'NFGC'

#TN
    def is_going_to_TNstate1(self, update):
        text = update.message.text
        return text == 'TN'

    def is_going_to_TNstate2(self, update):
        text = update.message.text
        return text == 'search'

    def is_going_to_TNstate3(self, update):
        text = update.message.text
        return check1(text) and TNcheck2(text)

    def is_going_to_TNerror1(self, update):
        text = update.message.text
        return text != 'search' and text != 'back'

    def is_going_to_TNerror2(self, update):
        text = update.message.text
        return check1(text)==False or TNcheck2(text)==False

#NF
    def is_going_to_NFstate1(self, update):
        text = update.message.text
        return text == 'NF'

    def is_going_to_NFstate2(self, update):
        text = update.message.text
        return text == 'search'

    def is_going_to_NFstate3(self, update):
        text = update.message.text
        return check1(text) and NFcheck2(text)

    def is_going_to_NFerror1(self, update):
        text = update.message.text
        return text != 'search' and text != 'back'
    
    def is_going_to_NFerror2(self, update):
        text = update.message.text
        return check1(text)==False or NFcheck2(text)==False

#NFGC
    def is_going_to_NFGCstate1(self, update):
        text = update.message.text
        return text == 'NFGC'

    def is_going_to_NFGCstate2(self, update):
        text = update.message.text
        return text == 'search'

    def is_going_to_NFGCstate3(self, update):
        text = update.message.text
        return check1(text) and NFGCcheck2(text)

    def is_going_to_NFGCerror1(self, update):
        text = update.message.text
        return text != 'search' and text != 'back'

    def is_going_to_NFGCerror2(self, update):
        text = update.message.text
        return check1(text)==False or NFGCcheck2(text)==False

    def on_enter_user(self, update):
        update.message.reply_text('請輸入代號以選擇台南影城:\nTN=>台南大遠百威秀\nNF=>台南南紡威秀\nNFGC=>台南南紡威秀(gold class)')

    def on_exit_user(self, update):
        print('Leaving user')

    def on_enter_usererror(self, update):
        self.go_back(update)

    def on_exit_usererror(self, update):
        print('Leaving usererror')

#TN
    def on_enter_TNstate1(self, update):
        update.message.reply_text('請輸入search 搜尋台南大遠百威秀院線電影\n或輸入back 重新選擇台南影城')

    def on_exit_TNstate1(self, update):
        print('Leaving TNstate1')

    def on_enter_TNstate2(self, update):
        response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=TN&visLang=2')
        html = response.read().decode('utf-8')
        parser = HTMLParser1()
        parser.feed(html)
        update.message.reply_text('請選擇電影編號\n'+parser.s)

    def on_exit_TNstate2(self, update):
        print('Leaving TNstate2')

    def on_enter_TNstate3(self, update):
        response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=TN&visLang=2')
        html = response.read().decode('utf-8')
        parser = HTMLParser2()
        parser.movie = []
        parser.feed(html)
        update.message.reply_text(parser.movie[int(update.message.text.lower())-1])
        self.TNback1(update)

    def on_exit_TNstate3(self, update):
        print('Leaving TNstate3')

    def on_enter_TNerror1(self, update):
        update.message.reply_text('錯誤輸入')
        self.TNback1(update)

    def on_exit_TNerror1(self, update):
        print('Leaving TNerror1')

    def on_enter_TNerror2(self, update):
        update.message.reply_text('錯誤輸入')
        self.TNback2(update)

    def on_exit_TNerror2(self, update):
        print('Leaving TNerror2')

#NF
    def on_enter_NFstate1(self, update):
        update.message.reply_text('請輸入search 搜尋台南南紡威秀院線電影\n或輸入back 重新選擇台南影城')

    def on_exitNFstate1(self, update):
        print('Leaving NFstate1')

    def on_enter_NFstate2(self, update):
        response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=NF&visLang=2')
        html = response.read().decode('utf-8')
        parser = HTMLParser1()
        parser.feed(html)
        update.message.reply_text('請選擇電影編號\n'+parser.s)

    def on_exit_NFstate2(self, update):
        print('Leaving NFstate2')

    def on_enter_NFstate3(self, update):
        response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=NF&visLang=2')
        html = response.read().decode('utf-8')
        parser = HTMLParser2()
        parser.movie = []
        parser.feed(html)
        update.message.reply_text(parser.movie[int(update.message.text.lower())-1])
        self.NFback1(update)

    def on_exit_NFstate3(self, update):
        print('Leaving NFstate3')

    def on_enter_NFerror1(self, update):
        update.message.reply_text('錯誤輸入')
        self.NFback1(update)

    def on_exit_NFerror1(self, update):
        print('Leaving NFerror1')

    def on_enter_NFerror2(self, update):
        update.message.reply_text('錯誤輸入')
        self.NFback2(update)

    def on_exit_NFerror2(self, update):
        print('Leaving NFerror2')

#NFGC
    def on_enter_NFGCstate1(self, update):
        update.message.reply_text('請輸入search 搜尋台南南紡(gold class)威秀院線電影\n或輸入back 重新選擇台南影城')

    def on_exit_NFGCstate1(self, update):
        print('Leaving NFGCstate1')

    def on_enter_NFGCstate2(self, update):
        response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=NFGC&visLang=2')
        html = response.read().decode('utf-8')
        parser = HTMLParser1()
        parser.feed(html)
        update.message.reply_text('請選擇電影編號\n'+parser.s)

    def on_exit_NFGCstate2(self, update):
        print('Leaving NFGCstate2')

    def on_enter_NFGCstate3(self, update):
        response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=NFGC&visLang=2')
        html = response.read().decode('utf-8')
        parser = HTMLParser2()
        parser.movie = []
        parser.feed(html)
        update.message.reply_text(parser.movie[int(update.message.text.lower())-1])
        self.NFGCback1(update)

    def on_exit_NFGCstate3(self, update):
        print('Leaving NFGCstate3')

    def on_enter_NFGCerror1(self, update):
        update.message.reply_text('錯誤輸入')
        self.NFGCback1(update)

    def on_exit_NFGCerror1(self, update):
        print('Leaving NFGCerror1')

    def on_enter_NFGCerror2(self, update):
        update.message.reply_text('錯誤輸入')
        self.NFGCback2(update)

    def on_exit_NFGCerror2(self, update):
        print('Leaving NFGCerror2')

def check1(s):
    if s=='1':
        return 1==1
    if s=='2':
        return 1==1
    if s=='3':
        return 1==1
    if s=='4':
        return 1==1
    if s=='5':
        return 1==1
    if s=='6':
        return 1==1
    if s=='7':
        return 1==1
    if s=='8':
        return 1==1
    if s=='9':
        return 1==1
    if s=='10':
        return 1==1 
    if s=='11':
        return 1==1
    if s=='12':
        return 1==1
    if s=='13':
        return 1==1
    if s=='14':
        return 1==1
    if s=='15':
        return 1==1
    if s=='16':
        return 1==1
    if s=='17':
        return 1==1
    if s=='18':
        return 1==1
    if s=='19':
        return 1==1
    if s=='20':
        return 1==1 
    if s=='21':
        return 1==1
    if s=='22':
        return 1==1
    if s=='23':
        return 1==1
    if s=='24':
        return 1==1
    if s=='25':
        return 1==1
    if s=='26':
        return 1==1
    if s=='27':
        return 1==1
    if s=='28':
        return 1==1
    if s=='29':
        return 1==1
    if s=='30':
        return 1==1   
    if s=='31':
        return 1==1
    if s=='32':
        return 1==1
    if s=='33':
        return 1==1
    if s=='34':
        return 1==1
    if s=='35':
        return 1==1
    if s=='36':
        return 1==1
    if s=='37':
        return 1==1
    if s=='38':
        return 1==1
    if s=='39':
        return 1==1
    if s=='40':
        return 1==1
    return 1==2

def TNcheck2(s):
    response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=TN&visLang=2')
    html = response.read().decode('utf-8')
    parser = HTMLParser2()
    parser.movie = []
    parser.feed(html)
    if(int(s)>parser.table-2):
        return 1==2 
    else:
        return 1==1

def NFcheck2(s):
    response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=NF&visLang=2')
    html = response.read().decode('utf-8')
    parser = HTMLParser2()
    parser.movie = []
    parser.feed(html)
    if(int(s)>parser.table-2):
        return 1==2 
    else:
        return 1==1
        
def NFGCcheck2(s):
    response = urllib.request.urlopen('http://www.vscinemas.com.tw/visPrintShowTimes.aspx?cid=NFGC&visLang=2')
    html = response.read().decode('utf-8')
    parser = HTMLParser2()
    parser.movie = []
    parser.feed(html)
    if(int(s)>parser.table-2):
        return 1==2 
    else:
        return 1==1
