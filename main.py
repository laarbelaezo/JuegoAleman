import pygame
import random
import sys
import os
from player import Jugador, Plataforma, Moneda

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()

try:
    sonidos = {
        'walk': pygame.mixer.Sound(resource_path("walk.wav")),
        'jump': pygame.mixer.Sound(resource_path("jump.wav")),
        'gameover': pygame.mixer.Sound(resource_path("gameover.wav"))
    }
except: sonidos = None

ANCHO_PANTALLA, ALTO_PANTALLA = 960, 540
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 28)
fuente_grande = pygame.font.SysFont("Arial", 80, bold=True)

# Inserta aquí tus 100 preguntas
banco_preguntas = [
    {"q": "Wie sagt man „Hola“?", "o": ["Hallo", "Tschüss", "Bitte"], "a": "a"},
    {"q": "Wie sagt man „Adiós“?", "o": ["Auf Wiedersehen", "Danke", "Ja"], "a": "a"},
    {"q": "Wie sagt man „Gracias“?", "o": ["Bitte", "Danke", "Nein"], "a": "a"},
    {"q": "Wie sagt man „Sí“?", "o": ["Nein", "Ja", "Vielleicht"], "a": "b"},
    {"q": "Wie sagt man „No“?", "o": ["Ja", "Nein", "Danke"], "a": "b"},
    {"q": "Wie sagt man „Por favor“?", "o": ["Bitte", "Danke", "Tschüss"], "a": "a"},
    {"q": "Wie sagt man „Buenos días“?", "o": ["Guten Abend", "Guten Morgen", "Gute Nacht"], "a": "b"},
    {"q": "Wie sagt man „Buenos días (tarde)“?", "o": ["Guten Tag", "Guten Nacht", "Tschüss"], "a": "a"},
    {"q": "Wie sagt man „Buenas noches (despedida)“?", "o": ["Guten Abend", "Gute Nacht", "Hallo"], "a": "b"},
    {"q": "Wie sagt man „Perdón“?", "o": ["Entschuldigung", "Bitte", "Ja"], "a": "a"},
    {"q": "Wie heißt „yo“?", "o": ["Du", "Ich", "Wir"], "a": "b"},
    {"q": "Wie heißt „tú“?", "o": ["Ich", "Du", "Er"], "a": "b"},
    {"q": "Wie heißt „él“?", "o": ["Sie", "Es", "Er"], "a": "c"},
    {"q": "Wie heißt „ella“?", "o": ["Sie", "Er", "Es"], "a": "a"},
    {"q": "Wie heißt „nosotros“?", "o": ["Ihr", "Wir", "Sie"], "a": "b"},
    {"q": "Wie heißt „ustedes“?", "o": ["Ihr", "Wir", "Sie"], "a": "c"},
    {"q": "Wie heißt „0“?", "o": ["Eins", "Null", "Zwei"], "a": "b"},
    {"q": "Wie heißt „1“?", "o": ["Eins", "Zwei", "Drei"], "a": "a"},
    {"q": "Wie heißt „2“?", "o": ["Drei", "Vier", "Zwei"], "a": "c"},
    {"q": "Wie heißt „3“?", "o": ["Drei", "Vier", "Fünf"], "a": "a"},
    {"q": "Wie heißt „4“?", "o": ["Vier", "Fünf", "Sechs"], "a": "a"},
    {"q": "Wie heißt „5“?", "o": ["Fünf", "Sechs", "Sieben"], "a": "a"},
    {"q": "Wie heißt „6“?", "o": ["Sechs", "Sieben", "Acht"], "a": "a"},
    {"q": "Wie heißt „7“?", "o": ["Acht", "Neun", "Sieben"], "a": "c"},
    {"q": "Wie heißt „8“?", "o": ["Acht", "Neun", "Zehn"], "a": "a"},
    {"q": "Wie heißt „9“?", "o": ["Neun", "Zehn", "Elf"], "a": "a"},
    {"q": "Wie heißt „10“?", "o": ["Elf", "Zwölf", "Zehn"], "a": "c"},
    {"q": "Wie heißt „lunes“?", "o": ["Dienstag", "Montag", "Mittwoch"], "a": "b"},
    {"q": "Wie heißt „martes“?", "o": ["Dienstag", "Montag", "Freitag"], "a": "a"},
    {"q": "Wie heißt „miércoles“?", "o": ["Mittwoch", "Donnerstag", "Samstag"], "a": "a"},
    {"q": "Wie heißt „jueves“?", "o": ["Freitag", "Donnerstag", "Montag"], "a": "b"},
    {"q": "Wie heißt „viernes“?", "o": ["Sonntag", "Freitag", "Dienstag"], "a": "b"},
    {"q": "Wie heißt „sábado“?", "o": ["Samstag", "Montag", "Mittwoch"], "a": "a"},
    {"q": "Wie heißt „domingo“?", "o": ["Samstag", "Sonntag", "Freitag"], "a": "b"},
    {"q": "Wie heißt „enero“?", "o": ["Februar", "März", "Januar"], "a": "c"},
    {"q": "Wie heißt „febrero“?", "o": ["Februar", "April", "Mai"], "a": "a"},
    {"q": "Wie heißt „marzo“?", "o": ["März", "Juni", "Juli"], "a": "a"},
    {"q": "Wie heißt „abril“?", "o": ["August", "April", "Mai"], "a": "b"},
    {"q": "Wie heißt „mayo“?", "o": ["Mai", "Juni", "Juli"], "a": "a"},
    {"q": "Wie heißt „junio“?", "o": ["Juli", "Juni", "August"], "a": "b"},
    {"q": "Wie heißt „julio“?", "o": ["Juli", "Juni", "Mai"], "a": "a"},
    {"q": "Wie heißt „agosto“?", "o": ["August", "September", "Oktober"], "a": "a"},
    {"q": "Wie heißt „septiembre“?", "o": ["Oktober", "November", "September"], "a": "c"},
    {"q": "Wie heißt „octubre“?", "o": ["Oktober", "Dezember", "August"], "a": "a"},
    {"q": "Wie heißt „noviembre“?", "o": ["November", "Dezember", "Januar"], "a": "a"},
    {"q": "Wie heißt „diciembre“?", "o": ["Januar", "Dezember", "März"], "a": "b"},
    {"q": "Wie heißt „rojo“?", "o": ["Blau", "Rot", "Gelb"], "a": "b"},
    {"q": "Wie heißt „azul“?", "o": ["Blau", "Rot", "Grün"], "a": "a"},
    {"q": "Wie heißt „verde“?", "o": ["Schwarz", "Weiß", "Grün"], "a": "c"},
    {"q": "Wie heißt „amarillo“?", "o": ["Gelb", "Grau", "Braun"], "a": "a"},
    {"q": "Wie heißt „blanco“?", "o": ["Schwarz", "Weiß", "Blau"], "a": "b"},
    {"q": "Wie heißt „negro“?", "o": ["Weiß", "Schwarz", "Rot"], "a": "b"},
    {"q": "Wie heißt „perro“?", "o": ["Katze", "Hund", "Maus"], "a": "b"},
    {"q": "Wie heißt „gato“?", "o": ["Hund", "Katze", "Vogel"], "a": "b"},
    {"q": "Wie heißt „agua“?", "o": ["Milch", "Saft", "Wasser"], "a": "c"},
    {"q": "Wie heißt „pan“?", "o": ["Brot", "Käse", "Fisch"], "a": "a"},
    {"q": "Wie heißt „leche“?", "o": ["Wasser", "Milch", "Tee"], "a": "b"},
    {"q": "Wie heißt „carne“?", "o": ["Fleisch", "Fisch", "Ei"], "a": "a"},
    {"q": "Wie heißt „pescado“?", "o": ["Fleisch", "Fisch", "Ei"], "a": "b"},
    {"q": "Wie heißt „fruta“?", "o": ["Gemüse", "Brot", "Obst"], "a": "c"},
    {"q": "Wie heißt „padre“?", "o": ["Mutter", "Vater", "Bruder"], "a": "b"},
    {"q": "Wie heißt „madre“?", "o": ["Vater", "Mutter", "Schwester"], "a": "b"},
    {"q": "Wie heißt „hermano“?", "o": ["Bruder", "Schwester", "Kind"], "a": "a"},
    {"q": "Wie heißt „hermana“?", "o": ["Bruder", "Vater", "Schwester"], "a": "c"},
    {"q": "Wie heißt „niño“?", "o": ["Kind", "Mann", "Frau"], "a": "a"},
    {"q": "Wie heißt „hombre“?", "o": ["Frau", "Mann", "Kind"], "a": "b"},
    {"q": "Wie heißt „mujer“?", "o": ["Mann", "Frau", "Kind"], "a": "b"},
    {"q": "Wie heißt „casa“?", "o": ["Schule", "Haus", "Auto"], "a": "b"},
    {"q": "Wie heißt „coche“?", "o": ["Auto", "Bus", "Zug"], "a": "a"},
    {"q": "Wie heißt „escuela“?", "o": ["Haus", "Schule", "Buch"], "a": "b"},
    {"q": "Wie heißt „libro“?", "o": ["Stift", "Buch", "Tisch"], "a": "b"},
    {"q": "Wie heißt „mesa“?", "o": ["Stuhl", "Tisch", "Bett"], "a": "b"},
    {"q": "Wie heißt „cama“?", "o": ["Tisch", "Bett", "Tür"], "a": "b"},
    {"q": "Wie heißt „puerta“?", "o": ["Fenster", "Tür", "Wand"], "a": "b"},
    {"q": "Wie heißt „ventana“?", "o": ["Wand", "Fenster", "Tür"], "a": "b"},
    {"q": "Wie heißt „estudiante“?", "o": ["Lehrer", "Schüler", "Arzt"], "a": "b"},
    {"q": "Wie heißt „maestro“?", "o": ["Schüler", "Lehrer", "Arzt"], "a": "b"},
    {"q": "Wie heißt „médico“?", "o": ["Arzt", "Polizist", "Koch"], "a": "a"},
    {"q": "Wie heißt „cocinero“?", "o": ["Arzt", "Koch", "Kellner"], "a": "b"},
    {"q": "Wie heißt „hoy“?", "o": ["Gestern", "Heute", "Morgen"], "a": "b"},
    {"q": "Wie heißt „ayer“?", "o": ["Heute", "Morgen", "Gestern"], "a": "c"},
    {"q": "Wie heißt „mañana“?", "o": ["Gestern", "Morgen", "Heute"], "a": "b"},
    {"q": "Wie heißt „grande“?", "o": ["Klein", "Groß", "Gut"], "a": "b"},
    {"q": "Wie heißt „pequeño“?", "o": ["Groß", "Klein", "Schön"], "a": "b"},
    {"q": "Wie heißt „bueno“?", "o": ["Schlecht", "Groß", "Gut"], "a": "c"},
    {"q": "Wie heißt „malo“?", "o": ["Gut", "Schlecht", "Schön"], "a": "b"},
    {"q": "Wie heißt „hermoso“?", "o": ["Schön", "Hässlich", "Gut"], "a": "a"},
    {"q": "Wie heißt „caliente“?", "o": ["Kalt", "Heiß", "Warm"], "a": "b"},
    {"q": "Wie heißt „frío“?", "o": ["Heiß", "Warm", "Kalt"], "a": "c"},
    {"q": "Wie heißt „rápido“?", "o": ["Langsam", "Schnell", "Gut"], "a": "b"},
    {"q": "Wie heißt „lento“?", "o": ["Schnell", "Langsam", "Schlecht"], "a": "b"},
    {"q": "Wie heißt „mucho“?", "o": ["Wenig", "Viel", "Sehr"], "a": "b"},
    {"q": "Wie heißt „poco“?", "o": ["Viel", "Wenig", "Sehr"], "a": "b"},
    {"q": "Wie heißt „siempre“?", "o": ["Nie", "Oft", "Immer"], "a": "c"},
    {"q": "Wie heißt „nunca“?", "o": ["Immer", "Nie", "Oft"], "a": "b"},
    {"q": "Wie heißt „a menudo“?", "o": ["Nie", "Oft", "Immer"], "a": "b"},
    {"q": "Wie heißt „ahora“?", "o": ["Später", "Jetzt", "Gleich"], "a": "b"},
    {"q": "Wie heißt „después“?", "o": ["Jetzt", "Später", "Gleich"], "a": "b"},
    {"q": "Wie heißt „fácil“?", "o": ["Schwer", "Einfach", "Gut"], "a": "b"},
    {"q": "Wie heißt „difícil“?", "o": ["Einfach", "Schwer", "Gut"], "a": "b"}
]

fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA)); fondo.fill((135, 206, 235))
try:
    fondo_img = pygame.image.load(resource_path("fondo.png")).convert()
    fondo = pygame.transform.scale(fondo_img, (ANCHO_PANTALLA, ALTO_PANTALLA))
except: pass

def reiniciar_juego():
    global plataformas, monedas, ultima_plataforma_x, contador_plataformas, score, indice_quiz, es_campeon, lista_quiz, sonido_go_disparado, teclado_buffer
    plataformas = pygame.sprite.Group()
    monedas = pygame.sprite.Group()
    plataformas.add(Plataforma(0, 500, 1000, 50, "piso.png"))
    ultima_plataforma_x = 1000
    contador_plataformas = 0
    score = 0
    indice_quiz = 0
    es_campeon = False
    sonido_go_disparado = False
    teclado_buffer = ""
    lista_quiz = random.sample(banco_preguntas, 10)
    return Jugador(100, 100, "jugador.png"), 0

jugador, camara_x = reiniciar_juego()
pausado = estado_quiz = es_campeon = False
corriendo = True
teclado_buffer = ""

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: corriendo = False
        if evento.type == pygame.KEYDOWN:
            teclado_buffer += pygame.key.name(evento.key)
            if "merequetengue" in teclado_buffer.lower(): es_campeon = True
            
            if not jugador.game_over and not es_campeon and not estado_quiz:
                if evento.key == pygame.K_RETURN: pausado = not pausado
            
            if estado_quiz:
                sel = None
                if evento.key == pygame.K_a: sel = "a"
                elif evento.key == pygame.K_b: sel = "b"
                elif evento.key == pygame.K_c: sel = "c"
                if sel:
                    if sel == lista_quiz[indice_quiz]["a"]:
                        score += 1
                        indice_quiz += 1
                        if indice_quiz >= 10: es_campeon = True
                    else: jugador.game_over = True
                    estado_quiz = False
            
            if pausado:
                if evento.key == pygame.K_w: pausado = False
                if evento.key == pygame.K_r: jugador, camara_x = reiniciar_juego()
                if evento.key == pygame.K_a: corriendo = False
            
            if jugador.game_over or es_campeon:
                if evento.key == pygame.K_r: jugador, camara_x = reiniciar_juego()
                if evento.key == pygame.K_a: corriendo = False

    if not pausado and not jugador.game_over and not estado_quiz and not es_campeon:
        jugador.update(plataformas, sonidos)
        if jugador.game_over and not sonido_go_disparado:
            if sonidos: sonidos['gameover'].play()
            sonido_go_disparado = True
            
        if ultima_plataforma_x < jugador.rect.x + 1000:
            p_ancho = random.randint(80, 180)
            p_x = ultima_plataforma_x + random.randint(80, 200)
            plataformas.add(Plataforma(p_x, random.randint(300, 450), p_ancho, 20, "bloque.png"))
            contador_plataformas += 1
            if contador_plataformas % 5 == 0 and indice_quiz < 10:
                monedas.add(Moneda(p_x + p_ancho // 2 - 15, 300))
            ultima_plataforma_x = p_x + p_ancho
        
        if pygame.sprite.spritecollide(jugador, monedas, True): estado_quiz = True
        if jugador.rect.x > ANCHO_PANTALLA // 2: camara_x = jugador.rect.x - ANCHO_PANTALLA // 2
    
    pantalla.blit(fondo, (0, 0))
    for p in plataformas: pantalla.blit(p.image, (p.rect.x - camara_x, p.rect.y))
    for m in monedas: pantalla.blit(m.image, (m.rect.x - camara_x, m.rect.y))
    pantalla.blit(jugador.image, (jugador.rect.x - camara_x, jugador.rect.y))
    pantalla.blit(fuente.render(f"Punkte: {score}/10", True, (255, 255, 255)), (800, 20))

    if es_campeon:
        pantalla.blit(pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA), (0,0)) # Overlay
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA)); overlay.set_alpha(180); overlay.fill((255, 215, 0))
        pantalla.blit(overlay, (0,0))
        txt_c = fuente_grande.render("CHAMPION", True, (255, 255, 255))
        pantalla.blit(txt_c, (ANCHO_PANTALLA//2 - txt_c.get_width()//2, 150))
        pantalla.blit(fuente.render("[R]estart, [A]us", True, (255, 255, 255)), (350, 400))
    elif jugador.game_over:
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA)); overlay.set_alpha(180); overlay.fill((150, 0, 0))
        pantalla.blit(overlay, (0,0))
        txt_g = fuente_grande.render("GAME OVER", True, (255, 255, 255))
        pantalla.blit(txt_g, (ANCHO_PANTALLA//2 - txt_g.get_width()//2, 150))
        pantalla.blit(fuente.render(f"Punkte: {score}/10", True, (255, 255, 255)), (380, 250))
        pantalla.blit(fuente.render("[R]estart, [A]us", True, (255, 255, 255)), (350, 400))
    elif estado_quiz:
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA)); overlay.set_alpha(150); overlay.fill((0, 100, 0))
        pantalla.blit(overlay, (0,0))
        q = lista_quiz[indice_quiz]
        pantalla.blit(fuente.render(q["q"], True, (255, 255, 255)), (100, 150))
        pantalla.blit(fuente.render(f"a) {q['o'][0]}", True, (255, 255, 255)), (100, 200))
        pantalla.blit(fuente.render(f"b) {q['o'][1]}", True, (255, 255, 255)), (100, 240))
        pantalla.blit(fuente.render(f"c) {q['o'][2]}", True, (255, 255, 255)), (100, 280))
    elif pausado:
        pantalla.blit(fuente.render("PAUSE - [W]eiter, [R]estart, [A]us", True, (255, 255, 255)), (250, 250))
    
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()