from pytest_bdd import scenarios

pytest_plugins = [
  "generic_api_testing.step_defs.steps.test_FlowControllers",
  "generic_api_testing.step_defs.steps.test_Generators", 
  "generic_api_testing.step_defs.steps.test_Database",
  "generic_api_testing.step_defs.steps.test_APICalls",
  "generic_api_testing.step_defs.steps.test_Storage"
]

scenarios("")