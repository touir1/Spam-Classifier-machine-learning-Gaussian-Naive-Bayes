import mailbox
import json
import jsonpickle
from six import string_types
from sys import maxunicode

_MBOX_PATH = 'messages.mbox'
non_bmp_map = dict.fromkeys(range(0x10000, maxunicode + 1), 0xfffd)

def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def handleerror(errmsg, emailmsg,cs):
    print()
    print(errmsg)
    print("This error occurred while decoding with ",cs," charset.")
    print("These charsets were found in the one email.",getcharsets(emailmsg))
    print("This is the subject:",emailmsg['subject'])
    print("This is the sender:",emailmsg['From'])

def getbodyfromemail(msg):
    body = None
    #Walk through the parts of the email to find the text body.    
    if msg.is_multipart():    
        for part in msg.walk():

            # If part is multipart, walk through the subparts.            
            if part.is_multipart(): 

                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        # Get the subpart payload (i.e the message body)
                        body = subpart.get_payload(decode=True) 
                        #charset = subpart.get_charset()

            # Part isn't multipart so get the email body
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                #charset = part.get_charset()

    # If this isn't a multi-part message then get the payload (i.e the message body)
    elif msg.get_content_type() == 'text/plain':
        body = msg.get_payload(decode=True) 

   # No checking done to match the charset with the correct part. 
    for charset in getcharsets(msg):
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            handleerror("UnicodeDecodeError: encountered.",msg,charset)
        except AttributeError:
            handleerror("AttributeError: encountered" ,msg,charset)
        except LookupError:
            handleerror("LookupError: encountered" ,msg,charset)
    return body

def cleanString(s):
    if isinstance(s, string_types):
        return s.replace('\n',' ').replace('\t',' ').replace('"',' ').replace('  ',' ').translate(non_bmp_map)
    else:
        return ''

mbox = mailbox.mbox(_MBOX_PATH)
to_file = {}
to_file['data'] = []

for message in mbox:
    now = {}
    now['subject'] = cleanString(message['Subject'])
    now['body'] = cleanString(getbodyfromemail(message))
    now['labels'] = message['X-Gmail-Labels']
    if now['labels'] is not None:
        if 'Spam' in now['labels'].split(','):
            now['type'] = 'spam'
        else:
            now['type'] = 'ham'
    else:
        now['type'] = 'ham'
    
    to_file['data'].append(now)
    #print('subject: ',now['subject'])
    #print('labels: ',now['labels'])
    print('type: ',now['type'])

with open("msgs.json", "w") as outfile:
    json_string = jsonpickle.encode(to_file)
    outfile.write(json_string)
    #json.dump(to_file, outfile, indent=4)
    
        
    
