from flask import (
    render_template,
    send_from_directory,
    redirect,
    flash,
    url_for,
    session,
    jsonify,
    request,
    current_app as app,
)
from . import dashboard
from app.extras import return_indicators_calculation
from app.models import UserData, UserModel
from flask_login import login_required, login_user, logout_user
import json
import pandas as pd
import numpy as np

from scikitmcda.topsis import TOPSIS
from scikitmcda.constants import (
    MAX,
    MIN,
    LinearMinMax_,
    LinearMax_,
    LinearSum_,
    Vector_,
    EnhancedAccuracy_,
    Logarithmic_,
)

# ONLY TEST
value = 60

strategies_definition = {
    "generation": {
        "process": "Generación",
        "models": [
            {
                "id": "d001",
                "name": "Estrategias de expansión",
                "descripcion": "Son aquellas asociadas al cambio en la generación eléctrica debido a la variación de la capacidad instalada en las plantas eléctricas",
                "strategies": [
                    # STRATEGY TEST #
                    # {
                    #     "id": "x099",
                    #     "name": "Test variables auxiliares",
                    #     "description": "N/A",
                    #     "variable": "Variable primaria",
                    #     "upper_value": 100,
                    #     "lower_value": 0,
                    #     "value": 50,
                    #     "year": 2025,
                    #     "unit": "%",
                    #     "variable_aux": "Variable test",
                    #     "upper_value_aux": 100,
                    #     "lower_value_aux": 0,
                    #     "value_aux": 39,
                    #     "year_aux": 2025,
                    #     "unit_aux": "%",
                    #     "fp": 35.2576182447618 / 100,
                    #     "id_relation": "r001",
                    # },
                    # END STRATEGY TEST #
                    {
                        "id": "x001",
                        "name": "Generación eléctrica a partir de plantas térmicas",
                        "description": "N/A",
                        "variable": "Capacidad Instalada",
                        "upper_value": 10,
                        "lower_value": 0,
                        "value": 10,
                        "year": 2025,
                        "unit": "GW",
                        "fp": 35.2576182447618 / 100,
                        "id_relation": "r001",
                        "generacion_historica": 12268, # generacion historica de 2021, se usa como base para los calculos
                        "values_CI": [ # valor por defecto para la capacidad instalada se toma desde informe (escenario de actualizacion) [2022 ...2030]
                            5.74083,
                            6,
                            6,
                            6,
                            6,
                            6,
                            6,
                            6,
                            6,
                        ],
                    },
                    {
                        "id": "x002",
                        "name": "Generación eléctrica a partir de plantas hidráulicas",
                        "description": "N/A",
                        "variable": "Capacidad Instalada",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 15,
                        "year": 2025,
                        "unit": "GW",
                        "fp": 51.4937014 / 100,
                        "id_relation": "r002",
                        "generacion_historica": 58118.491688874,
                        "values_CI": [
                            11.944792,
                            13,
                            15,
                            15,
                            15,
                            15,
                            15,
                            15,
                            15,
                        ],
                    },
                    {
                        "id": "x003",
                        "name": "Generación eléctrica a partir de plantas de Auto y Cogeneración",
                        "description": "N/A",
                        "variable": "Capacidad Instalada",
                        "upper_value": 10,
                        "lower_value": 0,
                        "value": 2,
                        "year": 2025,
                        "unit": "GW",
                        "fp": 91.3033263 / 100,
                        "id_relation": "r003",
                        "generacion_historica": 5254.93081734859,
                        "values_CI": [
                            1.329,
                            1.361,
                            1.396,
                            1.429,
                            1.467,
                            1.502,
                            1.54,
                            1.577,
                            1.614,
                        ],
                    },
                    {
                        "id": "x004",
                        "name": "Generación eléctrica a partir de plantas eólicas",
                        "description": "N/A",
                        "variable": "Capacidad Instalada",
                        "upper_value": 10,
                        "lower_value": 1,
                        "value": 3,
                        "year": 2025,
                        "unit": "GW",
                        "fp": 34.7849019 / 100,
                        "id_relation": "r004",
                        "generacion_historica": 60.46,
                        "values_CI": [
                            0.01842,
                            2,
                            2,
                            2,
                            2,
                            2,
                            3,
                            3,
                            3,
                        ],
                    },
                    {
                        "id": "x005",
                        "name": "Generación eléctrica a partir de plantas solares",
                        "description": "N/A",
                        "variable": "Capacidad Instalada",
                        "upper_value": 10,
                        "lower_value": 1,
                        "value": 1,
                        "year": 2025,
                        "unit": "GW",
                        "fp": 36.8224441 / 100,
                        "id_relation": "r005",
                        "generacion_historica": 323.02,
                        "values_CI": [
                            0.290114,
                            1,
                            1,
                            1,
                            1,
                            1,
                            1,
                            1,
                            1,
                        ],
                    },
                ],
            },
            {
                "id": "d002",
                "name": "Estrategias de actualización",
                "descripcion": "Son aquellas que buscan reducir el consumo de fuentes primarias en las plantas de generación eléctrica, mediante una mejora en la eficiencia de las tecnologías empleadas a través de un recambio tecnológico. Cada estrategia considera la generación eléctrica modelada en las estrategias de expansión",
                "strategies": [
                    {
                        "id": "y001",
                        "name": "Mejoras de eficiencia en plantas térmicas",
                        "description": "N/A",
                        "variable": "Eficiencia deseada",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 56,
                        "year": 2025,
                        "unit": "%",
                        "n_LB": 37.1999989362893 / 100,
                        "efi_deseada_base": [   #eficiencia deseada tomada de informe, usando como base el escenario de actializacion y un valor deseado
                            39.29,              #de 56% al año 2030
                            41.38,
                            43.47,
                            45.56,
                            47.64,
                            49.73,
                            51.82,
                            53.91,
                            56.00,
                        ],
                        "values_BAU": [ # valores de salida de la generacion para cada planta dada por el escenario de actualizacion
                            17730.94,   # viene desde el informe ... solo se usa si la planta no ha sido seleccionada en la estrategia
                            19359.14,   # de eapansion de otro modo los valores se toma de la salida de la est. de expansion por cada planta
                            19359.14,
                            19359.14,
                            19359.14,
                            19359.14,
                            19359.14,
                            19359.14,
                            19359.14,
                        ],
                        "id_relation": "r001",
                    },
                    {
                        "id": "y002",
                        "name": "Mejoras de eficiencia en plantas hidráulicas",
                        "description": "N/A",
                        "variable": "Eficiencia deseada",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 90,
                        "year": 2025,
                        "unit": "%",
                        "n_LB": 88.0834783514384 / 100,
                        "efi_deseada_base": [   #eficiencia deseada tomada de informe, usando como base el escenario de actializacion y un valor deseado de 90% al año 2030
                            88.30,
                            88.51,
                            88.72,
                            88.94,
                            89.15,
                            89.36,
                            89.57,
                            89.79,
                            90.00,
                        ],
                        "values_BAU": [
                            53881.14,
                            58641.03,
                            67662.72,
                            67662.72,
                            67662.72,
                            67662.72,
                            67662.72,
                            67662.72,
                            67662.72,
                        ],
                        "id_relation": "r002",
                    },
                    {
                        "id": "y003",
                        "name": "Mejoras de eficiencia en plantas de Auto y Cogeneración",
                        "description": "N/A",
                        "variable": "Eficiencia deseada",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 47,
                        "year": 2025,
                        "unit": "%",
                        "n_LB": 36.3372271796145 / 100,
                        "efi_deseada_base": [   #eficiencia deseada tomada de informe, usando como base el escenario de actializacion y un valor deseado de 47% al año 2030
                            37.52,
                            38.71,
                            39.89,
                            41.08,
                            42.26,
                            43.45,
                            44.63,
                            45.82,
                            47.00,
                        ],
                        "values_BAU": [
                            10629.57,
                            10885.51,
                            11165.45,
                            11429.39,
                            11733.32,
                            12013.25,
                            12317.18,
                            12613.12,
                            12909.05,
                        ],
                        "id_relation": "r003",
                    },
                    {
                        "id": "y004",
                        "name": "Mejoras de eficiencia en plantas eólicas",
                        "description": "N/A",
                        "variable": "Eficiencia deseada",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 55,
                        "year": 2025,
                        "unit": "%",
                        "n_LB": 53.725 / 100,
                        "efi_deseada_base": [   #eficiencia deseada tomada de informe, usando como base el escenario de actializacion y un valor deseado de 56% al año 2030
                            53.98,
                            54.23,
                            54.48,
                            54.74,
                            54.99,
                            55.24,
                            55.49,
                            55.75,
                            56.00,
                        ],
                        "values_BAU": [
                            56.13,
                            6094.31,
                            6094.31,
                            6094.31,
                            6094.31,
                            6094.31,
                            9141.47,
                            9141.47,
                            9141.47,
                        ],
                        "id_relation": "r004",
                    },
                    {
                        "id": "y005",
                        "name": "Mejoras de eficiencia en plantas solares",
                        "description": "N/A",
                        "variable": "Eficiencia deseada",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 22,
                        "year": 2025,
                        "unit": "%",
                        "n_LB": 20.8268 / 100,
                        "efi_deseada_base": [   #eficiencia deseada tomada de informe, usando como base el escenario de actializacion y un valor deseado de 22% al año 2030
                            20.96,
                            21.09,
                            21.22,
                            21.35,
                            21.48,
                            21.61,
                            21.74,
                            21.87,
                            22.00,
                        ],
                        "values_BAU": [
                            935.81,
                            3225.65,
                            3225.65,
                            3225.65,
                            3225.65,
                            3225.65,
                            3225.65,
                            3225.65,
                            3225.65,
                        ],
                        "id_relation": "r005",
                    },
                ],
            },
        ],
    },
    "distribution": {
        "process": "Distribución",
        "models": [
            {
                "id": "z001",
                "name": "Digitalización y gestión de la medida",
                "descripcion": "Digitalización y gestión de la medida es bbbbbbbbbbb",
                "strategies": [
                    {
                        "id": "w001",
                        "name": "AMI para la identificación de pérdidas no técnicas(Lineal)",
                        "description": "N/A",
                        "variable": "Porcentaje de incorporación AMI",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 50,
                        "year": 2025,
                        "unit": "%",
                        "variable_aux": "Reducción final",
                        "upper_value_aux": 100,
                        "lower_value_aux": 0,
                        "value_aux": 50,
                        "year_aux": 2025,
                        "unit_aux": "%",
                        "ami_bau": 0.127553083836326, # valor por defecto par el año 2021, se toma como inicio de la ecuacion ya que es recursiva
                        "final_reduction_bau": 0.11774817604788, # valor por defecto para el 2021,
                        "type": 1,
                    },
                    {
                        "id": "w002",
                        "name": "AMI para la identificación de pérdidas no técnicas(Progresivo)",
                        "description": "N/A",
                        "variable": "Porcentaje de incorporación AMI",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 85,
                        "year": 2025,
                        "unit": "%",
                        "variable_aux": "Reducción final",
                        "upper_value_aux": 100,
                        "lower_value_aux": 0,
                        "value_aux": 50,
                        "year_aux": 2025,
                        "unit_aux": "%",
                        "ami_bau": 0.127553083836326, # valor por defecto par el año 2021, se toma como inicio de la ecuacion ya que es recursiva
                        "final_reduction_bau": 0.11774817604788, # valor por defecto para el 2021
                        "type": 2,
                    },
                    {
                        "id": "w003",
                        "name": "Adopción de Sistemas Avanzados de Gestión de la Distribución",
                        "description": "N/A",
                        "variable": "Porcentaje de incorporación AMI",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 70,
                        "year": 2025,
                        "unit": "%",
                        "variable_aux": "Reducción final",
                        "upper_value_aux": 100,
                        "lower_value_aux": 0,
                        "value_aux": 50,
                        "year_aux": 2025,
                        "unit_aux": "%",
                        "ami_bau": 0.127553083836326, # valor por defecto par el año 2021, se toma como inicio de la ecuacion ya que es recursiva
                        "final_reduction_bau": 0.11774817604788, # valor por defecto para el 2021
                        "type": 3,
                    },
                ],
            },
        ],
    },
    "end_use": {
        "process": "Uso final",
        "models": [
            {
                "id": "u001",
                "name": "Estrategias de electrificación en el transporte",
                "descripcion": "Son estrategias de descarbonización que buscan incluir el uso de vehículos eléctricos en las diferentes categorías del parque automotor colombiano, calculando el consumo eléctrico necesario para suplir esta demanda",
                "strategies": [
                    {
                        "id": "e001",
                        "name": "Electrificación del transporte masivo microbuses",
                        "description": "N/A",
                        "variable": "Número de vehículos eléctricos",
                        "upper_value": 1000,
                        "lower_value": 0,
                        "value": 1, # valor por defecto de numero de vehiculos, su valor se reemplaza ...
                        "year": 2025, # con el valor de arr_value_aux dependiendo del año
                        "unit": "Vehículos",
                        "variable_aux": "Rendimiento del motor",
                        "upper_value_aux": 10,
                        "lower_value_aux": 0,
                        "value_aux": 1.298610908, # valor por defecto para rendimiento del motor constante para años [2022 ...2030] en kwh
                        "rm_Km_Lge": 7.2, # valor por defecto para rendimiento del motor constante para años [2022 ...2030] en KM/Lge
                        "year_aux": 2025,
                        "unit_aux": "kWh/km",
                        "avkt": 45000, # valor por defecto para promedio de vkt constante para años [2022 ...2030]
                        "id_tipo_vehiculo": "ve001",
                        "num_vehic_elect": [
                            25.70104,
                            36.01845,
                            51.0354,
                            72.6075,
                            103.65226,
                            147.76132,
                            209.49465,
                            293.2314,
                            428.69568,
                        ],
                        "incremto_n_vehiculos": [  #valor en porcentaje ya que es un imcrento
                            0.241186004,
                            0.401439397,
                            0.416923827,
                            0.422688957,
                            0.427569604,
                            0.425548464,
                            0.417790867,
                            0.399708298,
                            0.46197058,
                        ],
                    },
                    {
                        "id": "e002",
                        "name": "Electrificación del transporte masivo buses",
                        "description": "N/A",
                        "variable": "Número de vehículos eléctricos",
                        "upper_value": 10000,
                        "lower_value": 0,
                        "value": 1,
                        "year": 2025,
                        "unit": "Vehículos",
                        "variable_aux": "Rendimiento del motor",
                        "upper_value_aux": 10,
                        "lower_value_aux": 0,
                        "value_aux": 2.800007904,
                        "rm_Km_Lge": 3.33,
                        "year_aux": 2025,
                        "unit_aux": "kWh/km",
                        "avkt": 74750,
                        "id_tipo_vehiculo": "ve002",
                        "num_vehic_elect": [
                            34.13536,
                            47.83727,
                            67.7196,
                            96.35822,
                            137.4296,
                            195.92559,
                            277.6292,
                            388.6672,
                            567.15204,
                        ],
                        "incremto_n_vehiculos": [  #valor en porcentaje ya que es un imcrento
                            0.240481986,
                            0.401399311,
                            0.415624261,
                            0.422900017,
                            0.426236392,
                            0.425643311,
                            0.417013469,
                            0.399950726,
                            0.4592228,
                        ],
                    },
                    {
                        "id": "e003",
                        "name": "Electrificación del transporte ligero automóviles y camperos",
                        "description": "N/A",
                        "variable": "Número de vehículos eléctricos",
                        "upper_value": 100000,
                        "lower_value": 0,
                        "value": 2,
                        "year": 2025,
                        "unit": "Vehículos",
                        "variable_aux": "Rendimiento del motor",
                        "upper_value_aux": 10,
                        "lower_value_aux": 0,
                        "value_aux": 0.159385065,
                        "rm_Km_Lge": 58.5,
                        "year_aux": 2025,
                        "unit_aux": "kWh/km",
                        "avkt": 13206,
                        "id_tipo_vehiculo": "ve001",
                        "num_vehic_elect": [
                            7104.90914,
                            11479.8671,
                            16586.80318,
                            21314.35332,
                            24967.7838,
                            27510.2951,
                            29248.6113,
                            30480.6834,
                            36507.28406,
                        ],
                        "incremto_n_vehiculos": [  #valor en porcentaje ya que es un imcrento
                            0.586899899,
                            0.615765504,
                            0.444860209,
                            0.285018764,
                            0.171407053,
                            0.101831677,
                            0.063187843,
                            0.042124123,
                            0.197718686,
                        ],
                    },
                    {
                        "id": "e004",
                        "name": "Electrificación del transporte ligero motos",
                        "description": "N/A",
                        "variable": "Número de vehículos eléctricos",
                        "upper_value": 100000,
                        "lower_value": 1,
                        "value": 2,
                        "year": 2025,
                        "unit": "Vehículos",
                        "variable_aux": "Rendimiento del motor",
                        "upper_value_aux": 10,
                        "lower_value_aux": 0,
                        "value_aux": 0.032487897,
                        "rm_Km_Lge": 287,
                        "year_aux": 2025,
                        "unit_aux": "kWh/km",
                        "avkt": 22301,
                        "id_tipo_vehiculo": "ve001",
                        "num_vehic_elect": [
                            4153.5912,
                            6662.08416,
                            10510.80681,
                            16124.22939,
                            23828.71116,
                            33644.63676,
                            45221.15754,
                            57908.4616,
                            82721.80874,
                        ],
                        "incremto_n_vehiculos": [  #valor en porcentaje ya que es un imcrento
                            0.495554159,
                            0.603933521,
                            0.577705498,
                            0.534062007,
                            0.477820154,
                            0.411936908,
                            0.344082204,
                            0.280561241,
                            0.428492598,
                        ],
                    },
                    {
                        "id": "e005",
                        "name": "Electrificación del transporte ligero camionetas",
                        "description": "N/A",
                        "variable": "Número de vehículos eléctricos",
                        "upper_value": 100000,
                        "lower_value": 1,
                        "value": 1,
                        "year": 2025,
                        "unit": "Vehículos",
                        "variable_aux": "Rendimiento del motor",
                        "upper_value_aux": 10,
                        "lower_value_aux": 0,
                        "value_aux": 0.197962342,
                        "rm_Km_Lge": 47.1,
                        "year_aux": 2025,
                        "unit_aux": "kWh/km",
                        "avkt": 15187,
                        "id_tipo_vehiculo": "ve001",
                        "num_vehic_elect": [
                            171.25089,
                            338.1644,
                            666.71475,
                            1304.5494,
                            2518.27142,
                            4745.89206,
                            8590.80326,
                            14643.562,
                            24592.1032,
                        ],
                        "incremto_n_vehiculos": [  #valor en porcentaje ya que es un imcrento
                            0.844633743,
                            0.974672365,
                            0.971569893,
                            0.956682974,
                            0.930376435,
                            0.884583219,
                            0.810155636,
                            0.704562607,
                            0.679379867,
                        ],
                    },
                    {
                        "id": "e006",
                        "name": "Electrificación del transporte ligero taxis",
                        "description": "N/A",
                        "variable": "Número de vehículos eléctricos",
                        "upper_value": 10000,
                        "lower_value": 1,
                        "value": 1,
                        "year": 2025,
                        "unit": "Vehículos",
                        "variable_aux": "Rendimiento del motor",
                        "upper_value_aux": 10,
                        "lower_value_aux": 0,
                        "value_aux": 0.159385065,
                        "rm_Km_Lge": 58.5,
                        "year_aux": 2025,
                        "unit_aux": "kWh/km",
                        "avkt": 60320,
                        "id_tipo_vehiculo": "ve001",
                        "num_vehic_elect": [
                            31.40058,
                            62.4397,
                            124.02744,
                            244.6955,
                            476.44674,
                            906.26872,
                            1656.83173,
                            2853.81824,
                            4861.08009,
                        ],
                        "incremto_n_vehiculos": [  #valor en porcentaje ya que es un imcrento
                            0.850766168,
                            0.988488748,
                            0.986355476,
                            0.97291422,
                            0.947100539,
                            0.902140667,
                            0.828190352,
                            0.722455086,
                            0.703360089,
                        ],
                    },
                    {
                        "id": "e007",
                        "name": "Electrificación del transporte de carga camiones",
                        "description": "N/A",
                        "variable": "Número de vehículos eléctricos",
                        "upper_value": 10000,
                        "lower_value": 1,
                        "value": 1,
                        "year": 2025,
                        "unit": "Vehículos",
                        "variable_aux": "Rendimiento del motor",
                        "upper_value_aux": 10,
                        "lower_value_aux": 0,
                        "value_aux": 1.554004387,
                        "rm_Km_Lge": 6,
                        "year_aux": 2025,
                        "unit_aux": "kWh/km",
                        "avkt": 29000,
                        "id_tipo_vehiculo": "ve002",
                        "num_vehic_elect": [
                            68.6098,
                            88.9576,
                            115.72036,
                            149.89468,
                            193.26135,
                            247.28343,
                            313.7112,
                            325.09668,
                            394.2456,
                        ],
                        "incremto_n_vehiculos": [  #valor en porcentaje ya que es un imcrento
                            0.162208022,
                            0.296572793,
                            0.300848494,
                            0.295318127,
                            0.289314271,
                            0.279528628,
                            0.26863009,
                            0.036292871,
                            0.212702634,
                        ],
                    },
                ],
            },
            {
                "id": "u002",
                "name": "Estrategias de actualización tecnológica",
                "descripcion": "Estas estrategias están asociadas a la reducción del consumo eléctrico en los sectores de uso final, dado un cambio de tecnologías que tienden a una mejor eficiencia energética. La máxima eficiencia a alcanzar en el año de análisis, es aquella correspondiente a la mejor tecnología que se espera estará disponible en Colombia (BAT) para la fecha",
                "strategies": [
                    {
                        "id": "f001",
                        "name": "Equipos en el sector residencial a BAT",
                        "description": "N/A",
                        "variable": "Porcentaje de integración",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 50, # valor por defecto de porcentaje de integracion, su valor se reemplaza ...
                        "year": 2025,# con el valor de pi_bau [2022 ... 2030] dependiendo del año
                        "unit": "%",
                        "variable_aux": "Eficiencia deseada",
                        "upper_value_aux": 62.86,
                        "lower_value_aux": 33.86,
                        "value_aux": 46, # valor por defecto para mostrar en los sliders es constante
                        "year_aux": 2025,# para todos los años [2022 ... 2030 ] (viene de informe)
                        "unit_aux": "%",
                        "nb": 0.338571429, # valor constante para todos los años [2022 .. 2030 ]
                        "np": 46, # valor constante para todos los años [2022 .. 2030 ]
                        "consumption_percent": 0.365870975887343,
                        "ce_bau": [75787.66778, 77602.11774, 79114.00883, 80850.5365, 82748.11192, 84635.31618, 86473.81712, 88286.0776, 90113.08465,],
                        "poblacion": [51609470, 52156250, 52691440, 53216590, 53732420, 54237750, 54731190, 55211260, 55678080,],
                        "PIB_billones_USD": [
                            344.1612833,
                            355.4685381,
                            367.8705797,
                            380.837696,
                            394.8857455,
                            408.9742253,
                            423.1216551,
                            437.1906672,
                            451.7446956,
                        ],
                        "pi_bau": [
                            0.788451953 / 100,
                            1.030658539 / 100,
                            1.351527385 / 100,
                            1.775937717 / 100,
                            2.333159213 / 100,
                            3.059047229 / 100,
                            3.992018218 / 100,
                            5.172317986 / 100,
                            6.634338406 / 100,
                        ],
                    },
                    {
                        "id": "f002",
                        "name": "Equipos en el sector comercial y público a BAT",
                        "description": "N/A",
                        "variable": "Porcentaje de integración",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 50,
                        "year": 2025,
                        "unit": "%",
                        "variable_aux": "Eficiencia deseada",
                        "upper_value_aux": 77.33,
                        "lower_value_aux": 42,
                        "value_aux": 60.2, #valor por defecto- sale de tabla adjuntada en informe
                        "year_aux": 2025,
                        "unit_aux": "%",
                        "nb": 0.42,
                        "np": 60.2,
                        "consumption_percent": 0.247125862010456,
                        "ce_bau": [75787.66778, 77602.11774, 79114.00883, 80850.5365, 82748.11192, 84635.31618, 86473.81712, 88286.0776, 90113.08465,],
                        "poblacion": [51609470, 52156250, 52691440, 53216590, 53732420, 54237750, 54731190, 55211260, 55678080,],
                        "PIB_billones_USD": [
                            344.1612833,
                            355.4685381,
                            367.8705797,
                            380.837696,
                            394.8857455,
                            408.9742253,
                            423.1216551,
                            437.1906672,
                            451.7446956,
                        ],
                        "pi_bau": [
                            0.532556233 / 100,
                            0.696153553 / 100,
                            0.912882934 / 100,
                            1.199548934 / 100,
                            1.575921622 / 100,
                            2.066219332 / 100,
                            2.69639028 / 100,
                            3.493618311 / 100,
                            4.481133256 / 100,
                        ],
                    },
                    {
                        "id": "f003",
                        "name": "Equipos en el sector industrial a BAT",
                        "description": "N/A",
                        "variable": "Porcentaje de integración",
                        "upper_value": 100,
                        "lower_value": 0,
                        "value": 50,
                        "year": 2025,
                        "unit": "%",
                        "variable_aux": "Eficiencia deseada",
                        "upper_value_aux": 87.75,   # internacional
                        "lower_value_aux": 72.25,   # actual
                        "value_aux": 82.25,
                        "year_aux": 2025,
                        "unit_aux": "%",
                        "nb": 0.7225,
                        "np": 82.25,
                        "consumption_percent": 0.3870031621022,
                        "ce_bau": [75787.66778, 77602.11774, 79114.00883, 80850.5365, 82748.11192, 84635.31618, 86473.81712, 88286.0776, 90113.08465,],
                        "poblacion": [51609470, 52156250, 52691440, 53216590, 53732420, 54237750, 54731190, 55211260, 55678080,],
                        "PIB_billones_USD": [
                            344.1612833,
                            355.4685381,
                            367.8705797,
                            380.837696,
                            394.8857455,
                            408.9742253,
                            423.1216551,
                            437.1906672,
                            451.7446956,
                        ],
                        "pi_bau": [
                            0.833991814 / 100,
                            1.090187908 / 100,
                            1.429589681 / 100,
                            1.878513349 / 100,
                            2.467919165 / 100,
                            3.235733438 / 100,
                            4.222591502 / 100,
                            5.471063703 / 100,
                            7.017528338 / 100,
                        ],
                    },
                ],
            },
        ],
    },
}


