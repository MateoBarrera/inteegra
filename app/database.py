"""INTEGRA 2023 Platform Server database file

Contains the definition of the relational model and execution methods for requests to the database.
"""
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import select, insert, update
from app import db, admin

from flask_admin.contrib.sqla import ModelView
from flask import json
import datetime


# Table schema definition
metadata_obj = MetaData()

# Login table schema
login_table = Table('login', metadata_obj,
                    Column('idlogin', Integer,
                           primary_key=True, nullable=False, autoincrement=True),
                    Column('user', String),
                    Column('password', String)
                    )

# Users table schema
users_table = Table('users', metadata_obj,
                    Column('iduser', Integer,
                           primary_key=True, nullable=False),
                    Column('id_login', Integer,
                           ForeignKey('login.idlogin'), nullable=False),
                    Column('name', String),
                    Column('organization', String),
                    Column('position', String),
                    Column('phone', String),
                    Column('validated', String)
                    )

# Emissions Factor table schema
emission_table = Table('FEmision', metadata_obj,
                       Column('Año', Integer, nullable=False, unique=True),
                       Column('ECO2_CT_Carbon', String),
                       Column('ECO2_CT_Gas', String),
                       Column('ECO2_CT_Diesel', String),
                       Column('ECO2_CT_Fueloil', String),
                       Column('ECO2_CT_Kerosene', String),
                       Column('ECO2_CAyC_Bagazo', String),
                       Column('ECO2_CAyC_Carbon', String),
                       Column('ECO2_CAyC_Gas', String),
                       Column('ECO2_CAyC_Petroleo', String),
                       Column('ECO2_CAyC_Diesel', String),
                       Column('ECO2_CAyC_Gaslicuado', String),
                       Column('EmisionCO2_Total', String),
                       Column('EmisionCO2_SIN_Total', String),
                       Column('EmisionCO2_CT_Total', String),
                       Column('EmisionCO2_CAyC_Total', String),
                       Column('EmisionCO2_Carbon', String),
                       Column('EmisionesCO2_Gas', String),
                       Column('EmisionesCO2_Diesel', String),
                       Column('EmisionesCO2_Fueloil', String),
                       Column('EmisionesCO2_Petroleo', String),
                       Column('EmisionesCO2_Gaslicuado', String),
                       Column('EmisionesCO2_Bagazo', String)
                       )

# Electric generation consumption table schema
consumption_table = Table('G_Consumo', metadata_obj,
                          Column('Año', Integer, nullable=False, unique=True),
                          Column('C_CT_carbon_GWh', String),
                          Column('C_CT_Gas_GWh', String),
                          Column('C_CT_Diesel_GWh', String),
                          Column('C_CT_Fueloil_GWh', String),
                          Column('C_CT_Kerosene_GWh', String),
                          Column('C_CT_Total_GWh', String),
                          #Column('C_CE_Viento_GWh', String),
                          #Column('C_CS_Sol_GWh', String),
                          Column('C_CAyC_Bagazo_GWh', String),
                          Column('C_CAyC_Carbon_GWh', String),
                          Column('C_CAyC_Gas_GWh', String),
                          Column('C_CAyC_Petroleo_GWh', String),
                          Column('C_CAyC_Diesel_GWh', String),
                          Column('C_CAyC_Gaslicuado_GWh', String),
                          Column('C_CAyC_Total', String),
                          Column('Consumo_Total', String)
                          )

# Electric generation table schema
generation_table = Table('G_Electrica', metadata_obj,
                         Column('Año', Integer, nullable=False, unique=True),
                         Column('CH_Agua', String),
                         Column('CT_ACPM', String),
                         Column('CT_Carbon', String),
                         Column('CT_Combustoleo', String),
                         Column('CT_Gas', String),
                         Column('CT_GasNI', String),
                         Column('CT_JETA1', String),
                         Column('CT_Mezclas', String),
                         Column('CT_Querosene', String),
                         Column('CT_Bagazo', String),
                         Column('CT_Biogas', String),
                         Column('CT_Biomasa', String),
                         Column('CT_RadSol', String),
                         Column('CT_Total', String),
                         Column('CE_Viento', String),
                         Column('CS_Sol', String),
                         Column('CAyC_Bagazo', String),
                         Column('CAyC_Biomasa', String),
                         Column('CAyC_Carbon', String),
                         Column('CAyC_Gas', String),
                         Column('CAyC_SIN_Total', String),
                         Column('CAyC_NoSIN_Total', String),
                         Column('CAyC_Total', String),
                         Column('Porcentaje_CAyC_SIN', String),
                         Column('Generacion_fosiles_Total', String),
                         Column('Generacion_FNCE_Total', String),
                         Column('Generacion_SIN_Total', String),
                         Column('Generacion_Total', String)
                         )

# PIB table schema
pib_table = Table('PIB', metadata_obj,
                  Column('Año', Integer, nullable=False, unique=True),
                  Column('PIB_Total', String),
                  Column('PIB_Agro', String),
                  Column('PIB_Agro_Cultivos', String),
                  Column('PIB_Agro_Cafe', String),
                  Column('PIB_Agro_Ganado', String),
                  Column('PIB_Agro_Madera', String),
                  Column('PIB_Agro_Pesca', String),
                  Column('PIB_Minas', String),
                  Column('PIB_Minas_Carbon', String),
                  Column('PIB_Minas_Petroleo', String),
                  Column('PIB_Minas_Metales', String),
                  Column('PIB_Minas_Canteras', String),
                  Column('PIB_Minas_Otros', String),
                  Column('PIB_Alimentos', String),
                  Column('PIB_Alimentos_Carne', String),
                  Column('PIB_Alimentos_Aceite', String),
                  Column('PIB_Alimentos_Lacteos', String),
                  Column('PIB_Alimentos_Almidon', String),
                  Column('PIB_Alimentos_Cafe', String),
                  Column('PIB_Alimentos_Azucar', String),
                  Column('PIB_Alimentos_Cacao', String),
                  Column('PIB_Alimentos_Frutas', String),
                  Column('PIB_Alimentos_Bebidas', String),
                  Column('PIB_Textiles', String),
                  Column('PIB_Textiles_Confeccion', String),
                  Column('PIB_Textiles_Cuero', String),
                  Column('PIB_Madera', String),
                  Column('PIB_Madera_Transformacion', String),
                  Column('PIB_Madera_Papel', String),
                  Column('PIB_Madera_Impresion', String),
                  Column('PIB_Quimica', String),
                  Column('PIB_Quimica_Refinacion', String),
                  Column('PIB_Quimica_Otros', String),
                  Column('PIB_Quimica_Plastico', String),
                  Column('PIB_Quimica_Minerales', String),
                  Column('PIB_Metales', String),
                  Column('PIB_Metales_Basicos', String),
                  Column('PIB_Metales_Electrico', String),
                  Column('PIB_Metales_Maquinaria', String),
                  Column('PIB_Metales_Vehiculos', String),
                  Column('PIB_Muebles', String),
                  Column('PIB_Muebles_Colchones', String),
                  Column('PIB_Muebles_Otros', String),
                  Column('PIB_Electricidad', String),
                  Column('PIB_Electricidad_GTD', String),
                  Column('PIB_Electricidad_Gas', String),
                  Column('PIB_Agua', String),
                  Column('PIB_Agua_Tratamiento', String),
                  Column('PIB_Agua_Residuales', String),
                  Column('PIB_Agua_Reciclaje', String),
                  Column('PIB_Edificaciones', String),
                  Column('PIB_Carreteras', String),
                  Column('PIB_Civil', String),
                  Column('PIB_Comercio', String),
                  Column('PIB_Comercio_Vehiculos', String),
                  Column('PIB_Comercio_Mantenimiento', String),
                  Column('PIB_Transporte', String),
                  Column('PIB_Transporte_Terrestre', String),
                  Column('PIB_Transporte_Acuatico', String),
                  Column('PIB_Transporte_Aereo', String),
                  Column('PIB_Transporte_almacenamiento', String),
                  Column('PIB_Transporte_Correo', String),
                  Column('PIB_Alojamiento', String),
                  Column('PIB_Información', String),
                  Column('PIB_Financieras', String),
                  Column('PIB_Inmobiliarias', String),
                  Column('PIB_Profesionales', String),
                  Column('PIB_Profesionales_Cientificas', String),
                  Column('PIB_Profesionales_Servicios', String),
                  Column('PIB_Administracion', String),
                  Column('PIB_Educacion', String),
                  Column('PIB_Educacion_Mercado', String),
                  Column('PIB_Educacion_NoMercado', String),
                  Column('PIB_Salud', String),
                  Column('PIB_Entretenimiento', String),
                  Column('PIB_Hogar', String),
                  Column('PIB_Industria_Total', String),
                  Column('PIB_ComercialyPublico_Total', String)
                  )

