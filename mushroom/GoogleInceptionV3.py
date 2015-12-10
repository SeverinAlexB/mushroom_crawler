from keras.models import Graph
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.core import Activation
import datetime
'''
Inception v3 paper
http://arxiv.org/pdf/1512.00567v1.pdf

Old inception paper
http://arxiv.org/pdf/1409.4842.pdf

'''
def inception4g(pregraph, id):
    g = Graph()
    input_shape = list(pregraph.output_shape)
    input_shape.pop(0)
    g.add_input("input", input_shape)
    add_inception4(g,"input","incep4h")
    g.add_output("output", input="incep4h")
    return g

def add_inception4(pregraph, id):
    base = "input"
    input_shape = list(pregraph.output_shape)
    input_shape.pop(0)

    graph = Graph()
    graph.add_input(base, input_shape)

    graph.add_node(Convolution2D(16, 1, 1, activation="relu"), "conv1_1", "input")
    graph.add_node(ZeroPadding2D(padding=(2, 2)), "zero1_2", "conv1_1")
    graph.add_node(Convolution2D(32, 5, 5, activation="relu"), "conv1_3", "zero1_2")

    graph.add_node(Convolution2D(96, 1, 1, activation="relu"), "conv2_1", "input")
    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero2_2", "conv2_1")
    graph.add_node(Convolution2D(128, 3, 3, activation="relu"), "conv2_3", "zero2_2")

    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero3_1", "input")
    graph.add_node(MaxPooling2D((3, 3), stride=(1, 1)), "pool3_2", "zero3_1")
    graph.add_node(Convolution2D(32, 1, 1, activation="relu"), "conv3_3","pool3_2")

    graph.add_node(Convolution2D(64, 1, 1, activation="relu"), "conv4_1", "input")

    graph.add_output("output", inputs=["conv1_3", "conv2_3", "conv3_3", "conv4_1"], merge_mode="concat", concat_axis=1)
    return graph

def add_inception5(graph, base, id):
    graph.add_node(Convolution2D(16, 1, 1, activation="relu"), name=(id+"conv1_1"), input=base)
    graph.add_node(ZeroPadding2D(padding=(2, 2)), name=(id+"zero1_2"), input=(id+"conv1_1"))
    graph.add_node(Convolution2D(32, 3, 3, activation="relu"), name=(id+"conv1_3"), input=(id+"zero1_2"))
    graph.add_node(Convolution2D(32, 3, 3, activation="relu"), name=(id+"conv1_4"), input=(id+"conv1_3"))

    graph.add_node(Convolution2D(96, 1, 1, activation="relu"), name=(id+"conv2_1"), input=base)
    graph.add_node(ZeroPadding2D(padding=(1, 1)), name=(id+"zero2_2"), input=(id+"conv2_1"))
    graph.add_node(Convolution2D(128, 3, 3, activation="relu"), name=(id+"conv2_3"), input=(id+"zero2_2"))

    graph.add_node(ZeroPadding2D(padding=(1, 1)), name=(id+"zero3_1"), input=base)
    graph.add_node(MaxPooling2D((3, 3), stride=(1, 1)), name=(id+"pool3_2"), input=(id+"zero3_1"))
    graph.add_node(Convolution2D(32, 1, 1, activation="relu"), name=(id+"conv3_3"), input=(id+"pool3_2"))

    graph.add_node(Convolution2D(64, 1, 1, activation="relu"), name=(id+"conv4_1"), input=base)

    graph.add_node(Activation("linear"), name=id, inputs=[id+"conv1_4", id+"conv2_3", id+"conv3_3", id+"conv4_1"], merge_mode="concat", concat_axis=1)
    return id

def add_inception6(graph, base, id, n):
    graph.add_node(Convolution2D(16, 1, 1, activation="relu"), name=(id+"conv1_1"), input=base)
    graph.add_node(ZeroPadding2D(padding=(2, 2)), name=(id+"zero1_2"), input=(id+"conv1_1"))
    graph.add_node(Convolution2D(32, 1, n, activation="relu"), name=(id+"conv1_3"), input=(id+"zero1_2"))
    graph.add_node(Convolution2D(32, n, 1, activation="relu"), name=(id+"conv1_4"), input=(id+"conv1_3"))
    graph.add_node(Convolution2D(32, 1, n, activation="relu"), name=(id+"conv1_5"), input=(id+"conv1_4"))
    graph.add_node(Convolution2D(32, n, 1, activation="relu"), name=(id+"conv1_6"), input=(id+"conv1_5"))

    graph.add_node(Convolution2D(96, 1, 1, activation="relu"), name=(id+"conv2_1"), input=base)
    graph.add_node(ZeroPadding2D(padding=(1, 1)), name=(id+"zero2_2"), input=(id+"conv2_1"))
    graph.add_node(Convolution2D(128, 1, n, activation="relu"), name=(id+"conv2_3"), input=(id+"zero2_2"))
    graph.add_node(Convolution2D(128, n, 1, activation="relu"), name=(id+"conv2_4"), input=(id+"conv2_3"))

    graph.add_node(ZeroPadding2D(padding=(1, 1)), name=(id+"zero3_1"), input=base)
    graph.add_node(MaxPooling2D((3, 3), stride=(1, 1)), name=(id+"pool3_2"), input=(id+"zero3_1"))
    graph.add_node(Convolution2D(32, 1, 1, activation="relu"), name=(id+"conv3_3"), input=(id+"pool3_2"))

    graph.add_node(Convolution2D(64, 1, 1, activation="relu"), name=(id+"conv4_1"), input=base)

    graph.add_node(Activation("linear"), name=id, inputs=[id+"conv1_6", id+"conv2_4", id+"conv3_3", id+"conv4_1"], merge_mode="concat", concat_axis=1)
    return id

def printl(name):
    print str(datetime.datetime.now()) + name

def create_model():
    input_shape = (3,244,244)
    graph = Graph()

    graph.add_input(name="input", input_shape=input_shape)
    graph.add_node(Convolution2D(32, 3, 3, subsample=(2,2), activation="relu"), name="conv1", input="input")
    graph.add_node(Convolution2D(32, 3,3, activation="relu"), name="conv2", input="conv1")
    graph.add_node(Convolution2D(64, 3,3, activation="relu"), name="conv3", input="conv2")
    graph.add_node(MaxPooling2D((3, 3), stride=(2, 2)), name="pool4", input="conv3")
    graph.add_node(Convolution2D(80, 3,3, activation="relu"), name="conv5", input="pool4")
    graph.add_node(Convolution2D(192, 3,3, subsample=(2,2), activation="relu"), name="conv6", input="conv5")
    graph.add_node(Convolution2D(288, 3,3, activation="relu"), name="conv7", input="conv6")
    graph.add_output("output", input="conv7")

    g = inception4g(graph, "inasdf")

    inceptionv3 = Graph()
    inceptionv3.add_input("main_in",input_shape)
    inceptionv3.add_node(graph, "first", "main_in")
    inceptionv3.add_node(g,"second", "first")
    inceptionv3.add_output("output","second")
    inceptionv3.compile(optimizer='rmsprop', loss={'output':'mse'})
    '''
    base = "conv7"
    for i in range(3):
        base = add_inception4(graph,base,"inception4_" + str(i) + "_")
        printl(base)

    for i in range(5):
        base = add_inception5(graph,base,"inception5_" + str(i) + "_")
        printl(base)

    for i in range(2):
        base = add_inception6(graph,base,"inception6_" + str(i) + "_", 3)
        printl(base)

    '''
    for node in graph.nodes:
        print node
    return graph



graph = create_model()
print graph
