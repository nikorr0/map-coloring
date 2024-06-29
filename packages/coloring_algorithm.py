def quick_sort(array):
    stack = list()
    stack.append(0)
    stack.append(len(array) - 1)
    
    while stack:
        r = stack.pop()
        l = stack.pop()
        i = l
        j = r
        y = array[(l + r) // 2][1]
        while i <= j:
            while array[i][1] < y:
                i += 1
            while array[j][1] > y:
                j -= 1
            if i <= j:
                array[i], array[j] = array[j], array[i]
                i += 1
                j -= 1
                
        if i < r:
            stack.append(i)
            stack.append(r)
        r = j
        if l < r:
            stack.append(l)
            stack.append(r)
    return array

def find_countries_with_max_borders(countries_borders, return_counts=False):
    countries_count_borders = dict()
    for country in countries_borders.keys():
        countries_count_borders[country] = len(countries_borders[country])
    
    countries_count_borders = quick_sort(list(countries_count_borders.items()))[::-1] # sorted(countries_count_borders.items(), key=lambda x: x[1], reverse=True)
    
    if not return_counts:
        countries_count_borders = list(map(lambda x: x[0], countries_count_borders))
        
    return countries_count_borders

def to_paint_map(countries_borders=dict, colors=list):
    countries_count_borders = find_countries_with_max_borders(countries_borders)
    colored_countries = dict()
    a = 0
    while len(countries_count_borders) > 0:
        max_count_country = countries_count_borders.pop(0)
        colored_countries[max_count_country] = colors[0]
        
        for border in countries_borders[max_count_country]:
        
            if border not in colored_countries.keys():
                used_colors = set()
                
                for other_border in countries_borders[border]:
                    a += 1
                    if other_border in colored_countries.keys():
                        used_colors.add(colored_countries[other_border])
                
                used_colors = list(set(colors).difference(used_colors))
                try:
                    colored_countries[border] = sorted(used_colors).pop(0)
                except:
                    return "Входных цветов недостаточно для покраски карты."
                countries_count_borders.remove(border)
                
    return colored_countries