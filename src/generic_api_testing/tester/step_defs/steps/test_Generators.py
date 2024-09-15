from pytest_bdd import parsers, given, when, then
from test_classes.Generators import Generators

@given(parsers.cfparse(u'a new uuid will be generated and stored in the field named "{storage_field}"'))
@when(parsers.cfparse(u'a new uuid will be generated and stored in the field named "{storage_field}"'))
@then(parsers.cfparse(u'a new uuid will be generated and stored in the field named "{storage_field}"'))
def generate_uuid(storage_field):
    Generators.generate_uuid(storage_field)

@given(parsers.cfparse(u'a time "{time}" will be generated in the format "{format}" and stored in a field named "{storage_field}"'))
@when(parsers.cfparse(u'a time "{time}" will be generated in the format "{format}" and stored in a field named "{storage_field}"'))
@then(parsers.cfparse(u'a time "{time}" will be generated in the format "{format}" and stored in a field named "{storage_field}"'))
def generate_formatted_time(time, format, storage_field):
    Generators.generate_formatted_time(time, format, storage_field)

@given(parsers.cfparse(u'a random string of size "{string_size}" will be generated and stored in a field named "{storage_field}"'))
@when(parsers.cfparse(u'a random string of size "{string_size}" will be generated and stored in a field named "{storage_field}"'))
@then(parsers.cfparse(u'a random string of size "{string_size}" will be generated and stored in a field named "{storage_field}"'))
def generate_string(string_size, storage_field):
    Generators.generate_string(string_size, storage_field)

@given(parsers.cfparse(u'a CRC value is calculated with the polynomial "{poly}", initial value "{init}" e XOR value "{xorValue}", for the value stored in the field "{value_field}", and will be stored as a hexdigest in the field "{storage_field}"'))
@when(parsers.cfparse(u'a CRC value is calculated with the polynomial "{poly}", initial value "{init}" e XOR value "{xorValue}", for the value stored in the field "{value_field}", and will be stored as a hexdigest in the field "{storage_field}"'))
@then(parsers.cfparse(u'a CRC value is calculated with the polynomial "{poly}", initial value "{init}" e XOR value "{xorValue}", for the value stored in the field "{value_field}", and will be stored as a hexdigest in the field "{storage_field}"'))
def generate_crc(poly, init, xorValue, value_field, storage_field):
    Generators.generate_crc(poly, init, xorValue, value_field, storage_field)