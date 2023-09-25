from flask import Flask, render_template, request, jsonify
import subprocess
import uuid 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_pawn_code():
    code = request.form.get('code')

    fileName = str(uuid.uuid4()) + '.pwn'
    
    # Guarda el código en el archivo temporal
    with open(fileName, 'w') as f:
        f.write(code)
    
    try:
        output = subprocess.check_output(['compiler/pawncc', fileName], stderr=subprocess.STDOUT, universal_newlines=True)
        return jsonify({'success': True, 'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'output': e.output})

if __name__ == '__main__':
    app.run(debug=True)
