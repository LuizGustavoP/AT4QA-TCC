from pytest_bdd import parsers, given, when, then
from test_classes.Storage import Storage
from test_classes.APICalls import APICalls

@given(parsers.cfparse(u'the value of field "{api_field}" from "{field_origin}" of the response will be stored on field named "{storage_field}"'))
@when(parsers.cfparse(u'the value of field "{api_field}" from "{field_origin}" of the response will be stored on field named "{storage_field}"'))
@then(parsers.cfparse(u'the value of field "{api_field}" from "{field_origin}" of the response will be stored on field named "{storage_field}"'))
def store_api_response(api_field, field_origin, storage_field):
    Storage.store_api_response(api_field, field_origin, storage_field, APICalls.api_response)

@given(parsers.cfparse(u'the value of field "{api_returned_field}" present in the API body response related to the field(s) "{api_related_fields}" with value(s) "{api_related_values}" stored in field named "{storage_field}"'))
@when(parsers.cfparse(u'the value of field "{api_returned_field}" present in the API body response related to the field(s) "{api_related_fields}" with value(s) "{api_related_values}" stored in field named "{storage_field}"'))
@then(parsers.cfparse(u'the value of field "{api_returned_field}" present in the API body response related to the field(s) "{api_related_fields}" with value(s) "{api_related_values}" stored in field named "{storage_field}"'))
def store_api_response_in_unordered_field(api_returned_field, api_related_fields, api_related_values, storage_field):
    Storage.store_api_response_in_unordered_field(api_returned_field, api_related_fields, api_related_values, storage_field, APICalls.api_response)

@given(parsers.cfparse(u'a value of database "{database_name}" is adquired by the query "{query}" and stored in field named "{storage_field}"'))
@when(parsers.cfparse(u'a value of database "{database_name}" is adquired by the query "{query}" and stored in field named "{storage_field}"'))
@then(parsers.cfparse(u'a value of database "{database_name}" is adquired by the query "{query}" and stored in field named "{storage_field}"'))
def store_response_field_database(nome_bd, query, storage_field):
    Storage.store_response_field_database(nome_bd, query,storage_field)