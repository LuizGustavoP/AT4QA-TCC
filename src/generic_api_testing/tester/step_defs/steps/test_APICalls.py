from pytest_bdd import parsers, given, when, then
from test_classes.APICalls import APICalls

@given(parsers.cfparse(u'the API with method "{method}" is called on the endpoint "{url}" with headers "{headers}", parameters "{params}" and payload "{payload_api}"'))
@when(parsers.cfparse(u'the API with method "{method}" is called on the endpoint "{url}" with headers "{headers}", parameters "{params}" and payload "{payload_api}"'))
@then(parsers.cfparse(u'the API with method "{method}" is called on the endpoint "{url}" with headers "{headers}", parameters "{params}" and payload "{payload_api}"'))
def makes_api_call(method, url, headers, params, payload_api):
    return APICalls.makes_api_call(method, url, headers, params, payload_api)

@given(parsers.cfparse(u'the API will return "{status_code}"'))
@when(parsers.cfparse(u'the API will return "{status_code}"'))
@then(parsers.cfparse(u'the API will return "{status_code}"'))
def check_api_status_code(status_code):
    assert APICalls.check_api_status_code(status_code)

@given(parsers.cfparse(u'the value of the field(s) "{api_returned_field}" present in "{api_return_origin}" of the API response has the value(s) "{comparison_type}" to "{api_response_expected_values}" respectively'))
@when(parsers.cfparse(u'the value of the field(s) "{api_returned_field}" present in "{api_return_origin}" of the API response has the value(s) "{comparison_type}" to "{api_response_expected_values}" respectively'))
@then(parsers.cfparse(u'the value of the field(s) "{api_returned_field}" present in "{api_return_origin}" of the API response has the value(s) "{comparison_type}" to "{api_response_expected_values}" respectively'))
def check_api_response_values(api_returned_field, api_return_origin, comparison_type, api_response_expected_values):
    assert APICalls.check_api_response_values(api_returned_field, api_return_origin, comparison_type, api_response_expected_values)

@given(parsers.cfparse(u'the value of field "{api_returned_field}" located on the body of the API response in an unordered structure that has the field(s) "{api_related_fields}" with value(s) "{api_related_values}" has value equal to "{api_returned_expected_values}"'))
@when(parsers.cfparse(u'the value of field "{api_returned_field}" located on the body of the API response in an unordered structure that has the field(s) "{api_related_fields}" with value(s) "{api_related_values}" has value equal to "{api_returned_expected_values}"'))
@then(parsers.cfparse(u'the value of field "{api_returned_field}" located on the body of the API response in an unordered structure that has the field(s) "{api_related_fields}" with value(s) "{api_related_values}" has value equal to "{api_returned_expected_values}"'))
def check_api_response_values_in_unordered_fields(api_returned_field, api_related_fields, api_related_values, api_returned_expected_values):
    assert APICalls.check_api_response_values_in_unordered_fields(api_returned_field, api_related_fields, api_related_values, api_returned_expected_values)

@given(parsers.cfparse(u'the field(s) "{api_returned_field}" is(are) "{field_situation}" in the "{api_return_origin}" of the API response'))
@when(parsers.cfparse(u'the field(s) "{api_returned_field}" is(are) "{field_situation}" in the "{api_return_origin}" of the API response'))
@then(parsers.cfparse(u'the field(s) "{api_returned_field}" is(are) "{field_situation}" in the "{api_return_origin}" of the API response'))
def check_api_response_fields(api_returned_field, field_situation, api_return_origin):
    assert APICalls.check_api_response_fields(api_returned_field, field_situation, api_return_origin)