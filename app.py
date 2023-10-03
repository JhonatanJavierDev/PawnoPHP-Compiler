from flask import Flask, request, jsonify
from compiler import CodeCompiler

app = Flask(__name__)
    
compiler = CodeCompiler()

@app.route('/compile', methods=['POST'])
def compile_endpoint():
    code = request.json.get('code')
    result = compiler.compile_code(code)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=1337)