# PIB in dollars table schema
pib_usd_table = Table('PIB_USD', metadata_obj,
                      Column('Año', Integer, nullable=False, unique=True),
                      Column('PIBUSD_Total', String),
                      Column('PIBUSD_Agro', String),
                      Column('PIBUSD_Agro_Cultivos', String),
                      Column('PIBUSD_Agro_Cafe', String),
                      Column('PIBUSD_Agro_Ganado', String),
                      Column('PIBUSD_Agro_Madera', String),
                      Column('PIBUSD_Agro_Pesca', String),
                      Column('PIBUSD_Minas', String),
                      Column('PIBUSD_Minas_Carbon', String),
                      Column('PIBUSD_Minas_Petroleo', String),
                      Column('PIBUSD_Minas_Metales', String),
                      Column('PIBUSD_Minas_Canteras', String),
                      Column('PIBUSD_Minas_Otros', String),
                      Column('PIBUSD_Alimentos', String),
                      Column('PIBUSD_Alimentos_Carne', String),
                      Column('PIBUSD_Alimentos_Aceite', String),
                      Column('PIBUSD_Alimentos_Lacteos', String),
                      Column('PIBUSD_Alimentos_Almidon', String),
                      Column('PIBUSD_Alimentos_Cafe', String),
                      Column('PIBUSD_Alimentos_Azucar', String),
                      Column('PIBUSD_Alimentos_Cacao', String),
                      Column('PIBUSD_Alimentos_Frutas', String),
                      Column('PIBUSD_Alimentos_Bebidas', String),
                      Column('PIBUSD_Textiles', String),
                      Column('PIBUSD_Textiles_Confeccion', String),
                      Column('PIBUSD_Textiles_Cuero', String),
                      Column('PIBUSD_Madera', String),
                      Column('PIBUSD_Madera_Transformacion', String),
                      Column('PIBUSD_Madera_Papel', String),
                      Column('PIBUSD_Madera_Impresion', String),
                      Column('PIBUSD_Quimica', String),
                      Column('PIBUSD_Quimica_Refinacion', String),
                      Column('PIBUSD_Quimica_Otros', String),
                      Column('PIBUSD_Quimica_Plastico', String),
                      Column('PIBUSD_Quimica_Minerales', String),
                      Column('PIBUSD_Metales', String),
                      Column('PIBUSD_Metales_Basicos', String),
                      Column('PIBUSD_Metales_Electrico', String),
                      Column('PIBUSD_Metales_Maquinaria', String),
                      Column('PIBUSD_Metales_Vehiculos', String),
                      Column('PIBUSD_Muebles', String),
                      Column('PIBUSD_Muebles_Colchones', String),
                      Column('PIBUSD_Muebles_Otros', String),
                      Column('PIBUSD_Electricidad', String),
                      Column('PIBUSD_Electricidad_GTD', String),
                      Column('PIBUSD_Electricidad_Gas', String),
                      Column('PIBUSD_Agua', String),
                      Column('PIBUSD_Agua_Tratamiento', String),
                      Column('PIBUSD_Agua_Residuales', String),
                      Column('PIBUSD_Agua_Reciclaje', String),
                      Column('PIBUSD_Edificaciones', String),
                      Column('PIBUSD_Carreteras', String),
                      Column('PIBUSD_Civil', String),
                      Column('PIBUSD_Comercio', String),
                      Column('PIBUSD_Comercio_Vehiculos', String),
                      Column('PIBUSD_Comercio_Mantenimiento', String),
                      Column('PIBUSD_Transporte', String),
                      Column('PIBUSD_Transporte_Terrestre', String),
                      Column('PIBUSD_Transporte_Acuatico', String),
                      Column('PIBUSD_Transporte_Aereo', String),
                      Column('PIBUSD_Transporte_almacenamiento', String),
                      Column('PIBUSD_Transporte_Correo', String),
                      Column('PIBUSD_Alojamiento', String),
                      Column('PIBUSD_Información', String),
                      Column('PIBUSD_Financieras', String),
                      Column('PIBUSD_Inmobiliarias', String),
                      Column('PIBUSD_Profesionales', String),
                      Column('PIBUSD_Profesionales_Cientificas', String),
                      Column('PIBUSD_Profesionales_Servicios', String),
                      Column('PIBUSD_Administracion', String),
                      Column('PIBUSD_Educacion', String),
                      Column('PIBUSD_Educacion_Mercado', String),
                      Column('PIBUSD_Educacion_NoMercado', String),
                      Column('PIBUSD_Salud', String),
                      Column('PIBUSD_Entretenimiento', String),
                      Column('PIBUSD_Hogar', String),
                      Column('PIBUSD_Industria_Total', String),
                      Column('PIBUSD_ComercialyPublico_Total', String)
                      )

# Population table schema
population_table = Table('Poblacion', metadata_obj,
                         Column('Año', Integer, nullable=False, unique=True),
                         Column('P_Urbano', Float),
                         Column('P_Rural', Float),
                         Column('Poblacion_Total', Float)
                         )

# End use energy table schema
end_use_energy_table = Table('U_Energia', metadata_obj,
                             Column('Año', Integer,
                                    nullable=False, unique=True),
                             Column('C_Residencial_U', String),
                             Column('C_Residencia_R', String),
                             Column('C_Residencial_Total', String),
                             Column('C_CyP_Total', String),
                             Column('C_Ind_Alimentos', String),
                             Column('C_Ind_Bebidas', String),
                             Column('C_Ind_Tabaco', String),
                             Column('C_Ind_Textil', String),
                             Column('C_Ind_Vestimenta', String),
                             Column('C_Ind_Marroquineria', String),
                             Column('C_Ind_Madera', String),
                             Column('C_Ind_Papel', String),
                             Column('C_Ind_Impresion', String),
                             Column('C_Ind_Refinerias', String),
                             Column('C_Ind_Quimicos', String),
                             Column('C_Ind_Farmaceuticos', String),
                             Column('C_Ind_Plastico', String),
                             Column('C_Ind_Minerales', String),
                             Column('C_Ind_Metalurgia', String),
                             Column('C_Ind_Metal', String),
                             Column('C_Ind_Electronico', String),
                             Column('C_Ind_Electrico', String),
                             Column('C_Ind_Maquinaria', String),
                             Column('C_Ind_Vehiculos', String),
                             Column('C_Ind_Transporte', String),
                             Column('C_Ind_Muebles', String),
                             Column('C_Ind_Manufactura', String),
                             Column('C_Ind_Agropecuario', String),
                             Column('C_Ind_Mineria', String),
                             Column('C_Ind_Desconocido', String),
                             Column('C_Industrial_Total', String),
                             Column('ConsumoFinal_Total', String)
                             )

# Households table schema
households_table = Table('Viviendas', metadata_obj,
                         Column('Año', Integer, nullable=False, unique=True),
                         Column('V_Urbano', String),
                         Column('V_Rural', String),
                         Column('Vivienda_Total', String)
                         )

# Losses Factor table schema
loss_table = Table('D_Perdidas', metadata_obj,
                   Column('Año', Integer, nullable=False, unique=True),
                   Column('NT1', String),
                   Column('NT2', String),
                   Column('NT3', String),
                   Column('Total', String)
                   )

# Cost associated with losses table schema
loss_cost_table = Table('D_Costos_Perdidas', metadata_obj,
                        Column('Año', Integer, nullable=False, unique=True),
                        Column('NT1', String),
                        Column('NT2', String),
                        Column('NT3', String),
                        Column('Total', String)
                        )

# Equivalent losses table schema
equivalent_losses_table = Table('D_Perdidas_Equivalentes', metadata_obj,
                                Column('Año', Integer,
                                       nullable=False, unique=True),
                                Column('NT1', String),
                                Column('NT2', String),
                                Column('NT3', String),
                                Column('Total', String)
                                )

# IAAD table schema
iaad_table = Table('D_IAAD', metadata_obj,
                   Column('Año', Integer,
                          nullable=False, unique=True),
                   Column('NT1', String),
                   Column('NT2_NT3', String),
                   Column('Total', String)
                   )

# D_Saidi_Saifi table schema
saidi_table = Table('D_Saidi', metadata_obj,
                    Column('Año', Integer,
                           nullable=False, unique=True),
                    Column('Saidi', String)
                    )