def functionTopsis(output, weiths):
    topsis = TOPSIS()
    # topsis.dataframe([[0.898834783514384, 0.166638958655125, 0.0],[0.403999992022169, 0.106074659601237, 13.4056094057448],[0.473372271796145, 0.0603668284274698, 7.6290994098352],[0.55725, 0.0363139093316429, 0.0],[0.223268, 0.031981378104915,  0.0]],['P Hidro', 'P Termicas', 'P A&C', 'P Eolicas', 'P Solares'],['EFICIENCIA', 'IEP', 'IEC']
    #                 )
    weiths_ = weiths[0]
    for i in range(len(weiths_)):
        if weiths_[i] == 0:
            weiths_[i] = 0.0000001
    topsis.dataframe(output[0], output[1], output[2])
    print(topsis.pretty_original())
    w_TOPSIS = topsis.set_weights_manually(weiths_)
    topsis.set_signals([MAX, MIN, MIN])
    topsis.decide()
    df_topsis = topsis.df_decision
    rank_alternatives = df_topsis.to_json(force_ascii=False, orient="records")
    return rank_alternatives


@dashboard.route("/guia_usuario")
def guia_usuario():
    print("send user guide")
    return send_from_directory("dashboard", "test.pdf")

@dashboard.route("/edit_scenary/")
def edit_scenary():
    # obtener el id de la URL
    id = request.args.get('id')
    print(f"id for edit: {id}")
    edit = app.db_object.get_data_table_strategies_variable_value(id)
    return jsonify(
        edit
        )

