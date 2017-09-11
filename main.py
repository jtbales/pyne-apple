import math
import sys
mostFrequentClassOverall = -1

class node():
    def __init__(self):
        self.leftNode = None # 0 side
        self.rightNode = None # 1 side
        self.data = []
        self.splitOn =""
        self.entropy = 1
        self.leafClass = None

    def splitOnBestInformationGain (self, attributes):
        classIndex = attributes.index("class")

        # Calculate current Entropy of node
        if self.entropy == None:
            self.calEntropy(classIndex)
        H = self.entropy

        #print(attributes)

        IGList = [] # Information Gain List
        for attribute in attributes:
            # Skip Class column and completed columns
            if attribute.lower() == "class" or attribute == "splitColumn":
                continue

            # New left and right splits to work with
            leftSplit = []
            rightSplit = []

            # Split data on attribute
            index = attributes.index(attribute)
            for row in self.data:
                if row[index] == '0':
                    leftSplit.append(row)
                else:
                    rightSplit.append(row)
            # print(leftSplit)

            # Calculate IG with formula
            H_L = calcEntropy(leftSplit, classIndex)
            H_R = calcEntropy(rightSplit, classIndex)
            P_R = leftSplit.__sizeof__()/self.data.__sizeof__()
            P_L = rightSplit.__sizeof__()/self.data.__sizeof__()
            IG = H - ((P_L*H_L)+(P_R*H_R))
            IGList.append(IG)

        # Sets node to split on the attritute where we have maximum information gain
        #print(IGList)
        maxIG = max(IGList)
        if maxIG > 0 and attributes[IGList.index(maxIG)] != "splitColumn":
            self.splitOn = attributes[IGList.index(maxIG)]
            # Nodes to split on
            self.leftNode = node()
            self.rightNode = node()

            # Split data on attribute
            print("Splitting on " + self.splitOn)
            index = attributes.index(self.splitOn)

            # Mark split attribute as completed
            attributes[index] = "splitColumn"

            for each in self.data:
                if each[index] == '0':
                    self.leftNode.data.append(each)
                else:
                    self.rightNode.data.append(each)

            # Calculate entropies
            self.leftNode.calEntropy(classIndex)
            self.rightNode.calEntropy(classIndex)
        else:
            self.splitOn = None
            self.calLeafClass(classIndex)
            #print("Done splitting on this node")

        return

    # Easier call
    def calEntropy(self, classIndex):
        self.entropy = calcEntropy(self.data, classIndex);

    def calLeafClass(self, classIndex):
        total = 0
        for row in self.data:
            total += int(row[classIndex])

        # Tie breaking - If you reach a leaf node in the decision tree and have no examples left or the examples are equally split among multiple classes, then choose the class that is most frequent in the entire training set.
        if total == len(self.data)/2:
            self.leafClass = mostFrequentClassOverall
        # Set to the most frequent class
        else:
            # print("total = " + str(total))
            # print("len = " + str(len(self.data)))
            self.leafClass = round( total / len(self.data))
            # print("leafClass = " + str(self.leafClass))

def calcEntropy (data, classIndex):
    negatives = 0
    positives = 0
    for each in data:
        if each[classIndex]== '0':
            negatives = negatives + 1
        else:
            positives = positives + 1
    if negatives!=0 and positives != 0:
        P_1 = negatives / (negatives + positives)
        P_2 = positives/(negatives+positives)
        entropy = -(P_1)*math.log(P_1, 2) - (P_2)*math.log(P_2, 2)
        return entropy
    else:
        return 0 # Pure node

# Main ID3 algorithm
def ID3 (attributes, currentNode):
    # print("starting ID3")
    currentNode.splitOnBestInformationGain(attributes)

    # Base Case
    if currentNode.splitOn == None:
        return

    # Recursive calls
    if currentNode.leftNode.entropy != 0:
        ID3(attributes[:], currentNode.leftNode)
    else:
        # Pure node, determine class
        currentNode.leftNode.calLeafClass(attributes.index("class"))

    if currentNode.rightNode.entropy != 0:
        ID3(attributes[:], currentNode.rightNode)
    else:
        # Pure node, determine class
        currentNode.rightNode.calLeafClass(attributes.index("class"))

    return

def displayTree(currentNode, depth):
    # Base case
    if currentNode == None:
        return
    if currentNode.leftNode == None:
        print(str(currentNode.leafClass), end='')
        return

    # Print what this node split on
    # 0 side
    print("\n" + "| " * depth + currentNode.splitOn + " = 0 : ", end='')
    displayTree(currentNode.leftNode, depth+1)

    # 1 side
    print("\n" + "| " * depth + currentNode.splitOn + " = 1 : ", end='')
    displayTree(currentNode.rightNode, depth+1)

    pass

def getAccuracy(headNode, data, attributes):
    correct = 0

    # loop over data
    for row in data:
        # traverse binary tree
        node = headNode
        while node != None:
            # leaf node
            if node.leafClass == 0 or node.leafClass == 1:
                # add correct count
                # print("leaf class = " + str(node.leafClass))
                # print("row class = " + row[attributes.index("class")])
                if int(node.leafClass) == int(row[attributes.index("class")]):
                    correct += 1
                break
            # Go in direction of split
            else:
                # left
                if row[attributes.index(node.splitOn)] == 0:
                    node = node.leftNode
                else:
                    node = node.rightNode

    return (correct / int(len(data))) * 100


def main():
    if len(sys.argv)!=3:
        print ("requires two arguments. \"python3 <python file name> <training file> <testing file>\" ")
        exit()


    # Reading in data just reading in the training file (train.dat)
    with open(sys.argv[1]) as trainingFile, open (sys.argv[2]) as testFile:
        first_line = trainingFile.readline()
        attributes = first_line.split()

        trainingData = []
        for line in trainingFile:
            trainingData.append(line.strip().replace('\t', ''))

        # Calculate most frequent class, set global instead of passing mostFrequentClassOverall or full dataset around to ever function
        total = 0
        for each in trainingData:
            total += int(each[attributes.index("class")])
        global mostFrequentClassOverall
        mostFrequentClassOverall \
            = round(total / len(trainingData))

        # this is where we initialize the headNode (the very first node)
        headNode = node()
        headNode.data = trainingData[:]
        # Where the magic happens
        ID3(attributes[:], headNode)

        # Display the tree
        displayTree(headNode, 0)
        #print()
        #print()

        # Accuracy on training set
        trainingAccuracy = getAccuracy(headNode, trainingData, attributes)
        #print("Accuracy on training set (" + str(len(trainingData)) + "): " + "{0:.1f}".format(trainingAccuracy) + "%")

        # Parse Test data
        testData = []
        for line in testFile:
            testData.append(line.strip().replace('\t', ''))
        testData.pop(0) # Remove headers

        # Accuracy on test set
        testAccuracy = getAccuracy(headNode, testData, attributes)
        #print("Accuracy on test set (" + str(len(trainingData)) + "): " + "{0:.1f}".format(testAccuracy) + "%")



if __name__ == "__main__":
    main()