# D_Saidi_Saifi table schema
saifi_table = Table('D_Saifi', metadata_obj,
                    Column('Año', Integer,
                           nullable=False, unique=True),
                    Column('Saifi', String)
                    )
# Method that returns the table DESAGREGACION
# DATE: 14/06/2022

# Generation indicators table schema
desagregacion_table = Table('DESAGREGACION', metadata_obj,
                            Column('DESAGREGACION_ID', Integer,
                                   nullable=False, unique=True),
                            Column('DESAGREGACION_NOMBRE', String),
                            Column('REL_VARIABLES_DESAGREGACION', String)
                            )

# Method that returns the table RELACION_VARIABLES_INDICADORES
# DATE: 14/06/2022
# Variables relation for generation indicators table schema
rel_var_indic_table = Table('RELACION_VARIABLES_INDICADORES', metadata_obj,
                            Column('INDICADOR_ID', Integer,
                                   nullable=False, unique=True),
                            Column('INDICADOR_AGREGADO', String),
                            Column('FORMULA_RELACIONES', String),
                            Column('DESCRIPCION', String),
                            Column('VARIABLES', String)
                            )

# Method that returns the table data desagregation of generation
# DATE: 29/07/2022
# data for generation table schema

data_desag_gen_table = Table('DATOS_DESAGREGACION_GENERACION', metadata_obj,
                             Column('Año', Integer,
                                    nullable=False, unique=True),
                             Column('Participación_de_fuentes_fósiles', String),
                             Column('Participación_de_fuentes_hídricas', String),
                             Column('Participación_de_FNCER_en_matriz_energética', String),
                             Column('Eficiencia_de_centrales_hidroeléctricas', String),
                             Column('Eficiencia_de_centrales_térmicas', String),
                             Column('Eficiencia_de_centrales_de_auto_y_cogeneración', String),
                             Column('Eficiencia_de_centrales_solares', String),
                             Column('Eficiencia_de_centrales_eólicas', String),
                             Column('Intensidad_energética_primaria_de_centrales_hidroeléctricas', String),
                             Column('Intensidad_energética_primaria_de_centrales_térmicas', String),
                             Column('Intensidad_energética_primaria_de_centrales_de_auto_y_cogeneración', String),
                             Column('Emisiones_de_CO2eq_de_centrales_térmicas', String),
                             Column('Emisiones_de_CO2eq_de_centrales_de_auto_y_cogeneración', String),
                             Column('Intensidad_de_emisiones_de_centrales_térmicas', String),
                             Column('Intensidad_de_emisiones_de_centrales_de_auto_y_cogeneración', String),
                             Column('Emisiones_de_CO2eq_de_la_generación_eléctrica_SIN', String)
                             )

# distribution desagregation table schema
desagregation_dist_table = Table('DESAGREGACION_DISTRIBUCION', metadata_obj,
                                 Column('DESAGREGACION_ID', Integer,
                                        nullable=False, unique=True),
                                 Column('DESAGREGACION_NOMBRE', String),
                                 Column('REL_VARIABLES_DESAGREGACION', String)
                                 )

# Method that returns the table RELACION_VARIABLES_INDICADORES
# DATE: 14/06/2022
# Variables relation for distribution indicators table schema
rel_var_indic_dist_table = Table('RELACION_VARIABLES_INDICADORES_DISTRIBUCION', metadata_obj,
                                 Column('INDICADOR_ID', Integer,
                                        nullable=False, unique=True),
                                 Column('INDICADOR_AGREGADO', String),
                                 Column('FORMULA_RELACIONES', String),
                                 Column('DESCRIPCION', String),
                                 Column('VARIABLES', String)
                                 )

# Method that returns the table data desagregation of distribution
# DATE: 29/07/2022
# data for end use table schema
data_desag_dist_table = Table('DATOS_DESAGREGACION_DISTRIBUCION', metadata_obj,
                              Column('Año', Integer,
                                     nullable=False, unique=True),
                              Column('Factor_de_pérdidas_en_distribución_Nivel_de_Tensión_I', String),
                              Column('Factor_de_pérdidas_en_distribución_Nivel_de_Tensión_II', String),
                              Column('Factor_de_pérdidas_en_distribución_Nivel_de_Tensión_III', String),
                              Column('Costo_de_pérdidas_equivalentes_en_distribución_Nivel_de_Tensión_I', String),
                              Column('Costo_de_pérdidas_equivalentes_en_distribución_Nivel_de_Tensión_II', String),
                              Column('Costo_de_pérdidas_equivalentes_en_distribución_Nivel_de_Tensión_III', String),
                              Column('IAAD_Nivel_de_Tensión_I', String),
                              Column('IAAD_Nivel_de_Tensión_II_y_III', String),
                              Column('Saidi', String),
                              Column('Saifi', String)
                              )

# Method that returns the table DESAGREGACION
# DATE: 14/06/2022
# end use indicators table schema
desagregation_end_use_table = Table('DESAGREGACION_USO_FINAL', metadata_obj,
                                    Column('DESAGREGACION_ID', Integer,
                                           nullable=False, unique=True),
                                    Column('DESAGREGACION_NOMBRE', String),
                                    Column('REL_VARIABLES_DESAGREGACION', String)
                                    )

# Method that returns the table RELACION_VARIABLES_INDICADORES
# DATE: 14/06/2022
# Variables relation for end use indicators table schema
rel_var_indic_end_use_table = Table('RELACION_VARIABLES_INDICADORES_USO_FINAL', metadata_obj,
                                    Column('INDICADOR_ID', Integer,
                                           nullable=False, unique=True),
                                    Column('INDICADOR_AGREGADO', String),
                                    Column('FORMULA_RELACIONES', String),
                                    Column('DESCRIPCION', String),
                                    Column('VARIABLES', String)
                                    )

# Method that returns the table data desagregation of end use
# DATE: 29/07/2022
# data for end use table schema
data_desag_end_use_table = Table('DATOS_DESAGREGACION_USO_FINAL', metadata_obj,
                                 Column('Año', Integer,
                                        nullable=False, unique=True),
                                 Column('Consumo_residencial_per_cápita', String),
                                 Column('Consumo_per_cápita_urbano', String),
                                 Column('Consumo_per_cápita_rural', String),
                                 #Column('Consumo_residencial_por_vivienda', String),
                                 Column('Intensidad_energética_del_sector_industrial', String),
                                 Column('Intensidad_energética_del_sector_comercial_y_público', String)
                                 )

# Method that returns the table ESTRATEGIAS
# DATE: 16/03/2023
# end use indicators table schema
strategies_table = Table('ESTRATEGIAS', metadata_obj,
                         Column('ESTRATEGIA_ID', Integer,
                                nullable=False, unique=True),
                         Column('ESTRATEGIA_NOMBRE', String),
                         Column('MODELO_MATEMATICO', String),
                         Column('VARIABLES', String)
                         )

# Method that returns the table SUB_ESTRATEGIAS  by update
# DATE: 16/03/2023
# Variables relation for end use indicators table schema
sub_strategies_table = Table('SUB_ESTRATEGIA_GEN', metadata_obj,
                             Column('SUB_ESTRATEGIA_ID', Integer,
                                    nullable=False, unique=True),
                             Column('NOMBRE_SUB_ESTRATEGIA', String),
                             Column('ESTRATEGIA_ID', String)
                             )

# Method that returns the table SUB_ESTRATEGIAS  by update
# DATE: 16/03/2023
# Variables relation for end use indicators table schema
sub_strategies_distribution_table = Table('SUB_ESTRATEGIA_DISTRIBUTION', metadata_obj,
                                          Column('SUB_ESTRATEGIA_ID', Integer,
                                                 nullable=False, unique=True),
                                          Column('NOMBRE_SUB_ESTRATEGIA', String),
                                          Column('ESTRATEGIA_ID', String)
                                          )

# Method that returns the table SUB_ESTRATEGIAS  by expansion
# DATE: 16/03/2023
# Variables relation for end use indicators table schema
sub_strategies_table_exp = Table('SUB_ESTRATEGIA_GEN_EXP', metadata_obj,
                                 Column('SUB_ESTRATEGIA_ID', Integer,
                                        nullable=False, unique=True),
                                 Column('NOMBRE_SUB_ESTRATEGIA', String),
                                 Column('ESTRATEGIA_ID', String)
                                 )

