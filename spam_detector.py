import os
import pickle as pkl
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from optparse import OptionParser

_PROGRAM_NAME = os.path.basename(__file__)
_CLASSIFIER_MODEL_FILE = "spam_classifier_model.pkl"
_VECTORIZER_FILE = "spam_vectorizer.pkl"

def int_to_label(i):
    if i == 0:
        return 'ham'
    else:
        return 'spam'

def error(msg):
    print('Error: ',msg,'\nFor help type: ',_PROGRAM_NAME,' -h')
    quit()

parser = OptionParser(usage='Usage: %prog [options]')
parser.add_option("-c", "--classifier", dest="classifier",
                  help="import classifier from file", metavar="FILE")
parser.add_option("-v", "--vectorizer", dest="vectorizer",
                  help="import vectorizer from file", metavar="FILE")
parser.add_option("-m", "--message", dest="message",
                  help="required: classify the message given", metavar="MESSAGE")
parser.add_option("-s", "--subject", dest="subject",
                  help="required: classify the subject given", metavar="SUBJECT")

def script():
    (options, args) = parser.parse_args()

    global _CLASSIFIER_MODEL_FILE
    global _VECTORIZER_FILE
    
    clf = None
    subject = None
    message = None
    vec = None

    if options.message is not None:
        message = options.message
    else:
        error('Message was not given')

    if options.subject is not None:
        subject = options.subject
    else:
        error('Subject was not given')

    if options.classifier is not None:
        _CLASSIFIER_MODEL_FILE = options.classifier

    if options.vectorizer is not None:
        _VECTORIZER_FILE = options.vectorizer

    try:
        with open(_CLASSIFIER_MODEL_FILE, 'rb') as f:
            clf = pkl.load(f)
        with open(_VECTORIZER_FILE, 'rb') as f:
            vec = pkl.load(f)
    except FileNotFoundError:
        error('The file \''+_CLASSIFIER_MODEL_FILE+'\' does not exist')
        
    spam_test = vec.transform(np.array([subject + " " + message])).toarray()
    prediction = clf.predict(spam_test)
    print(int_to_label(prediction))

if __name__ == "__main__":
    script()
