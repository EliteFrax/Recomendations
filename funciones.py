#archivo que contiene las funciones para el programa

archratings = 'ratings.dat'
archmovies = 'movies.dat'


def Creacion_Diccionarios(ratings, movies):
	#crea los diccionarios usados en el programa
	diccionario_usuarios_info_peliculas = dict()
	ratings_file = open(ratings)
	for line in ratings_file:
		user,movie,rating,time = line.strip().split('::')
		if user in diccionario_usuarios_info_peliculas:
			diccionario_usuarios_info_peliculas[user].append((movie,rating,time))
		else:
			diccionario_usuarios_info_peliculas[user] = [[movie,rating,time]]
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
		
def Similitud_Entre_Usuarios(user1, user2):
	#calcula y retorna la similitud entre usuarios
	creacion_diccionarios(archratings,archmovies)
	diccionario_ratings_user1 = {}
	diccionario_ratings_user2 = {}
	peliculas_vistas_user_1 = set()
	peliculas_vistas_user_2 = set()
	for vistas in diccionario_usuarios_info_peliculas[user1] :
		peliculas_vistas_user_1.add(vistas[0])
		diccionario_ratings_user1[vistas[0]] = vistas[1]
	for vistas in diccionario_usuarios_info_peliculas[user2] :
		peliculas_vistas_user_2.add(vistas[0])
		diccionario_ratings_user2[vistas[0]] = vistas[1]
	conjunto_interseccion = list(peliculas_vistas_user_1&peliculas_vistas_user_2)
	peliculas_vistas_user_1 = list(peliculas_vistas_user_1)
	peliculas_vistas_user_2 = list(peliculas_vistas_user_2)
	sumatoria_ambos = sumante2(conjunto_interseccion,diccionario_ratings_user1,diccionario_ratings_user2)
	sumatoria_1 = sumante1(peliculas_vistas_user_1,diccionario_ratings_user1)
	sumatoria_2 = sumante1(peliculas_vistas_user_2,diccionario_ratings_user2)
	sim = sumatoria_ambos / ((sumatoria_1 ** (0.5)) * (sumatoria_2 ** (0.5)))
	return sim
	
def Rating_Pelicula(usuario, pelicula):
	#caulcula y retorna el rating de una pelicula para el usuario actual en base a su similitud con otros usuarios
	suma_rat = 0
	suma_rat_div = 0
	for Espectador in diccionario_usuarios_info_peliculas:
		for alguna_wea in diccionario_usuarios_info_peliculas[Espectador]:
			if alguna_wea[0] == pelicula:
				sim = similitud_entre_usuarios(usuario,Espectador)
				for mov,rat,time in diccionario_usuarios_info_peliculas[Espectador]:
					if mov  ==  pelicula:
						rat_spec = float(rat)
						suma_rat += sim * rat_spec
						suma_rat_div += float(sim)
	return suma_rat / suma_rat_div


print Rating_Pelicula('4','5')
