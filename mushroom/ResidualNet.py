from keras.models import Graph
from keras.layers.core import Dense, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D, AveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import PReLU
import sys
sys.setrecursionlimit(10000)

def activation():
    return PReLU()

def cinput_shape(graph):
    shape = list(graph.output_shape)
    shape.pop(0)
    return shape

def ConvB(input_shape, nb_filter, nb_row, nb_col, subsample=(1, 1)):
    g = Graph()
    g.add_input("input", input_shape)
    g.add_node(Convolution2D(nb_filter,nb_row,nb_col,subsample=subsample),"conv1", "input")
    g.add_node(BatchNormalization(),"bn", "conv1")
    g.add_node(activation(),"activ", "bn")
    g.add_output("output", "activ")
    return g

def Zero(input_shape, pad=(1,1)):
    g = Graph()
    g.add_input("input", input_shape)
    g.add_node(ZeroPadding2D(pad),"zero","input")
    g.add_output("output", "zero")
    return g

def convo1(input_shape):
    g = Graph()
    g.add_input("input", input_shape)
    g.add_node(ConvB(input_shape,64,7,7, subsample=(2, 2)),"conv1", "input")
    g.add_node(MaxPooling2D((3, 3),strides=(2, 2)), "maxpool","conv1")
    g.add_output("output", "maxpool")
    return g

def avgfc(input_shape, nb_outputs):
    pooling_size = list(input_shape)
    pooling_size.pop(0)
    g = Graph()
    g.add_input("input", input_shape)
    g.add_node(AveragePooling2D(pooling_size),"avgpool","input")
    g.add_node(Flatten(), "flatten", "avgpool")
    g.add_node(Dense(nb_outputs,activation="softmax"),"fc","flatten")
    g.add_output("output", "fc")
    return g

def time_block3(input_shape, nb_filter1, nb_filter2, nb_blocks, has_edge):
    convs = []
    last_shape = input_shape
    for i in range(nb_blocks):
        is_edge = i == 0 and has_edge
        c = block3(last_shape,nb_filter1, nb_filter2, is_edge)
        last_shape = cinput_shape(c)
        convs.append(c)

    g = Graph()
    g.add_input("input", input_shape)
    last_name = "input"
    for i in range(len(convs)):
        name = "conv" + str(i)
        g.add_node(convs[i],name,last_name)
        last_name = name
    g.add_output("output",last_name)
    return g

def block3(input_shape, nb_filter1, nb_filter2, is_edge):

    zerop = (1,1)
    subsample = (1,1)

    if is_edge:
        zerop = (2,2)
        subsample = (2,2)

    g = Graph()
    g.add_input("input",input_shape)

    zero = Zero(input_shape,zerop)
    conv1 = ConvB(cinput_shape(zero),nb_filter1,1,1,subsample=subsample)
    conv2 = ConvB(cinput_shape(conv1), nb_filter1, 3, 3)
    conv3 = ConvB(cinput_shape(conv2), nb_filter2, 1,1)
    shortcut = ConvB(input_shape,nb_filter2,1,1,subsample=subsample)

    g.add_node(zero,"zero","input")
    g.add_node(conv1,"conv1","zero")
    g.add_node(conv2,"conv2","conv1")
    g.add_node(conv3,"conv3","conv2")
    g.add_node(shortcut,"shortcut","input")
    g.add_output("output", inputs=["conv3", "shortcut"], merge_mode="sum")

    return g

def get_model(input_shape, nb_conv2, nb_conv3, nb_conv4, nb_conv5, nb_outputs):
    conv1 = convo1(input_shape)

    conv2 = time_block3(cinput_shape(conv1), 64, 256, nb_conv2, False)
    conv3 = time_block3(cinput_shape(conv2), 128, 512, nb_conv3, True)
    conv4 = time_block3(cinput_shape(conv3), 256, 1024, nb_conv4, True)
    conv5= time_block3(cinput_shape(conv4), 512, 2048, nb_conv5, True)
    last = avgfc(cinput_shape(conv5), nb_outputs)

    g = Graph()
    g.add_input("input",input_shape)
    g.add_node(conv1, "conv1", "input")

    g.add_node(conv2, "conv2", "conv1")
    g.add_node(conv3, "conv3", "conv2")
    g.add_node(conv4, "conv4", "conv3")
    g.add_node(conv5, "conv5", "conv4")
    g.add_node(last, "avgfc", "conv5")

    g.add_output("output", "avgfc")

    return g


def create_50_layer(input_shape, nb_outputs):
    print "create model"
    return get_model(input_shape, 3, 4, 6, 3, nb_outputs)

def create_101_layer(input_shape, nb_outputs):
    print "Create model. This could take some time..."
    return get_model(input_shape, 3, 4, 23, 3, nb_outputs)

def create_150_layer(input_shape, nb_outputs):
    print "Create model. This could take some time..."
    return get_model(input_shape, 3, 8, 36, 3, nb_outputs)


input_shape = (3,244,244)

model = create_50_layer(input_shape, 3)
for n in model.nodes:
    node = model.nodes[n]
    print n + str( node.output_shape)

