from flask import Flask, render_template, request, jsonify
from compiler import Compile

app = Flask(__name__)
    
compiler = Compile()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.form.get('code')
    result = compiler.CompileCode(code)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
