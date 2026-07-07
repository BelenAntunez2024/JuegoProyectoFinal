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
    VISTA DE INICIALIZACIÓN MULTIJUGADOR LOCAL:
    Prepara el estado de la sesión para 2 jugadores de forma independiente.
    """
    todos = list(Famoso.objects.all())
    if len(todos) < 10: 
        return HttpResponse("Carga al menos 10 famosos en el admin para poder jugar en modo multijugador.")
    
    # Selecciona 5 famosos únicos y aleatorios para la banca
    seleccion = random.sample(todos, 5)
    
    # --- SISTEMA DE SESIÓN COMPATIBLE CON EL NUEVO TABLERO ---
    request.session['banca_cartas'] = [f.id for f in seleccion]
    request.session['banca_suma'] = sum(f.edad for f in seleccion)
    
    # Datos específicos del Jugador 1
    request.session['j1_cartas'] = []
    request.session['j1_suma'] = 0
    
    # Datos específicos del Jugador 2
    request.session['j2_cartas'] = []
    request.session['j2_suma'] = 0
    
    # Control de flujo de la partida
    request.session['turno'] = 1  # Inicia el Jugador 1
    request.session['jugando'] = True
    request.session['resultado'] = "" 
    
    # Guardamos explícitamente en la base de sesiones antes de redirigir
    request.session.save()
    
    return redirect('jugar_partida')

@csrf_exempt
def jugar_partida(request):
    """
    VISTA PRINCIPAL DEL TABLERO MULTIJUGADOR LOCAL:
    Maneja el desarrollo del juego por turnos consecutivos (J1 luego J2) contra la Banca.
    """
    # Seguridad: Si falta alguna clave en la sesión, reiniciamos
    if 'banca_cartas' not in request.session or 'j1_cartas' not in request.session:
        return redirect('iniciar_partida')
        
    turno_actual = request.session.get('turno', 1)
    es_jugando = request.session.get('jugando', True)
    
    # --- ACCIONES DE LOS JUGADORES (PETICIONES POST) ---
    if request.method == 'POST' and es_jugando:
        
        # CASO A: El jugador del turno actual pide carta
        if 'pedir_carta' in request.POST:
            # Excluimos la banca y lo que ya tengan AMBOS jugadores para evitar cartas repetidas
            excluidos = (request.session['banca_cartas'] + 
                         request.session['j1_cartas'] + 
                         request.session['j2_cartas'])
            
            nuevo_famoso = Famoso.objects.exclude(id__in=excluidos).order_by('?').first()
            
            if nuevo_famoso:
                if turno_actual == 1:
                    request.session['j1_suma'] += nuevo_famoso.edad
                    request.session['j1_cartas'].append(nuevo_famoso.id)
                    # REGLA BUST J1: Si J1 se pasa, termina su turno forzosamente y pasa al J2
                    if request.session['j1_suma'] > request.session['banca_suma']:
                        request.session['turno'] = 2
                else:
                    request.session['j2_suma'] += nuevo_famoso.edad
                    request.session['j2_cartas'].append(nuevo_famoso.id)
                    # REGLA BUST J2: Si J2 se pasa, termina la partida ya que es el último
                    if request.session['j2_suma'] > request.session['banca_suma']:
                        es_jugando = False
                        request.session['jugando'] = False
            else:
                # Si se acaban los famosos, cerramos la partida
                es_jugando = False
                request.session['jugando'] = False
            
            request.session.save()
            
        # CASO B: El jugador del turno actual decide Plantarse
        elif 'plantarse' in request.POST:
            if turno_actual == 1:
                # J1 se planta, le pasamos el control al Jugador 2
                request.session['turno'] = 2
            else:
                # J2 se planta, finaliza la partida y evaluamos resultados
                es_jugando = False
                request.session['jugando'] = False
                
            request.session.save()

        # --- EVALUACIÓN DE GANADORES (Solo cuando la partida finaliza) ---
        if not es_jugando:
            banca = request.session['banca_suma']
            j1 = request.session['j1_suma']
            j2 = request.session['j2_suma']
            
            # Calculamos las distancias (si se pasaron, quedan descalificados poniendo una distancia infinita)
            dist_j1 = (banca - j1) if j1 <= banca else float('inf')
            dist_j2 = (banca - j2) if j2 <= banca else float('inf')
            
            if dist_j1 == float('inf') and dist_j2 == float('inf'):
                request.session['resultado'] = "¡Ambos se pasaron! Gana la banca."
            elif dist_j1 == dist_j2:
                request.session['resultado'] = f"¡Empate! Ambos quedaron a {dist_j1} años de la banca."
            elif dist_j1 < dist_j2:
                request.session['resultado'] = f"¡Ganó el Jugador 1! Quedó a {dist_j1} años."
            else:
                request.session['resultado'] = f"¡Ganó el Jugador 2! Quedó a {dist_j2} años."
                
            request.session.save()
            
    # --- RENDERIZADO DEL TABLERO ---
    # Enviamos las cartas reales de la banca para que se vean las fotos
    banca_mano = Famoso.objects.filter(id__in=request.session['banca_cartas'])
    
    # Cartas del jugador activo (para que vea a sus famosos)
    cartas_del_turno = request.session['j1_cartas'] if turno_actual == 1 and es_jugando else request.session['j2_cartas']
    mano = Famoso.objects.filter(id__in=cartas_del_turno)
    
    # Manos para el resumen del final
    j1_mano_final = Famoso.objects.filter(id__in=request.session['j1_cartas'])
    j2_mano_final = Famoso.objects.filter(id__in=request.session['j2_cartas'])
    
    return render(request, 'juego/partida.html', {
        'banca_mano': banca_mano,
        'mano': mano,  
        'j1_mano': j1_mano_final,
        'j2_mano': j2_mano_final,
        
        # --- MÁXIMO SECRETO EN LOS NÚMEROS ---
        # La suma de la banca NO se sabe hasta el final
        'banca_suma': "???" if es_jugando else request.session.get('banca_suma', 0),
        
        # Los jugadores NO ven sus sumas numéricas en pantalla mientras juegan. ¡A calcular de memoria!
        'j1_suma': request.session['j1_suma'] if not es_jugando else "???",
        'j2_suma': request.session['j2_suma'] if not es_jugando else "???",
        
        'turno': turno_actual,
        'jugando': es_jugando,
        'resultado': request.session.get('resultado', '')
    })