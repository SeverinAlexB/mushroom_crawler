from keras.models import Graph
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.core import Activation
'''
Inception v3 paper
http://arxiv.org/pdf/1512.00567v1.pdf

Old inception paper
http://arxiv.org/pdf/1409.4842.pdf

'''
def add_inception4(graph, base, id):

    conv1_1 = Convolution2D(16,1,1, activation="relu")
    zero1_2 = ZeroPadding2D(padding=(2,2))
    conv1_3 = Convolution2D(32,5,5, activation="relu")

    conv2_1 = Convolution2D(96,1,1, activation="relu")
    zero2_2 = ZeroPadding2D(padding=(1,1))
    conv2_3 = Convolution2D(128,3,3, activation="relu")

    zero3_1 = ZeroPadding2D(padding=(1,1))
    pool3_2 = MaxPooling2D((3, 3), stride=(1, 1))
    conv3_3 = Convolution2D(32,1,1, activation="relu")

    conv4_1 = Convolution2D(64,1,1, activation="relu")

    graph.add_node(conv1_1, name=(id+"conv1_1"), input=base)
    graph.add_node(zero1_2, name=(id+"zero1_2"), input=(id+"conv1_1"))
    graph.add_node(conv1_3, name=(id+"conv1_3"), input=(id+"zero1_2"))

    graph.add_node(conv2_1, name=(id+"conv2_1"), input=base)
    graph.add_node(zero2_2, name=(id+"zero2_2"), input=(id+"conv2_1"))
    graph.add_node(conv2_3, name=(id+"conv2_3"), input=(id+"zero2_2"))

    graph.add_node(zero3_1, name=(id+"zero3_1"), input=base)
    graph.add_node(pool3_2, name=(id+"pool3_2"), input=(id+"zero3_1"))
    graph.add_node(conv3_3, name=(id+"conv3_3"), input=(id+"pool3_2"))

    graph.add_node(conv4_1, name=(id+"conv4_1"), input=base)

    graph.add_node(Activation("linear"),name=id, inputs=[id+"conv1_3", id+"conv2_3", id+"conv3_3", id+"conv4_1"], merge_mode="concat")
    graph.output_shape

def create_model():
    input_shape = (3,244,244)
    graph = Graph()

    input_id = "input"
    graph.add_input(name=input_id, input_shape=input_shape)

    add_inception4(graph,input_id,"inception4_1_")

    return graph


create_model()