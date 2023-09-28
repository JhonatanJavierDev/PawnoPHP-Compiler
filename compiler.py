import subprocess, os
import uuid
import re

class Compile:
    def __init__(self):
        self.patternsOutput = {
            'header_size': r'Header size:\s*(\d+)',
            'code_size': r'Code size:\s*(\d+)',
            'data_size': r'Data size:\s*(\d+)',
            'stack_size': r'Stack/heap size:\s*(\d+)',
            'total_requirements': r'Total requirements:\s*(\d+)',
    }

    def CompileCode(self, code):
        fileName = str(uuid.uuid4()) + '.pwn'
        filePath = os.path.join('projects', fileName)
        os.makedirs('projects', exist_ok=True)

        with open(filePath, 'w') as f:
            f.write(f'//File generated by GigaPawn\n//Path: {filePath}\n\n#pragma option -d3\n')
            f.write(code)

        try:
            output = subprocess.check_output(['pawncc/pawncc', filePath], stderr=subprocess.STDOUT, universal_newlines=True)
            
            result = {
                'success': True,
                'complete_output': output,
            }
        
            for e, i in self.patternsOutput.items():
                match = re.search(i, output)
                result[e] = match.group(1) if match else None

            return result
        except subprocess.CalledProcessError as e:
            return {'success': False, 'complete_output': e.output}