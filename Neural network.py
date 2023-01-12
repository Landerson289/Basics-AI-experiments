def stringPop(string, index): #Function for deleting an letter from a string based off of its index

  list = []
  for i in string:
    list.append(i)

  list.pop(index)

  newString = ""
  for i in list:
    newString += i

  return newString

class Node:
  def __init__(self, layer, index):
    self.layer = layer  #Which layer the node is in
    self.index = index  #Which index in the list of nodes in the layer this node is.
    self.weights = [
    ]  #The value that you multiply all of the out going values by.
    self.biasWeight = 0  #The weight the balance node is multiplied by

  def get_weights(self):  ###Change Code To Allow For Machine Learning And Store The Weights in a file and read them of a file

    nodeList = open("weights.txt").read().splitlines()
    nodeList.pop(0)

    for i in nodeList:
      layer, index, weightsString = i.split(", ")
      #print(layer,index,self.layer,self.index,layer == self.layer and index == self.index)
      if int(layer) == self.layer and int(index) == self.index:
        if weightsString != "[]":
          weightsString = stringPop(weightsString, 0)
          #print(weightsString)
          weightsString = stringPop(weightsString, -1)
  
          weightsList = weightsString.split(",")

          for i in range(len(weightsList)): 
            weightsList[i] = int(weightsList[i])
        else: 
          weightsList = []

        if self.layer != len(layers)-1:
          if len(weightsList) != len(layers[self.layer+1].nodes): #Validation check
            print("ERROR: NUMBER OF WEIGHTS NOT EQUAL TO NUMBER OF NODES IN NEXT LAYER")
            #print()
            quit()

        self.weights = weightsList
        print(self.weights)
    
    """
    if self.layer != len(layers)-1:
      length = len(layers[self.layer + 1].nodes)
      for i in range(length):
        self.weights.append(1)
    """
    
  def update(self):
    self.get_weights()

    if self.layer == 0:
      self.value = int(input("ENTER 0 or 1\n>>>"))
    elif self.layer == len(layers):
      pass
    else:
      inputNodes = layers[self.layer - 1].nodes
      inputs = []
      for i in inputNodes:
        #print(self.layer)
        if self.layer != 0:
          inputs.append(i.outputs[self.index])

      self.value = self.biasWeight
      for i in inputs:
        self.value += i

      if self.value > 0:
        self.value = 1
      else:
        self.value = 0

    self.outputs = []
    for i in range(len(self.weights)):
      self.outputs.append(self.weights[i] * self.value)


class Layer:
  def __init__(self, number, nodes):
    self.number = number
    self.nodes = nodes

  def update(self):
    for i in self.nodes:
      i.update()


layers = [
  Layer(0, [Node(0, 0), Node(0, 1), Node(0, 2)]),
  Layer(1, [Node(1, 0), Node(1, 1), Node(1, 2)]),
  Layer(2, [Node(2, 0), Node(2, 1), Node(2, 2)]),
]

def run():
  for i in layers:
    i.update()
  
  for i in layers:
    for j in i.nodes:
      print(str(j.value),end=" ")
    print("\n")
