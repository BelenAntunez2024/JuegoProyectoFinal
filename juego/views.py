from django.test.utils import require_jinja2
from django.shortcuts import  HttpResponse,render, redirect
import random
from .models import Famoso

def iniciar_partida(request):
    todos = list(Famoso.objects.all())
    if len(todos) < 6: # Seguridad: necesitamos al menos 6 famosos
        return HttpResponse("Carga al menos 6 famosos en el admin.")
    
    seleccion = random.sample(todos, 5)
    request.session['banca_suma'] = sum(f.edad for f in seleccion)
    request.session['jugador_cartas'] = []
    request.session['jugador_suma'] = 0
    request.session['jugando'] = True
    request.session['resultado'] = "" #Limpiamos el resultado anterior
    return redirect('jugar_partida')

def jugar_partida(request):
    if 'jugador_cartas' not in request.session:
        return redirect('iniciar_partida')
        
    if request.method == 'POST' and request.session.get('jugando'):
        if 'pedir_carta' in request.POST:
            todos = Famoso.objects.exclude(id__in=request.session['jugador_cartas'])
            if todos.exists(): 
                nuevo_famoso = random.choice(todos)
            request.session['jugador_suma'] += nuevo_famoso.edad
            request.session['jugador_cartas'].append(nuevo_famoso.id)
        
            # Si el jugador se pasa del total de la banca, pierde automáticamente
            if request.session['jugador_suma'] > request.session ['banca_suma']:
                request.session['jugando'] = False
                request.session['resultado'] = "Te pasaste. Gana la banca." 
                request.session.save() # Guardamos sesión
        elif 'plantarse' in request.POST:
            request.session['jugando'] = False
            banca = request.session['banca_suma']
            jugador = request.session ['jugador_suma']
         # Lógica para determinar el resultado
            if jugador == banca:
                request.session['resultado'] = "Genial, Lograste una coincidencia exacta!"
            else: 
              dif = banca - jugador
              request.session['resultado'] = f"Te Plantaste. Quedaste a {dif} años del total de la banca."
            request.session.save()
    mano = Famoso.objects.filter(id__in=request.session['jugador_cartas'])
    return render(request, 'juego/partida.html', {
        'mano': mano,
        # Enviamos la suma real solo si el juego terminó. 
        # Si está jugando, la ocultamos.
        'jugador_suma': request.session['jugador_suma'] if not request.session.get('jugando') else "???",
        'banca_suma': request.session.get('banca_suma') if not request.session.get('jugando') else "???",
        'jugando': request.session.get('jugando'),
        'resultado': request.session.get('resultado', '')
    })