# coding =utf-8
import numpy as np
import matplotlib.pyplot as plt
import pygraphviz as pgv

# with open(
#         '/home/panyunyi/gt/Area_1/conferenceRoom_1/data/files/hier_cut.txt'
# ) as fp:
#     line_list = fp.readlines()
#     G = pgv.AGraph(directed=False, strict=True)
#     for line in line_list:
#         father = line.split()[0]
#         G.add_node(father)
#         child = line.split()[1]
#         G.add_edge(father, child)
#     G.write('fooOld.dot')
#
#     G.layout('dot')  # lGyout with dot
#     G.draw('./b.png')  # write to file
G = pgv.AGraph(directed=False, strict=False)
G.add_node(1)
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 4)
G.write('fooOld.dot')
G.layout('dot')  # lGyout with dot
G.draw('./b.png')  # write to file