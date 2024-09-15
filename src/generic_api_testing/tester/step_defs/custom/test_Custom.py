from pytest_bdd import scenarios

pytest_plugins = [
  "step_defs.steps.test_FlowControllers",
  "step_defs.steps.test_Generators", 
  "step_defs.steps.test_Database",
  "step_defs.steps.test_APICalls",
  "step_defs.steps.test_Storage"
]

scenarios("")