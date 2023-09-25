from flask import Flask, render_template, request, jsonify
import subprocess, os, uuid

app = Flask(__name__)

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
        return jsonify({'success': True, 'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify(
            {
                'success': False, 
                'output': e.output
            }
        )

if __name__ == '__main__':
    app.run(debug=True)
