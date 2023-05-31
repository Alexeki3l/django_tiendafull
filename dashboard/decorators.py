from django.shortcuts import render, redirect


def proveedor_required(function):
    def wrap(request, *args, **kwargs):
        a = str(request.user.profile.tipo)
        if not a == 'Proveedor':
            return redirect('Home')
        return function(request, *args, **kwargs)
    return wrap