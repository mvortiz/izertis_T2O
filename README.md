# izertis_T2O - Prueba técnica

Este proyecto implementa un cliente en Python que se conecta a la API de Open-Meteo para obtener los datos meteorológicos de temperatura y precipitación de una ciudad y un rango de fechas especificado.


## :gear: Instalación y configuración

1. Clonar el repositorio:
   ```
   bash
   git clone
   cd
   ```
3. Instalar dependencias
   ```
   bash
   pip install -r requirements.txt
   ```
## Uso del programa

````
bash
py main.py
````
El programa consta de 4 posibles opciones:
1. Carga de datos metereológicos por ciudad
   Para esta opción se debe introducir el nombre de la ciudad del que se quiere obtener la información y un rango de fechas (inicio y fin), almacenando los datos obtenidos en el sistema.
   
2. Estadísticas de temperatura
   En este caso, también debemos introducir la ciudad y el rango de fechas. Si los datos introducidos ya están almacenados no se realiza de nuevo la búsqueda.
   Esta consulta nos devuelve los datos de: Temperatura media, Temperatura media por día, Temperatura máxima y la fecha y hora en que se produjo, Temperatura mínima y la fecha y hora en que se produjo, Número de horas por encima de un umbral configurable (si no se proporciona se usará 30°C) y Número de horas por debajo de un umbral configurable (si no se proporciona, se usará 0°C).
   
3. Estadísticas de precipitaciones
   En este caso, también debemos introducir la ciudad y el rango de fechas. Si los datos introducidos ya están almacenados no se realiza de nuevo la búsqueda.
   Esta consulta nos devuelve los datos de: Precipitación total, Precipitación total por día, Promedio de precipitación en el rango de fechas, Número de días con precipitación (mayor a 0 mm) y Día de máxima precipitación y su valor.

4. Mostrar los datos almacenados
   En esta opción tenemos la posibilidad de ver todos los datos almacenados, únicamente los nombres de las ciudades guardadas o visualizar los datos para una ciudad en concreto.

Todos los datos mostrados en la pantalla son en formato JSON.

## Mejoras futuras
- Implementar Estadísticas generales, el cual reuniría los datos más relevantes para las ciudades almacenadas en el sistema.
- Captura de excepciones y validación de los datos introducidos para evitar errores en la ejecución.
- Realización completa de los test para todas las funcionalidades y test end-to-end para comprobar el funcionamiento completo de las opciones.
- Comentarios en el código, tanto generales como específicos.

## Autor
  María Victoria Ortiz  
  [email](mv.ortiz.guerra@gmail.com)  
  [Linkedin](https://www.linkedin.com/in/mariavictoriaortiz/)