# Method that returns the table VAR_SUB_ESTRATEGIAS
# DATE: 16/03/2023
# data for end use table schema
var_sub_strategies_table = Table('VARIABLES_SUB_ESTRATEGIA_GEN', metadata_obj,
                                 Column('VARIABLE_SUB_ESTRATEGIA_ID', String),
                                 Column('NOMBRE_VARIABLE', String),
                                 Column('SUB_ESTRATEGIA_ID', String)
                                 )

# Method that returns the table SUB_ESTRATEGIAS by update for end use
# DATE: 16/03/2023
# Variables relation for end use indicators table schema
sub_strategies_end_use_table = Table('SUB_ESTRATEGIA_END_USE', metadata_obj,
                                     Column('SUB_ESTRATEGIA_ID', Integer,
                                            nullable=False, unique=True),
                                     Column('NOMBRE_SUB_ESTRATEGIA', String),
                                     Column('ESTRATEGIA_ID', String)
                                     )

# Method that returns the table SUB_ESTRATEGIAS by expansion for end use
# DATE: 16/03/2023
# Variables relation for end use indicators table schema
sub_strategies_end_use_update_table = Table('SUB_ESTRATEGIA_END_USE_UPDATE', metadata_obj,
                                            Column('SUB_ESTRATEGIA_ID', Integer,
                                                   nullable=False, unique=True),
                                            Column('NOMBRE_SUB_ESTRATEGIA', String),
                                            Column('ESTRATEGIA_ID', String)
                                            )

projections_generation_table = Table('proyeccion_escenario_bau_generacion', metadata_obj,
                                     Column('Año', Integer,
                                            nullable=False, unique=True),
                                     Column('Generacion_Total', String)
                                     )

projections_distribution_table = Table('proyeccion_escenario_bau_distribucion', metadata_obj,
                                       Column('Año', Integer,
                                              nullable=False, unique=True),
                                       Column('Factor_de_pérdidas', String)
                                       )

projections_end_use_table = Table('proyeccion_escenario_bau_uso_final', metadata_obj,
                                  Column('Año', Integer,
                                         nullable=False, unique=True),
                                  Column('Consumo_eléctrico_total', String)
                                  )

'''
function saveDateStrategies
'''
table_save_strategies = Table("SAVE_STRATEGY", metadata_obj,
                        Column("id", Integer,
                                primary_key=True, nullable=False, autoincrement=True),
                        Column("strategy_name", String),
                        Column("user", String),
                        Column("type", String),
                        Column("anio", Integer),
                        Column("environmental_indicator", Integer),
                        Column("economic_indicator", Integer),
                        Column("energy_indicator", Integer),
                        Column("date", String),
                        Column("update_date", String)
                        )
table_save_strategies_values = Table("SAVE_STRATEGY_VALUES", metadata_obj,
                        Column("id", Integer,
                                primary_key=True, nullable=False, autoincrement=True),
                        Column("id_strategy_name", Integer),
                        Column("id_strategy", String),
                        Column("id_sub_strategy", String),
                        Column("value", String),
                        Column("value_aux", String)
                        )

'''engine = create_engine("sqlite:///app/sqlite/NewDB.db")
metadata_obj.reflect(engine, only=['users', 'login'])
Base = automap_base(metadata=metadata_obj)

Base.prepare()
for element in Base.classes:
    print(element)
Users, Login = Base.classes.users, Base.classes.login
admin.add_view(ModelView(Users, db.session))'''
# END schema definition

