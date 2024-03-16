class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {}
        self.carro = carro

    def agregar(self, producto):
        producto_id = str(producto.id)
        if producto_id not in self.carro.keys():
            self.carro[producto_id] = {
                "producto_id": producto_id,
                "nombre_producto": producto.name,
                "precio": str(producto.price),
                "cantidad": 1,
                "imagen": producto.image.url,
            }
        else:
            for value in self.carro.values():
                if value["producto_id"] == producto_id:
                    value["cantidad"] += 1
                    value["precio"] = str(float(value["precio"]) + float(producto.price))
                    break
        self.guardar_carro()

    def get_productos(self):
        productos_en_carro = []
        for item in self.carro.values():
            producto = {
                'id': item['producto_id'],
                'nombre': item['nombre_producto'],
                'precio': item['precio'],
                'cantidad': item['cantidad'],
                'imagen': item['imagen'],
            }
            productos_en_carro.append(producto)
        return productos_en_carro

    def get_total(self):
        total = 0
        for item in self.carro.values():
            total += float(item['precio']) * item['cantidad']
        return total

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar_carro()

    def restar_producto(self, producto):
        producto_id = str(producto.id)
        for value in self.carro.values():
            if value["producto_id"] == producto_id:
                value["cantidad"] -= 1
                value["precio"] = str(float(value["precio"]) - float(producto.price))
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True
