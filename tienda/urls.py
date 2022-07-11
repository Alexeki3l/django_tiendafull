from django.urls import path

from tienda import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # path('', views.Tienda, name="Tienda"),

# -----------------------------------------------PRODUCTOS------------------------------------------------------------------
    path('', views.Tienda.as_view(), name="productos"),

    path('productos/details_product/<int:pk>', views.DetalleProducto.as_view(), name="detalle_producto"),
# -----------------------------------------------------------------------------------------------------------------------
# --------------------------------COMENTARIOS Y RESPUESTAS DE LOS PRODUCTOS-------------------------------------------------
    path('productos/details_product/<int:producto_id>/add_commentario', views.add_comment_prod, name="adicionar_comentario"),
    path('productos/<int:comentario_id>/delete_comments', views.comment_delete, name="eliminar_comentario"),
    
    path('productos/details_product/edit_comment_prod/<int:pk>', views.EditarComentarioProd.as_view(), name="edit_comment_prod"),
    path('productos/details_product/edit_reply_prod/<int:pk>', views.EditarRespuestaProd.as_view(), name="edit_reply_prod"),
    

    path('productos/details_product/<int:comentario_id>/add_respuesta', views.responder_comment_prod, name="responder_comentario"),
    path('productos/details_product/<int:respuesta_id>/eliminar_respuesta', views.reply_delete, name="eliminar_respuesta"),
# -----------------------------------------------------------------------------------------------------------------------------------
    
]