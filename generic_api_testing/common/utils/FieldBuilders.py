import json
from generic_api_testing.common.utils.StringUtils import StringUtils

class FieldBuilders():

    def build_json_object(string, storage):
        
        if string == "omitido":
            return {}
        else:
            string = StringUtils.replace_placeholder_value_with_stored_value(string, storage)
            return json.loads(string)