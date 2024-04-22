from pytest_bdd import parsers, given, when, then
from generic_api_testing.test_classes.APICalls import APICalls

@given(parsers.cfparse(u'a API com o verbo "{verbo}" for chamada no endpoint "{caminho}" com os headers "{headers}", parâmetros "{params}" e payload "{payload_api}"'))    
@when(parsers.cfparse(u'a API com o verbo "{verbo}" for chamada no endpoint "{caminho}" com os headers "{headers}", parâmetros "{params}" e payload "{payload_api}"'))
@then(parsers.cfparse(u'a API com o verbo "{verbo}" for chamada no endpoint "{caminho}" com os headers "{headers}", parâmetros "{params}" e payload "{payload_api}"'))
def realiza_chamada_de_api(verbo, caminho, headers, params, payload_api):
    return APICalls.realiza_chamada_de_api(verbo, caminho, headers, params, payload_api)

@given(parsers.cfparse(u'a API retornará "{status_code}"'))
@when(parsers.cfparse(u'a API retornará "{status_code}"'))
@then(parsers.cfparse(u'a API retornará "{status_code}"'))
def checa_status_code_da_api(status_code):
    assert APICalls.checa_status_code_da_api(status_code)

@given(parsers.cfparse(u'o valor do(s) campo(s) "{campos_retorno_api}" presente(s) no "{origem_retorno_api}" da resposta da API possui(em) respectivamente valor(es) "{tipo_comparacao}" a "{valores_esperados_retorno_api}"'))
@when(parsers.cfparse(u'o valor do(s) campo(s) "{campos_retorno_api}" presente(s) no "{origem_retorno_api}" da resposta da API possui(em) respectivamente valor(es) "{tipo_comparacao}" a "{valores_esperados_retorno_api}"'))
@then(parsers.cfparse(u'o valor do(s) campo(s) "{campos_retorno_api}" presente(s) no "{origem_retorno_api}" da resposta da API possui(em) respectivamente valor(es) "{tipo_comparacao}" a "{valores_esperados_retorno_api}"'))
def checa_valores_resposta_da_api(campos_retorno_api, origem_retorno_api, tipo_comparacao, valores_esperados_retorno_api):
    assert APICalls.checa_valores_resposta_da_api(campos_retorno_api, origem_retorno_api, tipo_comparacao, valores_esperados_retorno_api)

@given(parsers.cfparse(u'o valor do campo "{campo_retorno_api}" presente no body da resposta da API em estrutura não ordenada que possui os campo(s) "{campos_relacionados_api}" com valor(es) "{valores_relacionados_api}" possui valor igual a "{valor_esperado_retorno_api}"'))
@when(parsers.cfparse(u'o valor do campo "{campo_retorno_api}" presente no body da resposta da API em estrutura não ordenada que possui os campo(s) "{campos_relacionados_api}" com valor(es) "{valores_relacionados_api}" possui valor igual a "{valor_esperado_retorno_api}"'))
@then(parsers.cfparse(u'o valor do campo "{campo_retorno_api}" presente no body da resposta da API em estrutura não ordenada que possui os campo(s) "{campos_relacionados_api}" com valor(es) "{valores_relacionados_api}" possui valor igual a "{valor_esperado_retorno_api}"'))
def checa_valores_resposta_da_api_em_campo_nao_ordenado(campo_retorno_api, campos_relacionados_api, valores_relacionados_api, valor_esperado_retorno_api):
    assert APICalls.checa_valores_resposta_da_api_em_campo_nao_ordenado(campo_retorno_api, campos_relacionados_api, valores_relacionados_api, valor_esperado_retorno_api)

@given(parsers.cfparse(u'o(s) campo(s) "{campos_retorno_api}" está(ão) "{situacao_campos}" no "{origem_retorno_api}" da resposta da API'))
@when(parsers.cfparse(u'o(s) campo(s) "{campos_retorno_api}" está(ão) "{situacao_campos}" no "{origem_retorno_api}" da resposta da API'))
@then(parsers.cfparse(u'o(s) campo(s) "{campos_retorno_api}" está(ão) "{situacao_campos}" no "{origem_retorno_api}" da resposta da API'))
def checa_campos_resposta_da_api(campos_retorno_api, situacao_campos, origem_retorno_api):
    assert APICalls.checa_campos_resposta_da_api(campos_retorno_api, situacao_campos, origem_retorno_api)