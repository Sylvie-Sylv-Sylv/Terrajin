from terrajin.graph import *

input_1 = OutNode()
input_1.value = 1

input_2 = OutNode()
input_2.value = 2

add = AddNode(inputs = [input_1, input_2])

print(add())