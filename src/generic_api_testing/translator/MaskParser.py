import re

class MaskParser():

  mask = {}
  
  def loadMask(file):

    mask = open("translator/masks/" + file, "r", encoding="utf-8")
    lines = mask.readlines()

    scenario = ""
    mask_statements = -1
    gathering_params = -1
    current_scenario_tags = ""

    for line in lines:

      phrase = line.strip()

      if(phrase):

        if(phrase.startswith("@")):
          current_scenario_tags = phrase
        elif(phrase.startswith("Scenario Mask:")):

          scenario = phrase[14:].strip()

          MaskParser.mask[scenario] = {}
          MaskParser.mask[scenario]["statements"] = {}
          MaskParser.mask[scenario]["examples_amount"] = 0
          MaskParser.mask[scenario]["tags"] = current_scenario_tags
          current_scenario_tags = ""

          mask_statements = 0
          gathering_params = -1

        elif((not phrase.startswith("Examples:")) and mask_statements >=0):

          MaskParser.mask[scenario]["statements"][phrase] = {}
          MaskParser.mask[scenario]["statements"][phrase]["params"] = {}
          MaskParser.mask[scenario]["statements"][phrase]["inline_values"] = {}
          params, values = MaskParser.extractParamsAndValues(phrase)

          for param in params:
            MaskParser.mask[scenario]["statements"][phrase]["params"][param[0]] = [[], param[1]]

          MaskParser.mask[scenario]["statements"][phrase]["inline_values"] = []
          for value in values:
            inlineValue = [value[0][:value[0].find("=")], value[0][value[0].find("=")+1:], value[1]]
            MaskParser.mask[scenario]["statements"][phrase]["inline_values"].append(inlineValue)

          mask_statements += 1
          
        elif(phrase.startswith("Examples:") and mask_statements > 0):
          mask_statements = -1
          gathering_params = 0

        elif(phrase.startswith("|") and gathering_params == 0):

          if(phrase.endswith("|")):

            generic_params = [ param.strip() for param in phrase[1:len(phrase)-1].split("|")]
            gathering_params = 1

          else:
            print("Parâmetros mal formatados! Quantidade de '|' incorreta!")
            print(scenario)
            return
          
        elif(phrase.startswith("|") and gathering_params == 1):

          if(phrase.endswith("|")):

            generic_values = [ example_values.strip() for example_values in phrase[1:len(phrase)-1].split("|")]
            MaskParser.mask[scenario]["examples_amount"] += 1

            if(len(generic_params) != len(generic_values)):
              print("Quantidade de parâmetros não bate com a de valores!")
              print(scenario)
              print(generic_params)
              print(generic_values)
              return
            
            for value_index in range(len(generic_values)):
              for current_statement in MaskParser.mask[scenario]["statements"].keys():
                  if generic_params[value_index] in MaskParser.mask[scenario]["statements"][current_statement]["params"].keys():
                    MaskParser.mask[scenario]["statements"][current_statement]["params"][generic_params[value_index]][0] += [generic_values[value_index]]

          else:
            print("Valores mal formatados! Quantidade de '|' incorreta!")
            print(scenario)
            return
          
        elif(phrase.startswith("Examples:") and mask_statements <= 0):
          print("Feature Mask mal formatada! Statement customizado sem equivalentes genéricos:")
          print(scenario +'\n')

  def extractParamsAndValues(statement):

    params = re.findall( r'"<(.*?)>"', statement)
    values = re.findall(r'<([^<>]+)>', statement)
    indexed_values = []
    indexed_params = []

    for index in range(len(values)):
      if values[index] not in params:
        indexed_values += [[values[index], index]]
      else:
        indexed_params += [[values[index], index]]

    return indexed_params, indexed_values