_translating_dict = {'NT1': 'Nivel de tensión 1',
                     'NT2': 'Nivel de tensión 2',
                     'NT3': 'Nivel de tensión 3',
                     'NT2_NT3': 'Niveles de tensión 2 y 3',
                     'Total': 'Total',

                     'CH_Agua': 'Centrales hidroeléctricas',
                     'CT_ACPM': 'Centrales térmicas de ACPM',
                     'CT_Carbon': 'Centrales térmicas de Carbón',
                     'CT_Combustoleo': 'Centrales térmicas de Combustoleo',
                     'CT_Gas': 'Centrales térmicas de Gas natural',
                     'CT_GasNI': 'Centrales térmicas de Gas NI',
                     'CT_JETA1': 'Centrales térmicas de JETA1',
                     'CT_Mezclas': 'Centrales térmicas de Mezclas',
                     'CT_Querosene': 'Centrales térmicas de Querosene',
                     'CT_Bagazo': 'Centrales térmicas de Bagazo',
                     'CT_Biogas': 'Centrales térmicas de Biogás',
                     'CT_Biomasa': 'Centrales térmicas de Biomasa',
                     'CT_RadSol': 'Centrales térmicas de RadSol',
                     'CT_Total': 'Centrales térmicas totales',
                     'CE_Viento': 'Centrales Eólicas',
                     'CS_Sol': 'Centrales Solares',
                     'CAyC_Bagazo': 'Centrales auto y cogeneración con Bagazo',
                     'CAyC_Biomasa': 'Centrales auto y cogeneración con Biomasa',
                     'CAyC_Carbon': 'Centrales auto y cogeneración con Carbón',
                     'CAyC_Gas': 'Centrales auto y cogeneración con Gas natural',
                     'CAyC_SIN_Total': 'Centrales auto y cogeneración SIN Total',
                     'CAyC_NoSIN_Total': 'Centrales auto y cogeneración NO - SIN Total',
                     'CAyC_Total': 'Centrales auto y cogeneración Total',
                     'Porcentaje_CAyC_SIN': 'Porcentaje centrales auto y cogeneración SIN',
                     'Generacion_fosiles_Total': 'Generación fósil total',
                     'Generacion_FNCE_Total': 'Generación FNCE total',
                     'Generacion_SIN_Total': 'Generación SIN total',
                     'Generacion_Total': 'Generación total',
                     'Consumo_eléctrico_total': 'Consumo eléctrico total',
                     'Factor_de_pérdidas': 'Factor de pérdidas',

                     'C_CH_Agua_GWh': 'Consumo en centrales hidroeléctricas',
                     'C_CT_carbon_GWh': 'Consumo en centrales térmicas de Carbón',
                     'C_CT_Gas_GWh': 'Consumo en centrales térmicas de Gas natural',
                     'C_CT_Diesel_GWh': 'Consumo en centrales térmicas de Diesel',
                     'C_CT_Fueloil_GWh': 'Consumo en centrales térmicas de Fueloil',
                     'C_CT_Kerosene_GWh': 'Consumo en centrales térmicas de Kerosene',
                     'C_CT_Total_GWh': 'Consumo total en centrales térmicas',
                     #'C_CE_Viento_GWh': 'Consumo en centrales eólicas',
                     #'C_CS_Sol_GWh': 'Consumo en centrales solares',
                     'C_CAyC_Bagazo_GWh': 'Consumo de Bagazo en centrales AyC',
                     'C_CAyC_Carbon_GWh': 'Consumo de Carbón en centrales AyC',
                     'C_CAyC_Gas_GWh': 'Consumo de Gas natural en centrales AyC',
                     #'C_CAyC_Hidro_GWh': 'Consumo de Hidro en centrales AyC',
                     'C_CAyC_Petroleo_GWh': 'Consumo de Petróleo en centrales AyC',
                     #'C_CAyC_Renovables_GWh': 'Consumo de Renovables en centrales AyC',
                     'C_CAyC_Diesel_GWh': 'Consumo de Diesel en centrales AyC',
                     'C_CAyC_Gaslicuado_GWh': 'Consumo de Gas licuado en centrales AyC',
                     'C_CAyC_Total': 'Consumo total en centrales AyC',
                     'Consumo_Total': 'Consumo total de la generación eléctrica',

                     'ECO2_CT_Carbon': 'Emisiones $CO_2$ Centrales Térmicas de Carbón',
                     'ECO2_CT_Gas': 'Emisiones $CO_2$ Centrales Térmicas de Gas natural',
                     'ECO2_CT_Diesel': 'Emisiones $CO_2$ Centrales Térmicas de Diesel',
                     'ECO2_CT_Fueloil': 'Emisiones $CO_2$ Centrales Térmicas de Fueloil',
                     'ECO2_CT_Kerosene': 'Emisiones $CO_2$ Centrales Térmicas de Kerosene',
                     'ECO2_CAyC_Bagazo': 'Emisiones $CO_2$ Centrales auto y cogeneración con Bagazo',
                     'ECO2_CAyC_Carbon': 'Emisiones $CO_2$ Centrales auto y cogeneración con Carbón',
                     'ECO2_CAyC_Gas': 'Emisiones $CO_2$ Centrales auto y cogeneración con Gas natural',
                     'ECO2_CAyC_Petroleo': 'Emisiones $CO_2$ Centrales auto y cogeneración con Petróleo',
                     'ECO2_CAyC_Diesel': 'Emisiones $CO_2$ Centrales auto y cogeneración con Diesel',
                     'ECO2_CAyC_Gaslicuado': 'Emisiones $CO_2$ Centrales auto y cogeneración con Gas licuado',
                     'EmisionCO2_Total': 'Emisiones $CO_2eq$ Total',
                     'EmisionCO2_SIN_Total': 'Emisión $CO_2eq$ SIN Total',
                     'EmisionCO2_CT_Total': 'Emisión $CO_2eq$ Centrales Térmicas Total',
                     'EmisionCO2_CAyC_Total': 'Emisión $CO_2eq$ Centrales Auto y Cogeneración Total',
                     'EmisionCO2_Carbon': 'Emisiones $CO_2eq$ por Carbón',
                     'EmisionesCO2_Gas': 'Emisiones $CO_2eq$ por Gas natural',
                     'EmisionesCO2_Diesel': 'Emisiones $CO_2eq$ por Diesel',
                     'EmisionesCO2_Fueloil': 'Emisiones $CO_2eq$ por Fueloil',
                     'EmisionesCO2_Petroleo': 'Emisiones $CO_2eq$ por Petróleo',
                     'EmisionesCO2_Gaslicuado': 'Emisiones $CO_2eq$ por Gas licuado',
                     'EmisionesCO2_Bagazo': 'Emisiones $CO_2eq$ por Bagazo',

                     'PIB_Total': 'PIB Total',
                     'PIB_Agro': 'Agro',
                     'PIB_Agro_Cultivos': 'Agro Cultivos',
                     'PIB_Agro_Cafe': 'Agro Café',
                     'PIB_Agro_Ganado': 'Agro Ganado',
                     'PIB_Agro_Madera': 'Agro Madera',
                     'PIB_Agro_Pesca': 'Agro Pesca',
                     'PIB_Minas': 'Minas',
                     'PIB_Minas_Carbon': 'Minas Carbón',
                     'PIB_Minas_Petroleo': 'Minas Petróleo',
                     'PIB_Minas_Metales': 'Minas Metales',
                     'PIB_Minas_Canteras': 'Minas Canteras',
                     'PIB_Minas_Otros': 'Minas Otros',
                     'PIB_Alimentos': 'Alimentos',
                     'PIB_Alimentos_Carne': 'Alimentos Carne',
                     'PIB_Alimentos_Aceite': 'Alimentos Aceite',
                     'PIB_Alimentos_Lacteos': 'Alimentos Lácteos',
                     'PIB_Alimentos_Almidon': 'Alimentos Almidón',
                     'PIB_Alimentos_Cafe': 'Alimentos Café',
                     'PIB_Alimentos_Azucar': 'Alimentos Azúcar',
                     'PIB_Alimentos_Cacao': 'Alimentos Cacao',
                     'PIB_Alimentos_Frutas': 'Alimentos Frutas',
                     'PIB_Alimentos_Bebidas': 'Alimentos Bebidas',
                     'PIB_Textiles': 'Textiles',
                     'PIB_Textiles_Confeccion': 'Textiles Confecciones',
                     'PIB_Textiles_Cuero': 'Textiles Cueros',
                     'PIB_Madera': 'Madera',
                     'PIB_Madera_Transformacion': 'Madera Transformación',
                     'PIB_Madera_Papel': 'Madera Papel',
                     'PIB_Madera_Impresion': 'Madera Impresión',
                     'PIB_Quimica': 'Quimica',
                     'PIB_Quimica_Refinacion': 'Química Refinación',
                     'PIB_Quimica_Otros': 'Química Otros',
                     'PIB_Quimica_Plastico': 'Químico Plástico',
                     'PIB_Quimica_Minerales': 'Químico Mineral',
                     'PIB_Metales': 'Metales',
                     'PIB_Metales_Basicos': 'Metales Básicos',
                     'PIB_Metales_Electrico': 'Metales Eléctrico',
                     'PIB_Metales_Maquinaria': 'Metales Maquinaria',
                     'PIB_Metales_Vehiculos': 'Metales Vehículos',
                     'PIB_Muebles': 'Muebles',
                     'PIB_Muebles_Colchones': 'Muebles Colchones',
                     'PIB_Muebles_Otros': 'Muebles Otros',
                     'PIB_Electricidad': 'Electricidad',
                     'PIB_Electricidad_GTD': 'Electricidad GTD',
                     'PIB_Electricidad_Gas': 'Electricidad Gas',
                     'PIB_Agua': 'Agua',
                     'PIB_Agua_Tratamiento': 'Agua Tratamiento',
                     'PIB_Agua_Residuales': 'Agua Residuales',
                     'PIB_Agua_Reciclaje': 'Agua Reciclaje',
                     'PIB_Edificaciones': 'Edificaciones',
                     'PIB_Carreteras': 'Carreteras',
                     'PIB_Civil': 'Civil',
                     'PIB_Comercio': 'Comercio',
                     'PIB_Comercio_Vehiculos': 'Comercio Vehículos',
                     'PIB_Comercio_Mantenimiento': 'Comercio Mantenimiento',
                     'PIB_Transporte': 'Transporte',
                     'PIB_Transporte_Terrestre': 'Transporte Terrestre',
                     'PIB_Transporte_Acuatico': 'Transporte Acuático',
                     'PIB_Transporte_Aereo': 'Transporte Aéreo',
                     'PIB_Transporte_almacenamiento': 'Transporte almacenamiento',
                     'PIB_Transporte_Correo': 'Transporte Correo',
                     'PIB_Alojamiento': 'Alojamiento',
                     'PIB_Información': 'Información',
                     'PIB_Financieras': 'Financieras',
                     'PIB_Inmobiliarias': 'Inmobiliarias',
                     'PIB_Profesionales': 'Profesionales',
                     'PIB_Profesionales_Cientificas': 'Profesionales Científicas',
                     'PIB_Profesionales_Servicios': 'Profesionales Servicios',
                     'PIB_Administracion': 'Administración',
                     'PIB_Educacion': 'Educación',
                     'PIB_Educacion_Mercado': 'Educación Mercado',
                     'PIB_Educacion_NoMercado': 'Educación No Mercado',
                     'PIB_Salud': 'Salud',
                     'PIB_Entretenimiento': 'Entretenimiento',
                     'PIB_Hogar': 'Hogar',
                     'PIB_Industria_Total': 'Industria Total',
                     'PIB_ComercialyPublico_Total': 'Comercial y Publico Total',

                     # 'PIB_Total': 'PIB Total USD',
                     'PIBUSD_Agro': 'Agro',
                     'PIBUSD_Agro_Cultivos': 'Agro Cultivos',
                     'PIBUSD_Agro_Cafe': 'Agro Café',
                     'PIBUSD_Agro_Ganado': 'Agro Ganado',
                     'PIBUSD_Agro_Madera': 'Agro Madera',
                     'PIBUSD_Agro_Pesca': 'Agro Pesca',
                     'PIBUSD_Minas': 'Minas',
                     'PIBUSD_Minas_Carbon': 'Minas Carbón',
                     'PIBUSD_Minas_Petroleo': 'Minas Petróleo',
                     'PIBUSD_Minas_Metales': 'Minas Metales',
                     'PIBUSD_Minas_Canteras': 'Minas Canteras',
                     'PIBUSD_Minas_Otros': 'Minas Otros',
                     'PIBUSD_Alimentos': 'Alimentos',
                     'PIBUSD_Alimentos_Carne': 'Alimentos Carne',
                     'PIBUSD_Alimentos_Aceite': 'Alimentos Aceite',
                     'PIBUSD_Alimentos_Lacteos': 'Alimentos Lácteos',
                     'PIBUSD_Alimentos_Almidon': 'Alimentos Almidón',
                     'PIBUSD_Alimentos_Cafe': 'Alimentos Café',
                     'PIBUSD_Alimentos_Azucar': 'Alimentos Azúcar',
                     'PIBUSD_Alimentos_Cacao': 'Alimentos Cacao',
                     'PIBUSD_Alimentos_Frutas': 'Alimentos Frutas',
                     'PIBUSD_Alimentos_Bebidas': 'Alimentos Bebidas',
                     'PIBUSD_Textiles': 'Textiles',
                     'PIBUSD_Textiles_Confeccion': 'Textiles Confecciones',
                     'PIBUSD_Textiles_Cuero': 'Textiles Cueros',
                     'PIBUSD_Madera': 'Madera',
                     'PIBUSD_Madera_Transformacion': 'Madera Transformación',
                     'PIBUSD_Madera_Papel': 'Madera Papel',
                     'PIBUSD_Madera_Impresion': 'Madera Impresión',
                     'PIBUSD_Quimica': 'Química',
                     'PIBUSD_Quimica_Refinacion': 'Química Refinación',
                     'PIBUSD_Quimica_Otros': 'Química Otros',
                     'PIBUSD_Quimica_Plastico': 'Química Plástico',
                     'PIBUSD_Quimica_Minerales': 'Química Minerales',
                     'PIBUSD_Metales': 'Metales',
                     'PIBUSD_Metales_Basicos': 'Metales Básicos',
                     'PIBUSD_Metales_Electrico': 'Metales Eléctrico',
                     'PIBUSD_Metales_Maquinaria': 'Metales Maquinaria',
                     'PIBUSD_Metales_Vehiculos': 'Metales Vehículos',
                     'PIBUSD_Muebles': 'Muebles',
                     'PIBUSD_Muebles_Colchones': 'Muebles Colchones',
                     'PIBUSD_Muebles_Otros': 'Muebles Otros',
                     'PIBUSD_Electricidad': 'Electricidad',
                     'PIBUSD_Electricidad_GTD': 'Electricidad GTD',
                     'PIBUSD_Electricidad_Gas': 'Electricidad Gas',
                     'PIBUSD_Agua': 'Agua',
                     'PIBUSD_Agua_Tratamiento': 'Agua Tratamiento',
                     'PIBUSD_Agua_Residuales': 'Agua Residuales',
                     'PIBUSD_Agua_Reciclaje': 'Agua Reciclaje',
                     'PIBUSD_Edificaciones': 'Edificaciones',
                     'PIBUSD_Carreteras': 'Carreteras',
                     'PIBUSD_Civil': 'Civil',
                     'PIBUSD_Comercio': 'Comercio',
                     'PIBUSD_Comercio_Vehiculos': 'Comercio Vehículos',
                     'PIBUSD_Comercio_Mantenimiento': 'Comercio Mantenimiento',
                     'PIBUSD_Transporte': 'Transporte',
                     'PIBUSD_Transporte_Terrestre': 'Transporte Terrestre',
                     'PIBUSD_Transporte_Acuatico': 'Transporte Acuático',
                     'PIBUSD_Transporte_Aereo': 'Transporte Aéreo',
                     'PIBUSD_Transporte_almacenamiento': 'Transporte almacenamiento',
                     'PIBUSD_Transporte_Correo': 'Transporte Correo',
                     'PIBUSD_Alojamiento': 'Alojamiento',
                     'PIBUSD_Información': 'Información',
                     'PIBUSD_Financieras': 'Financieras',
                     'PIBUSD_Inmobiliarias': 'Inmobiliarias',
                     'PIBUSD_Profesionales': 'Profesionales',
                     'PIBUSD_Profesionales_Cientificas': 'Profesionales Científicas',
                     'PIBUSD_Profesionales_Servicios': 'Profesionales Servicios',
                     'PIBUSD_Administracion': 'Administración',
                     'PIBUSD_Educacion': 'Educación',
                     'PIBUSD_Educacion_Mercado': 'Educación Mercado',
                     'PIBUSD_Educacion_NoMercado': 'Educación No Mercado',
                     'PIBUSD_Salud': 'Salud',
                     'PIBUSD_Entretenimiento': 'Entretenimiento',
                     'PIBUSD_Hogar': 'Hogar',
                     'PIBUSD_Industria_Total': 'Industria Total',
                     'PIBUSD_ComercialyPublico_Total': 'Comercial y Publico Total',

                     'P_Urbano': 'Población Urbana',
                     'P_Rural': 'Población Rural',
                     'Poblacion_Total': 'Población Total',

                     'C_Residencial_U': 'Consumo residencial Urbana',
                     'C_Residencia_R': 'Consumo residencial Rural',
                     'C_Residencial_Total': 'Consumo residencial Total',
                     'C_CyP_Total': 'Consumo CyP Total',
                     'C_Ind_Alimentos': 'Consumo industria de Alimentos',
                     'C_Ind_Bebidas': 'Consumo industria de Bebidas',
                     'C_Ind_Tabaco': 'Consumo industria de Tabaco',
                     'C_Ind_Textil': 'Consumo industria de Textiles',
                     'C_Ind_Vestimenta': 'Consumo industria de Vestimenta',
                     'C_Ind_Marroquineria': 'Consumo industria de Marroquinería',
                     'C_Ind_Madera': 'Consumo industria de Madera',
                     'C_Ind_Papel': 'Consumo industria de Papel',
                     'C_Ind_Impresion': 'Consumo industria de Impresión',
                     'C_Ind_Refinerias': 'Consumo industria de Refinerías',
                     'C_Ind_Quimicos': 'Consumo industria de Químicos',
                     'C_Ind_Farmaceuticos': 'Consumo industria de Farmacéuticos',
                     'C_Ind_Plastico': 'Consumo industria de Plástico',
                     'C_Ind_Minerales': 'Consumo industria de Minerales',
                     'C_Ind_Metalurgia': 'Consumo industria de Metalurgia',
                     'C_Ind_Metal': 'Consumo industria del Metal',
                     'C_Ind_Electronico': 'Consumo industria de Electrónicos',
                     'C_Ind_Electrico': 'Consumo industria Eléctrica',
                     'C_Ind_Maquinaria': 'Consumo industria de Maquinaria',
                     'C_Ind_Vehiculos': 'Consumo industria de Vehículos',
                     'C_Ind_Transporte': 'Consumo industria de Transporte',
                     'C_Ind_Muebles': 'Consumo industria de Muebles',
                     'C_Ind_Manufactura': 'Consumo industria de Manufactura',
                     'C_Ind_Agropecuario': 'Consumo industria Agropecuaria',
                     'C_Ind_Mineria': 'Consumo industria de Minería',
                     'C_Ind_Desconocido': 'Consumo industrial Desconocido',
                     'C_Industrial_Total': 'Consumo industrial Total ',
                     'ConsumoFinal_Total': 'Consumo Total',

                     'V_Urbano': 'Viviendas Zona Urbana',
                     'V_Rural': 'Viviendas  Zona Rural',
                     'Vivienda_Total': 'Viviendas Total',

                     'DESAGREGACION_ID': 'N°',
                     'DESAGREGACION_NOMBRE': 'Indicador desagregado',
                     'FORMULA_RELACIONES': 'Fórmula',
                     'INDICADOR_AGREGADO': 'Indicador agregado',
                     'INDICADOR_ID': 'ID Ind. Agregado'
                     }

