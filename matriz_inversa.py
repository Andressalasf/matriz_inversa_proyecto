# ------------------------------------------------- Importación de bibliotecas ------------------------------------------------------------- #

import tkinter as tk  # Importar la biblioteca de interfaz gráfica de usuario de Python
from tkinter import ttk, messagebox  # Importar elementos adicionales de tkinter
import numpy as np  # Biblioteca para manejo de matrices y operaciones numéricas
from fractions import Fraction  # Para manejar fracciones en las entradas de la matriz
from PIL import ImageTk, Image


# ------------------------------------------------- Codigo de las funciones del programa ---------------------------------------------------- #

# Función para calcular la matriz inversa utilizando el método Gauss-Jordan
def gauss_jordan_inversa(matriz, pasos_frame):
    n = len(matriz)  # Obtener la dimensión de la matriz cuadrada
    identidad = np.identity(n)  # Crear la matriz identidad del mismo tamaño
    matriz_extendida = np.hstack((matriz, identidad))  # Formar la matriz extendida [matriz | identidad]
    mostrar_matriz(pasos_frame, "Matriz extendida inicial", matriz_extendida)  # Mostrar la matriz inicial en la interfaz

    for i in range(n):  # Iterar sobre cada fila para aplicar el método de eliminación de Gauss-Jordan
        # Buscar el pivote máximo en la columna actual (i) y cambiar filas si es necesario
        max_index = np.argmax(abs(matriz_extendida[i:, i])) + i
        
        if max_index != i:  # Si el pivote máximo no está en la fila actual, intercambiar filas
            matriz_extendida[[i, max_index]] = matriz_extendida[[max_index, i]]
            mostrar_matriz(pasos_frame, f"Intercambio de fila {i + 1} con fila {max_index + 1} por mejor pivote", matriz_extendida)

        # Normalizar la fila actual dividiéndola por el valor del pivote
        pivote = matriz_extendida[i][i]
        matriz_extendida[i] = matriz_extendida[i] / pivote
        mostrar_matriz(pasos_frame, f"Dividiendo fila {i + 1} por el pivote {pivote:.4f}", matriz_extendida)

        # Eliminar los elementos en la columna i para otras filas (hacer ceros)
        for j in range(n):
            if i != j:  # No modificar la fila actual
                factor = matriz_extendida[j][i]  # Factor por el cual se multiplicará la fila para eliminar el valor
                matriz_extendida[j] = matriz_extendida[j] - factor * matriz_extendida[i]
                mostrar_matriz(pasos_frame, f"Haciendo cero en la posición ({j + 1},{i + 1})", matriz_extendida)

    inversa = matriz_extendida[:, n:]  # Extraer la matriz inversa de la parte derecha de la matriz extendida
    mostrar_matriz(pasos_frame, "Matriz inversa encontrada", inversa)  # Mostrar la matriz inversa
    return inversa

# Función para mostrar un mensaje de error en la interfaz de pasos
def mostrar_mensaje_error(pasos_frame, mensaje):
    # Crear una etiqueta con el mensaje de error y mostrarla en la interfaz
    label_error = tk.Label(pasos_frame, text=mensaje, font=('Arial', 10, 'bold'), fg='red', bg='#f8f9fa')
    label_error.grid(row=len(pasos_frame.grid_slaves()), column=0, columnspan=5, pady=5)

# Función para mostrar matrices en el frame de pasos con formato adecuado
def mostrar_matriz(pasos_frame, mensaje, matriz):
    start_row = len(pasos_frame.grid_slaves())  # Determinar la posición inicial en la interfaz
    
    # Mostrar el mensaje de título con la descripción de la operación realizada
    label_mensaje = tk.Label(pasos_frame, text=mensaje, font=('Arial', 12, 'bold'), bg='#415a77', fg='white', padx=10, pady=5)
    label_mensaje.grid(row=start_row, column=0, columnspan=len(matriz[0]), pady=10)

    # Mostrar cada elemento de la matriz en la interfaz con formato adecuado
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            label_elemento = tk.Label(pasos_frame, text=f"{valor:.4f}", font=('Courier', 10), width=10, 
                                      borderwidth=2, relief="groove", bg='#e0e1dd', fg='#1b263b', padx=5, pady=5)
            label_elemento.grid(row=start_row + i + 1, column=j, padx=5, pady=5)