@dashboard.route('/editData', methods=['GET', 'POST'])
def editData():
    id = request.form.get("id")
    all_data= request.form.get("all_data")
    data_indicators= request.form.get("data_indicators")

    print(f"id:  {id}, all_data: {all_data} ,data_indicators: {data_indicators}")
    resultado = app.db_object.update_strategy_with_id(id, all_data, data_indicators)
    if resultado:
        flash("Scenary add successfully")
        print("succes")
        return jsonify({"mensaje": "success"})
    else:
        print("failure")
        return jsonify({"mensaje": "failure"})

@dashboard.route("/delete/<id>")
def delete(id):
    print(id)
    delete_ = app.db_object.delete_strategy_with_id(id)
    # if delete_:
    #     return "succes"
    # else:
    #     return "failed"
    return redirect(url_for('dashboard.analysis'))

# @login_required
@dashboard.route("/analysis", methods=["GET", "POST"])
def analysis():
    admin_session = session.get("admin_session")
    print(f"admin session {admin_session}")  # REVISAR VARIABLES EN LA SESION
    if request.method == "POST":
        output = request.get_json()
        # This is the output that was stored in the JSON within the browser
        result = json.loads(
            output
        )  # this converts the json output to a python dictionary
        data_result = result.get("data_topsis")
        values = []
        name = []
        weiths = []
        dataframe = []
        for row in data_result:
            print("row")
            print(row)
            keys = row.keys()
            if [*row.keys()][0] == "criteria_values":
                row_values = row.values()
                for row_val in row_values:
                    for val in row_val:
                        number = [*val.values()]
                        weiths.append(number)
            else:
                name.extend(keys)
                row_values = row.values()
                for row_val in row_values:
                    for val in row_val:
                        number = [*val.values()]
                        for i in range(len(number)):
                            if number[i] < 0:
                                number[i] = 0
                        values.append(number)
        criterios_name = ["EFICIENCIA", "IEP", "IEC"]
        dataframe.append(values)
        dataframe.append(name)
        dataframe.append(criterios_name)
        topsis = functionTopsis(dataframe, weiths)
        return topsis
    else:
        data_table_init = app.db_object.get_data_table_strategies("alex")
        strategies = app.db_object.get_strategies()
        description_strategies = app.db_object.get_description_strategies()
        data, translating_dict = app.db_object.get_distribution()
        units = app.db_object.get_units()
        context = {
            "anonymous": False,
            "user_ip": "UserIp",
            "data": data,
            "strategies": strategies,
            "strategies_definition": strategies_definition,
            "description_strategies": description_strategies,
            "units": units,
            "translating_dict": translating_dict,
            "admin_session": admin_session,
            "data_table_init": data_table_init,
        }
        return render_template("module/analysis.html", **context)


