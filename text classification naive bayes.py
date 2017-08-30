from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
import json
import random
import numpy as np
import pickle as pkl

_DATA_FILE = "msgs_2.json"
_CLASSIFIER_MODEL_FILE = "spam_classifier_model.pkl"
_VECTORIZER_FILE = "spam_vectorizer.pkl"

def label_to_int(lbl):
    if lbl == 'ham':
        return 0
    else:
        return 1

def split_array(arr,size):
    result = []
    remaining = len(arr)
    now = 0
    while remaining != 0:
        new = []
        if remaining >= size:
            for i in range(size):
                new.append(arr[i+now])
            remaining = remaining - size
            now = now + size
        else:
            for i in range(remaining):
                new.append(arr[i+now])
            now = now + remaining
            remaining = 0
        result.append(new)
    return result 

vec = CountVectorizer()
clf = GaussianNB()

messages = []
labels = []

with open(_DATA_FILE) as data_file:
    data = np.asarray(json.loads(data_file.read())['data'])
    random.shuffle(data)
    for d in data:
        clean_data = d['subject'] + " " + d['body']
        clean_labels = d['type']
        messages.append(clean_data)
        labels.append(clean_labels)

msg = np.array(split_array(messages,500))
lbl = np.array(split_array(labels,500))

for idx,m in enumerate(msg):
    int_data = []
    if idx == 0:
        int_data = vec.fit_transform(m).toarray()
    else:
        int_data = vec.transform(m).toarray()
    
    int_labels = np.array([label_to_int(x) for x in lbl[idx]])
    if idx == 0:
        clf.partial_fit(int_data, int_labels, classes=np.unique(int_labels))
    else:
        clf.partial_fit(int_data, int_labels)

spam_test = vec.transform(np.array(["Western Union Money Transfer I have sent you several notices concerning the claim of your benefit that was paid to you as compensation from Benin Republic following my petition against the Government as a human right activist to compensate you with the sum of $1,500,000.00USD But I have not heard from you ever since and I hope you will reply this last notice. You were meant to be receiving $10,000.00usd daily until it completes the correct amount of $1,500,000.00USD For better understanding of what I mean, please copy this link https://wumt.westernunion.com/ asp/order Status.asp?country=CN browser Then enter the following details on the displayed box fields and click CHECK STATUS to track your money online with,  (1) Sender's Name:--------------MARK CABALLERO MTCN : -------------- 6344558979 Text Question:--------------- urgent Answer: --------------- yes Amount: --------------- USD $5000 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXX (2) Sender's Name:--------------SANTOS CABALLERO MTCN : -------------- 6344558979 Text Question:--------------- urgent Answer: --------------- yes Amount: --------------- USD $5000  The status now shows Available for pick up by receiver because this amount has been on the system so long for security reasons, since I did not get any reply message from you after sending you several notices with the transaction details to enable you pick up your MTCN, Now you are strongly advised for the last time to go on to make payment of $95 usd for the activation charges via western union money transfer immediately with the details of the western union agent in Benin.  LIKE I SAID YOUR URGE TO SEND THE $95 TO BELOW INFORMATION OKAY.  RECEIVER NAME; SAMUEL ADILI COUNTRY;............ BENIN REPUBLIC CITY................COTONOU TEST QUESTION; URGENT ANSWER; YES AMOUNT; $95 MTCN...............  And send the payment details via email as it clearly appear on the western union slip because it is impossible and illegal to em-bed the activation charges from the total funds transferred because of the lawful restriction that has been placed on your funds that restricts anyone from tempering with your funds. This amount will be made available again within 20 minutes at your resident local western union office after you have settled the activation fee and I will avail you with the full details of the first 2 M.T.C.N CONTROL NUMBERS of $10,000,00usd.IMPORTANT NOTICE: If your payment for the activation fee is not received after Four(4) days this time around, you risk forfeiting your benefit permanently.  NOTE; YOU WILL BE PICKING UP YOUR TWO TRANSFER TODAY IMMEDIATELY YOU SEND THIS 95 FOR US TO REACTIVATE YOUR TRANSFER AND DIRECT IT FOR YOU TO BE ABLE TO PICK IT UP IN YOUR COUNTRY TODAY.  Regards Mr. Anthony Robert Western Union Money Transfer Phone number +229 61 91 26 35 Email ) westernunion5678@gmail.com"])).toarray()
ham_test = vec.transform(np.array(["Access Expiring CompTIA IT Fundamentals Course Hi there,  The CompTIA IT Fundamentals Course of the Month expires in 4 days!  Get 19 hours of networking, security, hardware, and software training—for free as part of a Premium Membership or Team Account.  Take advantage of this training and certification opportunity by upgrading and enrolling before 8/31—you’ll continue to unlock a free, featured course every month."])).toarray()
print("spam?: ",clf.predict(spam_test)," ham?: ",clf.predict(ham_test))

with open(_CLASSIFIER_MODEL_FILE, 'wb') as f:
    pkl.dump(clf, f)
with open(_VECTORIZER_FILE, 'wb') as f:
    pkl.dump(vec, f)
