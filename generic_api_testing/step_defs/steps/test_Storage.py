from pytest_bdd import parsers, given, when, then
from generic_api_testing.test_classes.Storage import Storage
from generic_api_testing.test_classes.APICalls import APICalls

@given(parsers.cfparse(u'o valor do campo "{caminho_campo_api}" vindo do "{origem_campo}" da resposta for armazenado no campo de nome "{storage_field}"'))
@when(parsers.cfparse(u'o valor do campo "{caminho_campo_api}" vindo do "{origem_campo}" da resposta for armazenado no campo de nome "{storage_field}"'))
@then(parsers.cfparse(u'o valor do campo "{caminho_campo_api}" vindo do "{origem_campo}" da resposta for armazenado no campo de nome "{storage_field}"'))
def armazena_campo_resposta_api(caminho_campo_api, origem_campo, storage_field):
    Storage.armazena_campo_resposta_api(caminho_campo_api, origem_campo, storage_field, APICalls.api_response)

@given(parsers.cfparse(u'o valor do campo "{campo_retorno_api}" presente no body da resposta da API em estrutura não ordenada que possui os campo(s) "{campos_relacionados_api}" com valor(es) "{valores_relacionados_api}" for armazenado em campo de nome "{storage_field}"'))
@when(parsers.cfparse(u'o valor do campo "{campo_retorno_api}" presente no body da resposta da API em estrutura não ordenada que possui os campo(s) "{campos_relacionados_api}" com valor(es) "{valores_relacionados_api}" for armazenado em campo de nome "{storage_field}"'))
@then(parsers.cfparse(u'o valor do campo "{campo_retorno_api}" presente no body da resposta da API em estrutura não ordenada que possui os campo(s) "{campos_relacionados_api}" com valor(es) "{valores_relacionados_api}" for armazenado em campo de nome "{storage_field}"'))
def armazena_valores_resposta_da_api_em_campo_nao_ordenado(campo_retorno_api, campos_relacionados_api, valores_relacionados_api, storage_field):
    Storage.armazena_valores_resposta_da_api_em_campo_nao_ordenado(campo_retorno_api, campos_relacionados_api, valores_relacionados_api, storage_field, APICalls.api_response)

@given(parsers.cfparse(u'um valor do banco "{nome_bd}" seja adquirido pela query "{query}" e armazenado num campo de nome "{storage_field}"'))
@when(parsers.cfparse(u'um valor do banco "{nome_bd}" seja adquirido pela query "{query}" e armazenado num campo de nome "{storage_field}"'))
@then(parsers.cfparse(u'um valor do banco "{nome_bd}" seja adquirido pela query "{query}" e armazenado num campo de nome "{storage_field}"'))
def armazena_campo_resposta_banco(nome_bd, query, storage_field):
    Storage.armazena_campo_resposta_banco(nome_bd, query,storage_field)