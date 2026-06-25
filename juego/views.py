from django.shortcuts import HttpResponse, render, redirect
import random
from .models import Famoso
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def inicio(request):
    """
    VISTA DE INICIO:
    Esta función simplemente renderiza la pantalla de bienvenida (inicio.html).
    Funciona como el lobby o el 'splash screen' de nuestro juego.
    """
    return render(request, 'juego/inicio.html')

def iniciar_partida(request):
    """
    VISTA DE INICIALIZACIÓN:
    Esta función prepara todo el estado de una partida nueva.
    1. Trae a todos los famosos cargados en la base de datos PostgreSQL.
    2. Valida que haya al menos 6 famosos (5 para la banca + mínimo 1 para el jugador).
    3. Selecciona 5 famosos al azar para armar la META secreta (la banca).
    4. Guarda los datos clave en la sesión del usuario (en el servidor) para que no 
       puedan ser hackeados desde la consola de desarrollador del navegador.
    5. Redirecciona al jugador a la pantalla de la partida.
    """
    todos = list(Famoso.objects.all())
    if len(todos) < 6: 
        # Si no hay suficientes famosos, detenemos el juego e indicamos la acción correctiva
        return HttpResponse("Carga al menos 6 famosos en el admin.")
    
    # Selecciona 5 famosos únicos y aleatorios para la banca
    seleccion = random.sample(todos, 5)
    
    # --- SISTEMA DE SESIÓN (ESTADO DEL JUEGO) ---
    # Guardamos los IDs de la banca para poder mostrarlos pero sin revelar sus edades
    request.session['banca_cartas'] = [f.id for f in seleccion]
    # Suma total de las edades que el jugador debe intentar alcanzar sin pasarse
    request.session['banca_suma'] = sum(f.edad for f in seleccion)
    # Lista de IDs de famosos que el jugador ha solicitado (comienza vacía)
    request.session['jugador_cartas'] = []
    # Acumulador de edad de los famosos del jugador
    request.session['jugador_suma'] = 0
    # Bandera para saber si el juego sigue activo o ya terminó
    request.session['jugando'] = True
    # Mensaje de victoria/derrota que se revelará al final
    request.session['resultado'] = "" 
    
    # Redirecciona al tablero de juego
    return redirect('jugar_partida')

@csrf_exempt
def jugar_partida(request):
    """
    VISTA PRINCIPAL DEL TABLERO:
    Controla el desarrollo del juego por turnos (Pedir Carta / Plantarse).
    """
    # Seguridad: Si el jugador intenta entrar directamente a la partida sin haber
    # inicializado el juego, lo redirigimos a la pantalla de inicio.
    if 'jugador_cartas' not in request.session or 'banca_cartas' not in request.session:
        return redirect('iniciar_partida')
        
    # --- ACCIONES DEL JUGADOR (PETICIONES POST) ---
    if request.method == 'POST' and request.session.get('jugando'):
        
        # CASO A: El jugador presiona "Pedir Carta"
        if 'pedir_carta' in request.POST:
            # Creamos una lista de todos los famosos a excluir (los que ya tiene el jugador + los de la banca)
            excluidos = request.session['jugador_cartas'] + request.session['banca_cartas']
            
            # Buscamos un famoso aleatorio que no esté excluido
            nuevo_famoso = Famoso.objects.exclude(id__in=excluidos).order_by('?').first()
            
            if nuevo_famoso:
                # Actualizamos la suma de edad del jugador y añadimos la carta a su mano
                request.session['jugador_suma'] += nuevo_famoso.edad
                request.session['jugador_cartas'].append(nuevo_famoso.id)
                
                # REGLA DE BUST (PASARSE): Si la suma del jugador supera la de la banca, pierde automáticamente
                if request.session['jugador_suma'] > request.session['banca_suma']:
                    request.session['jugando'] = False
                    request.session['resultado'] = "Te pasaste. Gana la banca."
            else:
                # En caso extremo de que el jugador pida tantas cartas que se acabe la base de datos
                request.session['jugando'] = False
                request.session['resultado'] = "No hay más famosos disponibles. Fin de la partida."
            
            # Guardamos explícitamente los cambios de la sesión modificada
            request.session.save()
            
        # CASO B: El jugador presiona "Plantarse"
        elif 'plantarse' in request.POST:
            request.session['jugando'] = False
            banca = request.session['banca_suma']
            jugador = request.session['jugador_suma']
            
            # Determinamos quién ganó y calculamos la diferencia
            if jugador == banca:
                request.session['resultado'] = "¡Genial, lograste una coincidencia exacta!"
            else: 
                dif = banca - jugador
                request.session['resultado'] = f"Te plantaste. Quedaste a {dif} años del total de la banca."
            
            request.session.save()
            
    # --- RENDERIZADO DEL TABLERO ---
    # Traemos de la base de datos los famosos reales que corresponden a los IDs guardados en la sesión
    mano = Famoso.objects.filter(id__in=request.session['jugador_cartas'])
    banca_mano = Famoso.objects.filter(id__in=request.session['banca_cartas'])
    
    return render(request, 'juego/partida.html', {
        'mano': mano,
        'banca_mano': banca_mano,
        # PROTECCIÓN DE DATOS: Mientras el jugador esté jugando, le enviamos "???" para ocultar las sumas reales.
        # Solo revelamos los números cuando "jugando" pase a ser False.
        'jugador_suma': request.session['jugador_suma'] if not request.session.get('jugando') else "???",
        'banca_suma': request.session.get('banca_suma'),
        'jugando': request.session.get('jugando'),
        'resultado': request.session.get('resultado', '')
    })
