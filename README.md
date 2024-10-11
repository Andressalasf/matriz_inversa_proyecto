# Calculadora de Matriz Inversa: Método Gauss-Jordan 🔢

**Andrés Felipe Salas Niño**

## Descripción del Proyecto 👀
Este proyecto consiste en una calculadora que utiliza el método de Gauss-Jordan para encontrar la matriz inversa de una matriz dada. La calculadora muestra el proceso paso a paso, incluyendo el pivoteo parcial, que garantiza mayor estabilidad numérica al intercambiar filas para evitar divisiones por valores cercanos a cero. La aplicación cuenta con una interfaz gráfica amigable implementada con Tkinter, y presenta los resultados y cada operación realizada de forma clara y detallada.

## Instalar el Proyecto 🚀
Clona o descarga el repositorio:
```bash
git clone https://github.com/tu_usuario/calculadora-matriz-inversa.git
```
Ingresa a la carpeta del proyecto
```bash
cd calculadora-matriz-inversa
```
Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```
## Estructura del Proyecto 📂
1. Componentes

En este directorio se encuentran los widgets de la interfaz gráfica, como botones, etiquetas y tablas que se utilizan para la visualización del proceso de cálculo. Los componentes están separados para mantener un diseño modular y reutilizable, permitiendo que cada uno se encargue de una parte específica de la UI.

2. Documentación
Aquí se encuentra la documentación del proyecto, incluyendo guías de uso para el usuario final. Cada vez que se añada una nueva funcionalidad, se debe actualizar este directorio con las explicaciones correspondientes. Esta sección es fundamental para que los usuarios puedan entender cómo interactuar con la calculadora.

3. Servicios
Las funciones lógicas relacionadas con el cálculo de la matriz inversa, el pivoteo parcial y la validación de matrices residen en este directorio. Aquí se separa la lógica del cálculo de la visualización de los resultados para mantener una mejor organización del código.

4. Prototipos
Contiene representaciones de diseño o esquemas de cómo debería verse o funcionar la aplicación. Esto incluye ideas iniciales y prototipos que fueron creados para planificar la interfaz gráfica y el flujo del programa.

## Problemas ❎
Algunas matrices pueden no tener inversa, lo cual ocurre cuando su determinante es 0. En ese caso, la calculadora mostrará un mensaje de error y no procederá con el cálculo. Además, es posible que el formato de las matrices grandes desborde la pantalla de la interfaz; el manejo de scrolling aún está en desarrollo.

