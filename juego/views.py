"""Vistas del juego.

Contiene las vistas principales: `inicio`, `iniciar_partida`,
`iniciar_partida_solo` y `jugar_partida`. Estas vistas gestionan el estado
del juego mediante la sesión de Django usando claves como:

- `banca_cartas`: lista de IDs de famosos elegidos por la banca.
- `banca_suma`: suma de edades de la banca.
- `j1_cartas`, `j2_cartas`: listas de IDs con las cartas de cada jugador.
- `j1_suma`, `j2_suma`: sumas de edades de cada jugador.
- `turno`, `jugando`, `resultado`, `modo_solo`: control de flujo.
"""

from django.shortcuts import HttpResponse, render, redirect
import random
from .models import Famoso
from django.views.decorators.csrf import csrf_exempt

# ── Nuevos imports para autenticación ──
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistro, FormularioLogin

@login_required
@csrf_exempt
def inicio(request):
    """Renderiza la pantalla de bienvenida y resetea el estado de la sesión.

    Esta vista borra las claves de sesión asociadas a una partida previa para
    asegurar que se comience desde un estado limpio cuando el jugador vuelve
    al menú principal.
    """

    keys_a_borrar = ['banca_cartas', 'banca_suma', 'j1_cartas', 'j1_suma', 'j2_cartas', 'j2_suma', 'turno', 'jugando', 'resultado', 'modo_solo']
    for key in keys_a_borrar:
        if key in request.session:
            del request.session[key]

    request.session.save()
    return render(request, 'juego/inicio.html')

@login_required
def iniciar_partida_solo(request):
    """
    VISTA DE INICIALIZACIÓN MULTIJUGADOR LOCAL:
    Prepara el estado de la sesión para 2 jugadores de forma independiente.
    """
    todos = list(Famoso.objects.all())
    if len(todos) < 5: 
        return HttpResponse("Carga al menos 5 famosos en el admin para poder jugar en modo multijugador.")
    
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
    request.session['modo_solo'] = True
    
    # Guardamos explícitamente en la base de sesiones antes de redirigir
    request.session.save()
    
    return redirect('jugar_partida')

@login_required
def iniciar_partida(request):
    """
    VISTA DE INICIALIZACIÓN MULTIJUGADOR LOCAL:
    Prepara la sesión tradicional para 2 jugadores ("Pasa el celular").
    """
    todos = list(Famoso.objects.all())
    if len(todos) < 10: 
        return HttpResponse("Carga al menos 10 famosos en el admin para poder jugar en modo multijugador.")
    
    seleccion = random.sample(todos, 5)
    
    request.session['banca_cartas'] = [f.id for f in seleccion]
    request.session['banca_suma'] = sum(f.edad for f in seleccion)
    
    request.session['j1_cartas'] = []
    request.session['j1_suma'] = 0
    request.session['j2_cartas'] = []
    request.session['j2_suma'] = 0
    
    request.session['turno'] = 1
    request.session['jugando'] = True
    request.session['resultado'] = ""
    request.session['modo_solo'] = False
    
    request.session.save()
    return redirect('jugar_partida')

