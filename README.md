# INTEGRA2023_PRBA
## Repositorio oficial desarrollo web INTEGRA2023 UTP-UNIVALLE

### Proyecto:
Estrategia para la gestión y utilización de indicadores de eficiencia energética en los procesos de generación, distribución y uso final de la energía en Colombia.
#### Desarrolladores 
- Mateo Barrera
- Alex F. Pinchao
- Melissa Valencia
- Fabian Andres Zuñiga


### Proceso de instalación
- Crear la carpeta para contener el proyecto.
- Al interior de la carpeta crear un entorno virtual.

```bash
# Virtualenv
C:\ProjectFolder_Example> virtualenv venv.
# Activar virtualenv
C:\ProjectFolder_Example> venv\Scripts\activate
```

- Clonar el repositorio Integra2023.
```bash
# Clonar repositorio
(venv) C:\ProjectFolder_Example> git clone https://github.com/MateoBarrera/INTEGRA2023.git

# cd al repositorio
(venv) C:\ProjectFolder_Example> cd INTEGRA2023
```
- Instalar las dependencias del servidor Flask.
```bash
# Instalar dependencias
(venv) C:\ProjectFolder_Example> pip install -r requirements.txt
```
- Correr el servidor Flask.
```bash
# Run the app
(venv) C:\ProjectFolder_Example> set FLASK_APP=Flask\main.py
(venv) C:\ProjectFolder_Example> set FLASK_DEBUG=1
(venv) C:\ProjectFolder_Example> flask run
```