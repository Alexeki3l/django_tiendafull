from django.urls import path

from blog import views


urlpatterns = [
    
    path('', views.BlogView.as_view(), name="Blog"),

    path('completo/<int:post_id>', views.Blog_Full, name="blog_full"),

    path('completo/<int:comentario_id>/comments', views.Comment_Post, name="comments"),

    path('completo/<int:post_id>/add_comments', views.add_comment_post, name="add_comment"),

    path('comment/<int:comentario_id>/delete_comments', views.comment_delete, name="delete"),

    path('comment/<int:pk>/edit_comments', views.EditarComentario.as_view(), name="edit_comment"),

    path('comment/<int:pk>/edit_reply', views.EditarRespuesta.as_view(), name="edit_reply"),

    

    path('comment/<int:comentario_id>/reply', views.reply_comment_post, name="reply"),

    path('comment/<int:comentario_id>/likes', views.LikeComment, name="like_comment"),

    path('comment/<int:comentario_id>/dislikes', views.DislikeComment, name="dislike_comment"),


    path('comment/<int:respuesta_id>/delete_reply', views.reply_delete, name="delete_reply"),

    path('reply/<int:respuesta_id>/likes', views.LikeReply, name="like_reply"),

    path('reply/<int:respuesta_id>/dislikes', views.DislikeReply, name="dislike_reply"),

    path('completo/<int:pk>/likes', views.LikePost, name="like_post"),

    path('completo/<int:post_id>/dislikes', views.DislikePost, name="dislike_post"),
    
]

