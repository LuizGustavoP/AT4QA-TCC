
import json
import requests
from dateutil.parser import parse
from generic_api_testing.test_classes.Storage import Storage
from generic_api_testing.common.utils.JsonUtils import JsonUtils
from generic_api_testing.common.utils.StringUtils import StringUtils
from generic_api_testing.common.utils.ReportUtils import ReportUtils
from generic_api_testing.common.utils.FieldBuilders import FieldBuilders

class APICalls():

    api_response = None

    def realiza_chamada_de_api(verb, url, headers, params, api_payload):
        
        url = StringUtils.replace_placeholder_value_with_stored_value(url, Storage.storage)
            
        print("\n ================================== {} {}  ================================== ".format(verb, url))
        headers = FieldBuilders.build_json_object(headers, Storage.storage)
        params = FieldBuilders.build_json_object(params, Storage.storage)
        
        json_payload = None
        data_payload = None

        try:
            json.loads(api_payload)
            json_payload = FieldBuilders.build_json_object(api_payload, Storage.storage)
        except ValueError as e:
            data_payload = StringUtils.replace_placeholder_value_with_stored_value(api_payload, Storage.storage)

        if verb == "GET":
            APICalls.api_response = requests.get(url, params=params, headers=headers)
        elif verb == "POST":
            APICalls.api_response = requests.post(url, params=params, headers=headers, data=data_payload, json=json_payload)
        elif verb == "PUT":
            APICalls.api_response = requests.put(url, params=params, headers=headers, data=data_payload, json=json_payload)
        elif verb == "PATCH":
            APICalls.api_response = requests.patch(url, params=params, headers=headers, data=data_payload, json=json_payload)
        elif verb == "DELETE":
            APICalls.api_response = requests.delete(url, params=params, headers=headers, data=data_payload, json=json_payload)

        print("\nRequest Url ({}): {}".format(verb, str(APICalls.api_response.url)))
        print("\nRequest Headers: {}".format(str(headers)))
        
        if json_payload != None :
            print("\nRequest Body: {}".format(str(json.dumps(json_payload))))
        else:
            print("\nRequest Body: {}".format(str(data_payload)))
        print("\nResponse Status: {}".format(str(APICalls.api_response.status_code)))
        print("\nResponse Headers: {}".format(str(APICalls.api_response.headers)))

        if(len(APICalls.api_response.content) > 0):
            print("\nResponse body: {}".format(str(json.dumps(APICalls.api_response.json()))))
        else:
            print("\nResponse body: Não há response!")
        
        return APICalls.api_response

    def checa_status_code_da_api(status_code):
        ReportUtils.print_debug("\n  #################### Checando Status code #################### \n")
        ReportUtils.print_debug(f"Status code retornado = {APICalls.api_response.status_code} Status esperado = {status_code}\n")
        return APICalls.api_response.status_code == int(status_code)

    def checa_valores_resposta_da_api(campos_retorno_api, origem_retorno_api, tipo_comparacao, valores_esperados_retorno_api):

        print("\n #################### Checando valor(es) de resposta da chamada de API #################### \n")

        campos = campos_retorno_api.split("@@")
        valores_esperados = valores_esperados_retorno_api.split("@@")
        print("Checando valor(es) do(s) campo(s): {}".format(campos))
        
        valores_retorno = []
        for campo in campos:    
            if origem_retorno_api == "body":
                valores_retorno.append(JsonUtils.obtain_value_from_path(APICalls.api_response.json(), campo))
            elif origem_retorno_api == "header":
                valores_retorno.append(APICalls.api_response.headers[campo])

        divergencias = []
        for idx, valor_retorno in enumerate(valores_retorno):
            valores_esperados[idx] = StringUtils.replace_placeholder_value_with_stored_value(valores_esperados[idx], Storage.storage)
            if ((tipo_comparacao == "igual" and not str(valor_retorno) == str(valores_esperados[idx])) or 
                (tipo_comparacao == "diferentes" and str(valor_retorno) == str(valores_esperados[idx]))):
                print("Valor esperado como {}: {}. Valor retornado pelo campo {} do {} da resposta: {}".format(tipo_comparacao, valores_esperados[idx], campos[idx], origem_retorno_api, valor_retorno))
                divergencias.append(campos[idx])
            elif((tipo_comparacao == "maior ou igual" or tipo_comparacao == "menor ou igual")):
                try: 
                    valor_esperado_parsed = parse(str(valores_esperados[idx]))
                    valor_retorno_parsed = parse(str(valor_retorno))
                except ValueError:
                    valor_esperado_parsed = str(valores_esperados[idx])
                    valor_retorno_parsed = str(valor_retorno)
                if ((tipo_comparacao == "maior ou igual" and not str(valor_retorno_parsed) >= str(valor_esperado_parsed)) or 
                    (tipo_comparacao == "menor ou igual" and not str(valor_retorno_parsed) <= str(valor_esperado_parsed))):
                    print("Valor esperado como {}: {}. Valor retornado pelo campo {} do {} da resposta: {}".format(tipo_comparacao, valores_esperados[idx], campos[idx], origem_retorno_api, valor_retorno))
                    divergencias.append(campos[idx])
            
                
        if divergencias:
            print("\nO(s) seguinte(s) campo(s) possui(em) valor(es) divergente(s) do esperado: {}".format(divergencias))
            return False
        else:
            print("\nValor(es) da resposta corresponde(m) ao(s) valor(es) esperado(s)")
            return True

    def checa_valores_resposta_da_api_em_campo_nao_ordenado(campo_retorno_api, campos_relacionados_api, valores_relacionados_api, valor_esperado_retorno_api):

        print("\n #################### Checando valor de resposta da chamada de API #################### \n")

        print("\nChecando valor do campo: {}".format(campo_retorno_api))
        print("\nRelativo ao(s) valor(es): {}".format(valores_relacionados_api))
        print("\nRespectivamente relativo(s) ao(s) campo(s): {}".format(campos_relacionados_api))

        valor_retorno = JsonUtils.obtain_value_from_path_unordered(APICalls.api_response.json(), campo_retorno_api, campos_relacionados_api, valores_relacionados_api)

        valor_esperado_retorno_api = StringUtils.replace_placeholder_value_with_stored_value(valor_esperado_retorno_api, Storage.storage)
        if not str(valor_retorno) == str(valor_esperado_retorno_api):
            print("Valor esperado: {}. Valor retornado pelo campo {} do body da resposta: {}".format(valor_esperado_retorno_api, campo_retorno_api, valor_retorno))
            print("\nO seguinte campo possui valor divergente do esperado: {}".format(campo_retorno_api))
            return False
        else:
            print("Valor esperado: {}. Valor retornado pelo campo {} do body da resposta: {}".format(valor_esperado_retorno_api, campo_retorno_api, valor_retorno))
            print("\nValor(es) da resposta corresponde(m) ao(s) valor(es) esperado(s)")
            return True

    def checa_campos_resposta_da_api(campos_retorno_api, situacao_campos, origem_retorno_api):
        
        print("\n #################### Checando campo(s) de resposta da chamada de API #################### \n")
        
        campos = campos_retorno_api.split("@@")
        ausencia_presenca = "presença" if situacao_campos == "presente" or situacao_campos == "presentes" else "ausência"
        print("Checando {} do(s) campo(s): {}".format(ausencia_presenca, campos))
        
        resultado = True
        ausente_presente = "presente" if situacao_campos == "presente" or situacao_campos == "presentes" else "ausente"
        for campo in campos:
            if origem_retorno_api == "body":
                if ausente_presente == "presente" and JsonUtils.obtain_value_from_path(APICalls.api_response.json(), campo) == None:
                    resultado = False
                    print("Campo {} não foi encontrado no body da resposta da API".format(campo))
                elif ausente_presente == "ausente" and JsonUtils.obtain_value_from_path(APICalls.api_response.json(), campo) != None:
                    resultado = False
                    print("Campo {} encontrado no body da resposta da API".format(campo))
            elif origem_retorno_api == "header":
                if ausente_presente == "presente" and not campo in APICalls.api_response.headers:
                    resultado = False
                    print("Campo {} não foi encontrado no header da resposta da API".format(campo))
                elif ausente_presente == "ausente" and campo in APICalls.api_response.headers:
                    resultado = False
                    print("Campo {} encontrado no header da resposta da API".format(campo))
        
        if resultado and ausente_presente == "presente":
            print("\nO(s) campo(s) esperado(s) está(ão) presente(s) no retorno da API")
        elif resultado and ausente_presente == "ausente":
            print("\nO(s) campo(s) informado(s) está(ão) ausente(s) no retorno da API")
        
        return resultado