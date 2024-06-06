import io

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx

# create a `networkx` graph
g = nx.MultiDiGraph()
g.add_nodes_from([1,2])
g.add_edge(1, 2)

# convert from `networkx` to a `pydot` graph
pydot_graph = nx.drawing.nx_pydot.to_pydot(g)

# render the `pydot` by calling `dot`, no file saved to disk
png_str = pydot_graph.create_png(prog='dot')

# treat the DOT output as an image file
sio = io.BytesIO()
sio.write(png_str)
sio.seek(0)
img = mpimg.imread(sio)

# plot the image
imgplot = plt.imshow(img, aspect='equal')
plt.show()