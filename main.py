

archratings='controlratings.dat'
archmovies='controlmovies.dat'


def creacion_diccionarios(ratings,movies):
	users_pelis=dict()
	ratings_file=open(ratings)
	for line in ratings_file:
		user,movie,rating,time=line.strip().split('::')
		if user in users_pelis:
			users_pelis[user].append((movie,rating,time))
		else:
			users_pelis[user]=[(movie,rating,time)]
	ratings_file.close()
	movies_id=dict()
	movies_file=open(movies)
	for line in movies_file:
		movie,title,genres=line.strip().split('::')
		movies_id[movie]=(title,genres)
	movies_file.close()
	return users_pelis,movies_id		
		
def sumante1(a_sumar,dictsum):
	suma=0
	for z in a_sumar:
		suma+=float(dictsum[z])**2
	return suma
	
def sumante2(a_sumar,dictsum1,dictsum2):
	suma=0
	for z in a_sumar:
		suma+=float(dictsum1[z])*int(dictsum2[z])
	return suma
		
def similitud_entre_usuarios(user1,user2):
	dictrat1={}
	dictrat2={}
	vistas_user1=set()
	vistas_user2=set()
	for vistas in users_pelis[user1] :
		vistas_user1.add(vistas[0])
		dictrat1[vistas[0]]=vistas[1]
	for vistas in users_pelis[user2] :
		vistas_user2.add(vistas[0])
		dictrat2[vistas[0]]=vistas[1]
	conjunto_unido=list(vistas_user1&vistas_user2)
	vistas_user1=list(vistas_user1)
	vistas_user2=list(vistas_user2)
	sumatoria_ambos=sumante2(conjunto_unido,dictrat1,dictrat2)
	sumatoria_1=sumante1(vistas_user1,dictrat1)
	sumatoria_2=sumante1(vistas_user2,dictrat2)
	sim=sumatoria_ambos/((sumatoria_1**(0.5))*(sumatoria_2**(0.5)))
	return sumatoria_1,sumatoria_2,sumatoria_ambos,sim,((sumatoria_1**(0.5))*(sumatoria_2**(0.5)))
	

users_pelis,movies_id=creacion_diccionarios(archratings,archmovies)
print similitud_entre_usuarios('1','2')