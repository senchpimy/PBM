import os 
import hashlib
from os.path import isdir
from pathlib import Path
import time
import shutil
import sys
#################################################################################################################################
def init(): #creacion de la base de datos (completado)
    if os.path.exists(".pbm"):
        print("Database already exists")
    else:
        database=open(".pbm","a")
        t = time.localtime()
        current_time = time.strftime("Database Created the %d/%m at %H:%M:%S\n", t)
        database.write("INIT "+current_time)
        database.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
        database.close()
#################################################################################################################################
def ignore(): #Elimina todos las lineas de los archivos hasehados que esten en el archivo ".pbmignore"
    if os.path.exists(".pbmignore"):
        ignore=open(".pbmignore", "r").read().splitlines()
        return ignore
    else:
        return []
    
#################################################################################################################################
def hash_dir(dir): #Hashea todos los elementos de un directorio y regresa los hashes
    current_dir_hashes=list()
    current_dir_names=list()
    ignore_files=ignore()
    for i in os.listdir(dir):
        if os.path.isdir(i):
            continue
        else:
            for j in ignore_files:
                if str(i).find(j) != -1:
                    continue
                current_dir_hashes.append(hash_file(i))
                current_dir_names.append(i)
    return current_dir_names,current_dir_hashes
#################################################################################################################################
def hash_file(file): #Da el hash de el archivo (completado)
    BUF_SIZE = 65536 #El tamaño en el que el archivo se va adividir
    try:
        file_o=open(file,"rb") #abrimos el archivo para leer sus bytes
    except:
        #return hashlib.sha512(str("0").encode("utf-8"))
        return "0"
    sha512=hashlib.sha512() #creamos un obejeto en el que se guardara la shasum
    while True: #Leemos el archivo hast aque ya no halla info 
        data = file_o.read(BUF_SIZE)#Leemos el archivos en cachitos
        if not data: #Se acaba el loop cuando ya no hay mas bytes en el archivo
            break
        sha512.update(data) #Actualizamos la shasum de el archivo que estamos leyendo con el nuevo chachito que obtivumos
    return sha512
#################################################################################################################################
def hash_file_special(file): #Por algun motivo no queria aplicar la propiedad .hexdigest() a la salida de esta funcion por que la detectaba como str
    BUF_SIZE = 65536 #El tamaño en el que el archivo se va adividir
    try:
        file_o=open(file,"rb") #abrimos el archivo para leer sus bytes
    except:
        return "0"
    sha512=hashlib.sha512() #creamos un obejeto en el que se guardara la shasum
    while True: #Leemos el archivo hast aque ya no halla info 
        data = file_o.read(BUF_SIZE)#Leemos el archivos en cachitos
        if not data: #Se acaba el loop cuando ya no hay mas bytes en el archivo
            break
        sha512.update(data) #Actualizamos la shasum de el archivo que estamos leyendo con el nuevo chachito que obtivumos
    if str(sha512.hexdigest())!=None:
            return sha512.hexdigest()
    else:
            return "Imposible de hashear"
#################################################################################################################################
def formater(files,hashes): #Lee los nombres de los archivos y hashes y los guarda en .pbm (completado)
    len_hash=len(hashes) 
    len_list=len(files)
    if len_hash!=len_list: #Nos aseguramos que haya igual de hashes que de elementos
        print("Numero de archivos incongruente con numero de hashes\nNumero de archivos {}\nNumer de hashes:{}".format(len_list,len_hash))
        return
    database=open(".pbm","a")#Abrimos la base de datos
    for i in range(len_hash): #pasamos por cada elemento de nustras listas
        try:
            database.write(files[i]+"▓¥»╚▓¥»╚"+hashes[i].hexdigest()+"\n") #escribimos el archivo y su hash
        except:
            database.write(files[i]+"▓¥»╚▓¥»╚imposible_de_hashear\n") #escribimos el archivo y su hash
    database.close() #cerramos el archivo
#################################################################################################################################
def singleformater(files): #Lee los nombres de los archivos y hashes y los guarda en .pbm (completado)
    database=open(".pbm","a")#Abrimos la base de datos
    try:
            database.write(files+"▓¥»╚▓¥»╚"+hash_file_special(files)+"\n") #escribimos el archivo y su hash
    except:
            database.write(files+"▓¥»╚▓¥»╚imposible_de_hashear\n") #escribimos el archivo y su hash
    database.close() #cerramos el archivo
#################################################################################################################################
def recursive(pathe): #Escanea y hashea un directorio de forma recursiva (completado)
    if os.path.exists(".pbm")==False: #Nos aseguramos que ya existea una base de datos inicializada
        print("Database don exist run: pbm init")
        return
    listu=list(Path(pathe).rglob("*"))
    files=[]
    hashes=[]
    ignore_files=ignore()
    for i in listu:
        if isdir(str(i)):
            continue
        for j in ignore_files:
            if str(i).find(j) != -1:
                continue
            files.append("./"+str(i))
            hashes.append(hash_file("./"+str(i)))
    formater(files,hashes)
#################################################################################################################################
def GetDate():
    file=open(".pbm","r")
    date = file.readline().split()
    if len(date)>6:
        return date[4], date[6]
    else: return date[2], date[4]
#################################################################################################################################
def GetDataBase(): #Lee el archivo .pbm y regresa un alista de tuplas con el path de el archivo y el hash (completado)
    databse=list()
    file=open(".pbm","r")
    for h in file.read().splitlines()[2:]:
        i,j=h.split("▓¥»╚▓¥»╚")
        databse.append((i,j))
    return databse

