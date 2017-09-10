import math

#made some teeny tiny changes to the original code
class node():
    def __init__(self):
        self.leftNode = None
        self.rightNode = None
        self.data = []
        self.splitOn =""

def calcEntropy (node, classIndex):
    negatives = 0
    positives = 0
    entropy = 0
    for each in node.data:
        if each[classIndex]== '0':
            negatives = negatives + 1
        else:
            positives = positives + 1
    if negatives!=0 and positives != 0:
        P_1 = negatives / (negatives + positives)
        P_2 = positives/(negatives+positives)
        entropy = -(P_1)*math.log(P_1, 2) - (P_2)*math.log(P_2, 2)
        return entropy
    # it is 34 for no reason but this just exists when the node is pure.
    # we probably need to use this in recursion
    # As a reminder: recursion ends when the node is pure or all the attributes have been exhausted
    return 34;


def informationGain (data, arguments, headNode):
    classIndex = arguments.__len__()-1
    headNode.leftNode = node()
    headNode.rightNode = node()
    H = calcEntropy(headNode, classIndex)
    IGList = []
    for argument in arguments:
        if argument.lower() == "class":
            continue
        headNode.leftNode.data = []
        headNode.rightNode.data = []
        index = arguments.index(argument)
        for each in data:
            if each[index] == '0':
                headNode.leftNode.data.append(each)
            else:
                headNode.rightNode.data.append(each)
        #print(headNode.leftNode.data)
        H_L = calcEntropy(headNode.leftNode, classIndex)
        H_R = calcEntropy(headNode.rightNode, classIndex)
        P_R = headNode.rightNode.data.__sizeof__()/headNode.data.__sizeof__()
        P_L = headNode.leftNode.data.__sizeof__()/headNode.data.__sizeof__()
        IG = H - ((P_L*H_L)+(P_R*H_R))
        IGList.append(IG)
    # returns the value of the attritute where we have maximum information gain
    return arguments[IGList.index(max(IGList))]

def main():
    # Reading in data just reading in the training file (train.dat)
    with open("train.dat") as trainingFile:
        first_line = trainingFile.readline()
        argments = first_line.split()
        #this is where we initialize the headNode (the very first node)
        headNode = node()
        for line in trainingFile:
            headNode.data.append(line.strip().replace('\t', ''))
        #somewhere here I expect to have to implement recursion but I haven't worked it out yet
        #information gain is calculated in the next two functions and returns the value we need to split by
        headNode.splitOn = informationGain(headNode.data, argments, headNode)
        print (headNode.splitOn)

if __name__ == "__main__":
    main()