# Función para calcular la inversa de la matriz
def calcular_inversa():
    try:
        global matriz, inversa  # Variables globales para almacenar la matriz e inversa
        n = int(tamano_matriz.get())  # Obtener el tamaño de la matriz desde el campo de entrada
        matriz = []  # Inicializar la matriz
        for i in range(n):  # Leer cada fila de la matriz desde las entradas de la interfaz
            fila = []
            for j in range(n):
                valor = entradas[i][j].get()  # Obtener el valor de cada celda
                if '/' in valor:  # Si el valor es una fracción, convertirlo a decimal
                    valor = float(Fraction(valor))
                else:
                    valor = float(valor)  # Convertir el valor a flotante
                fila.append(valor)  # Añadir el valor a la fila
            matriz.append(fila)  # Añadir la fila a la matriz

        matriz = np.array(matriz)  # Convertir la lista de listas en un array de numpy

        for widget in pasos_frame.winfo_children():  # Limpiar los pasos anteriores en la interfaz
            widget.destroy()

        # Verificar si la matriz tiene inversa calculando su determinante
        determinante = np.linalg.det(matriz)
        if determinante == 0:
            messagebox.showerror("Error", "La matriz no tiene inversa porque su determinante es 0.")  # Mostrar error si el determinante es cero
            return
        inversa = gauss_jordan_inversa(matriz, pasos_frame)  # Calcular la inversa usando el método Gauss-Jordan

        if inversa is not None:
            btn_ver_pasos.pack(pady=10)  # Mostrar el botón para ver los pasos de la solución si se encuentra la inversa

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos.")  # Error en caso de valor no numérico
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")  # Capturar cualquier otro error

# Función para mostrar la nueva pestaña de pasos al usuario
def mostrar_pasos():
    notebook.select(tab_pasos)  # Cambiar la vista a la pestaña "Pasos" del notebook

# Función para generar la matriz con las entradas proporcionadas por el usuario
def generar_entradas():
    try:
        n = int(tamano_matriz.get())  # Obtener el tamaño de la matriz desde el campo de entrada
        if n <= 0:  # Validar que el tamaño sea positivo
            messagebox.showerror("Error", "Por favor, ingresa un número válido para el tamaño de la matriz.")
            return
        elif n == 1:  # Validar que el tamaño de la matriz sea al menos 2x2
            messagebox.showerror("Error", "El tamaño de la matriz debe ser mínimo de 2x2")
            return

        for widget in frame_matriz.winfo_children():  # Limpiar cualquier contenido previo en el frame de la matriz
            widget.destroy()

        global entradas  # Variable global para almacenar las entradas de la matriz
        entradas = []  # Inicializar la lista de entradas

        # Crear las entradas de la matriz con las dimensiones dadas por el usuario
        for i in range(n):
            fila_entradas = []  # Lista para almacenar las entradas de cada fila
            for j in range(n):
                entrada = tk.Entry(frame_matriz, width=5)  # Crear una entrada para cada celda de la matriz
                entrada.grid(row=i, column=j, padx=5, pady=5)  # Posicionar la entrada en la grilla
                fila_entradas.append(entrada)  # Añadir la entrada a la fila
            entradas.append(fila_entradas)  # Añadir la fila a la matriz de entradas

    except ValueError:  # Manejo de error si el tamaño de la matriz no es válido
        messagebox.showerror("Error", "Por favor, ingresa un número válido para el tamaño de la matriz.")

# Función para limpiar todos los datos de la interfaz
def limpiar():
    tamano_matriz.delete(0, 'end')  # Limpiar el campo de entrada para el tamaño de la matriz
    for widget in frame_matriz.winfo_children():  # Eliminar las entradas de la matriz generada
        widget.destroy()
    btn_ver_pasos.pack_forget()  # Ocultar el botón "Ver pasos de la solución"
    for widget in pasos_frame.winfo_children():  # Limpiar los pasos mostrados en la pestaña de pasos
        widget.destroy()
        
