from store.models import Product
import requests
# import cv2
import os


def get_image(folder_name, url_image):

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language":"en",
    }

    # Obtengo la imagen de dicha url_image  
    imagen = requests.get(url_image, headers).content
    # Obtengo el mismo nombre de la imagen de la URL para descargarla con el mismo nombre
    name = url_image.split('/')
    name = name[-1]

    if name[-3:] == "mp4" or name[-3:] == "avi":
        video = imagen
        name = name[:-4]
        print("Nombre de la imagen:",name)
        ruta = os.path.dirname(__file__)
        ruta = ruta[:-3]
        ruta = os.path.join(ruta, 'media')
        ruta_folder = ruta + folder_name
        if not os.path.exists(ruta_folder):
            os.mkdir(ruta_folder)
            fullname = ruta_folder + "/" + name
            open(fullname +'.mp4', 'wb').write(video)
            print('descargando:{}.mp4'.format(name))
        else:
            fullname = ruta_folder + "/" + name
        
            open(fullname +'.mp4', 'wb').write(video)
            print('descargando:{}.mp4'.format(name))

        folder_name=folder_name[1:]
        print("Retornando Video: ",folder_name + "/" + "{}.mp4".format(name))
        return folder_name + "/" + "{}.mp4".format(name)
        
    else:
        name = name[:-4]
        print("Nombre de la imagen:",name)
        # Obtengo la ruta del projecto para guardar las imagenes
        ruta = os.path.dirname(__file__)
        ruta = ruta[:-3]
        print(ruta)
        
        ruta = os.path.join(ruta, 'media')
        ruta_folder = ruta + folder_name
        print(ruta)
        # Creo una carpeta en caso de no existir en dicha ruta para guardar las imagenes.
        if not os.path.exists(ruta_folder):
            os.mkdir(ruta_folder)
            fullname = ruta_folder + "/" + name
            open(fullname +'.jpg', 'wb').write(imagen)
            print('descargando:{}.jpg'.format(name))
        else:
            # list_archivos = os.listdir(ruta)
            # if name in list_archivos:
            #     print("Ya existe este archivo")
            # else:
            fullname = ruta_folder + "/" + name
        
            open(fullname +'.jpg', 'wb').write(imagen)
            print('descargando:{}.jpg'.format(name))

        folder_name=folder_name[1:]

        # Retorno la ruta de la imagen apartir de la carpeta creada con nombre del Item para DJANGO la encuentre
        print("Retornando Imagen: ",folder_name + "/" + "{}.jpg".format(name))
        return folder_name + "/" + "{}.jpg".format(name)


