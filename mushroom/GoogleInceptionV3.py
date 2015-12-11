from keras.models import Graph
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.advanced_activations import PReLU
import datetime
'''
Inception v3 paper
http://arxiv.org/pdf/1512.00567v1.pdf

Old inception paper
http://arxiv.org/pdf/1409.4842.pdf

'''
def activation_function():
    return "relu"

def cinput_shape(graph):
    shape = list(graph.output_shape)
    shape.pop(0)
    return shape

def conv(input_shape):
    graph = Graph()
    graph.add_input("input", input_shape)

    graph.add_node(Convolution2D(32, 3, 3, subsample=(2,2), activation=activation_function()), name="conv1", input="input")
    graph.add_node(Convolution2D(32, 3,3, activation=activation_function()), name="conv2", input="conv1")
    graph.add_node(Convolution2D(64, 3,3, activation=activation_function()), name="conv3", input="conv2")
    graph.add_node(MaxPooling2D((3, 3), stride=(2, 2)), name="pool4", input="conv3")
    graph.add_node(Convolution2D(80, 3,3, activation=activation_function()), name="conv5", input="pool4")
    graph.add_node(Convolution2D(192, 3,3, subsample=(2,2), activation=activation_function()), name="conv6", input="conv5")
    graph.add_node(Convolution2D(288, 3,3, activation=activation_function()), name="conv7", input="conv6")
    graph.add_output("output", input="conv7")
    return graph

def inception4(input_shape):
    graph = Graph()
    graph.add_input("input", input_shape)

    graph.add_node(Convolution2D(16, 1, 1, activation=activation_function()), "conv1_1", "input")
    graph.add_node(ZeroPadding2D(padding=(2, 2)), "zero1_2", "conv1_1")
    graph.add_node(Convolution2D(32, 5, 5, activation=activation_function()), "conv1_3", "zero1_2")

    graph.add_node(Convolution2D(96, 1, 1, activation=activation_function()), "conv2_1", "input")
    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero2_2", "conv2_1")
    graph.add_node(Convolution2D(128, 3, 3, activation=activation_function()), "conv2_3", "zero2_2")

    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero3_1", "input")
    graph.add_node(MaxPooling2D((3, 3), stride=(1, 1)), "pool3_2", "zero3_1")
    graph.add_node(Convolution2D(32, 1, 1, activation=activation_function()), "conv3_3","pool3_2")

    graph.add_node(Convolution2D(64, 1, 1, activation=activation_function()), "conv4_1", "input")

    graph.add_output("output", inputs=["conv1_3", "conv2_3", "conv3_3", "conv4_1"], merge_mode="concat", concat_axis=1)
    return graph

def inception5(input_shape):
    graph = Graph()
    graph.add_input("input", input_shape)

    graph.add_node(Convolution2D(16, 1, 1, activation=activation_function()), "conv1_1", "input")
    graph.add_node(ZeroPadding2D(padding=(2, 2)), "zero1_2", "conv1_1")
    graph.add_node(Convolution2D(32, 3, 3, activation=activation_function()), "conv1_3", "zero1_2")
    graph.add_node(Convolution2D(32, 3, 3, activation=activation_function()), "conv1_4", "conv1_3")

    graph.add_node(Convolution2D(96, 1, 1, activation=activation_function()), "conv2_1", "input")
    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero2_2", "conv2_1")
    graph.add_node(Convolution2D(128, 3, 3, activation=activation_function()), "conv2_3", "zero2_2")

    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero3_1", "input")
    graph.add_node(MaxPooling2D((3, 3), stride=(1, 1)), "pool3_2", "zero3_1")
    graph.add_node(Convolution2D(32, 1, 1, activation=activation_function()), "conv3_3", "pool3_2")

    graph.add_node(Convolution2D(64, 1, 1, activation=activation_function()), "conv4_1", "input")

    graph.add_output("output",inputs=["conv1_4", "conv2_3", "conv3_3", "conv4_1"], merge_mode="concat", concat_axis=1)
    return graph

def inception6(input_shape, n):
    graph = Graph()
    graph.add_input("input", input_shape)

    graph.add_node(Convolution2D(16, 1, 1, activation=activation_function()), "conv1_1", "input")
    graph.add_node(ZeroPadding2D(padding=(2, 2)), "zero1_2", "conv1_1")
    graph.add_node(Convolution2D(32, 1, n, activation=activation_function()), "conv1_3", "zero1_2")
    graph.add_node(Convolution2D(32, n, 1, activation=activation_function()), "conv1_4", "conv1_3")
    graph.add_node(Convolution2D(32, 1, n, activation=activation_function()), "conv1_5", "conv1_4")
    graph.add_node(Convolution2D(32, n, 1, activation=activation_function()), "conv1_6", "conv1_5")

    graph.add_node(Convolution2D(96, 1, 1, activation=activation_function()), "conv2_1", "input")
    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero2_2", "conv2_1")
    graph.add_node(Convolution2D(128, 1, n, activation=activation_function()), "conv2_3", "zero2_2")
    graph.add_node(Convolution2D(128, n, 1, activation=activation_function()), "conv2_4", "conv2_3")

    graph.add_node(ZeroPadding2D(padding=(1, 1)), "zero3_1", "input")
    graph.add_node(MaxPooling2D((3, 3), stride=(1, 1)), "pool3_2", "zero3_1")
    graph.add_node(Convolution2D(32, 1, 1, activation=activation_function()), "conv3_3", "pool3_2")

    graph.add_node(Convolution2D(64, 1, 1, activation=activation_function()), "conv4_1", "input")

    graph.add_output("output", inputs=["conv1_6", "conv2_4", "conv3_3", "conv4_1"], merge_mode="concat", concat_axis=1)
    return graph

def printl(name):
    print str(datetime.datetime.now()) + name

def create_model():
    input_shape = (3,244,244)
    n = 3
    conv1 = conv(input_shape)

    inc41 = inception4(cinput_shape(conv1))
    inc42 = inception4(cinput_shape(inc41))
    inc43 = inception4(cinput_shape(inc42))

    inc51 = inception5(cinput_shape(inc43))
    inc52 = inception5(cinput_shape(inc51))
    inc53 = inception5(cinput_shape(inc52))
    inc54 = inception5(cinput_shape(inc53))
    inc55 = inception5(cinput_shape(inc54))

    inc61 = inception6(cinput_shape(inc55), n)
    inc62 = inception6(cinput_shape(inc61), n)
    inc63 = inception6(cinput_shape(inc62), n)


    graph = Graph()
    graph.add_input("input", input_shape)
    graph.add_node(conv1,"conv1", "input")
    graph.add_node(inc41, "inc41", "conv1")
    graph.add_node(inc42, "inc42", "inc41")
    graph.add_node(inc43, "inc43", "inc42")

    graph.add_node(inc51, "inc51", "inc43")
    graph.add_node(inc52, "inc52", "inc51")
    graph.add_node(inc53, "inc53", "inc52")
    graph.add_node(inc54, "inc54", "inc53")
    graph.add_node(inc55, "inc55", "inc54")

    graph.add_node(inc61, "inc61", "inc55")
    graph.add_node(inc62, "inc62", "inc61")
    graph.add_node(inc63, "inc63", "inc62")

    graph.add_output("output", "inc63")
    print "out " + str(graph.output_shape)

    return graph










graph = create_model()
graph.compile(optimizer='rmsprop', loss={'output':'mse'})
print graph