# Función para volver a la pestaña principal desde la pestaña de pasos
def volver_inicio():
     notebook.select(tab_principal)  # Cambiar la vista a la pestaña principal del notebook

# Función para mostrar la nueva pestaña del manual
def ver_manual():
    notebook.select(tab_manual)  # Cambiar la vista a la pestaña "Manual de Usuario"

# ------------------------------Configurar la ventana principal de la aplicación ------------------------------------------------------- #

ventana = tk.Tk()
ventana.title("Calculadora de Matriz Inversa - Método Gauss-Jordan")  # Título de la ventana principal
ventana.geometry("800x700")  # Tamaño inicial de la ventana
ventana.configure(bg='#1b263b')  # Color de fondo de la ventana principal
ventana.resizable(True, True)  # Permitir redimensionar la ventana

# Crear el notebook para manejar las pestañas dentro de la ventana principal
notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both")  # Expandir el notebook para llenar toda la ventana

# Crear la pestaña principal para la entrada de matriz
tab_principal = tk.Frame(notebook, bg='#1b263b')  # Fondo oscuro para la pestaña principal
notebook.add(tab_principal, text="Principal")  # Añadir la pestaña principal al notebook

# Título principal de la pestaña principal
label_titulo_pasos = tk.Label(tab_principal, text="Matriz inversa por el Método Gauss-Jordan", font=("Arial", 22, "bold"), fg="white", bg="#1b263b", pady=20)
label_titulo_pasos.pack(anchor="n")  # Colocar el título en la parte superior

# Crear un frame contenedor centrado para la pestaña principal
frame_contenido = tk.Frame(tab_principal, bg='#1b263b')
frame_contenido.pack(expand=True)  # Expandir para centrar el contenido

# Etiqueta en la pestaña principal para pedir el tamaño de la matriz
label_tamano = tk.Label(frame_contenido, text="Tamaño de la matriz:", font=("Arial", 16, "bold"), fg="white", bg="#1b263b")
label_tamano.pack(pady=10)

# Entrada para el tamaño de la matriz
tamano_matriz = tk.Entry(frame_contenido, borderwidth=3, width=5 , relief="ridge")
tamano_matriz.pack(pady=10)

# Botón para generar la matriz
btn_generar = tk.Button(frame_contenido, text="Generar matriz", command=generar_entradas, bg="#415a77", fg="white", font=("Arial", 10))
btn_generar.pack(pady=10)

# Frame que contendrá las entradas de la matriz generada
frame_matriz = tk.Frame(frame_contenido, bg='#415a77')
frame_matriz.pack(pady=10)

# Botón para calcular la inversa de la matriz
btn_calcular = tk.Button(frame_contenido, text="Calcular inversa", command=calcular_inversa, bg="#1b263b", fg="white", font=("Arial", 12, "bold"))
btn_calcular.pack(pady=15)

# Botón para limpiar la matriz y los datos ingresados
btn_limpiar = tk.Button(frame_contenido, text="Limpiar", command=limpiar, bg="#1b263b", fg="white", font=("Arial", 12, "bold"))
btn_limpiar.pack(pady=15)

# Botón para mostrar los pasos de la solución (oculto hasta que se calcule la inversa)
btn_ver_pasos = tk.Button(frame_contenido, text="Ver pasos de la solución", command=mostrar_pasos, bg="#415a77", fg="white", font=("Arial", 12, "bold"))
btn_ver_pasos.pack(pady=10)
btn_ver_pasos.pack_forget()  # Ocultar botón hasta que se calcule la inversa

# Botón para mostrar el manual de usuario
btn_ver_manual = tk.Button(tab_principal, text="Ver manual de usuario", command=ver_manual, width=30, bg="#415a77", fg="white", font=("Arial", 14, "bold") )
btn_ver_manual.pack(pady=30)  # Colocar el botón en la parte superior


