import os
import time
import numpy as np
import pickle as pkl
from sys import maxunicode
from six import string_types
from base64 import b64decode
from optparse import OptionParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from sklearn.feature_extraction.text import CountVectorizer

_PROGRAM_NAME = os.path.basename(__file__)
_HOSTNAME = "localhost"
_CLASSIFIER_MODEL_FILE = "spam_classifier_model.pkl"
_VECTORIZER_FILE = "spam_vectorizer.pkl"
_PORT = 9000
_CLF = None
_VEC = None

parser = OptionParser(usage='Usage: %prog [options]')
parser.add_option("-c", "--classifier", dest="classifier",
                  help="import classifier from file", metavar="FILE")
parser.add_option("-v", "--vectorizer", dest="vectorizer",
                  help="import vectorizer from file", metavar="FILE")
parser.add_option("-p", "--port", dest="port",
                  help="port of the server", metavar="PORT")
parser.add_option("-a", "--adress", dest="adress",
                  help="adress of the server", metavar="ADRESS")

def cleanString(s):
    non_bmp_map = dict.fromkeys(range(0x10000, maxunicode + 1), 0xfffd)
    
    if isinstance(s, string_types):
        return s.replace('\n',' ').replace('\t',' ').replace('"',' ').replace('  ',' ').translate(non_bmp_map)
    else:
        return ''

def int_to_label(i):
    if i == 0:
        return 'ham'
    else:
        return 'spam'

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        params = self.path.split('/')
        if len(params) != 3:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("error with the path", "utf-8"))
        else:
            subject = None
            message = None
            try:
                subject = cleanString(b64decode(params[1]).decode('utf8'))
                message = cleanString(b64decode(params[2]).decode('utf8'))

                print("----- Subject: ",subject)
                print(message)
                
                spam_test = _VEC.transform(np.array([subject + " " + message])).toarray()
                prediction = _CLF.predict(spam_test)

                print("=> verdict:",int_to_label(prediction))

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(int_to_label(prediction), "utf-8"))
                
            except UnicodeDecodeError:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("error while decoding params, they need to be encoded in base64 with utf-8", "utf-8"))
            
            

def init():
    (options, args) = parser.parse_args()

    global _CLASSIFIER_MODEL_FILE
    global _VECTORIZER_FILE
    global _CLF
    global _VEC
    global _HOSTNAME
    global _PORT

    if options.classifier is not None:
        _CLASSIFIER_MODEL_FILE = options.classifier

    if options.vectorizer is not None:
        _VECTORIZER_FILE = options.vectorizer

    if options.adress is not None:
        _HOSTNAME = options.adress

    if options.port is not None:
        _PORT = int(options.port)

    try:
        with open(_CLASSIFIER_MODEL_FILE, 'rb') as f:
            _CLF = pkl.load(f)
        with open(_VECTORIZER_FILE, 'rb') as f:
            _VEC = pkl.load(f)
    except FileNotFoundError:
        error('The file \''+_CLASSIFIER_MODEL_FILE+'\' does not exist')

    myServer = HTTPServer((_HOSTNAME, _PORT), MyServer)
    print(time.asctime(), "Server Starts - %s:%s" % (_HOSTNAME, _PORT))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (_HOSTNAME, _PORT))

if __name__ == "__main__":
    init()
