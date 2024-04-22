import json
import zulu
import uuid
import time
import crcmod
import string
import random
import datetime
from generic_api_testing.common.utils.StringUtils import StringUtils
from generic_api_testing.common.utils.FieldBuilders import FieldBuilders
from generic_api_testing.test_classes.Storage import Storage
from generic_api_testing.common.config.config import GeneralSettings


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