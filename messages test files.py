import json
import jsonpickle
from six import string_types
from sys import maxunicode
from os import listdir
from os.path import isfile, join

_EMAIL_PATH = "./CSDMC2010_SPAM/dest"
_LABEL_PATH = "./CSDMC2010_SPAM/SPAMTrain.label"

non_bmp_map = dict.fromkeys(range(0x10000, maxunicode + 1), 0xfffd)

def cleanString(s):
    if isinstance(s, string_types):
        return s.replace('\n',' ').replace('\t',' ').replace('"',' ').replace('  ',' ').translate(non_bmp_map)
    else:
        return ''

onlyfiles = [f for f in listdir(_EMAIL_PATH) if isfile(join(_EMAIL_PATH, f))]

to_file = {}
to_file['data'] = []

labels = []

with open(_LABEL_PATH) as f:
    content = f.readlines()
    labels = [int(x.strip().split(' ')[0]) for x in content]
    
count = 0
for file_name in onlyfiles:
    with open(_EMAIL_PATH + "/" + file_name, "r") as infile:
        content = infile.readlines()
        content = [x.strip() for x in content]
        msg = cleanString(' '.join(content))
        now = {}
        now['subject'] = ''
        now['body'] = msg
        now['type'] = ''
        if labels[count] == 0:
            now['type'] = 'spam'
        else:
            now['type'] = 'ham'
        to_file['data'].append(now)
        count = count + 1
        
with open("msgs_2.json", "w") as outfile:
    json_string = jsonpickle.encode(to_file)
    outfile.write(json_string)
