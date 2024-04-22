import pytest
from generic_api_testing.common.config.config import GeneralSettings
from generic_api_testing.common.config.database.DatabaseConnection import DatabaseConnection

def pytest_addoption(parser):
    
    parser.addoption(
        "--v",
        action="store_true",
        default=False,
    )

@pytest.fixture
def debug(request):
    return request.config.getoption("--v")

@pytest.fixture(scope='session', autouse=True)
def close_db():
    yield
    if DatabaseConnection.connections:
        for k in DatabaseConnection.connections:
            DatabaseConnection.connections[k]['cur'].close()
            DatabaseConnection.connections[k]['con'].close()
            print("Conexão ao banco de dados " + k + " fechada!")

def pytest_configure(config):
    GeneralSettings.debug = config.getoption('--v')

@pytest.hookimpl(tryfirst=True) 
def pytest_sessionfinish(session):
    html_report = getattr(session.config, "template_context", None)

    for item in html_report['tests']:
        full_name_function = item['item'].function.__doc__
        item['item'].variables = {}
        for _, values in item['item'].callspec.params.items():
            item['item'].variables.update(values)

        full_path = full_name_function.split(".feature")
        path_split = '/ ' if full_path[0].find('/') != -1 else '\\'
        file_name = full_path[0].split(path_split)[-1]
        item['item'].name_file = file_name

        if item['phases'][1]['report'].outcome == 'failed':
            error_type = item['phases'][1]['report'].longreprtext.split("\n")[-1]
            error_why = "No logs"

            if len(item['phases'][1]['report'].sections) > 0 :
                errors_out = item['phases'][1]['report'].sections[0][1].split("\n")
                errors_out.reverse()
                for er in errors_out:
                    if er != '':
                        error_why = er
                        break
            new_sections = ("Error", f"Error:{error_type}\n\Last Log: {error_why}")
            
            #Create new section
            test_report = pytest.TestReport(
                nodeid=item['phases'][1]['report'].nodeid,
                location=item['phases'][1]['report'].location,
                keywords=item['phases'][1]['report'].keywords,
                outcome='failed',
                longrepr=None,
                when='Error',
                sections=[new_sections],
                user_properties=item['phases'][1]['report'].user_properties,
                duration=0.00001
            )
            item['phases'].insert(0, {'report':test_report, 'sections': [new_sections]})

