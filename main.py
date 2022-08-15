import os 
import hashlib
import sys
import time 
#################################################################################################################################
#t = time.localtime()
#current_time = time.strftime("%H:%M:%S", t)
#print(current_time)
#################################################################################################################################
def init():
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
def directory_scan(path,subdirs):
    files=os.listdir(path) #Listamos todos los elementos de el directorio
    directories= [] #Lista para guradar las subcarpetas
    files_list=[] #Los nombres de los archivos 
    files_to_open=[] ##Lista para guardar archivos como objetos
    hashes=[] #Lista para guardar los hashes
    for i in files: #Leemos todos los archivos 
        if os.path.isdir(i):#Si es carpeta la guardamos 
            directory_scan(i) #Guardamos la carptea en el directorio de carpetas
        else: 
            file_hashed=hash_file(i)
    hashes.append(sha512.hexdigest()) #Guardamos el archivo en la lista de hashes de forma leegible
    files_list.append(i) 
    subdirs[path]=directories #añadimos los subdirectorios que contiene el directorio actual
    return files_list,hashes
#################################################################################################################################
def hash_file(file):
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
def formater(files,hashes,dire="."):
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
def recursive(dirs):
    dirs2=dirs
    for i in dirs2:
        for j in dirs2[i]:
            files,hashes=hash_directory(j,dirs2)
            formater(files,hashes)
#################################################################################################################################
#t2 = time.localtime()
#current_time2 = time.strftime("%H:%M:%S", t2)
#print(current_time2)
#################################################################################################################################
subdirs={}
files,hashes=hash_directory(".",subdirs)
formater(files,hashes)
#recursive(subdirs)
print(subdirs)