# ----------------------------------- CODIGO PARA LA PESTAÑA DE PASOS------------------------------------------------------------------------- #

# Crear la pestaña para mostrar los pasos con un diseño mejorado
tab_pasos = tk.Frame(notebook, bg='#1b263b')  # Fondo oscuro para la pestaña de pasos
notebook.add(tab_pasos, text="Pasos")  # Añadir la pestaña de pasos al notebook
# Título principal de la pestaña de pasos
label_titulo_pasos = tk.Label(tab_pasos, text="Pasos del Método Gauss-Jordan", font=("Arial", 16, "bold"), fg="white", bg="#1b263b", pady=10)
label_titulo_pasos.pack(anchor="n")  # Colocar el título en la parte superior

# Botón para volver a la pestaña inicial
btn_inicio= tk.Button(tab_pasos, text="Volver Inicio", bg="#415a77", fg="white", font=("Arial", 10), command=volver_inicio, width=10 )
btn_inicio.pack(anchor="n")  # Colocar el botón en la parte superior

# Crear el canvas y la scrollbar para visualizar los pasos de manera fluida
canvas = tk.Canvas(tab_pasos, bg='#f8f9fa', highlightthickness=0)
scrollbar = ttk.Scrollbar(tab_pasos, orient="vertical", command=canvas.yview) # Crear una barra de desplazamiento vertical para la pestaña "tab_pasos".
scrollable_frame = tk.Frame(canvas, bg='#f8f9fa') # Crear un frame dentro del canvas que actuará como contenedor del contenido que se desplazará.

# Configurar el tamaño dinámico del contenido en el canvas
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) # Configurar un evento que se activará cada vez que cambie el tamaño del frame `scrollable_frame`.

# Crear un marco en el canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") # Crear una ventana dentro del canvas en la posición (0, 0) y vincularla al frame `scrollable_frame` como contenido desplazable.
canvas.configure(yscrollcommand=scrollbar.set) # Configurar el canvas para que su desplazamiento vertical esté controlado por el scrollbar

# Añadir el canvas y la scrollbar al layout
canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.pack(side="right", fill="y", padx=10)

# Frame dentro del canvas para los pasos
pasos_frame = scrollable_frame

 # ------------------------------------------- CODIGO PARA LA PESTAÑA DE MANUAL DE USUARIO ------------------------------------------------------------ #
 
# Crear la pestaña del manual de usuario
tab_manual = tk.Frame(notebook, bg='#1b263b')  # Fondo oscuro similar a la pestaña "Pasos"
notebook.add(tab_manual, text="Manual de Usuario")  # Añadir la pestaña de manual al notebook

# Título de la pestaña de manual de usuario
label_titulo_manual = tk.Label(tab_manual, text="Manual de Usuario", font=("Arial", 16, "bold"), fg="white", bg="#1b263b", pady=10)
label_titulo_manual.pack(anchor="n")  # Colocar el título en la parte superior

# Botón para volver a la pestaña inicial
btn_inicio= tk.Button(tab_manual, text="Volver Inicio", bg="#415a77", fg="white", font=("Arial", 10), command=volver_inicio, width=10 )
btn_inicio.pack(anchor="n")  # Colocar el botón en la parte superior

# Crear un canvas y una barra de scroll para el contenido del manual
canvas_manual = tk.Canvas(tab_manual, bg='#f8f9fa')
scrollbar_manual = ttk.Scrollbar(tab_manual, orient="vertical", command=canvas_manual.yview)
scrollable_frame_manual = tk.Frame(canvas_manual, bg='#f8f9fa')

# Configurar el tamaño dinámico del contenido en el canvas
scrollable_frame_manual.bind("<Configure>", lambda e: canvas_manual.configure(scrollregion=canvas_manual.bbox("all")))

# Crear un marco en el canvas
canvas_manual.create_window((0, 0), window=scrollable_frame_manual, anchor="nw")
canvas_manual.configure(yscrollcommand=scrollbar_manual.set)

