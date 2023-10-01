import subprocess
import uuid
import re
from pathlib import Path

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
            project_dir = Path('projects')
            file_path = project_dir / file_name

            project_dir.mkdir(parents=True, exist_ok=True)

            with file_path.open('w') as f:
                f.write('#pragma option -d3\n\n') # bullshit
                f.write(code)
            
            output = subprocess.check_output([compiler_path, str(file_path)], stderr=subprocess.STDOUT, universal_newlines=True)

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
        
        for amx_file in Path('.').glob('*.amx'):
            try:
                amx_file.unlink()
                deleted_amx_files.append(amx_file)
                print(f'{amx_file} deleted')
            except OSError as e:
                print(f'Error deleting {amx_file}: {e}')

        return deleted_amx_files
