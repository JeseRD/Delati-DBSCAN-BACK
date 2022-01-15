from flask import Flask, request ,render_template, jsonify, Response
from flask_cors import CORS
from main import metodo_codo,dbscan_model

app= Flask(__name__)
CORS(app)
PORT= 5002
HOST='128.199.1.222'
#HOST='127.0.0.1'
#DEBUG=False
DEBUG=True

@app.route('/', methods=['GET'])
def index ():
    return '''<h1>DELATI - DBSCAN</h1>
                <ul>
                <li>dbscan_model</li>
                </ul>'''

@app.route('/metodo_codo', methods=['GET'])
def index3 ():
    return metodo_codo()


@app.route('/dbscan_model', methods=['GET', 'POST'])
def index5 ():
    sql="select o.htitulo_cat, o.htitulo, w.pagina_web, o.empresa, o.lugar, o.salario, date_part('year',o.fecha_publicacion) as periodo, f_dimPuestoEmpleo(o.id_oferta,1) as conocimiento, f_dimPuestoEmpleo(o.id_oferta,3) as habilidades, f_dimPuestoEmpleo(o.id_oferta,2) as competencias, f_dimPuestoEmpleo(o.id_oferta,17) as certificaciones, f_dimPuestoEmpleo(o.id_oferta,5) as beneficio, f_dimPuestoEmpleo(o.id_oferta,11) as formacion from webscraping w inner join oferta o on (w.id_webscraping=o.id_webscraping) where o.id_estado is null;"
    if request.method == 'POST':
        body = request.get_json(),
        #print(body)
        query       = body[0]['query']
        eps         = body[0]['eps']
        min_samples = body[0]['min_samples']     

        total_data = dbscan_model(float(eps), int(min_samples), query)
        return (total_data)

    #if request.method == 'GET':
        #total_data = dbscan_model(4, 4, sql); 
        #print("Cabecera", total_data['numColumn'])
        #print ("Data", total_data['data'])
        #return total_data

if __name__=="__main__":
    #app.run(debug=True)
    #app.run(port=PORT, debug=DEBUG)
    app.run(host=HOST,port=PORT,debug=DEBUG)