# Añadir el canvas y la scrollbar al layout
canvas_manual.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar_manual.pack(side="right", fill="y", padx=10)

# Frame dentro del canvas para las instrucciones del manual
instrucciones_frame = scrollable_frame_manual

 # ------------------------------------------------------ CONTENIDO DEL MANUAL -------------------------------------------------------------------- #
 
# Título del Manual
titulo_manual = ttk.Label(instrucciones_frame, text="Manual de Usuario", font=("Arial", 20, "bold"))
titulo_manual.pack(pady=20)

# Sección 1: Introducción
seccion1_titulo = ttk.Label(instrucciones_frame, text="1. Introducción", font=("Arial", 16, "bold"))
seccion1_titulo.pack(anchor="w", padx=20, pady=10)

seccion1_contenido = ttk.Label(instrucciones_frame, text="""Este manual tiene como objetivo guiar al usuario en el uso de la Calculadora de Matriz Inversa implementada con el método Gauss-Jordan.
Se explicarán las funcionalidades y limitaciones de la aplicación, así como los pasos necesarios para calcular la inversa de una matriz.""", wraplength=800, justify="left", font=("Arial", 12))
seccion1_contenido.pack(anchor="w", padx=40, pady=10)

# Sección 2: Requisitos
seccion2_titulo = ttk.Label(instrucciones_frame, text="2. Requisitos del Programa", font=("Arial", 16, "bold"))
seccion2_titulo.pack(anchor="w", padx=20, pady=10)

seccion2_contenido = ttk.Label(instrucciones_frame, text="""Antes de usar la calculadora, asegúrate de cumplir los siguientes requisitos:
                               
-Tener instalado: Python 3.7 o superior.

-Agregar Bibliotecas: tkinter, numpy, Fractions, Pillow. En este caso la biblioteca numpy y Pillow se deben descargar primero""", wraplength=800, justify="left", font=("Arial", 12))
seccion2_contenido.pack(anchor="w", padx=40, pady=10)

# Crear secciones con instrucciones con imagenes

# Generar las imagenes para mostrar las instrucciones

img1 = ImageTk.PhotoImage(Image.open('paso1.png'))
img2 = ImageTk.PhotoImage(Image.open('paso2.png'))
img3 = ImageTk.PhotoImage(Image.open('paso3.png'))
img4 = ImageTk.PhotoImage(Image.open('paso4.png'))
img5 = ImageTk.PhotoImage(Image.open('paso5.png'))
img6 = ImageTk.PhotoImage(Image.open('paso6.png'))