#################################################################################################################################
def GetDataBaseNames(): #Lee el archivo .pbm y regresa una lista de los nombres de los archivos (completado)
    databse=list()
    file=open(".pbm","r")
    for h in file.read().splitlines()[2:]:
        i,_=h.split("▓¥»╚▓¥»╚")
        databse.append(i)
    return databse

#################################################################################################################################
def DeletedAndUntracked():
    Database=GetDataBaseNames()
    CurrenteFiles=list()
    listu=list(Path(".").rglob("*"))
    ignore_files=ignore()
    filesignored=list()

    for i in listu:
        if isdir(i):
            continue
        CurrenteFiles.append("./"+str(i))

    Deleted=[x for x in Database if x not in CurrenteFiles]
    untracked=[x for x in CurrenteFiles if x not in Database]

    for i in untracked:
        for j in ignore_files:
            if i.find(j) == -1:
                continue
            else:
                filesignored.append(i)
    untracked=[x for x in untracked if x not in filesignored]

    return Deleted, untracked

#################################################################################################################################
def Compare(): #Obtiene los archvos que han sido modificados entre el .pbm y la carpeta y los regresa en una lista (completado)
    database=GetDataBase()
    ArchivosDiferentes=list()
    for i in database:
        if i[1]=="imposible_de_hashear":
            continue
        if i[1]!=hash_file_special(i[0]):
             ArchivosDiferentes.append(i[0])
    Deleted,_=DeletedAndUntracked()
    ArchivosDiferentes=[x for x in ArchivosDiferentes if x not in Deleted]
    return ArchivosDiferentes
#################################################################################################################################
def status():
    Deleted, untracked=DeletedAndUntracked()
    ArvhivosDiferentes=Compare()

    deletedlen=len(Deleted)
    Diferenteslen=len(ArvhivosDiferentes)
    Untrackedlen=len(untracked)

    date,time=GetDate()
    print(f"Last Database Update, the {date} at {time}\n\n")

    if deletedlen==0:
        print("No files deleted\n")
    else:
        print(f"{deletedlen} files were deleted\033[1m")
        for i in Deleted:
            print(i)
        print("\033[0m")

    if Untrackedlen==0:
        print("No untracked files\n")
    else:
        print(f"{Untrackedlen} files are untracked \033[1m")
        for i in untracked:
            print(i)
        print("\033[0m")

    if Diferenteslen==0:
        print("No files changed\n")
    else:
        print(f"{Diferenteslen} files were changed\033[1m")
        for i in ArvhivosDiferentes:
            print(i)
        print("\033[0m")
#################################################################################################################################
def UpdateDate():
    t = time.localtime()
    UpdateText ="Updated"+ time.strftime(" the %d/%m at %H:%M:%S\n", t)
    f = open("./.pbm")
    _, remainder = f.readline(), f.read()
    t = open("./.pbm","w")
    t.write(UpdateText)
    t.write(remainder)
    t.close()
#################################################################################################################################
def remove_line(stringtoskip):
    fileName="./.pbm"
    with open(fileName,'r') as read_file:
        lines = read_file.readlines()

    with open(fileName,'w') as write_file:
        for line in lines:
            if line.find(stringtoskip)!=-1:
                continue
            else:
                write_file.write(line)
 #################################################################################################################################
def Updateline(strinput):
    fileName="./.pbm"
    with open(fileName,'r') as read_file:
        lines = read_file.readlines()
    
    with open(fileName,'w') as write_file:
        for line in lines:
            if line.startswith(strinput+"▓"):
                write_file.write(strinput+"▓¥»╚▓¥»╚"+hash_file_special(strinput)+"\n")
            else:
                write_file.write(line)
#################################################################################################################################
def Update():
    UpdateDate()
    ArvhivosDiferentes=Compare()
    Deleted, _=DeletedAndUntracked()
    for i in Deleted:remove_line(i)
    for j in ArvhivosDiferentes:Updateline(j)
    print("UPDATE FINALIZED")

#################################################################################################################################
def Copy(location):
    if os.path.exists(location):
        if isdir(location):
            if location.startswith("~"):
                    location=os.path.expanduser('~')+location
            for i in GetDataBaseNames():
                shutil.copyfile(i,location+i[1:])
    else:print("La ubicacion no es valida")
#################################################################################################################################
def Add(file):
    if os.path.exists(file):
        singleformater(file)
    else:print("El archivo no existe")
#################################################################################################################################
def Use():
    print('\033[1m'+"PBM is a git-like backups manager"+'\033[0m\n')
    print('\033[91m'+"init                  "+'\033[0m'+"Starts a Database")
    print('\033[91m'+"recursive             "+'\033[0m'+"Adds all the files recursively")
    print('\033[91m'+"update                "+'\033[0m'+"Update the database")
    print('\033[91m'+"copy \033[92m\033[4m\x1B[3m*location*"+'\033[0m       '+"Copy the files in the database to a specified location")
    print('\033[91m'+"add \033[92m\033[4m\x1B[3m*file*"+'\033[0m            '+"Add a file to the database")
    print('\033[91m'+"status                "+'\033[0m'+"Get the status of the database")
    print('')

#################################################################################################################################
def main():

    if len(sys.argv)==1:
        Use()
    elif sys.argv[1]=="init": 
        init()
    elif sys.argv[1]=="recursive": 
        UpdateDate()
        recursive(".")
    elif sys.argv[1]=="status": 
        status()
    elif sys.argv[1]=="update": 
        Update()
    elif sys.argv[1]=="copy": 
        Copy(sys.argv[2])
    elif sys.argv[1]=="add": 
        Add(sys.argv[2])
    else:
        print("Invalid option\n")
        Use()

#################################################################################################################################
if __name__ == "__main__":
    main()
