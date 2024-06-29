from PIL import ImageDraw

def fill_circle(image, center, fill_color=(196, 204, 227)):
    draw = ImageDraw.Draw(image)
    draw.rectangle((center[0]-5, center[1]-8, 
                    center[0]+5, center[1]+8), 
                   fill=fill_color)
    draw.rectangle((center[0]-8, center[1]-5, 
                    center[0]+8, center[1]+5), 
                   fill=fill_color)
    for x1, x2, y1, y2 in zip(
                    [3, 3, 9, -9], 
                    [-3, -3, 9, -9],
                    [-9, 9, 3, 3],
                    [-9, 9, -3, -3]):
        draw.line((center[0]+x1, center[1]+y1, 
                center[0]+x2, center[1]+y2), 
                fill=fill_color, width=1)
    for x, y, a1, a2 in zip(
                    [-7, 7, 7, -7], 
                    [-6, 6, -6, 6],
                    [1, -1, -1, 1],
                    [-1, 1, -1, 1]):
        draw.point((center[0]+x, center[1]+y), fill=fill_color)
        draw.point((center[0]+x+a1, center[1]+y), fill=fill_color)
        draw.point((center[0]+x+a1, center[1]+y+a2), fill=fill_color)
    
    return draw._image

def fill_all_circles(image, nodes_centers, fill_color=(196, 204, 227)):
    image = image.copy()
    for center in nodes_centers:
        fill_circle(image, center, fill_color)
    return image