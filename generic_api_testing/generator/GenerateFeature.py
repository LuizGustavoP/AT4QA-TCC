from TestCase import TestCase
import os

class GenerateFeature:

    def __init__(self, file_name:str):
        self.test_cases = TestCase(file_name)

    def createFeature(self, path:str):
        scenarios = self.test_cases.createScenarios(path)
        feature_name = f"{path}".replace("/","_").replace('{', '').replace('}','')
        file = open(f"{os.path.basename(feature_name)}.feature", "w", encoding="utf-8")
        file.write(f"@{os.path.basename(feature_name)}\nFeature: {os.path.basename(feature_name)}\n\n")    

        for scenario, scenario_values in scenarios.items():
            path_completed = scenario_values['path']
            for param in scenario_values['params']:
                path_completed = scenario_values['path'].replace("{"+param['name']+"}", param['value'])
            file.write(f"\n Scenario Outline: {scenario} {scenario_values['summary']}\n\n")
            examples = []
            examples_sizes = []

            file.write('  When a API com o verbo "<method>" for chamada no endpoint "<path>" com os'
                    ' headers "<headers>", parâmetros "<query>" e payload "<payload>"')
            examples.extend([
                "method",
                "path",
                "headers",
                "query",
                "payload"
            ])
            examples_sizes.extend([
                len(examples[0]) + 2,
                max(len(scenario_values['method']), len(examples[1])),
                max(len(scenario_values['path']),len(examples[2]), len(path_completed)), 
                max(len(self.test_cases.convertToString(scenario_values['headers'],True)), len(examples[3])), 
                max(len(self.test_cases.convertToString(scenario_values['query'], True)), len(examples[4])), 
                max(len(self.test_cases.convertToString(scenario_values['payload'], True)), len(examples[5])),
            ])
            file.write("\n\n  Examples: \n  ")

            for i in range(0, len(examples)):
                file.write(f"|{examples[i].ljust(examples_sizes[i])} ")
            file.write("|\n  ")

            for status_code in scenario_values['status_codes']:
                path = scenario_values['path']
                use_values = False

                if(status_code[0] == '2'):
                    use_values = True
                    path = path_completed

                for i in range(0, len(examples)):
                    if examples[i] in scenario_values.keys():
                        string = ''

                        if examples[i] == 'path':
                            string = path
                        else:
                            string = self.test_cases.convertToString(scenario_values[examples[i]], use_values)
                        string = string
                        file.write(f"|{string.ljust(examples_sizes[i])} ")
                    else:
                        string = "*" + examples[i] + "*"

                        if examples[i] == 'status_code':
                            string = status_code
                        file.write(f"|{string.ljust(examples_sizes[i])} ")
                file.write('|\n  ')
        file.write("\n")
        file.close()