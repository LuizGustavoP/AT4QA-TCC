import json
from common.utils.StringUtils import StringUtils

class FieldBuilders():

    def build_json_object(string, storage):
        
        if string == "omitted":
            return {}
        else:
            string = StringUtils.replace_placeholder_value_with_stored_value(string, storage)
            return json.loads(string)