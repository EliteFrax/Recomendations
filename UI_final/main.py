# importar modulos necesarios
from Tkinter import *
import threading, Queue # para que la aplicacion principal no se congele al buscar el top ten
import ttk
import os

# importar plugins y otros programas propios
import Plugins
import Funciones

# crear ventana
maestro = Tk()
nombre_de_programa = "Recomendatron 9001+"
maestro.wm_title(nombre_de_programa)
maestro.overrideredirect(1)

# Queue
queue = Queue.Queue()

# variables globales a usar a lo largo del programa
tiempo_de_frame = 0
valor_suavizado = 0
temporizador_global = 0
fue_actualizado = False
recien_creado = True
ultima_geometria = Plugins.ObtenerGeometriaPrograma(maestro)
nueva_geometria = ultima_geometria
usuario_global = "__USERNAME__"
similitud_minima = 50

#datos a utilizar mas adelante
archratings = 'ratings.dat'
archmovies = 'movies.dat'

lista_de_nombres = []
lista_de_ratings = []
lista_de_generos = []

print "Generando listado de usuarios, porfavor espere... tiempo aproximado: 10~15s"
diccionario_usuarios_info_peliculas , diccionario_datos_peliculas = Funciones.Creacion_Diccionarios(archratings, archmovies)
print "Lanzando Interfaz grafica..."

# funcion en thread que busca el top ten
# se tuvo que googlear threading para impedir
# que el programa se congeleara durante la espera
# para poder ver la animacion de forma fluida
class TopThread(threading.Thread):
    def __init__(self, queue, usuario, dict1, dict2, minsim):
        self.usuario = usuario
        self.dict1 = dict1
        self.dict2 = dict2
        self.minsim = float(minsim)
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        global top_ten
        top_ten = Funciones.Top_Ten(self.usuario, self.dict1, self.dict2, self.minsim)
        self.queue.put("Task finished")
        
def buscar_top_ten(usuario, dict1, dict2, minsim=50):
    TopThread(queue, usuario, dict1, dict2, minsim).start()
top_ten = None
# colores
database_de_colores = [
    ("skin_blue", "#2980b9", "#1c567d", "#123a54", "#2e90d1", "#52a7e0", "#2c3e50", "#34495e", "#ffffff", "#000000", "#000000"),
    ("skin_red", "#b22d2d", "#771e1e", "#4f1414", "#d55a5a", "#c93232", "#812020", "#5c1717", "#ffffff", "#000000", "#eebbbb"),
    ("skin_green", "#6da838", "#497025", "#304b18", "#95cb64", "#7abd3f", "#4c7627", "#4c7627", "#ffffff", "#000000", "#bbeebb")
]
skin_de_programa = 0

color_bg = database_de_colores[skin_de_programa][1]
color_borde = database_de_colores[skin_de_programa][2]
color_borde_oscuro = database_de_colores[skin_de_programa][3]

color_fondo_claro_fg = database_de_colores[skin_de_programa][4]
color_fondo_oscuro_fg = database_de_colores[skin_de_programa][5]

color_fondo_claro_bg = database_de_colores[skin_de_programa][6]
color_fondo_oscuro_bg = database_de_colores[skin_de_programa][7]

color_claro = database_de_colores[skin_de_programa][8]
color_oscuro = database_de_colores[skin_de_programa][9]
color_texto = database_de_colores[skin_de_programa][10]

# asignar color de fondo al programa
maestro["bg"] = color_bg
borde_programa = Frame(maestro, bg=color_borde)
barra_superior = Frame(borde_programa, bg=color_borde)
barra_superior_name = Label(barra_superior, text=nombre_de_programa, bg=color_borde, fg=color_claro)
barra_superior_icon_image = PhotoImage(file="data/icon/icon_16x16.gif")
icono_de_programa_image = PhotoImage(file="data/icon/icon_196x196.gif")
barra_superior_icon = Label(barra_superior, text="", image=barra_superior_icon_image, bg=color_borde)
barra_superior_icon.pack(side=LEFT, padx=4, pady=4)
# mover programa si la barra superior es presionada
barra_superior.bind("<Button-1>", lambda x: Plugins.ProgramDragWithMouse(maestro, x))
barra_superior_name.bind("<Button-1>", lambda x: Plugins.ProgramDragWithMouse(maestro, x))
barra_superior_name.pack(side=LEFT, fill=X, expand=YES)
# funciones varias
def TerminarPrograma(frame=None):
    os._exit(1)
    
