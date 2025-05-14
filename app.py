from api import create_app
from flasgger import Swagger

app = create_app('app')
app.config['SWAGGER'] = {
    "title": "Disk API",
    "description": "Disk API",
    "version": "0.0.1",
    "termsOfService": "",
    "hide_top_bar": True
}
Swagger(app)


if __name__ == '__main__':
    app.run(debug=True)