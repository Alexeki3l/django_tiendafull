### Introducción
 La idea de este proyecto es crear una tienda donde los usuarios tengas la posibilidad de poner sus propios productos através de una tienda virtual que ellos creen. Dando tambien la posibilidad de:
 - Tener el control de ganancias y ventas realizadas.
 - Tener el listado de proveedores y clientesde cada tienda.

### Tecnologías usadas
- Bootstrap 5
- PostgreSQL
- Django

### Instalación y dependencias:
- **Bootstrap 5**
	 - Para la interfaz hice uso de una plantilla hecha en Bootstrap llamada HYPER. La puedes encontrar [aquí](https://themes.getbootstrap.com/product/hyper-responsive-admin-dashboard-template/ "aquí").


- **PostgreSQL**
	- Instale la versión 11.0. Sin hacer ningun cambio en su configuración predeterminada. En el archivo `settings.py` ya se encuentra configurado para hcer uso de postgreSQL. 
	- Para ellos instale el adaptador Psycopg `pip install psycopg2`.


- **Django**
	- Para instalar el framework solo corra en su consola el siguiente comando:
		`pip install Django`
		o vaya al siguiente [enlace](https://pypi.org/project/Django/#files "enlace").
	- Para visualizar las imagenes es necesario tener el siguiente paquete:
		`pip install Pillow`
