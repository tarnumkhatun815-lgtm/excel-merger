from flask import Flask, request, send_file, render_template_string
import pandas as pd
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Excel Merger</title>
</head>
<body>
    <h2>Upload Excel Files to Merge</h2>
    <form action="/merge" method="post" enctype="multipart/form-data">
        <input type="file" name="files" multiple required>
        <br><br>
        <button type="submit">Merge Files</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/merge', methods=['POST'])
def merge():
    files = request.files.getlist("files")
    df_list = []

    for file in files:
        df = pd.read_excel(file)
        df_list.append(df)

    merged_df = pd.concat(df_list)
    output_path = "merged.xlsx"
    merged_df.to_excel(output_path, index=False)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
