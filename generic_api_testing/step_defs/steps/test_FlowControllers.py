from pytest_bdd import parsers, given, when, then
from generic_api_testing.test_classes.FlowControllers import FlowControllers

@given(parsers.cfparse(u'o teste esperar "{espera_em_segundos}" segundos'))
@when(parsers.cfparse(u'o teste esperar "{espera_em_segundos}" segundos'))
@then(parsers.cfparse(u'o teste esperar "{espera_em_segundos}" segundos'))
def wait_seconds(espera_em_segundos):
    return FlowControllers.wait_seconds(espera_em_segundos)