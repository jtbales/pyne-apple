import math

class node():
    def __init__(self):
        self.leftNode = None # 0 side
        self.rightNode = None # 1 side
        self.data = []
        self.splitOn =""
        self.entropy = 1
        self.leafClass = None

    def splitOnBestInformationGain (self, attributes):
        classIndex = len(attributes)-1

        # Calculate current Entropy of node
        if self.entropy == None:
            self.calEntropy(classIndex)
        H = self.entropy

        print(attributes)

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
            for each in self.data:
                if each[index] == '0':
                    leftSplit.append(each)
                else:
                    rightSplit.append(each)
            # print(leftSplit)

            # Calculate IG with formula
            H_L = calcEntropy(leftSplit, classIndex)
            H_R = calcEntropy(rightSplit, classIndex)
            P_R = leftSplit.__sizeof__()/self.data.__sizeof__()
            P_L = rightSplit.__sizeof__()/self.data.__sizeof__()
            IG = H - ((P_L*H_L)+(P_R*H_R))
            IGList.append(IG)

        # Sets node to split on the attritute where we have maximum information gain
        print(IGList)
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
            print("Done splitting on this node")

        return

    # Easier call
    def calEntropy(self, classIndex):
        self.entropy = calcEntropy(self.data, classIndex);

    def calLeafClass(self, classIndex):
        total = 0
        for each in self.data:
            total += int(each[classIndex])
        # Set to the most frequet class
        print("total = " + str(total))
        print("len = " + str(len(self.data)))
        self.leafClass = round( total / len(self.data))
        print("leafClass = " + str(self.leafClass))

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
    print("starting ID3")
    currentNode.splitOnBestInformationGain(attributes)

    # Base Case
    if currentNode.splitOn == None:
        return

    # Recursive calls
    if currentNode.leftNode.entropy != 0:
        ID3(attributes[:], currentNode.leftNode)
    else:
        # Pure node, determine class
        currentNode.leftNode.calLeafClass(len(attributes) - 1)

    if currentNode.rightNode.entropy != 0:
        ID3(attributes[:], currentNode.rightNode)
    else:
        # Pure node, determine class
        currentNode.rightNode.calLeafClass(len(attributes) - 1)

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


def main():
    # Reading in data just reading in the training file (train.dat)
    with open("train.dat") as trainingFile:
        first_line = trainingFile.readline()
        attributes = first_line.split()
        #this is where we initialize the headNode (the very first node)
        headNode = node()
        for line in trainingFile:
            headNode.data.append(line.strip().replace('\t', ''))
        #somewhere here I expect to have to implement recursion but I haven't worked it out yet
        #information gain is calculated in the next two functions and returns the value we need to split by
        # Where the magic happens
        ID3(attributes[:], headNode)
        displayTree(headNode, 0)


if __name__ == "__main__":
    main()




