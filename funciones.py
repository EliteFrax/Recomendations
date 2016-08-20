#archivo que contiene las funciones para el programa

def Creacion_Diccionarios(ratings, movies):
	#crea los diccionarios usados en el programa
	diccionario_usuarios_info_peliculas = dict()
	ratings_file = open(ratings)
	for line in ratings_file:
		usuario,movie,rating,time = line.strip().split('::')
		if usuario in diccionario_usuarios_info_peliculas:
			diccionario_usuarios_info_peliculas[usuario].append((movie,rating,time))
		else:
			diccionario_usuarios_info_peliculas[usuario] = [[movie,rating,time]]
	ratings_file.close()
	diccionario_datos_peliculas = dict()
	movies_file = open(movies)
	for line in movies_file:
		movie,title,genres = line.strip().split('::')
		diccionario_datos_peliculas[movie] = (title,genres)
	movies_file.close()
	return diccionario_usuarios_info_peliculas,diccionario_datos_peliculas
		
def Sumante1(a_sumar, dictsum):
	#suma los ratings de los usuarios individualmente
	suma = 0
	for z in a_sumar:
		suma += float(dictsum[z])**2
	return suma
	
def Sumante2(a_sumar, dictsum1, dictsum2):
	#suma las multiplicaciones de ratings de ambos usuarios
	suma = 0
	for z in a_sumar:
		suma += float(dictsum1[z])*float(dictsum2[z])
	return suma
		
def Similitud_Entre_Usuarios(usuario1, usuario2, diccionario_usuarios_info_peliculas, diccionario_datos_peliculas):
	#calcula y retorna la similitud entre usuarios
	diccionario_ratings_usuario1 = {}
	diccionario_ratings_usuario2 = {}
	peliculas_vistas_usuario_1 = set()
	peliculas_vistas_usuario_2 = set()
	for vistas in diccionario_usuarios_info_peliculas[usuario1] :
		peliculas_vistas_usuario_1.add(vistas[0])
		diccionario_ratings_usuario1[vistas[0]] = vistas[1]
	for vistas in diccionario_usuarios_info_peliculas[usuario2] :
		peliculas_vistas_usuario_2.add(vistas[0])
		diccionario_ratings_usuario2[vistas[0]] = vistas[1]
	conjunto_interseccion = list(peliculas_vistas_usuario_1&peliculas_vistas_usuario_2)
	peliculas_vistas_usuario_1 = list(peliculas_vistas_usuario_1)
	peliculas_vistas_usuario_2 = list(peliculas_vistas_usuario_2)
	sumatoria_ambos = Sumante2(conjunto_interseccion,diccionario_ratings_usuario1,diccionario_ratings_usuario2)
	sumatoria_usuario_1 = Sumante1(peliculas_vistas_usuario_1,diccionario_ratings_usuario1)
	sumatoria_usuario_2 = Sumante1(peliculas_vistas_usuario_2,diccionario_ratings_usuario2)
	sim = sumatoria_ambos / ((sumatoria_usuario_1 ** (0.5)) * (sumatoria_usuario_2 ** (0.5)))
	return sim
	
def Rating_Pelicula(usuario, pelicula, diccionario_usuarios_info_peliculas, diccionario_datos_peliculas):
	#caulcula y retorna el rating de una pelicula para el usuario actual en base a su similitud con otros usuarios
	suma_rat = 0
	suma_rat_div = 0
	for Espectador in diccionario_usuarios_info_peliculas:
		for datos_ratings_usuario in diccionario_usuarios_info_peliculas[Espectador]:
			if datos_ratings_usuario[0] == pelicula:
				sim = Similitud_Entre_Usuarios(usuario, Espectador, diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)
				for mov,rat,time in diccionario_usuarios_info_peliculas[Espectador]:
					if mov  ==  pelicula:
						rat_spec = float(rat)
						suma_rat += sim * rat_spec
						suma_rat_div += float(sim)
	return suma_rat / suma_rat_div
	
def Peliculas_Sin_Rating(usuario, diccionario_usuarios_info_peliculas, diccionario_datos_peliculas):
	#busca las pelicula a las que el usuario no le ha dado rating o no ha visto (no puedo realmente determinar eso) y devuelve una lista
	buscar_rating = set(diccionario_datos_peliculas.keys())
	for datos_ratings_usuario in diccionario_usuarios_info_peliculas:
		if datos_ratings_usuario[0] in buscar_rating:
			buscar_rating.discard(datos_ratings_usuario[0])
	return list(buscar_rating)
