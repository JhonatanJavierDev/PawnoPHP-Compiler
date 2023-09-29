from flask import Flask, render_template, request, jsonify
from compiler import CodeCompiler

app = Flask(__name__)
    
compiler = CodeCompiler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.form.get('code')
    result = compiler.compile_code(code)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