def RecargarIndicesEnLista(nuevo_valor, lista_objetivo):
    pass

boton_cerrar = Button(barra_superior, text="x", command=lambda: TerminarPrograma(),
                      bg=color_borde_oscuro, fg="white", bd=0,
                      highlightthickness=0, activebackground="#ff2222",
                      activeforeground=color_oscuro)

def main(estado = "InicioSesion"):
    global ultima_geometria, nueva_geometria, fue_actualizado, recien_creado
    global lista_de_nombres, lista_de_generos, lista_de_ratings
    
    marco_principal = Frame(borde_programa, bg=color_bg)
    estado_de_programa = estado
    # Mas funciones
    def DesactivarRuedaDelMouse(widget):
        widget.bind("<MouseWheel>", HacerNada) # windows and mac
        widget.bind("<Button-4>", HacerNada) # linux specific
        widget.bind("<Button-5>", HacerNada) # linux specific
        
    def HacerNada(event):
            return "break"

    # constantes usadas a lo largo del programa, idealmente obtenerlas
    # usando Funciones.py
    lista_de_usuarios = diccionario_usuarios_info_peliculas.keys()
    
    lista_de_usuarios_largo = len(lista_de_usuarios)

    # colocar widgets basado en el estado_de_programa actual
    if estado_de_programa == "InicioSesion":
        texto0 = Label(marco_principal, text="Bienvenido a", font=("Mono", 16),
                       bg=color_bg, fg=color_texto)
        texto1 = Label(marco_principal, text=nombre_de_programa, font=("Mono", 24),
                       bg=color_bg, fg=color_texto)
        texto2 = Label(marco_principal, text="Elija su usuario de la lista:",
                       font=("Sans", 12), bg=color_bg, fg=color_texto)
        
        texto3 = Label(marco_principal, text="Elija precision del algoritmo",
                       font=("Sans", 9), bg=color_bg, fg=color_texto)
        texto4 = Label(marco_principal, text="(menor el valor, mayor el tiempo de espera):",
                       font=("Sans", 9), bg=color_bg, fg=color_texto)
                    
        icono_de_programa = Label(marco_principal, text="", image=icono_de_programa_image,
                             bg=color_bg, borderwidth=0)
                       
        barradeslizadora1 = Scale(marco_principal, from_=30, to_=60, orient="horizontal",
                                  showvalue=1, borderwidth=0, sliderrelief=FLAT, fg=color_claro,
                                  highlightthickness=0, highlightcolor = color_fondo_claro_bg, bg=color_bg,
                                  activebackground=color_borde, troughcolor=color_fondo_claro_fg)
        barradeslizadora1.set(50)
        
        listaencaja0 = Listbox(marco_principal, relief=FLAT, selectmode=SINGLE, bd=0,
                           highlightthickness=0)
        
        barradeslizadora0 = Scale(marco_principal, from_=0, to_=100, orient="vertical",
                       showvalue=0, borderwidth=0, sliderrelief=FLAT,
                       highlightthickness=0, bg=color_fondo_claro_bg,
                       activebackground=color_borde)
        
        marco_botones = Frame(marco_principal, bg=color_bg)
        marco_botones_izq = Frame(marco_botones, bg=color_bg)
        marco_botones_der = Frame(marco_botones, bg=color_bg)
        
        boton0 = Button(marco_botones_izq, text="Iniciar Sesion", relief=FLAT,
                         command=lambda: CambiarModoDePrograma("Cargando", "login"),
                         bg=color_bg, highlightthickness=0, fg=color_texto,
                         activebackground=color_borde, activeforeground=color_claro)
        boton1 = Button(marco_botones_der, text="Salir", relief=FLAT,
                         command=lambda: TerminarPrograma(marco_principal),
                         bg=color_bg, highlightthickness=0, fg=color_texto,
                         activebackground=color_borde, activeforeground=color_claro)
        
        texto0.grid(row=0, padx=8)
        texto1.grid(row=1, padx=8, pady=(0, 8))
        texto2.grid(row=5, padx=8, sticky=W)
        
        icono_de_programa.grid(row=2)
        
        texto3.grid(row=3, padx=8, sticky=W)
        barradeslizadora1.grid(row=5, sticky=W+E, padx=8)
        texto4.grid(row=4, padx=8, sticky=W)
        
        listaencaja0.grid(row=7, padx=(8,26), pady=(12,4), sticky=W+E)
        barradeslizadora0.grid(row=7, padx=(0, 8), pady=(12, 4), sticky=E+N+S)
        
        marco_botones.grid(row=8, sticky=W+E)
        marco_botones_izq.pack(fill=BOTH, expand=YES, side=LEFT, padx=(8, 0), pady=4)
        marco_botones_der.pack(fill=BOTH, expand=YES, side=RIGHT, padx=(0, 8), pady=4)

        boton0.pack(fill=BOTH)
        boton1.pack(fill=BOTH)
        
        DesactivarRuedaDelMouse(listaencaja0)
        for usuario in lista_de_usuarios:
            listaencaja0.insert(END, str(usuario))
        for i in range(len(lista_de_usuarios)):
            # asignar color a cada indice de la lista basado en su posicion
            # respecto al modulo de i en 2
            try:
                if i%2==0:
                    color = color_fondo_claro_fg
                    color2 = color_fondo_oscuro_bg
                else:
                    color = color_fondo_oscuro_fg
                    color2 = color_fondo_claro_bg
                listaencaja0.itemconfig(i, {'bg':color, "fg":color2})
            except:
                break
        
    elif estado_de_programa == "Cargando":
        # pantalla de carga, visual
        texto0 = Label(marco_principal, text="Cargando listado...",
                       font=("Monospaced", 24), bg=color_bg, fg=color_texto)
        (animacion0, 
        animacion0_lista, 
        animacion0_largo) = Plugins.ObtenerAnimacionDeGif(marco_principal, "data/running.gif")
        
        animacion0.config(bg=color_bg)
        texto0.grid(row=0)
        animacion0.grid(row=1, pady=8)
        
        buscar_top_ten(usuario_global, diccionario_usuarios_info_peliculas , diccionario_datos_peliculas, similitud_minima)

    elif estado_de_programa == "TopTen":
        # mostrar resultado de la carga
        textousuario = Label(marco_principal, text="Bienvenido: "+str(usuario_global),
                          font=("Serif", 22), bg=color_bg, fg=color_texto)
        texto0 = Label(marco_principal, text="Estas son las 10 peliculas\nrecomendadas para usted!",
                       font=("Serif", 16), bg=color_bg, fg=color_texto)
        data_frame = Frame(marco_principal, bg=color_bg)
        contador, contador_lista, contador_largo = Plugins.ObtenerAnimacionDeGif(marco_principal, "data/countdown.gif") 
        contador["bg"] = color_bg
        barradeslizadora0 = Scale(marco_principal, orient="horizontal", showvalue=0, relief=FLAT,
                       borderwidth=0, from_=0, to=9, sliderrelief=FLAT, highlightthickness=0,
                       bg=color_fondo_claro_bg, activebackground=color_borde)

        texto1 = Label(data_frame, text=" "*25, font=("Mono", 16), bg=color_bg, fg=color_texto)
        texto2 = Label(data_frame, text="", font=("Serif", 12), bg=color_bg, fg=color_texto)
        texto3 = Label(data_frame, text="", font=("Serif", 12), bg=color_bg, fg=color_texto)
        
        texto4 = Label(marco_principal, text="+1;", font=("Arial Black", 24), bg="#181818", fg="white")
        
        boton0 = Button(marco_principal, text="Volver Atras!",
                         command=lambda: CambiarModoDePrograma("InicioSesion"),
                         highlightthickness=0, bg=color_bg, relief=FLAT,
                         activebackground=color_borde, activeforeground=color_claro)
        
        print "creando estrellas"
        marco_estrellas = Frame(data_frame, bg=color_bg)
        print "primera estrella"
        estrella0, estrella0_lista, estrella0_largo = Plugins.ObtenerAnimacionDeGif(marco_estrellas, "data/star.gif") 
        print "estrellas copias"
        estrella1 = Label(marco_estrellas, bg=color_bg, image=estrella0_lista[0])
        estrella2 = Label(marco_estrellas, bg=color_bg, image=estrella0_lista[0])
        estrella3 = Label(marco_estrellas, bg=color_bg, image=estrella0_lista[0])
        estrella4 = Label(marco_estrellas, bg=color_bg, image=estrella0_lista[0])
        
        estrella0["bg"]=color_bg
        print "estrellas listas"
        textousuario.grid(row=0, columnspan=2, padx=8)
        texto0.grid(row=1, columnspan=2)
        texto1.pack(fill=BOTH, padx=8)
        texto2.pack(fill=X, padx=8)
        texto3.pack(fill=X, padx=8)
        print "posicionando estrellas"
        estrella0.pack(fill=X, expand=YES, side=LEFT)
        estrella1.pack(fill=X, expand=YES, side=LEFT)
        estrella2.pack(fill=X, expand=YES, side=LEFT)
        estrella3.pack(fill=X, expand=YES, side=LEFT)
        estrella4.pack(fill=X, expand=YES, side=LEFT)
        
        marco_estrellas.pack(fill=X, expand=YES,padx=8)
        data_frame.grid(row=2, column=1, sticky=N+S+W+E)
        
        
        contador.grid(row=2, padx=8)
        texto4.grid(row=2, sticky=E,padx=12) #topkek
        barradeslizadora0.grid(row=3, sticky=W+E, padx=8)
        boton0.grid(row=3, column=1, padx=8, pady=4, sticky=W+E)
        print "creando listas"
        lista_de_nombres = []
        lista_de_ratings = []
        lista_de_generos = []
        for indice in top_ten:
            try:
                lista_de_nombres.append( diccionario_datos_peliculas[indice[1]][0] )
                lista_de_ratings.append( str(indice[0]) )
                lista_de_generos.append( diccionario_datos_peliculas[indice[1]][1] )
            except:
                print "caso de emergencia"
                lista_de_nombres.append( "--|SIN DATOS|--" )
                lista_de_ratings.append( "0.0" )
                lista_de_generos.append( "-N-O-D-A-T-A-" )

    # Luego que los widgets fueron colocados en pantalla,
    # permitir actualizarlos
    fue_actualizado = True
    
    #Funcion de actualizacion de widgets
    def ActualizarPrograma():
        global tiempo_de_frame, temporizador_global, valor_suavizado, similitud_minima
        tiempo_de_frame += 1
        #maestro.update()
        maestro.geometry("")
        
        #dont update if no widgets exists
        if fue_actualizado == False:
            return 0
        if True:#try:
            if estado_de_programa == "None":
                TerminarPrograma(marco_principal)
                
            if estado_de_programa == "InicioSesion":
                try:
                    global usuario_global
                    #set barradeslizadora0 <to> based on listaencaja0 length
                    similitud_minima = float(barradeslizadora1.get())
                    
                    lista_de_usuarios_largo = len(lista_de_usuarios)
                    listaencaja0_max = max(lista_de_usuarios_largo - int(listaencaja0["height"]), 0)
                    barradeslizadora0.config(to=listaencaja0_max, resolution=0.01)
                    
                    #set listaencaja position based on barradeslizadora
                    listaencaja0_y = int(round(barradeslizadora0.get() ))
                    listaencaja0.yview(listaencaja0_y)
                    
                    usuario_global = listaencaja0.get(ACTIVE) 
                except:
                    pass
                
            elif estado_de_programa == "Cargando":
                # animar la imagen manualmente, ya que tkinter no soporta gifs
                # animados
                try:
                    animacion0.config(image=animacion0_lista[(tiempo_de_frame/400)%animacion0_largo])
                
                    #verificar resultado de top_ten cada 100ms
                    if tiempo_de_frame%100 == 0:
                        try:
                            msg = queue.get(0)
                            if top_ten is not None:
                                CambiarModoDePrograma("TopTen")
                        except Queue.Empty:
                            pass
                            #buscar_top_ten(usuario_global, diccionario_usuarios_info_peliculas , diccionario_datos_peliculas )
                except:
                    pass
            elif estado_de_programa == "TopTen":
                try:
                    estrella0.config(image=estrella0_lista[(tiempo_de_frame/400)%estrella0_largo])
                    estrella1.config(image=estrella0_lista[(tiempo_de_frame/400)%estrella0_largo])
                    estrella2.config(image=estrella0_lista[(tiempo_de_frame/400)%estrella0_largo])
                    estrella3.config(image=estrella0_lista[(tiempo_de_frame/400)%estrella0_largo])
                    estrella4.config(image=estrella0_lista[(tiempo_de_frame/400)%estrella0_largo])
                    
                    decimo = (contador_largo)/10.0
                    valor = decimo * float(barradeslizadora0.get())
                    valor_suavizado += (valor - valor_suavizado)/1000.0
                    
                    indice_de_pelicula = 9-barradeslizadora0.get()
                    rating = round(float(lista_de_ratings[indice_de_pelicula]),1)
                    
                    for index, star in enumerate([estrella0, estrella1, estrella2, estrella3, estrella4]):
                        if rating < index+0.5 :
                            if star.winfo_ismapped():
                                star.pack_forget()
                        else:
                            if not star.winfo_ismapped():
                                star.pack(fill=X, expand=YES, side=LEFT)
                    
                    contador.config(image=contador_lista[int(valor_suavizado%contador_largo)])
                    
                    #print "reemplazar textos"
                    indice_de_pelicula = 9-barradeslizadora0.get()
                    texto1.config(text=str(lista_de_nombres[indice_de_pelicula]).center(25))
                    texto2.config(text="Genero: "+str(lista_de_generos[indice_de_pelicula]))
                    texto3.config(text="Rating: "+str(rating))
                except:
                    pass
        #except:
        #    return 0
        
    def CambiarModoDePrograma(nuevo_modo="Cargando", razon="normal"):
        global fue_actualizado, ultima_geometria, usuario_global
        if usuario_global == "__USERNAME__":
            return 0
        ultima_geometria = Plugins.ObtenerGeometriaPrograma(maestro)
        marco_principal.destroy()
        fue_actualizado = False
        main(nuevo_modo)
        

    # show marco_principal, no longer available to edit
    boton_cerrar.pack(side=RIGHT)
    barra_superior.pack(fill=BOTH)
    marco_principal.pack(fill=BOTH, padx=4, pady=(0,4))
    borde_programa.pack(fill=BOTH)
    # resize program
    maestro.update()
    maestro.geometry("")
    maestro.update()
    if recien_creado:
        ultima_geometria = Plugins.ObtenerGeometriaPrograma(maestro)
        recien_creado = False
    else:
        maestro.update()
        nueva_geometria = Plugins.ObtenerGeometriaPrograma(maestro)
        Plugins.EscalarProgramaSuavemente(maestro, ultima_geometria, nueva_geometria)
    #print ultima_geometria, nueva_geometria
    
    # main loop
    maestro.resizable(width=False, height=False)
    maestro.protocol("WM_DELETE_WINDOW", lambda: TerminarPrograma(maestro))
    while True:
        maestro.after(1000/60, lambda: ActualizarPrograma())
        maestro.update()

if __name__ == "__main__":
    main("InicioSesion")
