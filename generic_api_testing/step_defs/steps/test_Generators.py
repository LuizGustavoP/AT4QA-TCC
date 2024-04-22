from pytest_bdd import parsers, given, when, then
from generic_api_testing.test_classes.Generators import Generators

@given(parsers.cfparse(u'um novo uuid seja gerado e armazenado num campo de nome "{storage_field}"'))
@when(parsers.cfparse(u'um novo uuid seja gerado e armazenado num campo de nome "{storage_field}"'))
@then(parsers.cfparse(u'um novo uuid seja gerado e armazenado num campo de nome "{storage_field}"'))
def generate_uuid(storage_field):
    Generators.generate_uuid(storage_field)

@given(parsers.cfparse(u'um horário "{tempo}" seja gerado no formato "{formato}" e armazenado num campo de nome "{storage_field}"'))
@when(parsers.cfparse(u'um horário "{tempo}" seja gerado no formato "{formato}" e armazenado num campo de nome "{storage_field}"'))
@then(parsers.cfparse(u'um horário "{tempo}" seja gerado no formato "{formato}" e armazenado num campo de nome "{storage_field}"'))
def generate_formatted_time(tempo, formato, storage_field):
    Generators.generate_formatted_time(tempo, formato, storage_field)

@given(parsers.cfparse(u'uma string aleatória de tamanho "{string_size}" seja gerada e armazenada num campo de nome "{storage_field}"'))
@when(parsers.cfparse(u'uma string aleatória de tamanho "{string_size}" seja gerada e armazenada num campo de nome "{storage_field}"'))
@then(parsers.cfparse(u'uma string aleatória de tamanho "{string_size}" seja gerada e armazenada num campo de nome "{storage_field}"'))
def generate_string(string_size, storage_field):
    Generators.generate_string(string_size, storage_field)

@given(parsers.cfparse(u'o valor CRC for computado com o polinômio inicial "{poly}", valor inicial "{init}" e valor XOR "{xorValue}", para o valor armazenado no campo "{campo_valor}", e será armazenado como um hexdigest no campo "{storage_field}"'))
@when(parsers.cfparse(u'o valor CRC for computado com o polinômio inicial "{poly}", valor inicial "{init}" e valor XOR "{xorValue}", para o valor armazenado no campo "{campo_valor}", e será armazenado como um hexdigest no campo "{storage_field}"'))
@then(parsers.cfparse(u'o valor CRC for computado com o polinômio inicial "{poly}", valor inicial "{init}" e valor XOR "{xorValue}", para o valor armazenado no campo "{campo_valor}", e será armazenado como um hexdigest no campo "{storage_field}"'))
def generate_crc(poly, init, xorValue, campo_valor, storage_field):
    Generators.generate_crc(poly, init, xorValue, campo_valor, storage_field)