# @login_required
@dashboard.route("/database", methods=["GET", "POST"])
def database():
    admin_session = session.get("admin_session")
    data, translating_dict = app.db_object.get_distribution()
    data_indicators = app.db_object.get_indicators()
    units = app.db_object.get_units()

    dict_total_indicadores = return_indicators_calculation()
    print("------------entra a database-------")
    #print(data)
    # print(data)
    # print(data)
    """     json_data = json.dumps(data, ensure_ascii=False)
    print(json_data)
    print(type(json_data)) """
    context = {
        "anonymous": False,
        "user": "UserIp",
        "data": data,
        "data_total_indicators": dict_total_indicadores,
        "translating_dict": translating_dict,
        "data_indicators": data_indicators,
        "units": units,
        "admin_session": admin_session,
    }
    return render_template("module/database.html", **context)


# @login_required
@dashboard.route("/calc", methods=["GET", "POST"])
def calc():
    data, translating_dict = app.db_object.get_distribution()
    data_indicators = app.db_object.get_indicators()
    data_projections = app.db_object.get_projections()
    units = app.db_object.get_units()

    dict_total_indicadores = return_indicators_calculation()
    context = {
        "anonymous": False,
        "user": "UserIp",
        "data": data,
        "data_total_indicators": dict_total_indicadores,
        "translating_dict": translating_dict,
        "data_indicators": data_indicators,
        "data_projections": data_projections,
        "units": units,
        "admin_session": session.get("admin_session"),
    }
    return render_template("module/calc.html", **context)


