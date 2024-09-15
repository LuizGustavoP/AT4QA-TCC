import zulu
import uuid
import crcmod
import time
import string
import random
import datetime
from test_classes.Storage import Storage
from common.utils.StringUtils import StringUtils

class Generators():

    def generate_uuid(storage_field):
        
        print("\n #################### Gerando UUID #################### ")
        
        Storage.storage[storage_field] = uuid.uuid4()
        print("\nNovo UUID gerado: {}. Armazenado com sucesso no campo: {}".format(Storage.storage[storage_field], storage_field))

    def generate_formatted_time(tempo, formato, storage_field):
        
        print("\n #################### Gerando horário {} no formato {} #################### ".format(tempo, formato))

        if formato == "zuluex":
            horario = zulu.now()
            if(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "atras" or tempo.split(" ")[1] == "atrás")):
                horario = horario.subtract(seconds=int(tempo.split()[0]))
            elif(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "adiante")):
                horario = horario.add(seconds=int(tempo.split()[0]))
        elif formato == "zuluz":
            horario = zulu.now()
            if(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "atras" or tempo.split(" ")[1] == "atrás")):
                horario = horario.subtract(seconds=int(tempo.split()[0]))
            elif(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "adiante")):
                horario = horario.add(seconds=int(tempo.split()[0]))
            horario = (str(horario).split(".")[0] + "Z")
        elif formato == "epoch":
            horario = time.time()
            if(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "atras" or tempo.split(" ")[1] == "atrás")):
                horario = horario - float(tempo.split()[0])
            elif(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "adiante")):
                horario = horario + float(tempo.split()[0])
        elif formato.split("@@")[0] == "datetime":
            horario = datetime.datetime.now()
            if(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "atras" or tempo.split(" ")[1] == "atrás")):
                horario = horario - datetime.timedelta(seconds=int(tempo.split()[0]))
            elif(len(tempo.split(" "))> 1 and (tempo.split(" ")[1] == "adiante")):
                horario = horario + datetime.timedelta(seconds=int(tempo.split()[0]))
            horario = horario.strftime(formato.split("@@")[1])

        Storage.storage[storage_field] = horario
        print("\nNovo horário no formato {} gerado: {}. Armazenado com sucesso no campo: {}".format(formato, Storage.storage[storage_field], storage_field))

    def generate_string(string_size, storage_field):
        
        print("\n #################### Generating random string of size {} #################### ".format(string_size))
        Storage.storage[storage_field] = ''.join(random.choice(string.ascii_letters) for i in range(int(string_size)))
        print("\n String aleatória gerada: {}. Armazenada com sucesso no campo: {}".format(Storage.storage[storage_field], storage_field))

    def generate_crc(poly, init, xorValue, value_field, storage_field):
        value_field = StringUtils.replace_placeholder_value_with_stored_value(value_field, Storage.storage)
        print("\n #################### Calculando CRC com polinômio inicial {} utilizando valor inicial {} e valor XOR {} para o valor {} e armazenando resultado no campo {} #################### \n".format(poly, init, xorValue, value_field, storage_field))
        
        crc = crcmod.Crc(int(poly, 16), int(init, 16), False, int(xorValue, 16))
        crc.update(value_field.encode("ascii"))
        Storage.storage[storage_field] = crc.hexdigest()

        print("\nCRC armazenado com sucesso no campo {}!".format(storage_field))