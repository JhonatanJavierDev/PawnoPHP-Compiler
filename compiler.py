import subprocess
import os
import uuid
import re
import glob

class CodeCompiler:
    def __init__(self):
        self.patterns_output = {
            'header_size': r'Header size:\s*(\d+)',
            'code_size': r'Code size:\s*(\d+)',
            'data_size': r'Data size:\s*(\d+)',
            'stack_size': r'Stack/heap size:\s*(\d+)',
            'total_requirements': r'Total requirements:\s*(\d+)',
        }

    def compile_code(self, code):
        try:
            compiler_path = 'pawncc/pawncc'
            file_name = str(uuid.uuid4()) + '.pwn'
            file_path = os.path.join('projects', file_name)
            os.makedirs('projects', exist_ok=True)

            with open(file_path, 'w') as f:
                f.write('#pragma option -d3\n\n')
                f.write(code)
            
            output = subprocess.check_output([compiler_path, file_path], stderr=subprocess.STDOUT, universal_newlines=True)

            self.delete_amx()

            result = {'success': True, 'complete_output': output}

            for key, pattern in self.patterns_output.items():
                match = re.search(pattern, output)
                result[key] = match.group(1) if match else None

            return result
        except subprocess.CalledProcessError as e:
            return {'success': False, 'complete_output': e.output}
        
    def delete_amx(self):
        deleted_amx_files = []
        for amx_file in glob.glob('*.amx'):
            if not os.path.join(os.getcwd(), amx_file).startswith(os.path.join(os.getcwd(), 'projects')):
                try:
                    os.remove(amx_file)
                    deleted_amx_files.append(amx_file)
                except OSError as e:
                    print(f'Error deleting {amx_file}: {e}')
                else:
                    print(f'{amx_file} deleted')

        return deleted_amx_files