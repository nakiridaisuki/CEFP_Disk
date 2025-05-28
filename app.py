from flask import Flask, render_template, send_from_directory
from api import create_app
from flasgger import Swagger

app = create_app('app')
app.config['SWAGGER'] = {
    "title": "Disk API",
    "description": "Disk API",
    "version": "0.0.1",
    "termsOfService": "",
    "hide_top_bar": True,
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Add a jwt with ** Bearer token"
        }
    },
    "security": "Bearer Auth"
}
Swagger(app)


@app.route('/assets/<path:filename>')
def serve_assets_static_files(filename):
    return send_from_directory(app.static_folder + '/assets', filename)

@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    return render_template('index.html')

if __name__ == '__main__':
    certificate_path = 'keys/server.crt'
    private_key_path = 'keys/server.key'

    print(app.template_folder)

    app.run(debug=True, host='127.0.0.1', port=5000)