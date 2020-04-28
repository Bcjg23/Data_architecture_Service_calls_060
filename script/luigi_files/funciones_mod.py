#import psycopg2 as pg
#import pandas.io.sql as psql
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn_pandas import CategoricalImputer


def preprocesamiento_variable(df):
    """
    Esta funcion realiza los siguientes cambios al df:
        1. Recategoriza la variable 'incidente_c4'
        2. Crea la variable 'hora' que guarda la solo la hora de la columna 'hora_creacion'
        3. Crea la variable objetivo 'target' 
    """

    # Split para las categorias
    df['incidente_c4_rec'] = df['incidente_c4'].str.split('-').str[0] 

    # Crear la variable hora que solo contenga la hora
    df['hora'] = df['hora_creacion'].astype('str').str.split(':').str[0]
    # Crear la variable target
    df['clave'] = df['codigo_cierre'].str[1:2]  # Obtiene la letra (categoria)
    df['target']=np.where(df['clave']=='a',1,0)  # la convierte a 0/1

    return df


def separa_train_y_test(df, vars_mod, var_obj):
    "Separacion de mi set de entrenamiento y prueba"

    PORCENTAJE_TEST = 0.3

    #Seleccionamos las variables del modelo
    datos_select=df[vars_mod]

    #Hacemos la separacion
    X_train, X_test, y_train, y_test = train_test_split(datos_select.loc[:, datos_select.columns != var_obj],
                                                         datos_select[[var_obj]], test_size=PORCENTAJE_TEST, random_state=0)


    return X_train, X_test, y_train, y_test



def imputacion_variable_delegacion(X_train, X_test):
    " Esta funcion imputa la variable 'delegacion_inicio' con la moda "

    #Para el set de entrenamiento
    X = X_train.delegacion_inicio.values.reshape(X_train.shape[0],1)
    delegacionInicio_imputer=CategoricalImputer(strategy='most_frequent')
    X_train['delegacion_inicio']=delegacionInicio_imputer.fit_transform(X)

    #Para el set de prueba
    X = X_test.delegacion_inicio.values.reshape(X_test.shape[0],1)
    X_test['delegacion_inicio']=delegacionInicio_imputer.transform(X) 


    return X_test, X_train




def asigna_nombre_archivo(i):
        switcher={
                0:'X_train',
                1:'X_test',
                2:'y_train',
                3:'y_test'
                }
        return switcher.get(i,"ERROR")