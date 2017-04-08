import sys

labelList = []
tokenSet = set([])
dict = {}
denominator = {}
numerator = []
output = ""

def readLabeled(inputFile):
    with open(inputFile) as f:
        content = f.readlines()
    return content

def paddingData(sent,padding):
    pads = "#"
    for j in range(1,padding): 
        pads = pads + "#"
    sent = pads + sent + pads;
    return sent

def train(data,ngrams):
    padding = ngrams - 1
    for i in range(0,len(data)):
        splitData = data[i].split("|")
        sent = paddingData(splitData[1],padding)
        label = splitData[2].replace("\n","")
        buildMap(sent,label,ngrams)
    return

def buildMap(sent,label,ngrams):
    if label not in dict.keys():
        dict[label] = {}
        labelList.append(label)
    pointer = 0
    while(pointer < len(sent) - ngrams - 1):
        token =  sent[pointer : pointer + ngrams]
        if token not in dict[label]:
            dict[label][token] = 1
        else:
            dict[label][token] = dict[label][token] + 1
        pointer = pointer + 1
    return

def setDenom(lam):
    for i in range(0,len(labelList)):
        denominator[labelList[i]] = float(denom(labelList[i],lam)/1000)
    return

def denom(lang,lam):
    sum1 = 0
    for i in range(0,21):
        sum1 = sum1 + len(dict[labelList[i]])
    den = lam * float(sum1) + sum(dict[lang].values())
    return den

def naiiveBayes(testsent,ngrams,lam):
    numerator = [1] * len(labelList)
    pointer = 0
    prob = [1] * len(labelList)
    while(pointer < len(testsent) - ngrams - 1):
        token =  testsent[pointer : pointer + ngrams]
        for i in range(0,len(labelList)):
            if token not in dict[labelList[i]]:
                numerator[i] = lam
            else:
                numerator[i] = dict[labelList[i]][token]
            prob[i] = prob[i] * (float(numerator[i] + lam) / denominator[labelList[i]])
        pointer = pointer + 1
    return labelList[prob.index(max(prob))]

def test(testdata,ngrams,lam):
    padding = ngrams - 1
    oneshot = 0
    output = ""
    for i in range(0,len(testdata)):
        splitData = testdata[i].split("|")
        testsent = paddingData(splitData[1],padding)
        testlabel = splitData[2].replace("\n","")
        hypo = naiiveBayes(testsent,ngrams,lam)
        output = output + splitData[0] + "|" + hypo + "\n"
        if (hypo) == testlabel:
            oneshot = oneshot + 1
    return output

def main(args,ngrams,lam):
    data = readLabeled(args[1])
    train(data,ngrams)
    setDenom(lam)
    testdata = readLabeled(args[2])
    return test(testdata,ngrams,lam)

if __name__ == '__main__':
    lam = float(sys.argv[4])
    n = int(sys.argv[3])
    main(sys.argv,n,lam)
    
