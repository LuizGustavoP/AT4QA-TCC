import re

class StringUtils():
    
    re_placeholder_storage = r'#(.*?)#'
    re_extract_param_value = r'(?<={0}=)[^&#]+'
    
    def replace_placeholder_value_with_stored_value(string, storage):

        matches = re.findall(StringUtils.re_placeholder_storage, string)
        if matches:
            for m in matches:
                if("[" in m):
                    n = int(m[-2])
                    field = m.split("[")[0]
                    string = string.replace("#"+m+"#", str(storage[field][n]))
                else:
                    string = string.replace("#"+m+"#", str(storage[m]))
        
        return string
    
    def obtain_param_value(url, param):
        
        pattern = StringUtils.re_extract_param_value.format(param)
        match = re.search(pattern, url)
        
        return match.group(0) if match else None