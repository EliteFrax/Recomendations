import funciones

archratings = 'ratings.dat'
archmovies = 'movies.dat'

#definicion de variables estaticas
diccionario_usuarios_info_peliculas , diccionario_datos_peliculas = funciones.Creacion_Diccionarios(archratings, archmovies)


print funciones.Rating_Pelicula('123','12', diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)
print funciones.Peliculas_Sin_Rating('123', diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)