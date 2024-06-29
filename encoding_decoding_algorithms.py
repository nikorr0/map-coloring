from PIL import Image, ImageDraw
import json
from .filling_algorithms import fill_circle

def codes_to_dictionary_and_position(codes, nodes_centers, path="", map_name="None"):
    if map_name == "Europe":
        # Индексы --> Страны
        IndexAndCountry = json.load(open(path + 'Index-Country_europe.json', 'r', encoding="utf-8"))    
        pos = dict()
        decodedDict = dict()
        for matrix, center in zip(codes, nodes_centers):
            dicti = Decode(matrix)
            for keyD, valueD in dicti.items():
                keyD = str(keyD)
                keyD = IndexAndCountry[keyD]
                for i in range(len(valueD)):
                    valueD[i] = IndexAndCountry[str(valueD[i])]
            decodedDict[keyD] = valueD
            pos[keyD] = center
    
    else:
        pos = dict()
        decodedDict = dict()
        for matrix, center in zip(codes, nodes_centers):
            dicti = Decode(matrix)
            for keyD, valueD in dicti.items():
                for i in range(len(valueD)):
                    valueD[i] = valueD[i]
            decodedDict[keyD] = valueD
            pos[keyD] = center 
    
    return decodedDict, pos

def dictionary_to_codes_nodes(countries, paths_to_codes=None):
    countries_codes = dict()
    
    CountryAndIndex = dict()
    # Индексы --> Страны
    IndexAndCountry = dict()

    # Заполняем словари
    index = 1
    for item in countries.items():
        if item[0] not in CountryAndIndex:
            CountryAndIndex[item[0]] = index
            IndexAndCountry[index] = item[0]
            index += 1
            if index % 10 == 9:
                index += 1
    if len(item[1]) > 0:
        for i in item[1]:
            if i not in CountryAndIndex:
                CountryAndIndex[i] = index
                IndexAndCountry[index] = i
                index += 1
                if index % 10 == 9:
                    index += 1

    ChangedCountries = {}
    # Преобразуем страны в число и заполняем словарь выше
    for key, value in countries.items():
        indexForKey = CountryAndIndex[key]
        indexesForValue = []
        for i in value:
            indexesForValue.append(CountryAndIndex[i])
        ChangedCountries[indexForKey] = indexesForValue
    
    # return ChangedCountries, IndexAndCountry
    for key, value in ChangedCountries.items():
        #Кодировка
        country = {key: value}
        # Получаем Массив из списков в 4 элемента
        new_country = ToQuadroList(ToList(country))
        # Матрица
        matrix = ToMatrix(new_country)
        code_image = matrix_to_3color_picture(matrix)
        
        image_size = (19, 19) 
        center = image_size[0] // 2, image_size[1] // 2
        image = Image.new(mode="RGBA", size=image_size, color=(196, 204, 227, 0))
        image = fill_circle(image, (center[0], center[1]), fill_color=(64, 63, 76))
        draw = ImageDraw.Draw(image)
        square_size = 13 // 2
        
        draw.rectangle((center[0] - square_size, 
                            center[1] - square_size, 
                            center[0] + square_size, 
                            center[1] + square_size), 
                            fill=(0, 0, 255))
        image.paste(code_image, (4, 4))
        countries_codes[IndexAndCountry[key]] = image
        
    images_paths = list()
    if paths_to_codes is not None:
        for name, image in list(countries_codes.items()):
            print(name, image)
            image.save(f"{paths_to_codes}/{name}.png", 'PNG')
            images_paths.append(f"{paths_to_codes}/{name}.png")
    
    return list(countries_codes.keys()), images_paths

def matrix_to_3color_picture(matrix, path_picture_name=None, save=False, return_images_paths=True):
    if (path_picture_name is not None) and ('\n' in path_picture_name):
        path_picture_name = path_picture_name.split('\n')[0] + path_picture_name.split('\n')[1]

    image = Image.new(mode="RGB", size=(10, 10), color=(0, 0, 255))
    draw = ImageDraw.Draw(image)
    for length in range(len(matrix)):
        for width in range(len(matrix[length])):
            if matrix[length][width] == 0:
                draw.point((width, length), fill=(0, 0, 255))
            elif matrix[length][width] == 1:
                draw.point((width, length), fill=(0, 255, 0))
            else:
                draw.point((width, length), fill=(255, 0, 0))
    return image

def ToStr(digit):
    digit = str(digit)
    if len(digit) < 2:
        digit = "0" + digit
    return digit

# ToStr делает из чисел 1 ... 9 в строки '01' '02' ... '09'
def ToList(dictionary):
  List = list(dictionary.keys())
  List.extend(list(dictionary.values())[0])
  endList = []
  for i in List:
    endList.append(ToStr(i))
  return endList

# ToList делает из словаря {1: [2, 5, 10]} в список ['01', '02', '05', '10']
def ToEncodedDigit(string):
  digit = int(string)
  m = 3
  string = ''
  if digit < 3:
    string += f'0{digit}'
  elif digit == 3:
    string = '10'
  else:
    while digit > 0:
      string = str(digit % m) + string
      digit //= m

  return string

# ToEncodedDigit преобразовывает строку-число в строку с числом в троичной системе '8' --> '22' '0' --> '00'
def ToQuadroList(array):
  endList = []
  for i in array:
    List = []
    for j in i:
      number = ToEncodedDigit(j)
      List.append(int(number[0]))
      List.append(int(number[1]))
    endList.append(List)

  return endList

# ToQuadroList делает из ['01', '18', '24', '05'] в [[0, 0, 0, 1], [0, 1, 2, 2], [0, 2, 1, 1], [0, 0, 1, 2]]
def ToMatrix(List):
  matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
  square = 0
  for i in range(0, len(matrix), 2):
    for j in range(0, len(matrix[i]), 2):

      matrix[i][j] = List[square][0]
      matrix[i][j+1] = List[square][1]
      matrix[i+1][j] = List[square][2]
      matrix[i+1][j+1] = List[square][3]
      square += 1
      if square > (len(List) - 1):
        return matrix

def Decode(matrix):
  QuadroList = []
  for i in range(0, len(matrix), 2):
    for j in range(0, len(matrix[i]), 2):
      List = []
      summa = matrix[i][j] + matrix[i][j+1] + matrix[i+1][j] + matrix[i+1][j+1]
      if summa == 0:
        break
      List.append(matrix[i][j])
      List.append(matrix[i][j+1])
      List.append(matrix[i+1][j])
      List.append(matrix[i+1][j+1])
      QuadroList.append(List)
  new_List = []

  for i in QuadroList:
    number1 = str(i[0] * 3 + i[1])
    number2 = str(i[2] * 3 + i[3])
    new_List.append(int(number1 + number2))
  dicti = {}
  dicti[new_List[0]] = new_List[1:]
  return dicti

# Decode превращает из матрицы в словарь численных стран
def PrintMatrix(matrix):
   for i in range(0, len(matrix)):
    print(matrix[i])