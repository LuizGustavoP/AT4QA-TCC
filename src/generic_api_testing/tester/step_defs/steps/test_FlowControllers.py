from pytest_bdd import parsers, given, when, then
from test_classes.FlowControllers import FlowControllers

@given(parsers.cfparse(u'the test waits "{time_in_seconds}" seconds'))
@when(parsers.cfparse(u'the test waits "{time_in_seconds}" seconds'))
@then(parsers.cfparse(u'the test waits "{time_in_seconds}" seconds'))
def wait_seconds(time_in_seconds):
    return FlowControllers.wait_seconds(time_in_seconds)