_unit_dict = {'Consumo de fuentes primarias por tipo de central eléctrica': 'GWh',
              'Emisiones de CO2 equivalentes': 'gCO2eq/Wh',
              'Generación eléctrica por fuente primaria': 'GWh',
              'Costo de Pérdidas': 'Millones de USD',
              'Factor de Pérdidas': 'Porcentaje %',
              'Pérdidas Equivalentes': 'MWh/año',
              'IAAD': 'IAAD',
              'PIB': 'Miles de Millones de COP [base 2015]',
              'PIB en USD': 'Billones de USD [base 2015]',
              'Población': 'N° de personas (Millones)',
              'Uso final de la energía': 'GWh',
              'Viviendas': 'N° de viviendas (Millones)',
              'Participación en la generación eléctrica': 'Porcentaje %',
              'Eficiencia de la generación eléctrica': 'Porcentaje %',
              'Intensidad energética primaria de la generación eléctrica': 'kWh/USD',
              'Emisiones de CO2eq de la generación eléctrica': 'MtCO2eq',
              'Emisiones de $CO_2eq$ de la generación eléctrica Total': 'MtCO2eq',
              'Intensidad de emisión de la generación eléctrica': 'gCO2eq/USD',
              'Consumo per cápita': 'MWh/persona',
              'Intensidad energética del uso final de la energía eléctrica': 'kWh/USD',
              'Factor de pérdidas en distribución (SOLO ADD)': 'Porcentaje %',
              'Costo de pérdidas equivalentes en distribución (SOLO ADD)': 'Millones USD',
              'Índice Anual Acumulado de Discontinuidad - IAAD': 'Porcentaje %',
              'Saidi': 'h / año',
              'Saifi': '# ocurrencia / año',
              'Consumo eléctrico total': 'Gwh',
              'Factor de pérdidas': 'Porcentaje %',
              'Generación total': 'Gwh',
              'Estrategias de actualización': 'Consumo eléctrico(Gwh)',
              'Estrategias de expansión': 'Generación eléctrica(Gwh)',
              'Indicador de eficiencia energética': 'Porcentaje %',
              'Indicador intensidad energética primaria': 'kWh/USD',
              'Indicador intensidad de emisiones de carbono': 'gCO2eq/USD',
              'Estrategias de electrificación en el transporte': 'Consumo eléctrico(GWh)',
              'Estrategias de actualización tecnológica': 'Consumo eléctrico(GWh)',
              'Indicador consumo per cápita': 'MWh/persona',
              'Indicador intensidad energética': 'kWh/USD',
              'Indicador emisiones evitadas': 'MtCO2eq',
              'Digitalización y gestión de la medida': 'Porcentaje %',
              'Indicador de factor de pérdidas': 'Porcentaje %',
              'Indicador costo equivalente a pérdidas': 'Millones USD',
              'Indicador emisiones equivalentes de las pérdidas de distribución': 'TCO2eq/año',
              }


