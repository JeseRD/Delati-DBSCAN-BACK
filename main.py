import json , io, base64
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import pandas as pd
from sklearn import preprocessing
from sklearn import cluster , metrics
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors

conn= psycopg2.connect(database="delati", user="modulo4", password="modulo4", host="128.199.1.222", port="5432")


def get_dataFrame(sql, conn):
    df = pd.read_sql(sql, con = conn)
    return df

def transform_data(dat):
    label_encoder = preprocessing.LabelEncoder()
    transformed_data = dat.apply(label_encoder.fit_transform)
    return transformed_data


def metodo_codo(dataTransformed):
    # Usamos vecinos más cercanos para calcular la distancia entre puntos.
    # calcular distancias 
    neigh=NearestNeighbors(n_neighbors=2)
    distance=neigh.fit(dataTransformed)
    # índices y valores de distancia
    distances,indices=distance.kneighbors(dataTransformed)
    # Ahora ordenando el orden creciente de distancia
    sorting_distances=np.sort(distances,axis=0)
    # distancias ordenadas
    sorted_distances=sorting_distances[:,1]
    return sorted_distances

#grafico entre distancia vs épsilon
#plt.plot(sorted_distances)
#plt.xlabel('Distancia')
#plt.ylabel('Epsilon')
#plt.show()

def dbscan_model(eps, min_samples, query):
    result = {}
    #TODO: Obtener data desde la query
    data=get_dataFrame(query, conn)
    #TODO: transformamos la data
    dataTransformed = transform_data(data)
    # inicializamos DBSCAN
    clustering_model=DBSCAN(eps=eps,min_samples=min_samples)
    # ajustamos el modelo a transform_data
    clustering_model.fit(dataTransformed)
    predicted_labels=clustering_model.labels_

    data['cluster'] = predicted_labels

    ########metrics and number of clusters####################
    n_clusters_ = len(set(predicted_labels)) - (1 if -1 in predicted_labels else 0)
    n_noise_    = list(predicted_labels).count(-1)
    coefficient = metrics.silhouette_score(dataTransformed, predicted_labels)

    result['data'] = json.loads(data.to_json(orient = 'records'))
    result['metricas'] = { 
                'n_clusters': n_clusters_,
                 'n_noise': n_noise_,
                 'Coefficient': coefficient}

    ##############visualizacion de DBSCAN ##################
#visualzing clusters

    dataTransformed['cluster']=predicted_labels

    clusters = dataTransformed['cluster'].apply(lambda x: 'cluster ' +str(x+1) if x != -1 else 'outlier')
    numero_clusters= len(set(clusters))
    XX=dataTransformed.iloc[:,[0,1]].values
    plt.figure(figsize=(15,10))

    for i in range(numero_clusters):
        if (i-1) != -1:
            plt.scatter(XX[clustering_model== (i-1), 0], XX[clustering_model==(i-1), 1], s=80, cmap='Paired', label = clusters.unique())
        else:
            plt.scatter(XX[clustering_model== (i-1), 0], XX[clustering_model==(i-1), 1], s=80, c='Grey', label = clusters.unique())

    plt.legend(clusters.unique(),bbox_to_anchor=(1.05,1),fontsize=25)
    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.6)
    plt.xlabel('Categoria')
    plt.ylabel('Datos')
    plt.title("DBSCAN")
 
    ##############
    
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    # plt.savefig("graphic2.jpg")
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    result["graphic_dbscan"] = my_base64_jpgData.decode()


    codo=metodo_codo(dataTransformed)
    #grafico entre distancia vs épsilon
    plt.plot(codo)
    plt.xlabel('Distancia')
    plt.ylabel('Epsilon')
    plt.title("GRÁFICO MÉTODO DEL CODO")
    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.6)

    codo_image = io.BytesIO()
    plt.savefig(codo_image, format='jpg')
    codo_image.seek(0)
    codo_image_decode = base64.b64encode(codo_image.read())
    result["graphic_method_codo"] = codo_image_decode.decode()

    return result





