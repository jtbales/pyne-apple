import math
import copy
mostFrequentClassOverall = -1

class node():
    def __init__(self):
        self.leftNode = None # 0 side
        self.rightNode = None # 1 side
        self.data = []
        self.splitOn =""
        self.entropy = 1
        self.leafClass = None
        self.attributes = []

    def splitOnBestInformationGain (self):
        # Calculate current Entropy of node
        if self.entropy == None:
            self.calEntropy()
        H = self.entropy

        print(self.attributes)

        IGList = [] # Information Gain List
        for attribute in self.attributes:
            # Skip Class column and completed columns
            if attribute.lower() == "class":
                continue

            # New left and right splits to work with
            leftSplit = []
            rightSplit = []

            # Split data on attribute
            splitIndex = self.attributes.index(attribute)
            for row in self.data:
                if row[splitIndex] == '0':
                    leftSplit.append(row)
                else:
                    rightSplit.append(row)
            # print(leftSplit)

            # Calculate IG with formula
            H_L = calcEntropy(leftSplit, self.attributes.index("class"))
            H_R = calcEntropy(rightSplit, self.attributes.index("class"))
            P_L = len(leftSplit)/len(self.data)
            P_R = len(rightSplit)/len(self.data)
            IG = H - ((P_L*H_L)+(P_R*H_R))
            # print("{0:.3f}".format(IG) + " = " + "{0:.3f}".format(H) + "(( " + "{0:.3f}".format(P_L) + " * " + "{0:.3f}".format(H_L) + ")+(" + "{0:.3f}".format(P_R) + " * " + "{0:.3f}".format(H_R) + "))")
            IGList.append(IG)

        # Sets node to split on the attritute where we have maximum information gain
        # print(IGList)
        # if the best IG is positive and there is more than just the Class left to split on
        if len(IGList) > 0 and max(IGList) > 0 and len(IGList) > 0:
            # print(IGList.index(maxIG))
            self.splitOn = self.attributes[IGList.index(max(IGList))]
            # Nodes to split on
            self.leftNode = node()
            self.rightNode = node()

            # Split data on attribute
            print("Splitting on " + self.splitOn)
            splitIndex = self.attributes.index(self.splitOn)

            for row in self.data:
                if row[splitIndex] == '0':
                    self.leftNode.data.append(row)
                else:
                    self.rightNode.data.append(row)

            # Remove attribute column that was used
            childAttributes = self.attributes[:]
            del childAttributes[splitIndex]
            for row in self.data:
                del row[splitIndex]
            
            self.leftNode.attributes = childAttributes[:]
            self.rightNode.attributes = childAttributes

            # Calculate entropies
            self.leftNode.calEntropy()
            self.rightNode.calEntropy()
        else:
            self.splitOn = None
            self.calLeafClass()
            print("Done splitting on this node")

        return 

    # Easier call
    def calEntropy(self):
        self.entropy = calcEntropy(self.data, self.attributes.index("class"));

    def calLeafClass(self):
        total = 0
        for row in self.data:
            total += int(row[self.attributes.index("class")])

        # Tie breaking - If you reach a leaf node in the decision tree and have no examples left or the examples are equally split among multiple classes, then choose the class that is most frequent in the entire training set.
        if total == len(self.data)/2:
            self.leafClass = mostFrequentClassOverall
        # Set to the most frequent class
        else:
            print("total = " + str(total))
            print("len = " + str(len(self.data)))
            print("leafClass = " + str(round( total / len(self.data))))
            if round( total / len(self.data)) == 1 :
                print(self.data)
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
def ID3 (currentNode):
    # print("starting ID3")
    currentNode.splitOnBestInformationGain()

    # Base Case
    if currentNode.splitOn == None:
        return

    # Recursive calls
    if currentNode.leftNode.entropy != 0:
        ID3(currentNode.leftNode)
    else:
        # Pure node, determine class
        currentNode.leftNode.calLeafClass()

    if currentNode.rightNode.entropy != 0:
        ID3(currentNode.rightNode)
    else:
        # Pure node, determine class
        currentNode.rightNode.calLeafClass()

    return


def displayTree(currentNode, depth):
    # Base case
    if currentNode == None:
        return
    if currentNode.leftNode == None:
        print("  " + str(currentNode.leafClass), end='')
        return

    # Print what this node split on
    # 0 side
    print("\n" + "| " * depth + currentNode.splitOn + " = 0 :", end='')
    displayTree(currentNode.leftNode, depth+1)

    # 1 sides
    print("\n" + "| " * depth + currentNode.splitOn + " = 1 :", end='')
    displayTree(currentNode.rightNode, depth+1)

    pass

def getAccuracy(headNode, data):
    correct = 0

    # loop over data
    for row in data:
        # traverse binary tree
        nodeT = headNode
        while nodeT != None:
            # leaf node
            if nodeT.leafClass == 0 or nodeT.leafClass == 1:
                # add correct count
                # print("leaf class = " + str(nodeT.leafClass))
                # print("row class = " + row[headNode.attributes.index("class")])
                if int(nodeT.leafClass) == int(row[headNode.attributes.index("class")]):
                    correct += 1
                break
            # Go in direction of split
            else:
                # left
                if row[headNode.attributes.index(nodeT.splitOn)] == '0':
                    nodeT = nodeT.leftNode
                # right
                else:
                    nodeT = nodeT.rightNode

    return (correct / int(len(data))) * 100


def main():
    # Reading in data just reading in the training file (train.dat)
    with open("train.dat") as trainingFile, open ("test.dat") as testFile:
        first_line = trainingFile.readline()
        attributes = first_line.split()

        trainingData = []
        for line in trainingFile:
            trainingData.append(list(line.strip().replace('\t', '')))

        # print(trainingData)

        # Calculate most frequent class, set global instead of passing mostFrequentClassOverall or full dataset around to ever function
        total = 0
        for each in trainingData:
            total += int(each[attributes.index("class")])
        global mostFrequentClassOverall
        mostFrequentClassOverall \
            = round(total / len(trainingData))

        # this is where we initialize the headNode (the very first node)
        headNode = node()
        headNode.data = copy.deepcopy(trainingData)
        headNode.attributes = attributes[:]
        # Where the magic happens
        ID3(headNode)

        # Display the tree
        displayTree(headNode, 0)
        print()
        print()

        # Accuracy on training set
        trainingAccuracy = getAccuracy(headNode, trainingData)
        print("Accuracy on training set (" + str(len(trainingData)) + "): " + "{0:.1f}".format(trainingAccuracy) + "%")

        # Parse Test data
        testData = []
        for line in testFile:
            testData.append(line.strip().replace('\t', ''))
        testData.pop(0) # Remove headers

        # Accuracy on test set
        testAccuracy = getAccuracy(headNode, testData)
        print("Accuracy on test set (" + str(len(testData)) + "): " + "{0:.1f}".format(testAccuracy) + "%")



if __name__ == "__main__":
    main()