# Instrucción 1: Ingresar el tamaño de la matriz
label_instruccion1 = tk.Label(instrucciones_frame, text="Paso 1: Ingresar el tamaño de la matriz",
                              font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#1b263b')
label_instruccion1.pack(anchor="w", padx=20, pady=5)

descripcion_instruccion1 = tk.Label(instrucciones_frame, text="En la pestaña principal, ingrese el tamaño de la matriz en el campo correspondiente. "
                                                              "Asegúrese de que el valor sea mayor a 1 para obtener una matriz válida.",
                                    font=("Arial", 12), bg='#f8f9fa', fg='#1b263b', justify="left", wraplength=700)
descripcion_instruccion1.pack(anchor="w", padx=20, pady=5)

#Imagen descriptiva 1
label_imagen1 = tk.Label(instrucciones_frame, image=img1, bg='#f8f9fa')
label_imagen1.pack(anchor="w", padx=20, pady=10)

# Instrucción 2: Generar la matriz
label_instruccion2 = tk.Label(instrucciones_frame, text="Paso 2: Generar la matriz",
                              font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#1b263b')
label_instruccion2.pack(anchor="w", padx=20, pady=5)

descripcion_instruccion2 = tk.Label(instrucciones_frame, text="Presione el botón 'Generar Matriz' para crear la matriz con las dimensiones especificadas. "
                                                              "Aparecerán campos vacíos donde podrá ingresar los elementos de la matriz.",
                                    font=("Arial", 12), bg='#f8f9fa', fg='#1b263b', justify="left", wraplength=700)
descripcion_instruccion2.pack(anchor="w", padx=20, pady=5)

#Imagen descriptiva 2
label_imagen2 = tk.Label(instrucciones_frame, image=img2, bg='#f8f9fa')
label_imagen2.pack(anchor="w", padx=20, pady=10)

# Instrucción 3: Ingresar los valores de la matriz
label_instruccion3 = tk.Label(instrucciones_frame, text="Paso 3: Ingresar los valores de la matriz",
                              font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#1b263b')
label_instruccion3.pack(anchor="w", padx=20, pady=5)

descripcion_instruccion3 = tk.Label(instrucciones_frame, text="Ingrese los valores de la matriz en los campos correspondientes. "
                                                              "Recuerde que los valores deben ser mayores a 0.00001 para evitar que sean redondeados a 0.",
                                    font=("Arial", 12), bg='#f8f9fa', fg='#1b263b', justify="left", wraplength=700)
descripcion_instruccion3.pack(anchor="w", padx=20, pady=5)

#Imagen descriptiva 3
label_imagen3 = tk.Label(instrucciones_frame, image=img3, bg='#f8f9fa')
label_imagen3.pack(anchor="w", padx=20, pady=10)

# Instrucción 4: Calcular la inversa de la matriz
label_instruccion4 = tk.Label(instrucciones_frame, text="Paso 4: Calcular la inversa de la matriz",
                              font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#1b263b')
label_instruccion4.pack(anchor="w", padx=20, pady=5)

descripcion_instruccion4 = tk.Label(instrucciones_frame, text="Presione el botón 'Calcular Inversa' para obtener la inversa de la matriz ingresada. "
                                                              "Si la matriz no tiene inversa, aparecerá un mensaje de error.",
                                    font=("Arial", 12), bg='#f8f9fa', fg='#1b263b', justify="left", wraplength=700)
descripcion_instruccion4.pack(anchor="w", padx=20, pady=5)

#Imagen descriptiva 4
label_imagen4 = tk.Label(instrucciones_frame, image=img4, bg='#f8f9fa')
label_imagen4.pack(anchor="w", padx=20, pady=10)

# Instrucción 5: Visualizar los pasos
label_instruccion5 = tk.Label(instrucciones_frame, text="Paso 5: Visualizar los pasos del cálculo",
                              font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#1b263b')
label_instruccion5.pack(anchor="w", padx=20, pady=5)

descripcion_instruccion5 = tk.Label(instrucciones_frame, text="""Tras presionar el botón 'calcular la inversa', se habilitará el botón Ver Pasos de la Solución.
Al presionarlo, se abrirá una nueva pestaña que muestra la matriz inicial y cada paso realizado con el método Gauss-Jordan.""",
                                    font=("Arial", 12), bg='#f8f9fa', fg='#1b263b', justify="left", wraplength=700)
descripcion_instruccion5.pack(anchor="w", padx=20, pady=5)

#Imagen descriptiva 5
label_imagen5 = tk.Label(instrucciones_frame, image=img5, bg='#f8f9fa')
label_imagen5.pack(anchor="w", padx=20, pady=10)

# Instrucción 6: Limpieza de datos
label_instruccion5 = tk.Label(instrucciones_frame, text="Paso 6: Limpiar datos",
                              font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#1b263b')
label_instruccion5.pack(anchor="w", padx=20, pady=5)

descripcion_instruccion5 = tk.Label(instrucciones_frame, text="Utilice el botón 'limpiar' para borrar todos los datos y reiniciar el programa a su estado inicial.",
                                    font=("Arial", 12), bg='#f8f9fa', fg='#1b263b', justify="left", wraplength=700)
descripcion_instruccion5.pack(anchor="w", padx=20, pady=5)

#Imagen descriptiva 6
label_imagen6 = tk.Label(instrucciones_frame, image=img6, bg='#f8f9fa')
label_imagen6.pack(anchor="w", padx=20, pady=10)

# Sección 4: Restricciones
seccion4_titulo = ttk.Label(instrucciones_frame, text="4. Restricciones y Comportamiento del Programa", font=("Arial", 16, "bold"))
seccion4_titulo.pack(anchor="w", padx=20, pady=10)

seccion4_contenido = ttk.Label(instrucciones_frame, text="""- Si se ingresa un valor menor a 0.00001, se considerará como 0.
                               
- El programa no puede calcular la inversa si el determinante de la matriz es igual a 0).

- No se permite el ingreso de texto o caracteres especiales en las celdas de la matriz.

- El tamaño de la matriz debe ser de al menos 2x2.

- Solo se aceptan números reales (no se permiten números complejos).

- En caso de números decimales en la salida, solo se mostraran estos con sus primeros 4 digitos despues de la coma.
""", wraplength=800, justify="left", font=("Arial", 12))
seccion4_contenido.pack(anchor="w", padx=40, pady=10)

# Sección 5: Funcionalidad del programa
seccion4_titulo = ttk.Label(instrucciones_frame, text="5.Comportamiento del Programa", font=("Arial", 16, "bold"))
seccion4_titulo.pack(anchor="w", padx=20, pady=10)
descripcion = tk.Label(instrucciones_frame, text="Esta sección describe el proceso y el método utilizado por el programa para calcular la inversa de matrices cuadradas, detallando cómo el algoritmo implementado opera para obtener el resultado.",
                                    font=("Arial", 12), bg='#f8f9fa', fg='#1b263b', justify="left", wraplength=700)
descripcion.pack(anchor="w", padx=20, pady=5)
seccion4_contenido = ttk.Label(instrucciones_frame, text="""6.1. Ingreso del Tamaño de la Matriz
El usuario comienza ingresando el tamaño de la matriz. El tamaño debe ser mayor que 1, ya que las matrices de dimensión 1x1 no se pueden invertir de manera práctica. El programa valida que el tamaño ingresado sea correcto y que se pueda crear una matriz con ese valor.

6.2. Generación de la Matriz
Después de ingresar el tamaño, el programa genera un conjunto de campos de entrada donde el usuario puede ingresar cada elemento de la matriz manualmente. Los valores deben ser numéricos, y no se permiten valores complejos. Si el valor ingresado es menor que 0.00001, se establece automáticamente en 0.0000. Esto evita errores en el cálculo y garantiza una mayor estabilidad en el procesamiento.

6.3. Verificación del Determinante
El cálculo de la inversa depende del determinante de la matriz. Si el determinante es 0, la matriz no tiene inversa. El programa realiza esta verificación antes de continuar con los cálculos.

6.4. Método de Gauss-Jordan
Si la matriz es invertible, el programa aplica el método de Gauss-Jordan. Este método consiste en formar una matriz extendida [A | I], donde A es la matriz ingresada e I es la matriz identidad del mismo tamaño. Los pasos son los siguientes:

---Selección del Pivote: Se elige el elemento de mayor valor absoluto en la columna actual como pivote. Si es necesario, se intercambian filas para colocar el mejor pivote en la posición correcta.

---Normalización de la Fila: La fila que contiene el pivote se divide por el valor del pivote para que el elemento pivote se convierta en 1.

---Eliminación hacia Ceros: Se ajustan las otras filas para que todos los elementos en la columna del pivote sean cero, dejando solo un 1 en la fila del pivote.

---Repetición: Estos pasos se repiten para cada columna hasta que la matriz A se convierte en la matriz identidad, y I se transforma en A^-1, que es la inversa de la matriz original.

6.5. Presentación de Resultados
Una vez que se encuentra la inversa, se muestra al usuario en la interfaz especificamente en la pestaña 'pasos'. El programa resalta cada paso, incluyendo los intercambios de filas y las operaciones realizadas, facilitando la comprensión del proceso de cálculo.
 
""", wraplength=800, justify="left", font=("Arial", 12))
seccion4_contenido.pack(anchor="w", padx=40, pady=10)

# ------------------------------------------------------------------------------------------------------------------------------------------------ #

# Iniciar la ventana principal y la interfaz gráfica
ventana.mainloop()