# @login_required
@dashboard.route("/config", methods=["GET", "POST"])
def config():
    context = {
        "anonymous": False,
        "user": "UserIp",
    }
    return render_template("module/config.html", **context)


# @login_required
@dashboard.route("/", methods=["GET", "POST"])
def main():
    admin_user = (False, True)[
        (session.get("username") == "mateo.barrera@correounivalle.edu.co")
    ]
    admin_session = session.get("admin_session")
    if request.method == "POST":
        admin_session = eval(request.form["admin-session"])
        session["admin_session"] = admin_session

    text_module_db = 'En este módulo se recopila la información de las variables y los indicadores de ' \
                     'eficiencia energética asociados a los procesos de generación, distribución y uso final de la ' \
                     'energía eléctrica en Colombia, visualizando su tendencia histórica.'
    text_module_calc = 'En este módulo se presenta la especificación del modelo de proyección para las variables, ' \
                       'empleadas en la evaluación de estrategias de eficiencia energética del sector eléctrico ' \
                       'en Colombia. También se incluye la visualización de los resultados de proyección con la ' \
                       'tendencia histórica de las variables hasta el 2030.'
    text_module_anl = 'En este módulo se construyen y evalúan las estrategias de eficiencia energética asociadas al ' \
                      'sector eléctrico colombiano, mediante criterios económicos, ambientales y energéticos, ' \
                      'permitiendo definir las estrategias más viables para el país, según el año de análisis.'
    text_module_conf = 'En el apartado de Configuración se puede acceder a la información del usuario y ajustes '\
                       'referentes con las credenciales empleadas en el acceso a la herramienta.'

    context = {
        "anonymous": False,
        "user": "UserIp",
        "admin_session": admin_session,
        "admin_user": admin_user,
        "text_module_db": text_module_db,
        "text_module_calc": text_module_calc,
        "text_module_anl": text_module_anl,
        "text_module_conf": text_module_conf,
    }

    return render_template("module/main.html", **context)
