from datetime import *
import random
from babel.dates import format_date
from tqdm import tqdm
import json



def string2int(str, length,vocab):
    str = str.lower()
    if(len(str)>length) :
        str=str[:length]
    rep = list(map(lambda x: vocab.get(x, '<unk>'), str))
    if len(str)<length:
        rep += [vocab['<pad>']] * (length - len(str))
    return 0


curdate = date.today()
daylength = 100*365.25
daydelta = timedelta(days=daylength)
begindate = curdate - daydelta
numsamples = 100000

#locales = ['ru_RU','es_ES','fr_FR','uk_UA','de_DE','fi_FI','sv_SE','be_BY'] #special digits locale
locales = ['ru_RU','uk_UA','be_BY']
formats = ['short','medium','long','full','d MMM YYY', 
           'd MMMM YYY',
           'dd MMM YYY',
           'd MMM, YYY',
           'd MMMM, YYY',
           'dd, MMM YYY',
           'd MM YY',
           'd MMMM YYY',
           'MMMM d YYY',
           'MMMM d, YYY',
           'dd.MM.YY']

human_vocab=set()
machine_vocab=set()
data=[]

Ty=10
Tx=0
## raw data generation
for i in tqdm(range(numsamples),desc="Initial generation") :
    locale = random.choice(locales)
    date1 = date.fromordinal(begindate.toordinal()+random.randrange(0,daylength))
    fmt = random.choice(formats)
    datestr=format_date(date1,format=fmt,locale=locale).lower().replace(",","")
    if len(datestr)>Tx: Tx=len(datestr)
    datemach=date1.isoformat().lower()
    human_vocab.update(tuple(datestr))
    machine_vocab.update(tuple(datemach))
    if fmt == 'short' : localind = 0 # special only digits locale
    data.append([datestr,locale,fmt,datemach])
    #print("{};{};{};{}".format(datestr,locale,fmt,datemach))

human = dict(zip(sorted(human_vocab) + ['<unk>', '<pad>'], 
                     list(range(len(human_vocab) + 2))))
inv_machine = dict(enumerate(sorted(machine_vocab)))
machine = {v:k for k,v in inv_machine.items()}

f = open("dataset.json","w")
data2write = {'data':data,'human':human,'machine':machine,'locales':locales,'inv_machine': inv_machine,'config':{'Tx':Tx,'Ty':Ty}}
json.dump(data2write,f)
f.close()