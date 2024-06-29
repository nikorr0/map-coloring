from PIL import Image, ImageDraw
import numpy as np

def check_if_in_area(selected_point, borders):
    if (selected_point[0] >= borders[1] and selected_point[0] <= borders[0]) and\
          (selected_point[1] >= borders[3] and selected_point[1] <= borders[2]):
        return True
    else:
        return False

def check_color(image_color, matching_colors=[[64, 63, 76], [255, 0, 0], [0, 255, 0], [0, 0, 255]]):
    matches = [True] * len(matching_colors)
    
    for matching_color_index in range(len(matching_colors)):
        for color_index in range(len(image_color)):
            if image_color[color_index] != matching_colors[matching_color_index][color_index]:
                matches[matching_color_index] = False
                break
    for match in matches:
        if match:
            return True
    return False

def search_nodes_and_codes_optimized(image_matrix):
    nodes_centers = list()
    codes = list()
    # image = Image.fromarray(image_matrix)
    # draw = ImageDraw.Draw(image)
    for length in range(0, image_matrix.shape[0], 13):
        for width in range(0, image_matrix.shape[1], 13):
            # drawing searching dots
            # draw.point((width, length), fill='purple')
            if check_color(image_matrix[length][width]):
                in_area = False
                found = False
                for node_length in range(length-14, length+14):
                    for node_width in range(width-14, width+14):
                        # drawing searching code dots
                        # draw.point((node_width, node_length), fill='green')
                        if check_color(image_matrix[node_length][node_width], [[64, 63, 76]]):
                            for center in nodes_centers:
                                if check_if_in_area((node_width, node_length), (center[0]+9, center[0]-9, 
                                                          center[1]+9, center[1]-9)):
                                    in_area = True
                                    break
                            if not in_area:
                                found = True
                                break
                    if (not in_area) and found:
                        break
                
                if in_area:
                    continue
                
                node_center = (node_width+3, node_length+9)
                nodes_centers.append(node_center)
                code = list()
                code_length = node_center[1] - 6
                code_width = node_center[0] - 6
                for col in range(code_length+1, code_length+11):
                    code_row = list()
                    for row in range(code_width+1, code_width+11):
                        if (col >= image_matrix.shape[0]) or (row >= image_matrix.shape[1]):
                            continue
                        elif check_color(image_matrix[col][row], [[0, 0, 255]]):
                            code_row.append(0)
                        elif check_color(image_matrix[col][row], [[0, 255, 0]]):
                            code_row.append(1)
                        elif check_color(image_matrix[col][row], [[255, 0, 0]]):
                            code_row.append(2)
                    code.append(code_row)
                codes.append(code)
    # draw._image.show()
    return nodes_centers, codes