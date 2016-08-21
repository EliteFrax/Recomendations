import funciones

archratings = 'ratings.dat'
archmovies = 'movies.dat'

#definicion de variables estaticas
diccionario_usuarios_info_peliculas , diccionario_datos_peliculas = funciones.Creacion_Diccionarios(archratings, archmovies)
usuario = '1'
usuario1 = '1'
usuario2 = '71568'

#print funciones.Rating_Pelicula('123','12', diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)
#print funciones.Peliculas_Sin_Rating('123', diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)
print funciones.Top_Ten(usuario, diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)
#print funciones.Similitud_Entre_Usuarios(usuario1, usuario2, diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)
#print funciones.Usuarios_Similares(usuario, diccionario_usuarios_info_peliculas, diccionario_datos_peliculas)