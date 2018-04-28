import plotly
import plotly.offline as offline
import plotly.graph_objs as go
from igraph import *


class Artist:
    def __init__(self):
        plotly.tools.set_credentials_file("PeachCobbler", "rk7L2GC5hMeTZWOvpZsg")
        # init_notebook_mode(connected=True)
        return

    def draw_objects(self, Xe, Ye, Xn, Yn, text):
        lines = go.Scatter(x=Xe,
                           y=Ye,
                           mode='lines',
                           line=dict(color='rgb(210,210,210)', width=1),
                           hoverinfo='none'
                           )
        dots = go.Scatter(x=Xn,
                          y=Yn,
                          mode='markers',
                          name='',
                          marker=dict(symbol='dot',
                                      size=32,
                                      color='#6175c1',  # '#DB4551',
                                      line=dict(color='rgb(50,50,50)', width=1)
                                      ),
                          text=text,
                          hoverinfo='text',
                          opacity=0.8
                          )

        return lines, dots

    def get_layout(self, max_y, position, names):
        axis = dict(showline=False,
                    # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        my_layout = dict(title='Tree with Reingold-Tilford Layout',
                      annotations=self.make_annotations(max_y, position, names),
                      font=dict(size=12),
                      showlegend=False,
                      xaxis=go.XAxis(axis),
                      yaxis=go.YAxis(axis),
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )

        return my_layout

    def count_verts(self, k_gene):
        balance = 1
        count = 0
        for node in k_gene:
            count += 1
            if not node[0] == "{":
                balance += 1
            else:
                balance -= 1

            if balance == 0:
                return count

        return count

    def get_adj(self, nodes):
        ret = [[0]*len(nodes) for _ in range(len(nodes))]
        taken = [False]*len(nodes)
        taken[0] = True
        for i in range(len(nodes)):
            if nodes[i][0] != "{":
                for _ in range(2):
                    ind = taken.index(False)
                    taken[ind] = True
                    ret[i][ind] = 1
                    ret[ind][i] = 1
        return ret

    def draw_tree(self, genes):
        gene_nodes = list(map(lambda x: x.split(","), genes))
        all_pos = []
        all_edges_x = []
        all_edges_y = []
        all_verts_x = []
        all_verts_y = []
        names = []
        max_y = 0

        gene_num = 0
        shift = 8.0
        for gene in gene_nodes:
            num_verts = self.count_verts(gene)
            names += gene[:num_verts]
            tree = Graph.Adjacency(self.get_adj(gene[:num_verts]),
                                   mode=ADJ_UNDIRECTED)
            lay = tree.layout_reingold_tilford(root=[0], rootlevel=[0])

            pos = [lay[k] for k in range(num_verts)]
            for i in range(len(pos)):
                pos[i][0] += shift*gene_num
            all_pos += pos
            max_height = max([lay[k][1] for k in range(num_verts)])
            max_y = max(max_y, max_height)

            edge_set = [e.tuple for e in tree.es]
            vert_x_pos = [pos[k][0] for k in range(num_verts)]
            vert_y_pos = [pos[k][1] for k in range(num_verts)]
            edge_x_pos = []
            edge_y_pos = []

            for edge in edge_set:
                edge_x_pos += [pos[edge[0]][0], pos[edge[1]][0], None]
                edge_y_pos += [pos[edge[0]][1], pos[edge[1]][1], None]

            all_edges_x += edge_x_pos
            all_edges_y += edge_y_pos
            all_verts_x += vert_x_pos
            all_verts_y += vert_y_pos
            gene_num += 1

        for i in range(len(all_verts_y)):
            all_verts_y[i] = 2*max_y - all_verts_y[i]
        for i in range(len(all_edges_y)):
            if all_edges_y[i] is not None:
                all_edges_y[i] = 2*max_y - all_edges_y[i]

        lines, dots = self.draw_objects(all_edges_x, all_edges_y,
                                        all_verts_x, all_verts_y, names)

        data = go.Data([lines, dots])
        fig = dict(data=data, layout=self.get_layout(max_y, all_pos, names))
        fig['layout'].update(annotations=self.make_annotations(max_y, all_pos,
                                                               names))
        offline.plot(fig, filename="Gene_Expression_Trees.html")

    def make_annotations(self, max_y, pos, text, font_size=10,
                         font_color='rgb(250,250,250)'):
        L = len(pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = go.Annotations()
        for k in range(L):
            annotations.append(
                go.Annotation(
                    text=text[k],
                    # or replace labels with a different list for the text within the circle
                    x=pos[k][0], y=2 * max_y - pos[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations
