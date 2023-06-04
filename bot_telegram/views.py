from asyncio.windows_events import NULL
from configparser import InterpolationError
from multiprocessing import managers
from random import randint
from time import sleep
from unittest.mock import call
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import store

from store.models import Product, Business
from multimedia.models import Multimedia
from usuarios.models import Profile
from django.contrib.auth.models import User

from django.db import connections

import telebot #pyTelegramBotApi
import os
# ForceReply:Para citar un mensaje
from telebot.types import ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
#Para usar los botones Inline
from telebot.types import InlineKeyboardButton # Para definir botones
from telebot.types import InlineKeyboardMarkup # Para crear la botonera inline
from telebot.types import InputMediaPhoto, InputMediaVideo
# from bot.utils import get_image

import requests
import pickle
from bs4 import BeautifulSoup

from django.conf import settings

#===============CONSTANTES PARA EL EJEMPLO DE LOS BOTONES=====================>

N_RES_PAG=8 # numero de resultados a mostrar en cada pagina
MAX_ANCHO_ROW = 8 # maximo de botones por fila(limitacion de telegram)
DIR = {"files" : "./files/"}# donde se guardan los archivos de las files
for key in DIR:
    try:
        os.mkdir(key)
    except:
        pass

# ==============================CONFIG=======================================================>


bot = telebot.TeleBot(settings.TOKEN_TELEGRAM)
# telebot.types.Chat
path_project = "D:\Alexei-Todo\Python\Estacion de Trabajo\Proyectos_Django\django_telebot"


# For free PythonAnywhere accounts
# tbot = telebot.TeleBot(TOKEN, threaded=False)

@csrf_exempt
def tbot(request):
    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])

        return HttpResponse("")

    else:
        raise PermissionDenied

# =========================================================================================>

business_name_list =[]
products_name_list =[]
list_image=[]
dict_aux={}
# ===================================START=================================================>
"""
Formato html
    mensaje = "<pre>Casi igual que la etiqueta code</pre>\n"
    mensaje += "<b>negrita</b>\n"
    mensaje += "<u>subrayado</u>\n"
    mensaje += "<i>cursiva</i>\n"
    mensaje += "<s>tachado</s>\n"
    mensaje += "<code>modo codigo</code>\n"
    mensaje += "<span class='tg-spoiler'>Spoiler</span>\n"
    mensaje += "<a href='https://youtube.com'>enlace</a>\n"
"""
"""@bot.message_handler(commands=["start"])
def start(message):
    mensaje  = "<b>Hola, ¿Como estas?</b>\n\n"
    mensaje += "<i>Soy un Bot de Gestion. Con los comandos que tengo predefinido espero que tengas una agradable interaccion conmigo.</i>\n"
    mensaje += "\n"
    bot.send_message(message.chat.id, mensaje, parse_mode="html")
    commands(message=message)"""

#=============================================================================================================>
#===========================================INTERFACE START===================================================>
@bot.message_handler(commands=['start'])
def cmd_start(message):
    print("cmd_start")
    
    if not Profile.objects.filter(chat_id=message.chat.id):
            
            print("NO EXISTE ESTE PERFIL") 
            mensaje  = "<b>Hola, ¿Como estas?</b>\n\n"
            mensaje += "<i>Soy un Bot de Gestion. Con los comandos que tengo predefinido espero que tengas una agradable interaccion conmigo.</i>\n"
            mensaje += "\n"
            # Muestra un mensaje con botones inline(a continuacion del mensaje)
            markup = InlineKeyboardMarkup(row_width=3) # numero de botones en cada fila(3 por defecto)
            b1=InlineKeyboardButton("👤 Registrarte", callback_data="sign_up")
            b2=InlineKeyboardButton("🔍 Buscar", callback_data="search")
            b3=InlineKeyboardButton("🔔 Notificar", callback_data="notify")
            b4=InlineKeyboardButton("🛂 Contacto", callback_data="contact")
            b5=InlineKeyboardButton("🆘 Ayuda", callback_data="help")
            # Esto por atras al programa de python el mensaje "cerrar"
            b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close")
            markup.add(b1,b2,b3,b4,b5,b_cerrar)
            bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")

    else:
            print("YA EXISTE ESTE PERFIL") 
            usuario = Profile.objects.get(chat_id = int(message.chat.id))
            mensaje = f"Hola, <b>{usuario}</b>"
            markup = InlineKeyboardMarkup(row_width=2) # numero de botones en cada fila(3 por defecto)
            b1=InlineKeyboardButton("👤 Perfil", callback_data="profile")
            b2=InlineKeyboardButton("🛰️ Mis Negocios", callback_data="my_business")
            b3=InlineKeyboardButton("🛄 Mis Productos", callback_data="my_products")
            b4=InlineKeyboardButton("🔍 Buscar", callback_data="search")
            b5=InlineKeyboardButton("🔔 Notificar", callback_data="notify")
            b6=InlineKeyboardButton("🛂 Contacto", callback_data="contact")
            b7=InlineKeyboardButton("🆘 Ayuda", callback_data="help")
            # Esto por atras al programa de python el mensaje "cerrar"
            b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close")
            markup.add(b1,b2,b3,b4,b5,b6,b7,b_cerrar)
            bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")


@bot.callback_query_handler(func=lambda x:True)
def respuesta_botones_inline(call):
    # Gestiona las acciones de los botones callback_data
    cid=call.from_user.id
    mid=call.message.id
    # Aqui verifico si se envio el mensaje "cerrar"

    # dict_aux = pickle.load(open(f'{DIR["files"]}{cid}_{mid}','rb'))

    if call.data =="close":
        # Aqui cierro la botonera
        bot.delete_message(cid,mid)
        return
    
    elif call.data =="sign_up":
        crear_usuario(call.message)
        return

    elif call.data =="profile":
        try:
            # msg=cmd_load(call.message)
            # bot.delete_message(cid,msg.message_id)
            interface_profile(call.message)
            bot.delete_message(cid,mid)
            return
        except:
            bot.delete_message(cid,mid)
            cmd_start(call.message)

    elif call.data =="close_return_start":
        cmd_start(call.message)
        bot.delete_message(cid,mid)
        dict_aux.clear()
        return
#=======================PROFILE====================================================
    elif call.data =="edit_profile":
        interface_edit_user(call.message)
        bot.delete_message(cid,mid)
        return

    elif call.data =="edit_profile_name":
        mensaje = "Escriba el nuevo nombre"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(name,edit_profile_name)
        return

    elif call.data=="edit_profile_last_name":
        mensaje = "Escriba sus apellidos"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(name,edit_profile_last_name)
        return

    elif call.data=="edit_profile_username":
        mensaje = "El usuario es unico. Lo cual no se puede cambiar. Por lo menos por ahora."
        bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        interface_edit_user(call.message)
        return
    
    elif call.data=="edit_profile_email":
        mensaje = "Escriba el correo"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(name,edit_profile_email)
        return

    elif call.data=="edit_profile_phone":
        mensaje = "Escriba su numero de telefono"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(name,edit_profile_phone)
        return

    elif call.data=="edit_profile_bio":
        mensaje = "Escriba en su Bio."
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(name,edit_profile_bio)
        return

    elif call.data=="edit_profile_address":
        mensaje = "Escriba su direccion."
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(name,edit_profile_address)
        return

    elif call.data=="edit_profile_image":
        mensaje = "Envieme su foto"
        name = bot.send_message(call.message.chat.id, mensaje)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(name,edit_profile_image)
        return

    elif call.data=="delete_profile":
        bot.delete_message(cid,mid)
        mensaje ="Si eliminas esta cuenta perdera todos los datos asociados a la misma.\n"
        mensaje += "<b>¿Estas seguro de querer eliminar tu perfil?</b>\n"
        markup = ReplyKeyboardMarkup().add("Si","No")
        name = bot.send_message(call.message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
        bot.register_next_step_handler(name,delete_profile)
        return
#===========================PRODUCTS=================================================

    elif call.data == "my_products":
        interface_menu_products(call.message)
        bot.delete_message(cid,mid)
        return

    elif call.data=="my_business":
        print("calling inferface menu business")
        interface_menu_business(call.message)
        bot.delete_message(cid,mid)
        return

    elif call.data=="create_business":
        bot.delete_message(call.message.chat.id, call.message.id, timeout=10)
        mensaje = "Enviame la una imagen que sera la de su nuevo negocio.\n"
        mensaje += "Y el nombre que tendra en la descripcion de la imagen.\n"
        # mensaje += "Y en la descripcion de la imagen envieme lo que sera el nombre de su negocio."
        msg=bot.send_message(call.message.chat.id, mensaje)
        bot.register_next_step_handler(msg,create_business)
    
    elif call.data =="back_menu_product":
        if dict_aux["pag"]==0:
            bot.answer_callback_query(call.id,"Ya estas en la primera pagina")
        else:
            dict_aux["pag"]-=1
            pickle.dump(dict_aux, open(f'{DIR["files"]}{cid}_{mid}','wb'))
            menu_products_aux(dict_aux["lista"],cid,dict_aux["pag"],mid)
        return

    elif call.data=="next_menu_product":
        # Si ya estamos en la ultima pagina
        if dict_aux["pag"]*N_RES_PAG+N_RES_PAG >=len(dict_aux["lista"]):
            print("EL IF")
            bot.answer_callback_query(call.id,"Ya estas en la ultima pagina")
        else:
            dict_aux["pag"]+=1
            pickle.dump(dict_aux, open(f'{DIR["files"]}{cid}_{mid}','wb'))
            menu_products_aux(dict_aux["lista"],cid,dict_aux["pag"],mid)
        return

    elif Business.objects.filter(name=call.data, manager=Profile.objects.get(chat_id=call.message.chat.id), is_active=True):
        
        interface_details_business(call.message, call.data)
        bot.delete_message(cid,mid)
        return

#==========================BUSINESS=================================================
    entrada = str(call.data).split("-")
    print(entrada)
    numbers = entrada[1].split("/")

    if len(numbers)==2 and numbers[0].isdigit() and numbers[1].isdigit():
        dict_aux[numbers[0]]=numbers[1]
        
        edit_business(call.message)
        bot.delete_message(cid,mid)
        return
    
    elif len(entrada)==2 and entrada[1].isdigit() and entrada[0]=="add_image_business":
        dict_aux[entrada[1]]="add_image_business"
        edit_business(call.message)
        bot.delete_message(cid,mid)
        return
        
    elif entrada[0]=="edit_business":
        if entrada[1].isdigit():
            interface_edit_business(call.message, entrada[1])
            bot.delete_message(cid,mid)
            return

    elif len(entrada)==2 and entrada[0]=="business_multimedia" and entrada[1].isdigit():
        business = Business.objects.get(id = int(entrada[1]))
        if Multimedia.objects.filter(business = business).count()==1:
            bot.answer_callback_query(call.id,"Solo tienes esta imagen.")
            return
        else:
            dict_aux[entrada[1]]="business_multimedia"
            business_multimedia(call.message)
            bot.delete_message(cid,mid)
            return

    elif len(entrada)==2 and entrada[0]=="delete_business" and entrada[1].isdigit():
        dict_aux[entrada[1]]="business_multimedia"
        mensaje = "Si eliminas este negocio eliminaras todos los productos que hay asociados a él.\n"
        mensaje += "¿Aun asi quieres eliminarlo?"
        markup = ReplyKeyboardMarkup()
        markup.add("Si","No")
        msg = bot.send_message(call.message.chat.id, mensaje, reply_markup=markup)
        bot.delete_message(cid,mid)
        bot.register_next_step_handler(msg, delete_business)
        return

    
#===========================================================================================>
#=================================CONTACTO==============================================>
# @bot.message_handler(commands=["contacto"])
def contacto(message):
    bot.send_message(message.chat.id, "nada")

#================================================================================================>
#=================================METHODS FOR CREATE USER==========================================>
# @bot.message_handler(commands=["crear_usuario"])
def crear_usuario(message):
    print("CREAR USUARIO")
    
    if Profile.objects.filter(chat_id=message.chat.id):
        usuario = Profile.objects.get(chat_id = int(message.chat.id))
        
        bot.send_message(message.chat.id,f"<b>{usuario}</b>. Ya usted está registrado.", parse_mode="html")
        bot.delete_message(message.chat.id, message.id)
        cmd_start(message)
    else:
        mensaje = "Esta opcion sirve para registrarte en nuestro sistema.\n"
        mensaje += "¿Quieres registrarte en nuestra Base de Datos?\n\n"
        mensaje += "<i>Espero respuesta de <b>SI</b> o <b>NO</b></i>"
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa el boton",resize_keyboard=True)
        markup.add("Si","No")
        msg = bot.send_message(message.chat.id, mensaje, parse_mode="html", reply_markup=markup)
        bot.delete_message(message.chat.id, message.id)
        bot.register_next_step_handler(msg, aux_create_user)


def aux_create_user(message):
    if message.text =="No" or message.text == "NO" or message.text == "no":
        markup=ReplyKeyboardRemove()
        bot.send_chat_action(message.chat.id, "typing")
        mensaje = "<b>OK</b>\n"
        mensaje += "En caso que quieras. No podras registrar ningun servicio"
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
        cmd_start(message)

    elif message.text =="Si" or message.text == "SI" or message.text == "si":
        bot.send_chat_action(message.chat.id, "typing")
        mensaje = "¿Quieres que lo cree apartir de tus datos de <b>Telegram</b>?\n\n"
        mensaje += "<i>Espero respuesta de <b>SI</b> o <b>NO</b></i>"
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa el boton",resize_keyboard=True)
        markup.add("Si","No")
        msg=bot.send_message(message.chat.id, mensaje, parse_mode="html", reply_markup=markup)
        bot.register_next_step_handler(msg,auxiliar)
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"No son las palabras exactas que esperaba.")
        mensaje = "¿Quieres o no quieres registrarte?"
        msg = bot.send_message(message.chat.id, mensaje)
        bot.register_next_step_handler(msg, aux_create_user)

def auxiliar(message):
    markup=ReplyKeyboardRemove()

    if message.text == "Si" or message.text == "SI" or message.text == "si":
        
        mensaje = "Entre un correo y su contraseña.\n"
        mensaje += "Ejemplo:\n"
        mensaje += "<code>ejemplo@dominio.com</code>\n"
        mensaje += "<code>mipassword</code>\n"
        mensaje += "Los demas datos se obtendran de su perfil de <b>Telegram</b>"
        msg=bot.send_message(message.chat.id, mensaje, reply_markup=markup ,parse_mode="html")
        bot.register_next_step_handler(msg, create_user)

    elif message.text == "No" or message.text == "NO" or message.text == "no":
        try:
            mensaje = "Pon tus datos de la siguiente forma. En el mismo orden que te indico:\n"
            mensaje += "<code>nombre_usuario</code>\n"
            mensaje += "<code>tu_correo</code>\n"
            mensaje += "<code>password</code>\n\n"
            mensaje += "<b>NOTA:</b>El correo tiene que ser funcional lo usare para notificarte de algun problema en caso que no pueda hacerlo por aqui."
            print(mensaje)
            msg=bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
        except:
            print("error")
        bot.register_next_step_handler(msg, create_user)

    else:
        mensaje = "Haz salido de la opcion /crear_usuario"
        bot.send_message(message.chat.id, mensaje, reply_markup=markup)

def create_user(message):
    lista = message.text.split("\n")
    print(lista)

    if len(lista)==3:
        try:
            user = User.objects.create_user(lista[0], lista[1], lista[2])
            Profile.objects.filter(user_id = user.id).update(chat_id = message.chat.id)
            bot.send_message(message.chat.id,
            "Falta registrar una foto tuya con tu verdadero nombre y apellidos.\nPor cuestiones de etica hacia tus proveedores.\nTu nombre y apellidos escribelos con salto de linea.En la descripcion de la foto que envies\nASI:")
            bot.send_chat_action(message.chat.id, "upload_photo")
            foto = open(path_project+"/media/send_image.jpg","rb")
            msg = bot.send_photo(message.chat.id, foto)
            bot.register_next_step_handler(msg,set_image_name_user)
        except:
            bot.send_message(message.chat.id,"Ups...No puede registrarte.Intenta de nuevo.")  
            User.obejcts.filter(id=user.id).dele

    elif len(lista)==2:
        if len(lista[0].split("@"))==2 and len(lista[1])>=8:
            try:
                info_chat = bot.get_chat(message.chat.id)

                if User.objects.filter(email=lista[0], is_active=False).distinct():
                    user = User.objects.get(email=lista[0], is_active=False)
                    User.objects.filter(id = user.id).update(email = 'modificate_'+f'{user.email}', username = 'modificate_'+f'{user.username}')

                if User.objects.filter(email=lista[0], is_active=True).distinct():
                    bot.send_message(message.chat.id, "Este correo esta en uso")
                    return
                
                usuario = User.objects.create_user(info_chat.username, lista[0], lista[1])
                if info_chat.first_name:
                    usuario.first_name = info_chat.first_name
                    usuario.save()
                if info_chat.last_name:
                    usuario.last_name  = info_chat.last_name
                    usuario.save() 
                Profile.objects.filter(user_id = usuario.id).update(bio= info_chat.bio, chat_id= message.chat.id)  
                profile = Profile.objects.get(user_id=usuario.id)
            except:
                bot.send_message(message.chat.id,"Ups..Ah ocurrido un error. Intenta de nuevo.")
                cmd_start(message)

            try:
                url_image = bot.get_file_url(info_chat.photo.big_file_id)
                image = get_image("\profile", url_image)
                multimedia = Multimedia(profiles=profile, file=image, type="1")
                multimedia.save()

            except:
                multimedia=Multimedia(profiles=profile, file="profile/sin-foto.png", type="1")
                multimedia.save()
                bot.send_message(message.chat.id,"Deberias actualizar tu perfil y añadir una imagen.")
                cmd_start(message)
                
            mensaje = "Te has registrado <b>satisfactoriamente</b>!!!"
            bot.send_message(message.chat.id, mensaje, parse_mode="html")
            cmd_start(message)

        else:
            mensaje = "El correo debe ser:\n"
            mensaje += "Ejemplo:\n"
            mensaje += "<code>ejemplo@dominio.com</code>\n\n"
            mensaje += "La contraseña debe tener:\n"
            mensaje += "Ejemplo:\n"
            mensaje += "<code>Debe tener mas de 8 caracteres y debe tener caracteres extraños</code>\n\n"
            msg = bot.send_message(message.chat.id, mensaje, parse_mode="html")
            bot.register_next_step_handler(msg,create_user)
    
    else:
        mensaje = f"Esto:\n<pre>{message.text}</pre>\nNo cumple con lo que te dije.\nIntente de nuevo"
        bot.send_message(message.chat.id, mensaje, parse_mode = "html")
        cmd_start(message)

def set_image_name_user(message):
    try:
        url_image = bot.get_file_url(message.photo[-1].file_id)
        image = get_image("\profile",url_image)
        caption = message.caption.split("\n")
        profile = Profile.objects.get(chat_id=message.chat.id)
        multimedia = Multimedia(profiles=profile, file=image, type="1")
        multimedia.save()
        User.objects.filter(username=profile).update(first_name=caption[0],last_name=caption[1])
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"Perfecto!!!....Ya puedes hacer uso de mis servicios.")
        cmd_start(message)
    except:
        profile = Profile.objects.get(chat_id=message.chat.id)
        User.objects.filter(username = profile).delete()
        bot.send_message(message.chat.id,"🚫 Ocurrio un error 🚫.\n🚫 Valores enviados no eran correctos. 🚫")
        cmd_start(message)
#=============================================================================================>
#================================INTERFACE PROFILE===============================================>

def interface_profile(message):
    # bot.delete_message(message.chat.id, message.id)
    profile = Profile.objects.get(chat_id = int(message.chat.id))
    user = User.objects.get(username = profile, is_active=True)
    
    if Multimedia.objects.filter(profiles = profile).exists():
        print("INTERFACE PROFILE")
        multimedia = Multimedia.objects.get(profiles = profile)
        print(multimedia)
        mensaje = "❎⚜️⚜️⚜️❎<b>PERFIL</b>❎⚜️⚜️⚜️❎\n\n"
        if user.first_name:
            mensaje += f"✅ <b>Nombre</b>- - --: {user.first_name}\n"
        if user.last_name:
            mensaje += f"✅ <b>Apellidos</b>- --: {user.last_name}\n"
        if profile:
            mensaje += f"✅ <b>Username</b>- -: {profile}\n"
        if user.email:
            mensaje += f"✅ <b>Email</b>- - - - --: {user.email}\n"
        if profile.phone:
            mensaje += f"✅ <b>Telefono</b>- ---: {profile.phone}\n"
        if profile.bio:
            mensaje += f"✅ <b>Bio</b>- - - - - - --: {profile.bio}\n"
        if profile.address:
            mensaje += f"✅ <b>Direccion</b>- --: {profile.address}\n"
            
        multimedia = "../django_telebot"+str(multimedia.file.url)
        
        markup = InlineKeyboardMarkup(row_width=2) # numero de botones en cada fila(3 por defecto)
        
        b1=InlineKeyboardButton("🖋️ Editar", callback_data="edit_profile")
        b_delete=InlineKeyboardButton("🗑️ Eliminar",callback_data="delete_profile")
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
        
        markup.add(b1,b_delete)
        markup.row(b_cerrar)
        bot.send_chat_action(message.chat.id, "upload_photo")
        photo = open(multimedia,"rb")
        
        bot.send_photo(message.chat.id, photo, mensaje, parse_mode="html", reply_markup=markup)
        
    else:
        bot.send_message(message.chat.id, "🚫 Upss...Pasa algo con su perfil.🚫\nComuniquese con soporte.")

#==================================================================================================>
#================================INTERFACE EDIT USER===============================================>

def interface_edit_user(message):
    print("INTERFACE EDIT USER")
    username = Profile.objects.get(chat_id = int(message.chat.id))
    usuario = User.objects.get(username = username, is_active = True)
    multimedia = Multimedia.objects.get(profiles = username)
    multimedia = "../django_telebot/"+str(multimedia.file.url)[1:]
    markup=InlineKeyboardMarkup(row_width=1)

    mensaje = "❎⚜️⚜️❎<b>EDITAR PERFIL</b>❎⚜️⚜️❎\n\n"
    mensaje += f"1️⃣☑️ <b>Nombre</b>- - --: {usuario.first_name}\n"
    mensaje += f"2️⃣☑️ <b>Apellidos</b>- --: {usuario.last_name}\n"
    mensaje += f"3️⃣☑️ <b>Username</b>- -: {username}\n"
    mensaje += f"4️⃣☑️ <b>Email</b>- - - - --: {usuario.email}\n"
    mensaje += f"5️⃣☑️ <b>Telefono</b>- ---: {username.phone}\n"
    mensaje += f"6️⃣☑️ <b>Bio</b>- - - - - - --: {username.bio}\n"
    mensaje += f"7️⃣☑️ <b>Direccion</b>- --: {username.address}\n"
    mensaje += f"8️⃣☑️ <b>Imagen</b>\n"

    b1=InlineKeyboardButton("1",callback_data="edit_profile_name")
    b2=InlineKeyboardButton("2",callback_data="edit_profile_last_name")
    b3=InlineKeyboardButton("3",callback_data="edit_profile_username")
    b4=InlineKeyboardButton("4",callback_data="edit_profile_email")
    b5=InlineKeyboardButton("5",callback_data="edit_profile_phone")
    b6=InlineKeyboardButton("6",callback_data="edit_profile_bio")
    b7=InlineKeyboardButton("7",callback_data="edit_profile_address")
    b8=InlineKeyboardButton("8",callback_data="edit_profile_image")
    
    inicio = InlineKeyboardButton("⏮️ Atras",callback_data="profile")
    b_cerrar=InlineKeyboardButton("❌ Cerrar",callback_data="close_return_start")
    markup.row(b1,b2,b3,b4,b5,b6,b7,b8)
    markup.row(inicio)
    markup.row(b_cerrar)
    
    bot.send_chat_action(message.chat.id, "upload_photo")
    photo = open(multimedia,"rb")
    bot.send_photo(message.chat.id, photo, mensaje, reply_markup=markup, parse_mode="html")

#===================================================================================================>
#================================METHODS FOR EDIT USER===============================================>

def edit_profile_name(message):
    
    username = Profile.objects.get(chat_id = int(message.chat.id))
    User.objects.filter(username = username, is_active = True).update(first_name = str(message.text))
    bot.send_message(message.chat.id, "Nombre guardado satisfactoriamente")
    interface_edit_user(message)

def edit_profile_last_name(message):
    
    username = Profile.objects.get(chat_id = int(message.chat.id))
    User.objects.filter(username = username, is_active = True).update(last_name = str(message.text))
    bot.send_message(message.chat.id, "Apellidos guardados satisfactoriamente")
    interface_edit_user(message)

def edit_profile_email(message):
    mensaje = message.text.split("@")
    if len(mensaje)==2:
        username = Profile.objects.get(chat_id = int(message.chat.id))
        User.objects.filter(username = username, is_active = True).update(email = str(message.text))
        bot.send_message(message.chat.id, "Correo guardado satisfactoriamente")
        interface_edit_user(message)
    else:
        bot.send_message(message.chat.id, "Correo invalido.")
        interface_edit_user(message)

def edit_profile_phone(message):
    Profile.objects.get(chat_id = int(message.chat.id))
    mensaje = message.text[1:]
    if mensaje.isdigit():
        Profile.objects.filter(chat_id = int(message.chat.id)).update(phone=message.text)
        bot.send_message(message.chat.id, "Numero de telefono guardado satisfactoriamente.")
        interface_edit_user(message)
    else:
        bot.send_message(message.chat.id, "Tienes que enviarme tu numero de telefono.")
        interface_edit_user(message)

def edit_profile_bio(message):
    Profile.objects.filter(chat_id = int(message.chat.id)).update(bio=message.text)
    bot.send_message(message.chat.id, "Su Bio fue actualizadda satisfactoriamente.")
    interface_edit_user(message)

def edit_profile_address(message):
    Profile.objects.filter(chat_id = int(message.chat.id)).update(address=message.text)
    bot.send_message(message.chat.id, "Su Direccion fue actualizadda satisfactoriamente.")
    interface_edit_user(message)

def edit_profile_image(message):
    url_image = bot.get_file_url(message.photo[-1].file_id)
    image = get_image("\profile",url_image)
    username = Profile.objects.get(chat_id = int(message.chat.id))
    Multimedia.objects.filter(profiles = username).update(file=image)
    bot.send_message(message.chat.id, "Imagen guardada satisfactoriamente")
    interface_edit_user(message)

#===================================================================================================>
#====================================METHODS FOR DELETE USER========================================>
def delete_profile(message):
    if message.text == "Si" or message.text == "SI" or message.text == "si":
        print("DELETE PROFILE")
        markup= ReplyKeyboardRemove()
        profile= Profile.objects.get(chat_id=message.chat.id)
        User.objects.filter(username=profile).delete()
        # off_active(profile)
        bot.send_message(message.chat.id, "❌ Perfil Eliminido ❌ ", reply_markup=markup)
        sleep(1)
        cmd_start(message)
    elif message.text == "No" or message.text == "SI" or message.text == "no":
        print("CANCEL DELETE PROFILE")
        markup= ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Que bien!!", reply_markup=markup)
        sleep(1)
        cmd_start(message)
    else:
        mensaje = "Respuesta no validada. Espero una respuesta de <b>Si</b> o <b>No</b>."
        msg=bot.send_message(message.chat.id, mensaje, parse_mode="html")
        bot.register_next_step_handler(msg, delete_profile)
#===================================================================================================>
#==================================INTERFACE MENU BUSINESS==========================================>
def interface_menu_business(message):
    print("INTERFACE MENU BUSINESS")
    mensaje = "❎⚜️❎<b>Mis Servicios/Negocios</b>❎⚜️❎\n\n"
    username = Profile.objects.get(chat_id = int(message.chat.id))
    markup = InlineKeyboardMarkup(row_width=5)
    if Business.objects.filter(manager=username).count()==0:
        
        b1=InlineKeyboardButton("➕ Negocio", callback_data="create_business")
        b2=InlineKeyboardButton("🆘 Ayuda", callback_data="help_business")
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
        markup.row(b1,b2)
        markup.row(b_cerrar)
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
    
    else:  
        n=1
        buttons=[]
        for business in Business.objects.filter(manager=username, is_active=True):
            buttons.append(InlineKeyboardButton(str(n),callback_data=f"{business.name}"))
            business_name_list.append(business.name)
            mensaje +=f'[<b>{n}</b>] {business.name}\n'
            n+=1
        if n <= 5:
            
            b1=InlineKeyboardButton("➕ Negocio", callback_data="create_business")
            b2=InlineKeyboardButton("🆘 Ayuda", callback_data="help_services")
            b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
            markup.add(*buttons)
            markup.row(b1,b2)
            markup.row(b_cerrar)
        else:
            
            b2=InlineKeyboardButton("🆘 Ayuda", callback_data="help_services")
            b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
            markup.add(*buttons)
            markup.row(b2)
            markup.row(b_cerrar)
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
#===================================================================================================>
#================================METHODS FOR CREATE BUSINESS========================================>
def create_business(message):
    
    try:
        url_image = bot.get_file_url(message.photo[-1].file_id)
        image = get_image("/business",url_image)
        caption = message.caption
        profile = Profile.objects.get(chat_id=message.chat.id)

        business = Business(
            name = caption,
            manager = profile
                )
        business.save()

        multimedia = Multimedia(business=business, file=image, type="2")
        multimedia.save()
        print("CREATE BUSINESS")
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"Perfecto!!!")
        interface_details_business(message, caption)
    except:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,"🚫 Ocurrio un error 🚫.\n")
        interface_menu_business(message)

            
#===================================================================================================>
#================================INTERFACE DETAILS BUSINESS========================================>

def interface_details_business(message, name):
    
    business = Business.objects.get(name = name, is_active=True)
    
    mensaje = f"❎⚜️⚜️❎<b>DETALLE NEGOCIO</b>❎⚜️⚜️❎\n\n"
    if Multimedia.objects.filter(business = business):
        print("INTERFACE DETAILS BUSINESS")
        multimedia=0
        for element in Multimedia.objects.filter(business = business):
            multimedia= element
            break
        # multimedia = Multimedia.objects.get(business = business)
        if business.name:
            mensaje += f"✅ <b>Nombre</b>- - - - --: {business.name}\n"
        if business.description:
            mensaje += f"✅ <b>Descripcion</b>- --: {business.description}\n"
        if business.open:
            mensaje += "✅ <b>Estado</b>- - - - - --: Abierto\n"
        if not business.open:
            mensaje += "✅ <b>Estado</b>- - - - - --: Cerrado\n"   
        if business.address:
            mensaje += f"✅ <b>Direccion</b>- - - --: {business.address}\n"
        
        multimedia = "../django_telebot/"+str(multimedia.file.url)[1:]
        markup = InlineKeyboardMarkup(row_width=3) # numero de botones en cada fila(3 por defecto)

        # b_anterior = InlineKeyboardButton("⬅️ Anterior", callback_data="edit_profile")
        # b_siguiente = InlineKeyboardButton("➡️ Siguiente", callback_data="edit_profile")
        b_media = InlineKeyboardButton("🎞️ Multimedias", callback_data=f"business_multimedia-{business.id}")
        b_edit=InlineKeyboardButton("🖋️ Editar", callback_data=f"edit_business-{business.id}")
        b_add_producto=InlineKeyboardButton("➕ Producto", callback_data="create_product")
        b_help=InlineKeyboardButton("🆘 Ayuda", callback_data="help_business")
        b_delete=InlineKeyboardButton("🗑️ Eliminar",callback_data=f"delete_business-{business.id}")
        inicio = InlineKeyboardButton("⏮️ Atras",callback_data="my_business")
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")

        markup.add(b_add_producto,b_media)
        markup.row( b_edit,b_delete)
        markup.row(b_help)
        markup.row(inicio)
        markup.row(b_cerrar)

        bot.send_chat_action(message.chat.id, "upload_photo")
        foto = open(multimedia,"rb")
        bot.send_photo(message.chat.id, foto, mensaje, reply_markup=markup, parse_mode="html")
    else:
       mensaje= "🚫 Upss...Pasa algo con este negocio.🚫\nComuniquese con soporte." 
       bot.send_message(message.chat.id, mensaje, parse_mode="html")

def business_multimedia(message):
    # bot.delete_message(message.chat.id, message.id)
    print("business_multimedia")
    lista = list(dict_aux)
    list_input_media=[]
    business = Business.objects.get(id=lista[0], is_active=True)
    multimedias = Multimedia.objects.filter(business=business)
    for multimedia in multimedias:
        print(multimedia.file.url)
        multimedia = "../django_telebot"+str(multimedia.file.url)
        
        if multimedia[-3:]=="mp4" or multimedia[-3:]=="avi":
            list_input_media.append(InputMediaVideo(open(multimedia, 'rb'), caption=f'{business.name}\n'))
        else:
            list_input_media.append(InputMediaPhoto(open(multimedia, 'rb'), caption=f'{business.name}\n'))
    try:
        bot.send_media_group(message.chat.id, media=list_input_media)
        
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton("⏮️ Atras",callback_data=f"{business.name}")
        markup.row(back)
        bot.send_message(message.chat.id,"------------------",reply_markup=markup)
        # sleep(4)
        # interface_details_business(message, business.name)
    except:
        print("error al cargar las multimedias")
        bot.send_message(message.chat.id, "🚫 Upss...Pasa algo con su multimedias.🚫\nComuniquese con soporte.")
        return
    
def delete_business(message):
    lista = list(dict_aux)
    print(lista)
    business = Business.objects.get(id = int(lista[0]))
    if message.text =="Si" or message.text == "SI" or message.text == "si" and dict_aux[lista[0]]=="delete_business":
        markup=ReplyKeyboardRemove()
        # if dict_aux[lista[0]]=="delete_business":
        print("ELIMANDO NEGOCIO")
        Business.objects.filter(id = int(lista[0])).update(is_active=False)
        Product.objects.filter(business=business).update(is_active=False)
        bot.send_message(message.chat.id, "Negocio eliminado correctamente.", reply_markup=markup)
        lista.clear()
        dict_aux.clear()
        interface_menu_business(message)
    elif (message.text =="NO" or message.text == "no" or message.text == "No"):
        markup=ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "❌Eliminar Negocio❌.\n ⛔Cancelado", reply_markup=markup)
        interface_details_business(message, business.name)
    else:
        mensaje = "Valor no esperado"
        bot.send_message(message.chat.id, mensaje, reply_markup=markup)
        interface_details_business(message, business.name)
#===================================================================================================>
#================================INTERFACE EDIT BUSINESS========================================>

def interface_edit_business(message, id):
    print("INTERFACE EDIT BUSINESS")

    business = Business.objects.get(id=id)
    multimedia =0
    for element in Multimedia.objects.filter(business = business):
        multimedia= element
        break
    
    markup=InlineKeyboardMarkup(row_width=3)
    mensaje = f"❎⚜️⚜️❎<b>EDITAR NEGOCIO</b>❎⚜️⚜️❎\n\n"
    mensaje += f"1️⃣☑️ <b>Nombre</b>- - - - --: {business.name}\n"
    mensaje += f"2️⃣☑️ <b>Descripcion</b>- --: {business.description}\n"
    mensaje += f"3️⃣☑️ <b>Direccion</b>- - - --: {business.address}\n"
    if business.open:
        mensaje += f"4️⃣☑️ <b>Estado</b>- - - - - --: Abierto\n"
    elif not business.open:
        mensaje += f"4️⃣☑️ <b>Estado</b>- - - - - --: Cerrado\n"
    mensaje += f"5️⃣☑️ <b>Editar Imagen</b>\n"

    b1=InlineKeyboardButton("1",callback_data=f"edit_business_name-{id}/1")
    b2=InlineKeyboardButton("2",callback_data=f"edit_business_description-{id}/2")
    b3=InlineKeyboardButton("3",callback_data=f"edit_business_address-{id}/3")
    b4=InlineKeyboardButton("4",callback_data=f"edit_business_open-{id}/4")
    b5=InlineKeyboardButton("5",callback_data=f"edit_business_edit_image-{id}/5")

    multimedia = "../django_telebot/"+str(multimedia.file.url)[1:]
    markup = InlineKeyboardMarkup(row_width=2) # numero de botones en cada fila(3 por defecto)
    # b_anterior = InlineKeyboardButton("⬅️ Anterior", callback_data="edit_profile")
    # b_siguiente = InlineKeyboardButton("➡️ Siguiente", callback_data="edit_profile")
    b_add_image=InlineKeyboardButton("➕ Imagen", callback_data=f"add_image_business-{id}")
    b_help=InlineKeyboardButton("🆘 Ayuda", callback_data="help_services")
    atras = InlineKeyboardButton("⏮️ Atras",callback_data=f"{business.name}")
    b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")

    markup.row(b1,b2,b3,b4,b5)
    markup.row(b_add_image,b_help)
    markup.row(atras)
    markup.row(b_cerrar)
    bot.send_chat_action(message.chat.id, "upload_photo")
    foto = open(multimedia,"rb")
    bot.send_photo(message.chat.id, foto, mensaje, reply_markup=markup, parse_mode="html")


def edit_business(message):
    lista = list(dict_aux)
    print(lista)
    if dict_aux[lista[0]]=="1":
        mensaje= "Entre el nuevo nombre."
        msg = bot.send_message(message.chat.id, mensaje)
        bot.register_next_step_handler(msg, edit_business_name)

    if dict_aux[lista[0]]=="2":
        mensaje= "Entre una nueva descripcion."
        msg = bot.send_message(message.chat.id, mensaje)
        bot.register_next_step_handler(msg, edit_business_description)

    if dict_aux[lista[0]]=="3":
        mensaje= "Entre una nueva direccion."
        msg = bot.send_message(message.chat.id, mensaje)
        bot.register_next_step_handler(msg, edit_business_address)

    if dict_aux[lista[0]]=="4":
        business = Business.objects.get(id=int(lista[0]))
        if business.open:
            Business.objects.filter(id=int(lista[0])).update(open=False)
            bot.send_message(message.chat.id, "Estado editado: Cerrado")
        else:
            Business.objects.filter(id=int(lista[0])).update(open=True)
            bot.send_message(message.chat.id, "Estado editado: Abierto")
        interface_edit_business(message, int(lista[0]))

    if dict_aux[lista[0]]=="5":
        mensaje= "Envie la imagen."
        msg = bot.send_message(message.chat.id, mensaje)
        bot.register_next_step_handler(msg, edit_business_image)

    if dict_aux[lista[0]]=="add_image_business":
        mensaje= "Envie una imagen para adicionarla a este negocio."
        msg = bot.send_message(message.chat.id, mensaje)
        bot.register_next_step_handler(msg, add_image_business)
    
def edit_business_name(message):
    print(dict_aux)
    lista = list(dict_aux)
    Business.objects.filter(id=int(lista[0])).update(name=message.text)
    mensaje="Nombre editado satisfactoriamente!!!"
    bot.send_message(message.chat.id, mensaje)
    dict_aux.clear()
    interface_edit_business(message, int(lista[0]))

def edit_business_description(message):
    lista = list(dict_aux)
    Business.objects.filter(id=int(lista[0])).update(description=message.text)
    mensaje="Descripcion editada satisfactoriamente!!!"
    bot.send_message(message.chat.id, mensaje)
    dict_aux.clear()
    interface_edit_business(message, int(lista[0]))

def edit_business_address(message):
    lista = list(dict_aux)
    Business.objects.filter(id=int(lista[0])).update(address=message.text)
    mensaje="Direccion editada satisfactoriamente!!!"
    bot.send_message(message.chat.id, mensaje)
    dict_aux.clear()
    interface_edit_business(message, int(lista[0]))

def edit_business_image(message):
    lista = list(dict_aux)
    business=Business.objects.get(id=int(lista[0]))
    url_image = bot.get_file_url(message.photo[-1].file_id)
    image = get_image("/business",url_image)
    Multimedia.objects.filter(business=business).update(file=image)
    mensaje="Imagen editada satisfactoriamente!!!"
    bot.send_message(message.chat.id, mensaje)
    dict_aux.clear()
    interface_edit_business(message, int(lista[0]))

def add_image_business(message):
    print("ADD IMAGE BUSINESS")

    lista = list(dict_aux)
    business=Business.objects.get(id=int(lista[0]))
    try:
        if message.video == None:

            url_image = bot.get_file_url(message.photo[-1].file_id)
            print(url_image)
            image = get_image("/business",url_image)
        else:
            url_video = bot.get_file_url(message.video.file_id)
            print(url_video)
            image = get_image("/business",url_video)

        media = Multimedia(
            business = business,
            file=image,
            type="2"
        )
        media.save()
        mensaje="Imagen/es añadidas satisfactoriamente!!!"
        bot.send_message(message.chat.id, mensaje)
    except:
        mensaje="Ups..Ocurrio un error. Alparecer es el formato del archivo que me estas enviando\n"
        mensaje+="Solo puedo almacenar estos por ahora.\n"
        mensaje+="<code>.mp4</code>\n<code>.avi</code>"
        bot.send_message(message.chat.id, mensaje, parse_mode="html")

    dict_aux.clear()
    interface_edit_business(message, int(lista[0]))

#============================================================================================>
#=========================INTERFACE MENU PRODUCTS====================================================>
def interface_menu_products(message):
    print("INTERFACE MENU PRODUCTS")
    mensaje = "❎⚜️⚜️❎<b>Mis Productos</b>❎⚜️⚜️❎\n\n"
    list_products=[]
    profile = Profile.objects.get(chat_id = int(message.chat.id))
    
    for business in Business.objects.filter(manager= profile, is_active= True):
        for product in Product.objects.filter(business=business, is_active= True):
            list_products.append(product)
    
    markup = InlineKeyboardMarkup(row_width=8)
    if len(list_products)==0:

        b1=InlineKeyboardButton("➕ Producto", callback_data="create_business")
        b2=InlineKeyboardButton("🆘 Ayuda", callback_data="help_business")
        b_cerrar=InlineKeyboardButton("❌ Cerrar", callback_data="close_return_start")
        markup.row(b1,b2)
        markup.row(b_cerrar)
        bot.send_message(message.chat.id, mensaje, reply_markup=markup, parse_mode="html")
    
    else: 
        menu_products_aux(list_products, message.chat.id)

def menu_products_aux(lista, cid, pag=0, mid=None):

    mensaje = "❎⚜️⚜️❎<b>Mis Productos</b>❎⚜️⚜️❎\n\n"
    markup=InlineKeyboardMarkup(row_width=MAX_ANCHO_ROW)

    b_anterior  =InlineKeyboardButton("⬅️",callback_data ="back_menu_product")
    b_cerrar    =InlineKeyboardButton("❌ Cerrar",callback_data ="close_return_start")
    b_siguiente =InlineKeyboardButton("➡️",callback_data ="next_menu_product")
    # b_help      =InlineKeyboardButton("🆘 Ayuda", callback_data="help_product")
    # b_search    =InlineKeyboardButton("🔍 Buscar", callback_data="search_product")
    inicio =pag*N_RES_PAG
    fin=inicio+N_RES_PAG
    if fin > len(lista):
        fin=len(lista)
    mensaje += f'<i>Resultados {inicio+1}-{fin} de {len(lista)}</i>\n\n'
    n=1
    botones =[]
    for product in lista[inicio:fin]:
        botones.append(InlineKeyboardButton(str(n),callback_data=f"{product.name}-{product.id}"))
        mensaje+=f'[<b>{n}</b>] {product.name}\n'
        n+=1
    markup.add(*botones)    
    markup.row(b_anterior,b_cerrar,b_siguiente)
    if mid:
        bot.edit_message_text(mensaje, cid, mid, reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
    else:
        res=bot.send_message(cid,mensaje, reply_markup=markup,parse_mode="html",disable_web_page_preview=True)
        mid=res.message_id
        dict_aux={"pag":0,"lista":lista}
        pickle.dump(dict_aux, open(f'{DIR["files"]}{cid}_{mid}','wb'))

#==================================================================================>
#===============BOTONES INLINE====================================================>
"""@bot.message_handler(commands=['botones'])
def cmd_botones(message):
    # Muestra un mensaje con botones inline(a continuacion del mensaje)
    markup = InlineKeyboardMarkup(row_width=2) # numero de botones en cada fila(3 por defecto)
    b1=InlineKeyboardButton("TOP Descuentazos",url="https://t.me/top_descuentazos")
    b2=InlineKeyboardButton("TOP hgjgf",url="https://t.me/top_descuentazos")
    b3=InlineKeyboardButton("TOP vcnvcbc",url="https://t.me/top_descuentazos")
    b4=InlineKeyboardButton("TOP nvcbvnb",url="https://t.me/top_descuentazos")
    b5=InlineKeyboardButton("TOP vcbnvbnvcb",url="https://t.me/top_descuentazos")
    # Esto por atras al programa de python el mensaje "cerrar"
    b_cerrar=InlineKeyboardButton("CERRAR",callback_data="cerrar")
    markup.add(b1,b2,b3,b4,b5,b_cerrar)
    bot.send_message(message.chat.id, "Mis canales de ofertas",reply_markup=markup)"""

"""@bot.callback_query_handler(func=lambda x:True)
def respuesta_botones_inline(call):
    # Gestiona las acciones de los botones callback_data
    cid=call.from_user.id
    mid=call.message.id
    # Aqui verifico si se envio el mensaje "cerrar"
    if call.data =="cerrar":
        # Aqui cierro la botonera
        bot.delete_message(cid,mid)
        return 
    datos = pickle.load(open(f'{DIR["files"]}{cid}_{mid}','rb'))
    if call.data =="anterior":
        if datos["pag"]==0:
            bot.answer_callback_query(call.id,"Ya estas en la primera pagina")
        else:
            datos["pag"]-=1
            pickle.dump(datos, open(f'{DIR["files"]}{cid}_{mid}','wb'))
            mostrar_pagina(datos["lista"],cid,datos["pag"],mid)
        return
    elif call.data=="siguiente":
        # Si ya estamos en la ultima pagina
        if datos["pag"]*N_RES_PAG+N_RES_PAG >=len(datos["lista"]):
            bot.answer_callback_query(call.id,"Ya estas en la ultima pagina")
        else:
            datos["pag"]+=1
            pickle.dump(datos, open(f'{DIR["files"]}{cid}_{mid}','wb'))
            mostrar_pagina(datos["lista"],cid,datos["pag"],mid)
        return"""

# =========================MISMO TEMA==================================================>
@bot.message_handler(commands=['buscar'])
def cmd_buscar(message):
    texto_buscar=" ".join(message.text.split()[1:])
    if not texto_buscar:
        texto='Debes introducir una busqueda.\n'
        texto+='Ejemplo:\n'
        texto+=f'<code>{message.text} zapatos puma</code>'
        bot.send_message(message.chat.id,texto,parse_mode="html")
        return 1
    else:
        print(f'Buscando en Amazon: "{texto_buscar}"')
        url="https://www.amazon.com/s?k={0}".format(texto_buscar.replace(" ","+"))
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                "Accept-Language":"en",
                }
        response=requests.get(url,headers=headers)
        if response.status_code != 200:
            print(f'ERROR al buscar:{response.status_code} {response.reason}')
            bot.send_message(message.chat.id, "Se ha producido un error. Intentalo mas tarde")
            return 1
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            elementos = soup.find_all('div', {'class':'s-result-item', 'data-component-type':'s-search-result'})
            lista=[]
            for elemento in elementos:
                try:
                    # product_name = result.h2.text
                    product_name = elemento.find('span', {'class':'a-text-normal'}).text 
                    product_url = elemento.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).get('href')
                    product_url = "https://www.amazon.com" + product_url
                    print("No hubo problema")
                    lista.append([product_name, product_url])
                except:
                    print("ERROR")
                    continue
        
        mostrar_pagina(lista,message.chat.id)
        

def mostrar_pagina(lista, cid, pag=0, mid=None):
    #Crea o edita un mensaje de la pagina
    # Creamos botonera
    markup=InlineKeyboardMarkup(row_width=MAX_ANCHO_ROW)
    b_anterior  =InlineKeyboardButton("🡠",callback_data="anterior")
    b_cerrar    =InlineKeyboardButton("🗙",callback_data="cerrar")
    b_siguiente =InlineKeyboardButton("🡢",callback_data="siguiente")
    inicio =pag*N_RES_PAG
    fin=inicio+N_RES_PAG
    if fin > len(lista):
        fin=len(lista)
    mensaje = f'<i>Resultados {inicio+1}-{fin} de {len(lista)}</i>\n\n'
    n=1
    botones =[]
    for item in lista[inicio:fin]:
        botones.append(InlineKeyboardButton(str(n),url=item[1]))
        mensaje+=f'[<b>{n}</b>] {item[0]}\n'
        n+=1
    markup.add(*botones)    
    markup.row(b_anterior,b_cerrar,b_siguiente)
    if mid:
        bot.edit_message_text(mensaje, cid, mid, reply_markup=markup, parse_mode="html",disable_web_page_preview=True)
    else:
        res=bot.send_message(cid,mensaje, reply_markup=markup,parse_mode="html",disable_web_page_preview=True)
        mid=res.message_id
        datos={"pag":0,"lista":lista}
        pickle.dump(datos, open(f'{DIR["files"]}{cid}_{mid}','wb'))
    
            
#======================================================================================>    


@bot.message_handler(commands=["localizar"])
def localizar(message):
    bot.send_location(message.chat.id, 22.0221205,-80.8247165, proximity_alert_radius=100)


@bot.message_handler(content_types=['location'])
def prueba(message):
    
    print(message.location.latitude)
    print(message.location.longitude)
    bot.send_message(message.chat.id,f"Tu posicion es: \nlatitud:{message.location.latitude}\nlongitud:{message.location.longitude}")
    

@bot.message_handler(content_types=['venue'])
def pru(message):
    print(message.live_period)
    print(message.location.latitude)
    print(message.location.longitude)
    bot.send_message(message.chat.id,"pasa algo")

# @bot.message_handler(content_types=["text"])
# def bot_message_texto(message):
#     if message.text.startswith("/"):
#         print(message)
#         bot.send_message(message.chat.id, "No tengo registrado ese comando. Fijese bien en el listado")
        
#     else:
#         print("======MESSAGE======")
#         print(message)
#         print("======CHAT======")
#         print(bot.get_chat(message.chat.id))
#         # print(message.contact)
#         bot.send_message(message.chat.id, "Lo sentimos servidor reiniciado. Intente su operacion desde el principio")
#         cmd_start(message)
        

@bot.message_handler(content_types=['video','photo'])
def bot_message_texto(message):
    print("ENTRO AL METODO DE LAS FOTOS")
    # print(message)
    print(message)
    print(message.video)

@bot.message_handler(commands=["load"])
def cmd_load(message):
    decimal = 0
    mensaje = "Cargando\n"
    cuadrados =f"⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ "
    porcent =f'<code>{decimal}%</code>'
    n=1
    while True:
        sleep(1)
        if decimal == 0:
            msg = bot.send_message(message.chat.id, mensaje+cuadrados+porcent, parse_mode="html")
            decimal +=10
            continue

        elif decimal > 0 and decimal <= 100:
            cuadrados_negros = cuadrados[:n]
            cuadrados_negros = cuadrados_negros.replace('⬜','⬛')
            cuadrados = cuadrados_negros+cuadrados[n:]
            porcent =f'<code>{decimal}%</code>'
            print(mensaje+cuadrados+porcent)
            bot.edit_message_text(mensaje+cuadrados+porcent, message.chat.id, msg.message_id, parse_mode="html")
            decimal+=10
            n+=2
            continue

        elif decimal > 100:
            print("fin")
            break
    return msg
    

    

#===========================================================================================>
#=================================SOBRE EL BOT==============================================>
@bot.message_handler(commands=["the_bot"])
def the_Bot(message):
    mensaje = "Hola. ¿Como estas?\n\n"
    mensaje += "Si has llegado hasta aqui es que has husmeando ha fondo."
    mensaje += " Es broma!!. Aqui te contare sobre el surgimiento de esta idea.\n"
    mensaje += "La idea de crear este <b>bot</b> surje con el problema de que las personas que brindan determinados productos o servicios no llegan a la mayor cantidad de personas posibles."
    mensaje += " Y dadas las bondades que nos da la <a href='https://https://core.telegram.org/bots/api'>API</a> de Telegram y dado que este cliente de mensajeria es uno de los mas usados.\n"
    mensaje += "Para no decir el <b>mas usado</b>.\n Nos vino la idea de crear un Bot lo suficientemente versatil como para gestionar dichos servicios.\n\n"
    mensaje += "Pero, <b>¿Que tiene este Bot que lo hace diferente a una APK o los demas Bots?</b>\n"
    mensaje += "Bueno, diferente a otros Bots no tiene mucha diferencia. Digamos que la diferencia la marca en el enfasis de desarrollo o sentido de desarrollo que se le ha dado al crear este Bot."
    mensaje += "Y el sistema tendra una APK pero por ahora hemos usado a Telegram como interfaz de nuestro software.\n\n"
    mensaje += "<b>¿Que beneficios le da el uso de este Bot a las personas comunes y aquellas que tengan un servicio que ofertar?</b>\n"
    mensaje += "[Por escribir]"
    bot.send_message(message.chat.id, mensaje, parse_mode="html") 

bot.set_my_commands([
        telebot.types.BotCommand("/start","Da la Bienvenida"),
        telebot.types.BotCommand("/help","Ayuda")
    ])


