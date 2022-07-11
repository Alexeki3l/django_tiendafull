class Carro:
    def __init__(self, request):
        self.request=request
        self.session= request.session
        carro=self.session.get("carro")
        if not carro:
            self.session["carro"]={}
            self.carro=self.session['carro']
        else: 
            self.carro=carro

    def agregar(self, producto):
        if(str(producto.id) not in self.carro.keys()):
            self.carro[producto.id]={
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "descripcion":producto.descripcion,
                "precio":str(producto.precio),
                "cantidad":1,
                "imagen":producto.image.url,
                "total":str(producto.precio)
                                    }
        else:
            for key,value in self.carro.items():
                if key == str(producto.id):
                    value["cantidad"]=value["cantidad"] + 1
                    value["total"]=float(value["precio"]) * value["cantidad"]
                    
                    break
        
        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True

    def eliminar(self, producto):
        producto.id=str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()

    def restar_producto(self, producto):
        for key,value in self.carro.items():
            if key==str(producto.id):
                value["cantidad"]=value["cantidad"] - 1
                value["total"]=float(value["precio"])-producto.precio
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                break
        
        self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified=True
