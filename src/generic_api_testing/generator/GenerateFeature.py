from TestCase import TestCase
import argparse
import os

class GenerateFeature:

    def __init__(self, file_name:str):
        self.test_cases = TestCase(file_name)

    def createName(self, path:str) -> str:
        feature_name = f"{path}".replace('{', '').replace('}','')

        delimiters = ["/", "-",]

        for delimiter in delimiters:
            feature_name = " ".join(feature_name.split(delimiter))
        feature_names = feature_name.split()
        feature_name = ''
        for name in feature_names:
            feature_name += name.capitalize()

        return feature_name
    
    def createMultiFeatures(self, paths =[]):
        if paths == []:
            paths = self.test_cases.paths
        
        for path in paths:
            self.createFeature(path)

    def createFeature(self, path:str):
        scenarios = self.test_cases.createScenarios(path)
        feature_name = self.createName(path)

        file = open(f"features/{os.path.basename(feature_name)}.feature", "w", encoding="utf-8")
        file.write(f"@{os.path.basename(feature_name)}\nFeature: {os.path.basename(feature_name)}\n\n")    

        size_scenarios = len(scenarios.items())

        for scenario, scenario_values in scenarios.items():
            path_completed = scenario_values['path']
            for param in scenario_values['params']:
                path_completed = scenario_values['path'].replace("{"+param['name']+"}", param['value'])
            if size_scenarios <=1 and scenario_values['summary'] != '':
                scenario = ''
            file.write(f"\n  Scenario Outline: {scenario} {scenario_values['summary']}\n\n")
            examples = []
            examples_sizes = []

            file.write('    When the API with method "<method>" is called on the endpoint "<url>"'
                            ' with headers "<headers>", parameters "<params>" and payload "<payload_api>"')
            examples.extend([
                "method",
                "url",
                "headers",
                "params",
                "payload_api"
            ])
            examples_sizes.extend([
                len(examples[0]) + 2,
                max(len(scenario_values['method']), len(examples[1])),
                max(len(scenario_values['path']),len(examples[2]), len(path_completed)), 
                max(len(self.test_cases.convertToString(scenario_values['headers'],True)), len(examples[3])), 
                max(len(self.test_cases.convertToString(scenario_values['params'], True)), len(examples[4])), 
            ])
            if len(examples) > 5:
                examples_sizes.extend(max(
                    len(self.test_cases.convertToString(scenario_values['payload'], True)),
                    len(examples[5])
                ))
                

            examples.append('status_code')
            examples_sizes.append(len(examples[-1]))
            file.write('\n    Then the API will return "<status_code>"')
            file.write("\n\n    Examples: \n      ")

            for i in range(0, len(examples)):
                file.write(f"| {examples[i].ljust(examples_sizes[i])} ")
            file.write("|\n      ")

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
                        file.write(f"| {string.ljust(examples_sizes[i])} ")
                    else:
                        string = "*" + examples[i] + "*"

                        if examples[i] == 'status_code':
                            string = status_code
                        file.write(f"| {string.ljust(examples_sizes[i])} ")
                file.write('|\n      ')
        file.write("\n")
        file.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("paths", nargs='?', default=[])
    args = parser.parse_args()
    print(args)
    generate_feature = GenerateFeature(args.file)
    paths = args.paths
    if isinstance(args.paths, str):
        paths = args.paths.split(',')
    generate_feature.createMultiFeatures(paths)
if __name__ == '__main__':
    main()