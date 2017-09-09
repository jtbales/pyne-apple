import math


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
        print (each)
        if each[classIndex]==0:
            negatives = negatives + 1
        else:
            positives = positives + 1
    print(negatives, " ", positives)
    #print (negatives/(negatives+positives))
    #P_2 = positives/(negatives+positives)
    #entropy = -(P_1)*math.log(P_1, 2) - (P_2)*math.log(P_2, 2)
    return entropy


def informationGain (data, arguments, headNode):
    #print (data)
    #print (arguments)
    classIndex = arguments.__len__()-1
    headNode.leftNode = node()
    headNode.rightNode = node()
    for argument in arguments:
        index = arguments.index(argument)
        for each in data:
            if each[index] == '0':
                headNode.leftNode.data.append(each)
            else:
                headNode.rightNode.data.append(each)
        print (calcEntropy(headNode.leftNode, classIndex))

def main():
    # Reading in data just reading in the training file (train.dat)
    with open("train.dat") as trainingFile:
        first_line = trainingFile.readline()
        argments = first_line.split()
        headNode = node()
        for line in trainingFile:
            headNode.data.append(line.strip().replace('\t', ''))
        informationGain(headNode.data, argments, headNode)

if __name__ == "__main__":
    main()




