class Bolsa:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        bolsa = self.session.get('bolsa')
        if not bolsa:
            bolsa = self.session['bolsa'] = {}
        self.bolsa = bolsa

    def agregar(self, asset):
        id_str = str(asset.id)
        # Solo lo agregamos si no está ya en la bolsa
        if id_str not in self.bolsa:
            self.bolsa[id_str] = {
                'recurso_id': asset.id,
                'titulo': asset.titulo,
                'precio_clp': asset.precio_clp,
            }
        self.guardar()

    def guardar(self):
        self.session['bolsa'] = self.bolsa
        self.session.modified = True

    def vaciar(self):
        self.session['bolsa'] = {}
        self.session.modified = True

    # Permite saber cuántos assets hay en la bolsa
    def cantidad_total(self):
        return len(self.bolsa.keys())
    
    # Calcula el valor total en CLP
    def total_pagar(self):
        total = 0
        for item in self.bolsa.values():
            total += item['precio_clp']
        return total