from django.shortcuts import render, redirect


def proveedor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            a = str(request.user.profile.tipo)
            if not a == '1': #1 is proveedor
                return redirect('Home')
            return function(request, *args, **kwargs)
        else:
            return redirect('Home')
    return wrap