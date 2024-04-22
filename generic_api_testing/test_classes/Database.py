from generic_api_testing.test_classes.Storage import Storage
from generic_api_testing.common.utils.JsonUtils import JsonUtils
from generic_api_testing.common.utils.StringUtils import StringUtils
from generic_api_testing.test_classes.APICalls import APICalls
from generic_api_testing.common.config.database.DatabaseConnection import DatabaseConnection

class Database():
    
    def checa_valor_de_coluna_do_bd(database_name, database_table, database_analised_column, comparison, expected_value, query_where_column, query_where_column_type, query_where_value, field_name, field_origin):
        
        print("\n #################### Checking value in database {}, table {} #################### \n".format(database_name, database_table))

        DatabaseConnection.obtain_connection(database_name)
        
        query_where_value = Database.obtain_field_value(field_origin, field_name, query_where_value)
        where_field = "'{}'".format(query_where_value) if (query_where_column_type == "uuid" or query_where_column_type == "varchar") else query_where_value
        database_analised_column = JsonUtils.format_select_query_column(database_analised_column)
        
        query = "select {} from \"{}\" where \"{}\" = {}".format(database_analised_column, database_table, query_where_column, where_field)
        print("\nExecutando a query: {}".format(query))
        query_result = DatabaseConnection.select_one(database_name, query)
        
        if query_result:
            valor_query_result = "NULL" if query_result[0] == None else query_result[0]
            print("\nValor {} encontrado com sucesso na coluna {}!".format(query_where_value, query_where_column))
            print("query_result do select: {}".format(valor_query_result))
        else:
            print("\nValor {} não localizado na coluna {}!".format(query_where_value, query_where_column))
            return False

        if comparison == "igual a":
            if expected_value == "igual do where":
                return True
            elif expected_value == "vazio":
                print("\nValor esperado: {}. Valor obtido na consulta: {}".format(expected_value, valor_query_result))
                return valor_query_result == "NULL"
            else:
                expected_value = StringUtils.replace_placeholder_value_with_stored_value(expected_value, Storage.storage)
                print("\nValor esperado: {}. Valor obtido na consulta: {}".format(expected_value, valor_query_result))
                return str(valor_query_result) == expected_value
        else:
            if expected_value == "igual do where":
                print("\nErro de configuração. O parâmetro '{}' não deve ser utilizado junto do parâmetro '{}'".format(comparison, expected_value))
                return False
            elif expected_value == "vazio":
                print("\nValor deveria ser diferente de: {}. Valor obtido na consulta: {}".format(expected_value, valor_query_result))
                return valor_query_result != "NULL"
            else:
                expected_value = StringUtils.replace_placeholder_value_with_stored_value(expected_value, Storage.storage)
                print("\nValor deveria ser diferente de: {}. Valor obtido na consulta: {}".format(expected_value, valor_query_result))
                return expected_value != valor_query_result

    def update_database_column_value(database_name, database_table, coluna_update, tipo_coluna_update, campo_coluna_update, valor_update, tipo_valor_update, query_where_column, query_where_column_type, query_where_value, field_name, field_origin):
        
        print("\n #################### Atualizando valor no BD {}, tabela {}, coluna {} #################### \n".format(database_name, database_table, coluna_update))

        DatabaseConnection.obtain_connection(database_name)
        
        query_where_value = Database.obtain_field_value(field_origin, field_name, query_where_value)
        where_field = "'{}'".format(query_where_value) if (query_where_column_type == "uuid" or query_where_column_type == "varchar") else query_where_value
        campo_set = None
        if tipo_coluna_update == "uuid" or tipo_coluna_update == "varchar":
            campo_set = "'{}'".format(valor_update)
        elif tipo_coluna_update == "jsonb":
            valor_campo = "'{}'".format(valor_update) if (tipo_valor_update == "uuid" or tipo_valor_update == "varchar") else valor_update
            campo_set = "jsonb_set(\"" + coluna_update + "\", '{" + campo_coluna_update + "}', '" + valor_campo + "')"
        else:
            campo_set = valor_update
        
        query = "update \"{}\" set \"{}\" = {} where \"{}\" = {}".format(database_table, coluna_update, campo_set, query_where_column, where_field)
        print("\nExecutando a query: {}".format(query))        
        DatabaseConnection.update(database_name, query)
        
        print("\nValor {} atualizado com sucesso na coluna {}!".format(valor_update, coluna_update))

    def execute_database_query(database_name, query, expected_value):
        
        print("\n #################### Executando query arbitrária no BD {} #################### \n".format(database_name))
        
        DatabaseConnection.obtain_connection(database_name)
        query = StringUtils.replace_placeholder_value_with_stored_value(query, Storage.storage)
        print("\nExecutando a query: {}".format(query))        
        
        if not "where" in query:
            print("Only 'where' queries can be executed!")
            return False
        
        if "update" in query or "delete" in query:
            DatabaseConnection.update(database_name, query)
            return True
        else:
            query_result = DatabaseConnection.select_one(database_name, query)
            if expected_value == "omitido":
                return True
            else:
                expected_value = StringUtils.replace_placeholder_value_with_stored_value(expected_value, Storage.storage)
                if(query_result is not None):
                    print("Valor esperado: {}. Valor retornado: {}".format(expected_value, str(query_result[0])))
                    return str(expected_value) == str(query_result[0])
                else:
                    print("Valor esperado: {}. Valor retornado: {}".format(expected_value, str(query_result)))
                    return str(expected_value) == str(query_result)

    def obtain_field_value(field_origin, field_name, valor_campo):

        if (field_origin == "header da resposta"):
            valor_campo = APICalls.api_response.headers[field_name]
        elif (field_origin == "body da resposta"):
            valor_campo = JsonUtils.obtain_value_from_path(APICalls.api_response.json(), field_name)
        
        return valor_campo