import os
import argparse
from DictParser import DictParser
from MaskParser import MaskParser

class FeatureTranslator():

  def translateFeature(mask, dictionary=None):

    MaskParser.loadMask(mask)

    if dictionary != None:
      dictionary = dictionary.split(",")
      for dict in dictionary:
        DictParser.loadDictionary(dict)

      for scenario in MaskParser.mask:
        translated_statements = {}
        mask_statements = list(MaskParser.mask[scenario]["statements"].keys())
        for mask_statement in mask_statements:
          translated_statement = {}
          translated_statement[mask_statement] = MaskParser.mask[scenario]["statements"][mask_statement]
          translated_statement = DictParser.translateStatement(translated_statement, MaskParser.mask[scenario]["examples_amount"])
          del MaskParser.mask[scenario]["statements"][mask_statement]
          for statement in translated_statement.keys():
            translated_statements[statement] = translated_statement[statement]
        MaskParser.mask[scenario]["statements"] = translated_statements

    FeatureTranslator.writeFeature(mask.replace(".mask", ""))

  def writeFeature(feature_name):

    file = open(f"features/{os.path.basename(feature_name)}Translated.feature", "w", encoding="utf-8")

    file.write(f"@{os.path.basename(feature_name)}\nFeature: {os.path.basename(feature_name)}\n\n")

    for scenario in MaskParser.mask.keys():
      tags = MaskParser.mask[scenario]["tags"]
      file.write(f"  {tags}\n  Scenario Outline: {scenario}\n\n")
      
      scenario_params = []
      scenario_values = []
      for statement in MaskParser.mask[scenario]["statements"].keys():

        for param in MaskParser.mask[scenario]["statements"][statement]["params"].keys():
          if param not in scenario_params:
            scenario_params += [param]
            scenario_values += [MaskParser.mask[scenario]["statements"][statement]["params"][param][0]]
        
        for value in MaskParser.mask[scenario]["statements"][statement]["inline_values"]:
          statement = statement.replace(f"<{value[0]}={value[1]}>", f"\"<{value[0]}>\"")
          if value[0] not in scenario_params:
            scenario_params += [value[0]]
            scenario_values += [[bytes(value[1], "utf-8").decode("unicode_escape")]*MaskParser.mask[scenario]["examples_amount"]]

        file.write(f"    {statement}\n")

      file.write("\n    Examples: \n")
      param_string = "| " 
      values_strings = ["| "]* MaskParser.mask[scenario]["examples_amount"]

      for param_index in range(len(scenario_params)):
        
        if len(scenario_params[param_index]) > len(max(scenario_values[param_index], key=len)):
          param_string += f"{str(scenario_params[param_index])} | "
          for example in range(MaskParser.mask[scenario]["examples_amount"]):
            values_strings[example] += f"{str(scenario_values[param_index][example]).ljust(len(str(scenario_params[param_index])))} | "

        elif len(scenario_params[param_index]) < len(max(scenario_values[param_index], key=len)):
          param_string += f"{str(scenario_params[param_index]).ljust(len(max(scenario_values[param_index], key=len)))} | "
          for example in range(MaskParser.mask[scenario]["examples_amount"]):
            if(scenario_values[param_index][example] != max(scenario_values[param_index], key=len)):
              values_strings[example] += f"{str(scenario_values[param_index][example]).ljust(len(max(scenario_values[param_index], key=len)))} | "
            else:
              values_strings[example] += f"{str(scenario_values[param_index][example])} | "

        else: 
          param_string += f"{str(scenario_params[param_index])} | "
          for example in range(MaskParser.mask[scenario]["examples_amount"]):
            values_strings[example] += f"{str(scenario_values[param_index][example]).ljust(len(scenario_params[param_index]))} | "
        
      file.write(f"      {param_string}\n")
      for example in values_strings:
        file.write(f"      {example}\n")
      file.write("\n")
    file.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mask")
    parser.add_argument("dictionary", nargs='?', default=None)
    args = parser.parse_args()
    print(args)
    FeatureTranslator.translateFeature(args.mask, args.dictionary)
if __name__ == '__main__':
    main()