@login_required
@csrf_exempt
def jugar_partida(request):
    """
    VISTA PRINCIPAL DEL TABLERO:
    Maneja el desarrollo del juego en Modo Solitario o Multijugador por turnos.
    """
    # Seguridad: Si falta alguna clave en la sesión, reiniciamos al inicio limpio
    if 'banca_cartas' not in request.session or 'j1_cartas' not in request.session:
        return redirect('inicio')
        
    turno_actual = request.session.get('turno', 1)
    es_jugando = request.session.get('jugando', True)
    es_modo_solo = request.session.get('modo_solo', False)
    
    # --- ACCIONES DE LOS JUGADORES (PETICIONES POST) ---
    if request.method == 'POST' and es_jugando:
        
        # CASO A: El jugador del turno actual pide carta
        if 'pedir_carta' in request.POST:
            # Excluimos la banca y lo que ya tengan ambos jugadores
            excluidos = (request.session['banca_cartas'] + 
                         request.session['j1_cartas'] + 
                         request.session['j2_cartas'])
            
            nuevo_famoso = Famoso.objects.exclude(id__in=excluidos).order_by('?').first()
            
            if nuevo_famoso:
                if turno_actual == 1:
                    request.session['j1_suma'] += nuevo_famoso.edad
                    request.session['j1_cartas'].append(nuevo_famoso.id)
                    # REGLA BUST J1: Si J1 se pasa de la banca
                    if request.session['j1_suma'] > request.session['banca_suma']:
                        if es_modo_solo:
                            es_jugando = False
                            request.session['jugando'] = False
                        else:
                            request.session['turno'] = 2
                else:
                    request.session['j2_suma'] += nuevo_famoso.edad
                    request.session['j2_cartas'].append(nuevo_famoso.id)
                    # REGLA BUST J2: Fin de partida
                    if request.session['j2_suma'] > request.session['banca_suma']:
                        es_jugando = False
                        request.session['jugando'] = False
            else:
                es_jugando = False
                request.session['jugando'] = False
            
            request.session.save()
            
        # CASO B: El jugador del turno actual decide Plantarse
        elif 'plantarse' in request.POST:
            if turno_actual == 1:
                if es_modo_solo:
                    es_jugando = False
                    request.session['jugando'] = False
                else:
                    request.session['turno'] = 2
            else:
                es_jugando = False
                request.session['jugando'] = False
                
            request.session.save()

        # --- EVALUACIÓN DE GANADORES (Solo cuando la partida finaliza) ---
        if not es_jugando:
            banca = request.session['banca_suma']
            j1 = request.session['j1_suma']
            j2 = request.session['j2_suma']
            
            if es_modo_solo:
                # Textos personalizados para un solo jugador
                if j1 > banca:
                    request.session['resultado'] = "¡Te pasaste! Gana la banca."
                elif j1 == banca:
                    request.session['resultado'] = "¡Clavado perfecto! Le ganaste a la banca de forma exacta."
                else:
                    dist_j1 = banca - j1
                    request.session['resultado'] = f"¡Te plantaste! Quedaste a sólo {dist_j1} años de la banca."
            else:
                # Lógica tradicional multijugador
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
    banca_mano = Famoso.objects.filter(id__in=request.session['banca_cartas'])
    
    cartas_del_turno = request.session['j1_cartas'] if turno_actual == 1 and es_jugando else request.session['j2_cartas']
    mano = Famoso.objects.filter(id__in=cartas_del_turno)
    
    j1_mano_final = Famoso.objects.filter(id__in=request.session['j1_cartas'])
    j2_mano_final = Famoso.objects.filter(id__in=request.session['j2_cartas'])
    
    return render(request, 'juego/partida.html', {
        'banca_mano': banca_mano,
        'mano': mano,  
        'j1_mano': j1_mano_final,
        'j2_mano': j2_mano_final,
        
        'banca_suma': "???" if es_jugando else request.session.get('banca_suma', 0),
        'j1_suma': request.session['j1_suma'] if not es_jugando else "???",
        'j2_suma': request.session['j2_suma'] if not es_jugando else "???",
        
        'turno': turno_actual,
        'jugando': es_jugando,
        'resultado': request.session.get('resultado', '')
    })

def vista_login(request):
    """Vista de inicio de sesión.
    Si el usuario ya está logueado, lo redirige directo al inicio del juego.
    Si recibe un POST, intenta autenticar con las credenciales del formulario.
    Si son válidas, inicia la sesión y redirige al juego.
    """
    # Si el usuario ya está logueado, no tiene sentido mostrarle el login
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        # Creamos el formulario con los datos que envió el usuario
        formulario = FormularioLogin(request, data=request.POST)
        if formulario.is_valid():
            # Si las credenciales son correctas, extraemos el usuario validado
            usuario = formulario.get_user()
            # login() crea la sesión del usuario en la base de datos
            login(request, usuario)
            # Redirigimos al inicio del juego
            return redirect('inicio')
    else:
        # Si es GET (primera vez que entra), mostramos el formulario vacío
        formulario = FormularioLogin()
    return render(request, 'juego/login.html', {'formulario': formulario})

def vista_registro(request):
    """Vista de registro de nuevo usuario.
    Muestra el formulario de registro. Si es válido, crea el usuario,
    lo loguea automáticamente y lo redirige al juego sin necesidad de
    pasar por el login.
    """
    # Si ya está logueado, mandalo al juego
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            # .save() crea el usuario en la base de datos
            usuario = formulario.save()
            # Logueamos al usuario recién creado automáticamente
            login(request, usuario)
            # Lo mandamos al juego, ya logueado
            return redirect('inicio')
    else:
        formulario = FormularioRegistro()
    return render(request, 'juego/registro.html', {'formulario': formulario})
def vista_logout(request):
    """Vista de cierre de sesión.
    Cierra la sesión del usuario y lo redirige a la pantalla de login.
    Acepta tanto GET como POST para simplicidad.
    """
    # logout() elimina la sesión del usuario de la base de datos
    logout(request)
    return redirect('vista_login')