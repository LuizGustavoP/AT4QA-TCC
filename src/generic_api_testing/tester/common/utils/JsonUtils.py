import re

class JsonUtils():
    
    re_table_name_json_path = r'(.*)->(.*)'
    re_json_field_index = r'(.+?)\[(\d+)\]'
    
    # Dado um caminho em formato string retorna o valor do campo do json passado como parâmetro
    def obtain_value_from_path(json, caminho):
        
        keys = caminho.split('.')
        keys = [k.replace('[', '.').replace(']', '') for k in keys]
        
        valor = json
        for key in keys:
            if '.' in key:
                field_idx = key.split('.')
                valor = valor.get(field_idx[0])[int(field_idx[1])]
            elif valor != None:
                valor = valor.get(key)
        
        return valor if valor != json else None
    
    # Dado um caminho em formato string retorna o valor do campo do json passado como parâmetro para casos em que o campo se localiza em um array não ordenado
    def obtain_value_from_path_unordered(json, caminho_retorno, campos_relacionado, valores_relacionado):
        
        keys = caminho_retorno.split('.')
        relKeys = campos_relacionado.split('@@')
        relValues = valores_relacionado.split('@@')

        if(len(relKeys) != len (relValues)):
            print("\nA quantidade de campos relativos não é igual a quantidade de valores relativos passados!")
            return None
        
        rel_idx = 0
        valor = json

        for key in keys:
            if '[?]' in key:
                field = key[:-3]
                valor = valor.get(field)
                relIdKeys = relKeys[rel_idx].split('&&&')
                relIdValues = relValues[rel_idx].split('&&&')

                matches = 0
                for item in valor:

                    for idx, subKey in enumerate(relIdKeys):

                        if item[subKey] != relIdValues[idx]: break
                        else: matches+=1

                    if(matches == len(relIdKeys)):
                        valor = item
                        break
                    else: matches = 0
                
                if(matches == 0):
                    print("\nNão foi encontrado valor que condiz com as chaves {}.".format(relIdKeys))
                    return None
                
                if(rel_idx+1 < len(relKeys)):
                    rel_idx+=1

            elif valor != None:
                valor = valor.get(key)
        
        return valor if valor != json else None

    # Dada uma string que contém o nome da coluna e o caminho do campo JSON desejado retorna a anotação correspondente para uso na query postgres
    def format_select_query_column(coluna_esperada_bd):
        if "->" not in coluna_esperada_bd:
            return coluna_esperada_bd
        
        matches = re.match(JsonUtils.re_table_name_json_path, coluna_esperada_bd)
        tabela = matches.group(1)
        caminho_json = matches.group(2)
        campos_json = caminho_json.split(".")
        
        select = tabela
        for campo in campos_json:
            if "[" in campo:
                matches = re.match(JsonUtils.re_json_field_index, campo)
                select += "->'{}'->{}".format(matches.group(1), matches.group(2))
            else:
                select += "->'{}'".format(campo)
        
        return select