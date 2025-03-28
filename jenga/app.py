from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        # Run the script and capture its output
        result = subprocess.run(['python', 'script.py'], capture_output=True, text=True, check=True)
        # Parse the output into a list of lines
        output_lines = result.stdout.strip().split('\n')
        # Return the output as JSON
        return jsonify({"output": output_lines})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to run script", "details": e.stderr.strip()}), 500

if __name__ == '__main__':
    app.run(debug=True)