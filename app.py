from flask import Flask, request ,render_template, jsonify, Response
from flask_cors import CORS
from main import metodo_codo,dbscan_model

app= Flask(__name__)
CORS(app)
PORT= 5000
DEBUG=False

@app.route('/', methods=['GET'])
def index ():
    return '''<h1>TCS 2021 - RUTAS</h1>
                <ul>
                <li>dbscan_model</li>
                </ul>'''

@app.route('/metodo_codo', methods=['GET'])
def index3 ():
    return metodo_codo()


@app.route('/dbscan_model', methods=['GET', 'POST'])
def index5 ():
    sql="select distinct o.htitulo_cat, o.htitulo from webscraping w inner join oferta o on (w.id_webscraping=o.id_webscraping) where o.id_estado is null order by 1,2 limit 500;"
    if request.method == 'POST':
        body = request.get_json(),
        print(body)
        query       = body[0]['query']
        eps         = body[0]['eps']
        min_samples = body[0]['min_samples']     

        total_data = dbscan_model(int(eps), int(min_samples), query)
        return (total_data)

    if request.method == 'GET':
        total_data = dbscan_model(4, 4, sql); 
        return total_data

if __name__=="__main__":
    app.run(port=PORT, debug=DEBUG)
