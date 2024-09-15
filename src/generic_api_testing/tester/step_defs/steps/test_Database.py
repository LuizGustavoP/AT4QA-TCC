from pytest_bdd import parsers, given, when, then
from test_classes.Database import Database

@given(parsers.cfparse(u'a database connection named "{name}" with host "{host}", port "{port}", user "{user}", password "{password}" and database "{database}" is defined'))
@when(parsers.cfparse(u'a database connection named "{name}" with host "{host}", port "{port}", user "{user}", password "{password}" and database "{database}" is defined'))
@then(parsers.cfparse(u'a database connection named "{name}" with host "{host}", port "{port}", user "{user}", password "{password}" and database "{database}" is defined'))
def define_database_connection(name, host, port, user, password, database):
    Database.define_database_connection(name, host, port, user, password, database)

@given(parsers.cfparse(u'on database "{database_name}" on table "{database_table}" the column "{database_expected_column}" must contain the value "{equals_or_differs}" "{expected_value}", in the row where the column "{database_column_where}" of type "{database_column_where_type}" has the value "{where_value}" from the field "{field_name}" originated from "{field_origin}"'))
@when(parsers.cfparse(u'on database "{database_name}" on table "{database_table}" the column "{database_expected_column}" must contain the value "{equals_or_differs}" "{expected_value}", in the row where the column "{database_column_where}" of type "{database_column_where_type}" has the value "{where_value}" from the field "{field_name}" originated from "{field_origin}"'))
@then(parsers.cfparse(u'on database "{database_name}" on table "{database_table}" the column "{database_expected_column}" must contain the value "{equals_or_differs}" "{expected_value}", in the row where the column "{database_column_where}" of type "{database_column_where_type}" has the value "{where_value}" from the field "{field_name}" originated from "{field_origin}"'))
def check_database_column_value(database_name, database_table, database_expected_column, equals_or_differs, expected_value, database_column_where, database_column_where_type, where_value, field_name, field_origin):
    assert Database.check_database_column_value(database_name, database_table, database_expected_column, equals_or_differs, expected_value, database_column_where, database_column_where_type, where_value, field_name, field_origin)
    
@given(parsers.cfparse(u'on database "{database_name}" on table "{database_table}" the column "{update_column}" of type "{update_column_type}" must update the value of field "{update_field_column}" to the value "{update_value}" of type "{update_value_type}", in the row where the column "{database_column_where}" of type "{database_column_where_type}" has the value "{where_value}" from the field "{field_name}" originated from "{field_origin}"'))
@when(parsers.cfparse(u'on database "{database_name}" on table "{database_table}" the column "{update_column}" of type "{update_column_type}" must update the value of field "{update_field_column}" to the value "{update_value}" of type "{update_value_type}", in the row where the column "{database_column_where}" of type "{database_column_where_type}" has the value "{where_value}" from the field "{field_name}" originated from "{field_origin}"'))
@then(parsers.cfparse(u'on database "{database_name}" on table "{database_table}" the column "{update_column}" of type "{update_column_type}" must update the value of field "{update_field_column}" to the value "{update_value}" of type "{update_value_type}", in the row where the column "{database_column_where}" of type "{database_column_where_type}" has the value "{where_value}" from the field "{field_name}" originated from "{field_origin}"'))
def update_database_column_value(database_name, database_table, update_column, update_column_type, update_field_column, update_value, update_value_type, database_column_where, database_column_where_type, where_value, field_name, field_origin):
    Database.update_database_column_value(database_name, database_table, update_column, update_column_type, update_field_column, update_value, update_value_type, database_column_where, database_column_where_type, where_value, field_name, field_origin)

@given(parsers.cfparse(u'on database "{database_name}" run query "{query}" whose expected returned value must be equal to "{expected_value}"'))
@when(parsers.cfparse(u'on database "{database_name}" run query "{query}" whose expected returned value must be equal to "{expected_value}"'))
@then(parsers.cfparse(u'on database "{database_name}" run query "{query}" whose expected returned value must be equal to "{expected_value}"'))
def execute_database_query(database_name, query, expected_value):
    assert Database.execute_database_query(database_name, query, expected_value)