class SQLConnector:
    """Platform server connection class

    Contains the constructor for the connection and execution methods for requests to the database.
    """

    def __init__(self) -> None:
        """Parameterized constructor
        """
        self.engine = create_engine('sqlite:///app/sqlite/TestDB.db')
        self.connection = self.engine.connect()

    def get_user(self, user):
        """Get user from login table by username

        Args:
            user (str): user identification. 

        Returns:
            dict: query result of the --select-- on the login table for the given user credentials.
        """
        query = select(login_table).where(
            login_table.c.user == user)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        result.close()
        return rows

    def get_user_data(self, id_login):
        """Select data from users table

        Args:
            id_login (str): id for user login identification. 

        Returns:
            dict: query result of the --select-- on the user table for the given id.
        """
        query = select(users_table).where(
            users_table.c.id_login == id_login)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        result.close()
        return rows

    # Incompleto
    # Verificación y creación de usuario
    def set_user(self, user, password):
        """Save users credential on database

        Args:
            user (str): user identification.
            password (str -hash value-): user-provided password.

        Returns:
            dict: query result from validation --select-- for the given user credentials.
        """
        query_1 = insert(login_table).values(user=user, password=password)
        result = self.engine.execute(query_1)

        query_2 = select(login_table).where(login_table.c.user == user)
        result = self.engine.execute(query_2)
        columns = [col for col in result.keys()]
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        result.close()
        return rows

    def set_user_data(self, id_login, name, organization):
        """Save users information on database

        Args:
            id_login (int): index of login table from method 
            name (_type_): _description_
            organization (_type_): _description_
        """
        query_1 = insert(users_table).values(id_login=id_login, name=name, organization=organization)
        result = self.engine.execute(query_1)

    def get_emissions(self):
        query = select(emission_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Emisiones de CO2 equivalentes': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_generation(self):
        query = select(generation_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Generación eléctrica por fuente primaria': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_consumption(self):
        query = select(consumption_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Consumo de fuentes primarias por tipo de central eléctrica': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_iaad(self):
        query = select(iaad_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'IAAD': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_saidi(self):
        query = select(saidi_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Saidi': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_saifi(self):
        query = select(saifi_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Saifi': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    # ---funciones para generacion ---
    def get_desagregation(self):
        query = select(desagregacion_table)

        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Desagregacion': [dict(zip(columns, row)) for row in result.fetchall()]}

        # print(f" rows_desagregacion : {rows}")
        result.close()

        return rows

    def get_rel_var_indic(self):
        query = select(rel_var_indic_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Indicadores': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_data_desag_gen(self):
        query = select(data_desag_gen_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Data': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    # --- Funciones para distribucion ---
    def get_desagregation_dist(self):
        query = select(desagregation_dist_table)

        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Desagregacion': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_rel_var_indic_dist(self):
        query = select(rel_var_indic_dist_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Indicadores': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_data_desag_dist(self):
        query = select(data_desag_dist_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Data': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    # --- Funciones para uso final ---
    def get_desagregation_end_use(self):
        query = select(desagregation_end_use_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Desagregacion': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_rel_var_indic_end_use(self):
        query = select(rel_var_indic_end_use_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Indicadores': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_data_desag_end_use(self):
        query = select(data_desag_end_use_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Data': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_gen_strategies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query = select(strategies_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'estrategias': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_gen_sub_strategies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query = select(sub_strategies_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Estrategias de expansión': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_gen_sub_strategies_exp(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query = select(sub_strategies_table_exp)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Estrategias de actualización': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_gen_var_sub_strategies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query = select(var_sub_strategies_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'variables': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_dist_sub_strategies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query = select(sub_strategies_distribution_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {
            'Digitalización y gestión de la medida': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_end_use_sub_strategies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query = select(sub_strategies_end_use_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {
            'Estrategias de electrificación en el transporte': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_end_use_sub_strategies_update(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query = select(sub_strategies_end_use_update_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Estrategias de actualización tecnológica': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()

        return rows

    def get_projections_gen(self):
        query = select(projections_generation_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Generación': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_projections_dist(self):
        query = select(projections_distribution_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Distribución': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_projections_end_use(self):
        query = select(projections_end_use_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Uso final': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_loss(self):
        query = select(loss_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Factor de Pérdidas': [dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_loss_cost(self):
        query = select(loss_cost_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Costo de Pérdidas': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_equivalent_losses(self):
        query = select(equivalent_losses_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Pérdidas Equivalentes': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_pib(self):
        query = select(pib_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'PIB': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_pib_usd(self):
        query = select(pib_usd_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'PIB en USD': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_population(self):
        query = select(population_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Población': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_households(self):
        query = select(households_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Viviendas': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_end_use_energy(self):
        query = select(end_use_energy_table)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        rows = {'Uso final de la energía': [
            dict(zip(columns, row)) for row in result.fetchall()]}
        result.close()
        return rows

    def get_indicators(self):
        indicators_dict = {}
        _dict = {}
        # distribution_dict.update(self.get_desagregation())
        indicators_dict.update(self.get_rel_var_indic())
        indicators_dict.update(self.get_desagregation())
        indicators_dict.update(self.get_data_desag_gen())
        # print(f"indicators_dict:  {indicators_dict}")
        _dict.update({'generation': indicators_dict})

        end_use_dict_dist = {}
        end_use_dict_dist.update(self.get_rel_var_indic_dist())
        end_use_dict_dist.update(self.get_desagregation_dist())
        end_use_dict_dist.update(self.get_data_desag_dist())

        _dict.update({'distribution': end_use_dict_dist})

        end_use_dict_ind = {}
        end_use_dict_ind.update(self.get_rel_var_indic_end_use())
        end_use_dict_ind.update(self.get_desagregation_end_use())
        end_use_dict_ind.update(self.get_data_desag_end_use())

        _dict.update({'end_use': end_use_dict_ind})
        return _dict

    def get_strategies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        _dict_strategies = {}
        _dict_gen_strategies = {}
        # _dict_gen_strategies.update(self.get_gen_strategies())
        _dict_gen_strategies.update(self.get_gen_sub_strategies())
        _dict_gen_strategies.update(self.get_gen_sub_strategies_exp())
        # _dict_gen_strategies.update(self.get_gen_var_sub_strategies())

        _dict_strategies.update({'generation': _dict_gen_strategies})

        _dist_dist_strategies = {}
        _dist_dist_strategies.update(self.get_dist_sub_strategies())

        _dict_strategies.update({'distribution': _dist_dist_strategies})

        # _dict_end_use_strategies = {}
        # _dict_end_use_strategies.update(self.)
        # _dict_end_use_strategies.update(self.)
        # _dict_end_use_strategies.update(self.)
        _dict_end_use_strategies = {}
        _dict_end_use_strategies.update(self.get_end_use_sub_strategies())
        _dict_end_use_strategies.update(self.get_end_use_sub_strategies_update())
        _dict_strategies.update({'end_use': _dict_end_use_strategies})

        # _dict_strategies.update({'end_use':_dict_end_use_strategies})
        return _dict_strategies

    def get_description_strategies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        _dict_desc_strategies = {}
        _dict_gen_strategies = {}
        _dict_gen_strategies.update(self.get_gen_strategies())
        _dict_gen_strategies.update(self.get_gen_var_sub_strategies())

        _dict_desc_strategies.update({'description_strategies': _dict_gen_strategies})

        # _dist_dist_strategies = {}
        # _dist_dist_strategies.update(self.)
        # _dist_dist_strategies.update(self.)
        # _dist_dist_strategies.update(self.)

        # _dict_strategies.update({'distribution':_dist_dist_strategies})

        # _dict_end_use_strategies = {}
        # _dict_end_use_strategies.update(self.)
        # _dict_end_use_strategies.update(self.)
        # _dict_end_use_strategies.update(self.)

        # _dict_strategies.update({'end_use':_dict_end_use_strategies})
        return _dict_desc_strategies

    def get_projections(self):
        _dict = {}
        projections_gen_dict = {}
        projections_gen_dict.update(self.get_projections_gen())
        _dict.update({'generation': projections_gen_dict})

        projections_dist_dict = {}
        projections_dist_dict.update(self.get_projections_dist())
        _dict.update({'distribution': projections_dist_dict})

        projections_end_use_dict = {}
        projections_end_use_dict.update(self.get_projections_end_use())
        _dict.update({'end_use': projections_end_use_dict})

        return _dict

    # function return dictionary data table information for calc interface
    # date: 27/07/2022
    # dev: Alex Pinchao

    def get_data_table(self):
        indicators_dict = {}
        _dict = {}
        # distribution_dict.update(self.get_desagregation())
        indicators_dict.update(self.get_rel_var_indic())
        indicators_dict.update(self.get_desagregation())
        # print(f"indicators_dict:  {indicators_dict}")
        _dict.update({'generation': indicators_dict})
        end_use_dict_ind = {}
        end_use_dict_ind.update(self.get_rel_var_indic_end_use())
        end_use_dict_ind.update(self.get_desagregation_end_use())

        _dict.update({'end_use': end_use_dict_ind})
        return _dict

    def get_distribution(self):
        distribution_dict = {}
        _dict = {}
        distribution_dict.update(self.get_iaad())
        distribution_dict.update(self.get_loss())
        distribution_dict.update(self.get_loss_cost())
        distribution_dict.update(self.get_equivalent_losses())
        distribution_dict.update(self.get_saidi())
        distribution_dict.update(self.get_saifi())
        _dict.update({'distribution': distribution_dict})
        generation_dict = {}
        generation_dict.update(self.get_generation())
        generation_dict.update(self.get_emissions())
        generation_dict.update(self.get_consumption())
        _dict.update({'generation': generation_dict})
        end_use_dict = {}
        end_use_dict.update(self.get_pib())
        end_use_dict.update(self.get_pib_usd())
        end_use_dict.update(self.get_population())
        end_use_dict.update(self.get_households())
        end_use_dict.update(self.get_end_use_energy())
        _dict.update({'end_use': end_use_dict})
        return _dict, _translating_dict

    def update_strategy_with_id(self, id, new_data_values, new_indicators_values):
        """Save users credential on database

        Args:
            user (str): user identification.
            password (str -hash value-): user-provided password.

        Returns:
            dict: query result from validation --select-- for the given user credentials.
        """
        print(f"id: {id}")
        fecha_actual = datetime.datetime.today()
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
        data_insert = json.loads(new_indicators_values)
        query = table_save_strategies.update().where(table_save_strategies.c.id == id).values(
                environmental_indicator= data_insert[0],
                economic_indicator = data_insert[1],
                energy_indicator = data_insert[2],
                update_date = fecha_formateada
                )
        try:
            result = self.engine.execute(query)
            num_filas_actualizadas = result.rowcount
            print(f"Update success. {num_filas_actualizadas}")
            query2 = table_save_strategies_values.delete().where(table_save_strategies_values.c.id_strategy_name == id)
            result2 = self.engine.execute(query2)
            num_filas_eliminadas2 = result2.rowcount
            print(f"Delete success. {num_filas_eliminadas2}")
            rows = json.loads(new_data_values)
            for row in rows:
                row['id_strategy_name'] = id
            self.engine.execute(table_save_strategies_values.insert(), rows)
            print(f"Insert success.")
            return True
        except Exception as e:
            print(f"Error inserting data: {type(e)} - {e}")
            return False

    def delete_strategy_with_id(self, id):
        """Save users credential on database

        Args:
            user (str): user identification.
            password (str -hash value-): user-provided password.

        Returns:
            dict: query result from validation --select-- for the given user credentials.
        """
        print(f"id: {id}")

        query = table_save_strategies.delete().where(table_save_strategies.c.id == id)
        result = self.engine.execute(query)
        num_filas_eliminadas = result.rowcount
        if num_filas_eliminadas > 0:
            query2 = table_save_strategies_values.delete().where(table_save_strategies_values.c.id_strategy_name == id)
            result2 = self.engine.execute(query2)
            num_filas_eliminadas2 = result2.rowcount
            if num_filas_eliminadas2 > 0:
                print("The delation was successful.")
                return True
            else:
                print("The delation failed sub.")
        else:
            print("The delation failed scenary.")
            return False

    def get_data_table_strategies_variable_value(self, id):
        """Save users credential on database

        Args:
            user (str): user identification.
            password (str -hash value-): user-provided password.

        Returns:
            dict: query result from validation --select-- for the given user credentials.
        """
        # query_1 = insert(login_table).values(user=user, password=password)
        # result = self.engine.execute(query_1)
        print(f"id: {id}")

        query = select(table_save_strategies_values).where(table_save_strategies_values.c.id_strategy_name == id)
        result = self.engine.execute(query)
        columns = [col for col in result.keys()]
        print(f"columns: {columns}")
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        result.close()
        print(f"rows: {rows}")
        return rows

    def get_data_table_strategies(self, user):
        """Save users credential on database

        Args:
            user (str): user identification.
            password (str -hash value-): user-provided password.

        Returns:
            dict: query result from validation --select-- for the given user credentials.
        """
        # query_1 = insert(login_table).values(user=user, password=password)
        # result = self.engine.execute(query_1)
        print(f"user: {user}")

        query_2 = select(table_save_strategies).where(table_save_strategies.c.user == user)
        result = self.engine.execute(query_2)
        columns = [col for col in result.keys()]
        print(f"columns: {columns}")
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        result.close()
        print(f"rows: {rows}")
        return rows

    # def get_data_table_strategies(self):
    #     distribution_dict = {}
    #     _dict = {}
    #     distribution_dict.update(self.get_table_strategies())
    #     _dict.update({'distribution': distribution_dict})
    #     return _dict

    def set_save_strategy(self, strategy_name,user,chain_type, anio, all_data, data_indicators):
        """Save users strategies on database

        Args:
            id_login (int): index of login table from method
            name (_type_): _description_
            organization (_type_): _description_
        """
        fecha_actual = datetime.datetime.today()
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
        print("La fecha actual es:", fecha_formateada)
        data_insert = json.loads(data_indicators)
        stmt = insert(table_save_strategies).values(
                strategy_name=strategy_name,
                user=user,
                type=chain_type,
                anio=anio,
                environmental_indicator= data_insert[0],
                economic_indicator = data_insert[1],
                energy_indicator = data_insert[2],
                date= fecha_formateada
            )
        try:
            result_proxy = self.engine.execute(stmt)
            strategy_id = result_proxy.inserted_primary_key[0]
            rows = json.loads(all_data)
            for row in rows:
                row['id_strategy_name'] =strategy_id
            self.engine.execute(table_save_strategies_values.insert(), rows)
            print(f"Data inserted correctly id: {strategy_id}")
            return True
        except Exception as e:
            print(f"Error inserting data: {type(e)} - {e}")
            return False

    def update_from_admin(self, table, data):
        print(data)
        if table == 'users':
            for record in data:
                record = self.rename_key(record)
                try:
                    query = update(users_table).values(record).where(users_table.c.iduser == record['iduser'])
                    result = self.engine.execute(query)
                    if result.rowcount == 0:
                        query = insert(users_table).values(record)
                        self.engine.execute(query)
                except:
                    pass
            return True
        if table == 'viviendas':
            for record in data:
                record = self.rename_key(record, typ='capitalized')
                try:
                    query = update(households_table).values(record)
                    result = self.engine.execute(query)
                    if result.rowcount == 0:
                        query = insert(users_table).values(record)
                        self.engine.execute(query)
                except:
                    pass
            return True
        else:
            return False

    @staticmethod
    def get_units():
        return _unit_dict

    @staticmethod
    def rename_key(dicts, typ='none'):
        output_dic = dict()
        for key in dicts:
            new_key = key
            if typ != 'capitalized':
                new_key = new_key.lower()
            try:
                new_key = new_key.replace(' ', '_')
            except:
                pass

            output_dic[new_key] = dicts[key]
        return output_dic


""" class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, fullname, email, phone):
        self.fullname = fullname
        self.email = email
        self.phone = phone
 """
