from django.shortcuts import render


def inicio(request):
    return render(request, 'inicio.html')

def contacto(request):
    return render(request, 'Contacto.html')

def blog(request):
    return render(request, 'Blog.html')

def sobre_nosotros(request):
    return render(request, 'Sobre_Nosotros.html')

def precios(request):
    productos = [
        {'nombre': 'Air Max 270 React', 'link': 'https://www.nike.com/t/air-max-270-react-eng-mens-shoe-JKj16v/CW2628-100'},
        {'nombre': 'Air Jordan 1 Mid SE', 'link': 'https://www.nike.com/t/air-jordan-1-mid-se-mens-shoe-nNScBn/CK6587-100'},
        {'nombre': 'Nike ZoomX Invincible Run Flyknit', 'link': 'https://www.nike.com/t/nike-zoomx-invincible-run-flyknit-mens-running-shoe-hG5f5K/CW1597-100'}
    ]
    contexto = {'productos': productos}
    return render(request, 'Precios.html', contexto)

