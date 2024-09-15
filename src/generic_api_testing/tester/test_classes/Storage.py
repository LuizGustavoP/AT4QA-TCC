from common.utils.JsonUtils import JsonUtils
from common.utils.StringUtils import StringUtils
from common.config.database.DatabaseConnection import DatabaseConnection

class Storage():

    storage = {}

    def store_api_response(api_field, field_origin, storage_field, api_response):
        print("\n #################### Armazenando valor do campo {} do {} da resposta da API em campo de nome {} #################### \n".format(api_field, field_origin, storage_field))
        
        if field_origin == "body":
            Storage.storage[storage_field] = JsonUtils.obtain_value_from_path(api_response.json(), api_field)
        elif field_origin == "header":
            Storage.storage[storage_field] = api_response.headers[api_field]
        
        print("Valor {} armazenado no campo {}".format(Storage.storage[storage_field], storage_field))

    def store_api_response_in_unordered_field(campo_retorno_api, campos_relacionados_api, valores_relacionados_api, storage_field, api_response):
        
        print("\n #################### Armazenando valor do campo {} da resposta da API em campo de nome {} #################### \n".format(campo_retorno_api, storage_field))

        print("\nRelativo ao(s) valor(es): {}".format(valores_relacionados_api))
        print("\nRespectivamente relativo(s) ao(s) campo(s): {}".format(campos_relacionados_api))
        
        Storage.storage[storage_field] = JsonUtils.obtain_value_from_path_unordered(api_response.json(), campo_retorno_api, campos_relacionados_api, valores_relacionados_api)
        
        print("Valor {} armazenado no campo {}".format(Storage.storage[storage_field], storage_field))


    def store_response_field_database(nome_bd, query, storage_field):

        print("\n #################### Armazenando valor retornado na query {} da resposta do banco {} em campo de nome {} #################### \n".format(query, nome_bd, storage_field))

        DatabaseConnection.obtain_connection(nome_bd)
        query = StringUtils.replace_placeholder_value_with_stored_value(query, Storage.storage)
        print("\nExecutando a query: {}".format(query))        
        
        if not "where" in query:
            print("Apenas queries com condicionais 'where' podem ser executadas!")
            return False
        
        if query.split(" ")[0] == "update" or query.split(" ")[0] == "delete":
            print("Apenas queries do tipo select podem ser executadas por este statement!")
            return False
        
        resultado = DatabaseConnection.select_one(nome_bd, query)

        if(resultado != None and len(resultado) > 1 ):
            Storage.storage[storage_field] = resultado
            print("\n{} armazenado no campo {}".format(Storage.storage[storage_field], storage_field))
        elif(resultado == None):
            Storage.storage[storage_field] = str(resultado)
            print("\n{} armazenado no campo {}".format(Storage.storage[storage_field], storage_field))
        else:
            Storage.storage[storage_field] = str(resultado[0])
            print("\n{} armazenado no campo {}".format(Storage.storage[storage_field], storage_field))