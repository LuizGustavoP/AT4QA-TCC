import re
import copy

class DictParser():
  
  dictionaries = {}
  
  def loadDictionary(files):
    
    files = files.split(",")
    for file in files:
      DictParser.dictionaries[file] = {}

      dict = open("translator/dictionaries/" + file, encoding="utf-8")
      lines = dict.readlines()
      statement = ""
      equivalent_statements = -1
      gathering_params = -1

      for line in lines:

        phrase = line.strip()
        if(phrase):

          if(phrase.startswith("Statement:")):
            statement = phrase[10:].strip()
            DictParser.dictionaries[file][statement] = {}
            DictParser.dictionaries[file][statement]["equivalent_statements"] = {}
            DictParser.dictionaries[file][statement]["params"] = []

            params = DictParser.extractParams(statement)
            for param in params:
              DictParser.dictionaries[file][statement]["params"] = DictParser.dictionaries[file][statement]["params"] + [param]
            equivalent_statements = 0
          
          elif((not phrase.startswith("Statement Params:")) and equivalent_statements >=0):
            DictParser.dictionaries[file][statement]["equivalent_statements"][phrase] = {}
            DictParser.dictionaries[file][statement]["equivalent_statements"][phrase]["params"] = {}
            params = DictParser.extractParams(phrase)
            for param in params:
              DictParser.dictionaries[file][statement]["equivalent_statements"][phrase]["params"][param] = ""
            equivalent_statements += 1
            
          elif(phrase.startswith("Statement Params:") and equivalent_statements > 0):
            equivalent_statements = -1
            gathering_params = 0

          elif(phrase.startswith("|") and gathering_params == 0):
            if(phrase.endswith("|")):
              generic_params = [ param.strip() for param in phrase[1:len(phrase)-1].split("|")]
              gathering_params = 1
            else:
              print("Parâmetros mal formatados! Quantidade de '|' incorreta!")
              print(statement)
              return

          elif(phrase.startswith("|") and gathering_params == 1):
            if(phrase.endswith("|")):
              generic_values = [ values.strip() for values in phrase[1:len(phrase)-1].split("|")]
              if(len(generic_params) != len(generic_values)):
                print("Quantidade de parâmetros não bate com a de valores!")
                print(statement)
                print(generic_params)
                print(generic_values)
                return
              
              for value in range(len(generic_values)):
                for param in DictParser.dictionaries[file][statement]["equivalent_statements"].keys():
                    if generic_params[value] in DictParser.dictionaries[file][statement]["equivalent_statements"][param]["params"].keys():
                      DictParser.dictionaries[file][statement]["equivalent_statements"][param]["params"][generic_params[value]] = generic_values[value]
            else:
              print("Valores mal formatados! Quantidade de '|' incorreta!")
              print(statement)
              return

          elif(phrase.startswith("Statement Params:") and equivalent_statements <= 0):
            print("Dicionário mal formatado! Statement customizado sem equivalentes genéricos:")
            print(statement +'\n')

  def translateStatement(mask_statement, examples_amount):
    
    translated_statement = {}
    clean_mask_statement = list(mask_statement.keys())[0].replace('"', '')
    clean_mask_statement = re.sub('<[^>]+>', '', clean_mask_statement)
    statement_type = clean_mask_statement[:clean_mask_statement.find(" ")+1]
    clean_mask_statement = clean_mask_statement[clean_mask_statement.find(" ")+1:]

    for dict in DictParser.dictionaries:
      for statement in DictParser.dictionaries[dict].keys():
        
        clean_statement = statement.replace('"', '')
        clean_statement = re.sub('<[^>]+>', '', clean_statement)

        if clean_statement == clean_mask_statement:

          translated_statement = copy.deepcopy(DictParser.dictionaries[dict][statement]["equivalent_statements"])
          
          for equivalent_statement in translated_statement.keys():
            
            param_names = DictParser.extractValues(statement)
            translated_statement[equivalent_statement]["inline_values"] = []

            for param in translated_statement[equivalent_statement]["params"].keys():

              translated_statement[equivalent_statement]["params"][param] = [[translated_statement[equivalent_statement]["params"][param]] * examples_amount, 0]
              
              for example in range(examples_amount):
                for param_index in range(len(param_names)):
                  
                  if f"@{param_names[param_index]}@" in translated_statement[equivalent_statement]["params"][param][0][example]:
                    
                    for value in mask_statement[list(mask_statement.keys())[0]]["inline_values"]:
                      
                      if(value[2] == param_index): 
                        translated_statement[equivalent_statement]["params"][param][0][example] = translated_statement[equivalent_statement]["params"][param][0][example].replace(f"@{param_names[param_index]}@", value[1])
                        break
                    
                    for param_value in mask_statement[list(mask_statement.keys())[0]]["params"]:
                      if(mask_statement[list(mask_statement.keys())[0]]["params"][param_value][1] == param_index):
                        translated_statement[equivalent_statement]["params"][param][0][example] = translated_statement[equivalent_statement]["params"][param][0][example].replace(f"@{param_names[param_index]}@", mask_statement[list(mask_statement.keys())[0]]["params"][param_value][0][example])
            
          translation = {}
          for statement in translated_statement.keys():
            translation[statement_type+statement] = translated_statement[statement]
          return translation

    return mask_statement

  def extractParams(statement):
    params = re.findall(r'"<([^"]*)>"', statement)
    return params
  
  def extractValues(statement):
    values = re.findall(r'<([^"]*)>', statement)
    return values