
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from blog.forms import CommentForm, ReplyCommentForm, EditarComentarioForm, EditarRespuestaForm
from django.views.generic import CreateView
# Create your views here.
from .models import Comentario, Post, Categoria, Respuesta
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from .forms import EditarComentarioForm
from django.utils import timezone


# def Blog(request):
#     posts = Post.objects.all()        
#     return render(request, "blog/blog.html",{"posts":posts })

def Blog_Full(request, post_id):
    
# -----------------------------------------------------------
    post=Post.objects.get(id=post_id)
    total = post.comentarios.count()
    count=0
    for comentario in post.comentarios.all():
        count+=comentario.respuestas.count()
    total = total +count
       
    lista=[]
    temp=[]
    posters=[]
    order=[]
    cont=0
    for categoria in post.categorias.all():

        temp.append(categoria)
        lista.append(categoria.nombre)      
 # -----------------------Para los posters relacionados--------------------------------------
    for ele in temp:
        for poster in Post.objects.filter(categorias=ele).order_by("-created"):
            if cont < 4:
                    if not poster in posters:
                        posters.append(poster)
                        cont+=1
                    else:continue
    for elemento in posters:
         # if not elemento in order:
            order.append(elemento.id)
            order.sort(reverse=True)
    nueva=[]
    for element in order:
        if not element == post_id:
            nueva.append(Post.objects.get(id=element))
        else:continue
#-------------------------------------------------------------------------------------------   

    return render(request, "blog/blog_full.html", {"post":post, "total":total})
   
def add_comment_post(request, post_id):
    
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            context ={
             
             'form':form,
                    }
            contenido = request.POST.get('contenido')
            # comentario = Comentario.objects.create(autor = request.user, contenido = contenido, post = post, approved_comment = True)
            comentario = Comentario(
                autor = request.user, 
            contenido = contenido, 
            post_id = post_id, 
            approved_comment = True
            )
            comentario.save()
            return HttpResponseRedirect(reverse('blog_full', args=[str(post_id)]))
        
    else:
      form = CommentForm()   
    context ={
             'form':form,
            }
        
    return render(request, "blog/blog_full.html", context)

def reply_comment_post(request, comentario_id):

    comentario = Comentario.objects.get(id = comentario_id)
    if request.method == 'POST':
        form = ReplyCommentForm(request.POST or None)
        if form.is_valid():
            context ={
             
             'form':form,
                    }
            contenido = request.POST.get('contenido')
            # comentario = Comentario.objects.create(autor = request.user, contenido = contenido, post = post, approved_comment = True)
            respuesta = Respuesta(contenido = contenido, approved_comment = True, autor = request.user, comentarios_id = comentario_id )
            respuesta.save()
            # return redirect('blog_full', comentario.post_id)
            return HttpResponseRedirect(reverse('blog_full', args=[str(comentario.post_id)]))
        
    else:
      form = ReplyCommentForm()   
    context ={
             'form':form,
            }
        
    return render(request, "blog/blog_full.html", context)

def comment_delete(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    comentario.delete()
    return redirect ("blog_full", comentario.post.id)

def reply_delete(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, pk=respuesta_id)
    comentario = Comentario.objects.get(id = respuesta.comentarios_id)
    post = Post.objects.get(id = comentario.post_id)
    respuesta.delete()
    return redirect("blog_full", post.id)

def LikePost(request, pk):
    post = get_object_or_404(Post, id = pk)
    post.likes.add(request.user)
    # return redirect("blog_full", post.id)    
    return HttpResponseRedirect(reverse('blog_full', args=[str(pk)]))
    
def DislikePost(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('blog_full', args=[str(post_id)]))

def LikeComment(request, comentario_id):
    comentario = get_object_or_404(Comentario, id = comentario_id)
    comentario.likes.add(request.user)
    post = Post.objects.get(id = comentario.post_id)
    return redirect("blog_full", post.id)

def DislikeComment(request, comentario_id):
    comentario = get_object_or_404(Comentario, id = comentario_id)
    comentario.likes.remove(request.user)
    post = Post.objects.get(id = comentario.post_id)
    return redirect("blog_full", post.id)

def LikeReply(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id = respuesta_id)
    respuesta.likes.add(request.user)
    comentario = Comentario.objects.get(id = respuesta.comentarios_id)
    post = Post.objects.get(id = comentario.post_id)
    return redirect("blog_full", post.id)

def DislikeReply(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id = respuesta_id)
    respuesta.likes.remove(request.user)
    comentario = Comentario.objects.get(id = respuesta.comentarios_id)
    post = Post.objects.get(id = comentario.post_id)
    # return redirect("Blog_Full", post.id)
    return redirect(reverse("blog_full",args=[str(post.id)]))

def Comment_Post(request, comentario_id):
    comentario = Comentario.objects.get(id = comentario_id)
    post = Post.objects.get(id = comentario.post_id)
    return render(request,"blog/comments.html",{'post':post})
        
class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    
class EditarComentario(UpdateView):
    model = Comentario
    form_class = EditarComentarioForm
    template_name='blog/editar_comments.html'
    # success_url= reverse('comments', args=[str('comentario.pk')])

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EditarRespuesta(UpdateView):
    model = Respuesta
    form_class = EditarRespuestaForm
    template_name='blog/editar_reply.html'
    # success_url= reverse('comments', args=[str('comentario.pk')])


    def form_valid(self, form):
        form.instance.updated = timezone.now()
        form.instance.autor = self.request.user
        return super().form_valid(form)

    

    

    

        
    
    