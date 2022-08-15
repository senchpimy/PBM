import os 
import hashlib
import sys
import time 
#################################################################################################################################
#t = time.localtime()
#current_time = time.strftime("%H:%M:%S", t)
#print(current_time)
#################################################################################################################################
def init(): #creacion de la base de datos
    if os.path.exists(".pbm"):
        print("Database already exists")
    else:
        database=open(".pbm","a")
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        database.write("INIT "+current_time)
        database.close()
#################################################################################################################################
def ignore():
    if os.path.exists(".pbmignore"):
        1+1
#################################################################################################################################
def hash_dir(dir,dirs_dict): #Hashea todos los elementos de un directorio y regresa los hashes
    current_dir_hashes=list()
    current_dir_names=list()
    for i in os.lisdir():
        if os.path.isdir(i):
            continue
        else:
            cuurent_dir_hashes.append(hash_file(i))
            current_dir_names.append(i)
#################################################################################################################################
def hash_file(file): #Da el hash de el archivo (completado)
    BUF_SIZE = 65536 #El tamaño en el que el archivo se va adividir
    file=open(i,"rb") #abrimos el archivo para leer sus bytes
    sha512=hashlib.sha512() #creamos un obejeto en el que se guardara la shasum
    while True: #Leemos el archivo hast aque ya no halla info 
        data = file.read(BUF_SIZE)#Leemos el archivos en cachitos
        if not data: #Se acaba el loop cuando ya no hay mas bytes en el archivo
            break
        sha512.update(data) #Actualizamos la shasum de el archivo que estamos leyendo con el nuevo chachito que obtivumos
        return sha512
#################################################################################################################################
def formater(files,hashes,dire="."): #Lee los nombres de los archivos y hashes y los guarda en .pbm (completado)
    len_hash=len(hashes) 
    len_list=len(files)
    if len_hash!=len_list: #Nos aseguramos que haya igual de hashes que de elementos
        print("Numero de archivos incongruente con numero de hashes\nNumero de archivos {}\nNumer de hashes:{}".format(len_list,len_hash))
        return
    if os.path.exists(".pbm")==False: #Nos aseguramos que ya existea una base de datos inicializada
        print("Database don exist run: pbm init")
        return

    database=open(".pbm","a")#Abrimos la base de datos
    for i in range(len_hash): #pasamos por cada elemento de nustras listas
       database.write(dire+"/"+files[i]+"   "+hashes[i]+"\n") #escribimos el archivo y su hash
    database.close() #cerramos el archivo
#################################################################################################################################
#t2 = time.localtime()
#current_time2 = time.strftime("%H:%M:%S", t2)
#print(current_time2)
#################################################################################################################################
