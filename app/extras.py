"""_summary_
        INTEGRA 2023 Platform Server extras File

        This file is part of the INTEGRA 2023 platform flask server.
        This contains the extra functions required to calculate energy efficiency indicators
        using the variables associated with the system.

    @Author: Alex Pinchao
    @Date: 18-10-2022
"""
from flask import current_app as app


def return_indicators_calculation():
    """generates a dictionary that contains the energy indicators
    taken into account by the platform between the years 2010 and 2020.

    Returns:
        dict_total_indicadores: dictionary of energy indicators
    """
    data, translating_dict = app.db_object.get_distribution()
    array_default = []
    array_default1 = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    array_default.append(array_default1)
    array_default.append(array_default1)

    data_generation_total_generation = data["generation"]["Generación eléctrica por fuente primaria"]
    data_generation_consumo = data["generation"]["Consumo de fuentes primarias por tipo de central eléctrica"]
    data_generation_emisiones_total = data["generation"]["Emisiones de CO2 equivalentes"]
    data_generation_emisiones_SIN = data["generation"]["Emisiones de CO2 equivalentes"]

    data_distribution_factor_perdidas = data["distribution"]["Factor de Pérdidas"]
    data_distribution_costo_perdidas = data["distribution"]["Costo de Pérdidas"]
    data_distribution_iaad = data["distribution"]["IAAD"]
    data_distribution_saidi_table = data["distribution"]["Saidi"]
    data_distribution_saifi_table = data["distribution"]["Saifi"]

    data_end_use_pib = data["end_use"]["PIB en USD"]
    data_end_use_population = data["end_use"]["Población"]
    data_end_use_total_consumption = data["end_use"]["Uso final de la energía"]

    def loopData(loop_data, variable):
        """function that returns a dictionary with year and the value of the
        variable of interest for the calculation of the indicator.

        Args:
            loop_data (array): array data
            variable (string): name of variable of interest to search

        Returns:
            anio (array): current year
            varible_return (array) : variable value
        """
        anio = []
        varible_return = []
        for n in loop_data:
            anio.append(n["Año"])
            if (len(varible_return) < 12):
                x = n[variable].replace(",", ".")
                y = float(x)
                varible_return.append(y)
        return anio, varible_return

    def prepareData(data_input_1, data_input_2, nombre, tipo):
        """function that returns a dictionary with year and calculation of the value of the indicator

        Args:
            data_input_1 (array): variable data 1
            data_input_2 (array): variable data 2
            nombre (string): indicator name
            tipo (number): type of operation

        Returns:
            salida (array): array containing the value of the indicator between the years 2010 to 2020
        """
        input_1 = data_input_1[1]
        anio_input_1 = data_input_1[0]
        input_2 = data_input_2[1]
        anio_input_2 = data_input_2[0]
        if len(input_1) == len(input_2):
            j = len(input_1)
            i = 0
            salida = []
            while i < j:
                salida_dict = {}
                if tipo == "1":
                    salida_dict.update({"Año": anio_input_1[i], nombre: (input_1[i] / input_2[i]) * 1000})
                    salida.append(salida_dict)
                elif tipo == "2":
                    salida_dict.update({"Año": anio_input_1[i], nombre: (input_1[i] / input_2[i]) / 1000})
                    salida.append(salida_dict)
                elif tipo == "3":
                    salida_dict.update({"Año": anio_input_1[i], nombre: input_1[i] / input_2[i]})
                    salida.append(salida_dict)
                elif tipo == "4":
                    salida_dict.update({"Año": anio_input_1[i], nombre: input_1[i]})
                    salida.append(salida_dict)
                i += 1
            return salida
        else:
            return []

    def prepareDataTwo(data_input_1, nombre_variable):
        """function that returns a dictionary with year and total of the input array

        Args:
            data_input_1 (array): array input
            nombre_variable (string): variable name
        Returns:
            variable_return (array): array containing the value of the indicator between the years 2010 to 2020
        """
        varible_return = []
        for n in data_input_1:
            if len(varible_return) < 12:
                salida_dict = {}
                salida_dict.update({"Año": n["Año"], nombre_variable: n["Total"]})
                varible_return.append(salida_dict)
        return varible_return

    generation_total_generation = loopData(data_generation_total_generation, "Generacion_Total")
    generation_consumo = loopData(data_generation_consumo, "Consumo_Total")
    generation_emisiones_total = loopData(data_generation_emisiones_total, "EmisionCO2_Total")
    generation_emisiones_SIN = loopData(data_generation_emisiones_SIN, "EmisionCO2_SIN_Total")

    data_distribution_saidi = loopData(data_distribution_saidi_table, "Saidi")
    data_distribution_saifi = loopData(data_distribution_saifi_table, "Saifi")

    end_use_pib = loopData(data_end_use_pib, "PIBUSD_Total")
    end_use_population = loopData(data_end_use_population, "Poblacion_Total")
    end_use_total_consumption = loopData(data_end_use_total_consumption, "ConsumoFinal_Total")

    # carga de indicadores en la generacion
    eficienc_gen_electrica = prepareData(generation_total_generation, generation_consumo,
                                         "Eficiencia de la generación eléctrica", "3")
    intens_energ_gen = prepareData(generation_consumo, end_use_pib,
                                   "Intensidad energética primaria de la generación eléctrica", "2")
    inten_emision_gen_electrica = prepareData(generation_emisiones_SIN, end_use_pib,
                                              "Intensidad de emisión de la generación eléctrica", "3")
    # emisiones_co2_sin_total = prepareData(generation_emisiones_SIN, array_default,"Emisiones de CO2eq de la generación eléctrica SIN", "3")
    emisiones_co2_total = prepareData(generation_emisiones_total, array_default,
                                      "Emisiones de CO2eq de la generación eléctrica Total", "3")

    dict_generacion = {}
    dict_generacion.update({"Eficiencia de la generación eléctrica": eficienc_gen_electrica})
    dict_generacion.update({"Intensidad energética primaria de la generación eléctrica": intens_energ_gen})
    dict_generacion.update({"Intensidad de emisión de la generación eléctrica": inten_emision_gen_electrica})
    # dict_generacion.update({"Emisiones de CO2eq de la generación eléctrica SIN":emisiones_co2_sin_total})
    dict_generacion.update({"Emisiones de $CO_2eq$ de la generación eléctrica Total": emisiones_co2_total})

    # carga de indicadores en la distribucion
    distribution_factor_perdida = prepareDataTwo(data_distribution_factor_perdidas,
                                                 "Factor de pérdidas en distribución (SOLO ADD)")
    distribution_costo_perdidas = prepareDataTwo(data_distribution_costo_perdidas,
                                                 "Costo de pérdidas equivalentes en distribución (SOLO ADD)")
    distribution_iaad = prepareDataTwo(data_distribution_iaad, "Índice Anual Acumulado de Discontinuidad - IAAD")

    distribution_saidi = prepareData(data_distribution_saidi, array_default, "Saidi", "4")
    distribution_saifi = prepareData(data_distribution_saifi, array_default, "Saifi", "4")

    dict_distribuciones = {}
    dict_distribuciones.update({"Factor de pérdidas en distribución (SOLO ADD)": distribution_factor_perdida})
    dict_distribuciones.update(
        {"Costo de pérdidas equivalentes en distribución (SOLO ADD)": distribution_costo_perdidas})
    dict_distribuciones.update({"Índice Anual Acumulado de Discontinuidad - IAAD": distribution_iaad})
    dict_distribuciones.update({"Saidi": distribution_saidi})
    dict_distribuciones.update({"Saifi": distribution_saifi})

    # carga de indicadores en la uso final
    consumo_per_capita = prepareData(end_use_total_consumption, end_use_population, "Consumo per cápita", "1")
    int_ener_uso_final = prepareData(end_use_total_consumption, end_use_pib,
                                     "Intensidad energética del uso final de la energía eléctrica", "2")

    dict_uso_final = {}
    dict_uso_final.update({"Consumo per cápita": consumo_per_capita})
    dict_uso_final.update({"Intensidad energética del uso final de la energía eléctrica": int_ener_uso_final})

    dict_total_indicadores = {}
    dict_total_indicadores.update({"Generación": dict_generacion})
    dict_total_indicadores.update({"Distribución": dict_distribuciones})
    dict_total_indicadores.update({"Uso final": dict_uso_final})
    #print("dict_total_indicadores")
    #print(dict_total_indicadores)
    return dict_total_indicadores
