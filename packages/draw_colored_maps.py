from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import time
from colormap.colors import Color
from .search_codes_algorithm import search_nodes_and_codes_optimized
from .encoding_decoding_algorithms import codes_to_dictionary_and_position
from .coloring_algorithm import to_paint_map
from .filling_algorithms import fill_all_circles

def draw_two_maps(image_path, colors, path="",
                  node_size=1100, width=2, font_size=4.5, figsize=(15, 15), map_name="None"):
    image = Image.open(image_path)
    image_matrix = np.asarray(image)
    nodes_centers, codes = search_nodes_and_codes_optimized(image_matrix)
    
    countries_borders, pos = codes_to_dictionary_and_position(codes, nodes_centers, path=path, map_name=map_name)
    
    countries_colors = to_paint_map(countries_borders, colors)
    time_mark = f"{time.time():.2f}"
    filename_graph = path + f"graph_map_{time_mark}.png" 
    graph_image_path = draw_graph_on_map(image, pos, countries_borders, countries_colors=countries_colors,
                        node_size=node_size, width=width, font_size=font_size, filename=filename_graph, figsize=figsize)
    
    filename_filled = path + f"filled_map_{time_mark}.png" 
    filled_image_path = fill_image_with_colors(countries_colors, pos, image, nodes_centers, map_name=map_name, filename=filename_filled)
    
    used_colors = list(np.unique(np.array(list(countries_colors.values()))))
    
    return graph_image_path, filled_image_path, used_colors
    

def draw_graph_on_map(image, pos, countries_borders, filename, countries_colors=None,
                     node_size=1100, width=2, font_size=4.5, figsize=(15, 15)):
    image_matrix = np.asarray(image)
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.imshow(image_matrix)
    

    ax, graph_image_path = draw_countries_graph(countries_borders, pos=pos, ax=ax, 
                         countries_colors=countries_colors, node_size=node_size, 
                         width=width, font_size=font_size, filename=filename)
    
    return graph_image_path

def fill_image_with_colors(countries_colors, pos, image, nodes_centers, filename, map_name="None"):
    filled_image = fill_all_circles(image, nodes_centers)

    color_pos = list()
    for country in list(countries_colors.keys()):
        for i in range(len(pos.keys())):
            if country == list(pos.keys())[i]:
                color_pos.append([countries_colors[country], list(pos.values())[i]])
                break

    for color_coords in color_pos:
        color = color_coords[0]
        coords = color_coords[1]
        ImageDraw.floodfill(filled_image, xy=coords, value=from_str_color_to_rgb(color))


    if map_name == "Europe":
        kaliningrad_color = list(countries_colors.values())[0]
        ImageDraw.floodfill(filled_image, xy=(1095, 784), value=from_str_color_to_rgb(kaliningrad_color))
        
    filled_image.save(filename, transparent=True)
    
    return filename

def from_str_color_to_rgb(str_color):
    return tuple([int(x * 255) for x in Color(str_color).rgb])

def from_hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_countries_graph(countries_borders, pos=None, ax=None, 
                         countries_colors=None, node_size=1100, 
                         width=2, font_size=4.5, save_fig=True, figsize=(15, 15),
                         return_path=True, filename='graph_map.png'):
    
    indexes_countries = dict()
    for i in range(len(countries_borders)):
        indexes_countries[list(countries_borders.keys())[i]] = i
    
    graph = nx.Graph()
    graph.add_nodes_from(countries_borders.keys())

    counted_edges = list()
    for country in countries_borders.keys():
        for border in countries_borders[country]:
            if set([country, border]) not in counted_edges: 
                counted_edges.append(set([country, border]))
                
    graph.add_edges_from(counted_edges)
    
    if pos is None:
        pos = nx.spring_layout(graph, scale=2, seed=1)
    
    if countries_colors is not None:
        colors = [None] * len(countries_borders)
        for country, color in countries_colors.items():
            index = indexes_countries[country]
            colors[index] = color
        
        for i in range(len(colors)):
            if colors[i] is None:
                colors[i] = '#909497' # 'gray'
    else:
        colors = '#909497' # 'gray'
    
    node_options = {
        'node_color': colors,     # color of node
        'node_size': node_size,   # size of node
       }
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        nodes = nx.draw_networkx_nodes(graph, pos, linewidths=width, **node_options)
    
    else:
        nodes = nx.draw_networkx_nodes(graph, pos, ax=ax, linewidths=width, **node_options)
        
    nodes.set_edgecolor('black')
    nx.draw_networkx_edges(graph, pos, width=width)
    nx.draw_networkx_labels(graph, pos, font_size=font_size)

    if save_fig:
        plt.tight_layout()
        plt.savefig(filename, transparent=True)
        if return_path:
            return ax, filename
    
    return ax