import yaml
import json
from pathlib import Path
import rstr

class TestCase:
    tags = []
    paths = {}
    schemas = {} 

    def __init__(self, file_name: str):
        print(file_name)
        if file_name.endswith('.yml'):
            with Path('documentation/'+file_name).open('r', encoding="utf8") as file:
                document = yaml.safe_load(file)
        elif file_name.endswith('.json'):
            with Path('documentation/'+file_name).open('r', encoding="utf8") as file:
                document = json.load(file)
        else:
            raise Exception('File must be a yaml or json file')

        self.document = document
        
        if('components' in document.keys()):
            self.createSchemas(document['components']['schemas'])
        
        if('tags' in document.keys()):
            self.createTags(document['tags'])
        self.createPaths(document['paths'])

    def createTags(self, tags):
        for tag in tags:
            self.tags.append({
                'name': tag['name'], 
            })
            
    def filterParameters(self, parameters: dict):
        query = []
        params = []
        headers = []
        for parameter_name, parameter_value in parameters.items():
            if 'example' in parameter_value.keys():
                value = parameter_value['example']
                if type(value) == 'list':
                    value = value[0]
            else:
                value = self.createExample(parameter_value['schema'])

            if parameter_value['in'] == 'params':
                query.append({
                    'name': parameter_name,
                    'value': value,
                    'other_properties': parameter_value
                })
            elif parameter_value['in'] == 'headers':
                headers.append({
                    'name': parameter_name,
                    'value': value,
                    'other_properties': parameter_value
                })
            elif parameter_value['in'] == 'url':
                params.append({
                    'name': parameter_name,
                    'value': value,
                    'other_properties': parameter_value
                })
        return params, query, headers

    def createExample(self, properties):

        if properties['type'] == 'integer':
            value = 0
            if 'min' in properties.keys():
                value = properties['min']
            return value
        if properties['type'] == 'string':
            value = "''"
            if 'pattern' in properties.keys():
                value  = rstr.xeger(properties['pattern'])
            return value        
        if properties['type'] == 'array':
            value = [self.createExample(properties['items'])]
            return value

    def createPayload(self, body:dict):
        payloads = []

        if 'oneOf' in body.keys():
            for oneOf in body['oneOf']:
                payloads.append(self.createPayload(oneOf))
        
        if 'anyOf' in body.keys():
            for anyOf in body['anyOf']:
                payloads.append(self.createPayload(anyOf))
        
        if 'allOf' in body.keys():
            payload_aux = []
            for allof_body in body['allOf']:
                payload_aux.extend(self.createPayload(allof_body)[0])
            payloads.append(payload_aux)
        
        if 'properties' in body.keys():
            properties_payloads = []

            for propertie_name, propertie_value in body['properties'].items():
                is_object = True
                if 'oneOf' in propertie_value:
                    value = self.createPayload(propertie_value)[0][0]
                elif 'type' not in propertie_value.keys():
                    value = self.createPayload(propertie_value)[0]
                elif propertie_value['type'] == 'object':
                    value = self.createPayload(propertie_value)[0]
                elif 'example' in propertie_value.keys():
                    value = propertie_value['example']
                    is_object = False
                else:
                    is_object = False
                    print(propertie_value)
                    value = self.createExample(propertie_value)
                
                properties_payloads.append({
                    "name": propertie_name,
                    "value": value,
                    "is_object": is_object
                })
        
            if payloads == []:
                payloads.append(properties_payloads)
            else:
                for payload in payloads:
                    payload.extend(properties_payloads)
        return payloads

    def createScenarios(self, path):
        scenarios = {}
    
        for method, method_schema in self.paths[path].items():
            scenario_name = method

            params, query, headers = self.filterParameters(method_schema['parameters'])
            if 'body' in method_schema.keys() and method_schema['body'] != None:

                aux = 1
                payloads = self.createPayload(method_schema['body'])
                for payload in payloads:
                    scenarios[f'{scenario_name}_{aux}'] = {
                        "params": params,
                        "query":query,
                        "headers": headers, 
                        "payload": payload,
                        "status_codes": method_schema['responses'],
                        'path': path,
                        "method": method,
                        "summary": self.check_key(method_schema, 'summary'),
                    }
                    aux+=1
            else:
    
                scenarios[f'{scenario_name}'] = {
                    "params": params,
                    "query": query,
                    "headers": headers, 
                    "status_codes": method_schema['responses'],
                    "payload": [],
                    'path': path,
                    "method": method,
                    "summary": self.check_key(method_schema, 'summary'),
                }
        return scenarios
    
    def convertToString(self, payload: any, use_values: bool) -> str:
        if isinstance(payload, str):
            return payload
        if payload == []:
            return 'omitted'
        string = '{'

        for items in payload:
            if 'is_object' in items.keys() and items['is_object']:
                value = self.convertToString(items['value'], use_values)
            elif isinstance(items['value'], list):
                value = '['
                for item in items['value']:
                    value += f' {self.convertToString(item, use_values)}, '
                value += ']'
            else:
                items['value'] = items['value'] if items['value'] != '' else "''"
                value = items['value'] if use_values else ''
            string += f" {items['name']}: {value},"
        string += '}'
        return string.replace('\n', '')

    def createPaths(self, paths:dict):
        for path, value in paths.items():
            self.paths[path] = {}

            for method, method_schema in value.items():
                responses = []

                for response in method_schema['responses']:
                    responses.append(response)
                body = None
                if 'requestBody' in method_schema.keys():
                    application = 'application/json'

                    name_ref_schema = method_schema['requestBody']['content'][application]['schema']['$ref'].split('/')[-1]
                    body = self.schemas[name_ref_schema]
                self.paths[path][method] = {
                    "path": path,
                    "summary": self.check_key(method_schema, 'summary'),
                    "method": method,
                    "parameters": self.findParameters(path, method_schema),
                    "body": body,
                    "responses": responses,
                }

    def findParameters(self,path: str, value: dict) -> dict :
        if 'parameters' not in value.keys():
            return {}
        init_search = 0
        aux = 0
        parameters = {}
        while(1):
            index_start = path.find('{', init_search)
            if index_start == -1:
                break
            index_final = path.find('}', index_start)
            name_ref_schema = value['parameters'][aux]['$ref'].split('/')[-1]
            parameters[path[index_start+1: index_final]] = self.document['components']['parameters'][name_ref_schema]
            init_search = index_final
            aux +=1
        for i in range(aux, len(value['parameters'])):
            name_ref_schema = value['parameters'][i]['$ref'].split('/')[-1]
            parameters[name_ref_schema] = self.document['components']['parameters'][name_ref_schema]
        return parameters

    def createSchemas(self, schemas:dict):
        for key, value in schemas.items():
            self.findSchemas(key, value)

    def findSchemas(self, schema_name:str, schema:dict):
            if schema_name in self.schemas.keys():
                return
            self.schemas[schema_name] = self.getType(schema)

    def getType(self, schema: dict):

        schema_convert = {}
        schema_convert.update(schema)
        if 'allOf' in schema.keys():
            schema_convert['allOf'] = self.getRef(schema, 'allOf')
        if 'anyOf' in schema.keys():
            schema_convert['anyOf'] = self.getRef(schema, 'anyOf')
        if 'oneOf' in schema.keys():
            schema_convert['oneOf'] = self.getRef(schema, 'oneOf')

        if '$ref' in schema.keys():
            name_ref_schema = schema['$ref'].split('/')[-1]
            if name_ref_schema not in self.schemas.keys():
                self.findSchemas(name_ref_schema, self.document['components']['schemas'][name_ref_schema])
            schema_convert[name_ref_schema] = self.schemas[name_ref_schema]

        schema_properties = {}
        if 'type' in schema.keys() and schema['type'] == 'object':
            if 'properties' in schema.keys():
                for properties_name, properties in schema['properties'].items():
                    if '$ref' in properties.keys():
                        name_ref_schema = properties['$ref'].split('/')[-1]
                        if name_ref_schema not in self.schemas.keys():
                            self.findSchemas(name_ref_schema, self.document['components']['schemas'][name_ref_schema])
                        schema_properties[properties_name] = self.schemas[name_ref_schema]
                    else:
                        schema_properties[properties_name] = self.getType(properties)

            schema_convert['properties'] = schema_properties
        return schema_convert

    def getRef(self, schema:dict, key:str) -> list:
        schema_list = []
        for value in schema[key]:
            value = value['$ref']
            name_ref_schema = value.split('/')[-1]
            if name_ref_schema not in self.schemas.keys():
                self.findSchemas(name_ref_schema, self.document['components']['schemas'][name_ref_schema])
            schema_list.append(self.schemas[name_ref_schema])
        return schema_list
    
    def check_key(self, dictionary: dict, key: str, default = ''):
        if key in dictionary.keys():
            return dictionary[key]
        return default