from flask import Flask, render_template, request, jsonify
import subprocess, os
import uuid
import re

app = Flask(__name__)

patternsOutput = {
    'header_size': r'Header size:\s*(\d+)',
    'code_size': r'Code size:\s*(\d+)',
    'data_size': r'Data size:\s*(\d+)',
    'stack_size': r'Stack/heap size:\s*(\d+)',
    'total_requirements': r'Total requirements:\s*(\d+)',
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_pawn_code():
    code = request.form.get('code')

    fileName = str(uuid.uuid4()) + '.pwn'

    filePath = os.path.join('projects', fileName)
    os.makedirs('projects', exist_ok=True)
    
    with open(filePath, 'w') as f:
        f.write(code)
    
    try:
        output = subprocess.check_output(['compiler/pawncc', filePath], stderr=subprocess.STDOUT, universal_newlines=True)
        
        result = {
            'success': True,
            'complete_output': output,
        }
        

        for i, e in patternsOutput.items():
            match = re.search(e, output)
            result[i] = match.group(1) if match else None

        return jsonify(result)
    
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'complete_output': e.output,})

if __name__ == '__main__':
    app.run(debug=True)
