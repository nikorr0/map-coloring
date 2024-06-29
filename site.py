from flask import Flask, render_template, request, redirect, flash
from packages.encoding_decoding_algorithms import dictionary_to_codes_nodes
import json
from packages import draw_colored_maps
import time
import os

language = "eng"

if language == "rus":
    error_index = "Произошла ошибка. Повторите попытку снова! Можете выбрать карту Европы или вымышленную карту!"
    error_dict = "Произошла ошибка. Повторите попытку снова!"
elif language == "eng":
    error_index = "An error has occurred. Try again! You can choose a map of Europe or a fantasy map!"
    error_dict = "An error has occurred. Try again!"

basepath = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

# Обработчик главной страницы
@app.route("/", methods=["POST", "GET"])
def index():   
    try:
        if request.method == "POST":

            # Если нажата кнопка «Раскрасить»
            if 'ColoredButton' in request.form:
                UserMapFileName = None  
                file = request.files['photo']

                # Если добавлена карта пользователя
                if file.filename != "":
                    UserMap = request.files['photo']
                    
			
			        # Формат png
                    if UserMap.filename.split('.')[-1] == "png":
    
                        UserMapFileName = f"static/Maps/UserMap_{time.time():.2f}.png"

                        UserMap.save(f"{UserMapFileName}")
                    else:
                        return render_template(f"index_{language}.html")

		        # Запрашиваемые цвета от пользователя
                colors = request.form['Colors'].split(' ')

                # Если достаточно цветов
                if len(colors) >= 5:

                    # Пользователь выбрал свою карту
                    if request.form['pets'] == "UserMap":
                        if UserMapFileName is not None:
                            graph_image_path, filled_image_path, UsedColors = draw_colored_maps.draw_two_maps(image_path=basepath + f"/{UserMapFileName}", 
                                                                                                  colors=colors, path=f"{basepath}/static/Maps/")

                            UsedColorsCount = len(UsedColors)
                            UsedColors = ', '.join(UsedColors)

                            graph_image_path = graph_image_path.split(basepath)[1]
                            filled_image_path = filled_image_path.split(basepath)[1]

                            return render_template(f"index_{language}.html", image=UserMapFileName, result1=graph_image_path, 
                                                   result2=filled_image_path, UsedColors = UsedColors, UsedColorsCount=UsedColorsCount)
                    
                    else:
			            # Модель карты
                        map_name = request.form['pets']
                        
                        if map_name == 'Europe':
                            UserMapFileName =  "/static/PreparedMaps/3_color_europe_map_all_nodes_codes.png"
                        elif map_name == "Fantasy":
                            UserMapFileName = "/static/PreparedMaps/fantasy_map_1_with_codes.png"


                        # Берем путь до изображений и использованные цвета
                        graph_image_path, filled_image_path, UsedColors = draw_colored_maps.draw_two_maps(image_path=basepath + UserMapFileName,
                                                                                            colors=colors, path=f"{basepath}/static/Maps/", map_name=map_name)

                        UsedColorsCount = len(UsedColors)
                        UsedColors = ', '.join(UsedColors)

                        graph_image_path = graph_image_path.split(basepath)[1]
                        filled_image_path = filled_image_path.split(basepath)[1]
                        

                        return render_template(f"index_{language}.html",   image=UserMapFileName, 
                        result1=graph_image_path, 
                        result2=filled_image_path, UsedColors = UsedColors, UsedColorsCount=UsedColorsCount)
                                            
                    return render_template(f"index_{language}.html")
                # Цветов не хватает
                else:
                    error = "ColorError"
                    return render_template(f"index_{language}.html", error=error) 

            if 'NewSite' in request.form:
                return redirect("/code")
        return render_template(f"index_{language}.html")
    
    except Exception as e:
        print("Error on the page /:", e, "\n")
  	    # На случай ошибки выводить в отдельный блок на сайте эту запись
        flash(error_index)
        return render_template(f"index_{language}.html")
    
# Обработчик второй страницы (страницы с генерации кодов)
@app.route("/code", methods=["POST", "GET"])
def code():
    try:
        if request.method == "POST":
		# Если пользователем указан словарь
            if "Dict" in request.form:
		        # Преобразуем словарь в виде строки в словарь
                Dict = json.loads(request.form['Dict'].replace("'", '"'))
		        # Получаем сгенерированные ячейки с информацией
                countries_names, images_paths =  dictionary_to_codes_nodes(Dict, basepath + "/static/Maps/ImageCodes")

                for i in range(len(images_paths)):
                    images_paths[i] = images_paths[i].split(basepath)[1]

                array = list(zip(countries_names, images_paths))

                return render_template(f"dict_{language}.html", array=array)
            
		# Переход на главную страницу
            if "MainPage" in request.form:
                return redirect("/")
            
        return render_template(f"dict_{language}.html")
            
    except Exception as e:
        print("Error on the page /code:", e, "\n")
        flash(error_dict)
        return render_template(f"dict_{language}.html")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="localhost", port=8080)
