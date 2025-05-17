from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS
import shlex

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def search_username():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        command = ["sherlock", username]  # Removed --output, so output goes to stdout
        print(f"Running command: {command}")

        # Capture the output and errors from the subprocess
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Command output: {result.stdout}")
        print(f"Command errors: {result.stderr}")

        # Process the output directly from result.stdout
        lines = result.stdout.splitlines()  # Split the output into lines

        formatted_results = []
        for line in lines:
            line = line.strip()
            if line.startswith("http"):
                formatted_results.append({'url_user': line, 'status': 'Found'})

        print(f"Formatted results: {formatted_results}")
        return jsonify({'results': formatted_results})

    except FileNotFoundError:
        print("Error: 'sherlock' command not found. Ensure it is installed and in PATH.")
        return jsonify({'error': "'sherlock' command not found. Ensure it is installed and in PATH."}), 500

    except subprocess.CalledProcessError as e:
        print(f"Error running sherlock: {e}")
        return jsonify({'error': f"Error running sherlock: {str(e)}", 'output': e.output, 'stderr': e.stderr}), 500
if __name__ == '__main__':
    app.run(debug=True)
