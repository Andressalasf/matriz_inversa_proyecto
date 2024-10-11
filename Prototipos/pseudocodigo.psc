Algoritmo calcularMatrizInversa

    Definir matriz, identidad, matrizExtendida Como Matriz
    Definir n, i, j, pivote, factor Como Real
    Definir inversa, filaPivote, filaActual Como Matriz
    Definir error Como Lógico
    error = Falso
    
    matriz = generarEntradas() // Generar las entradas de la matriz
    n = dimension(matriz) // Tamaño de la matriz (n x n)
    identidad = crearMatrizIdentidad(n) // Crear la matriz identidad
    matrizExtendida = unirMatrices(matriz, identidad) // Concatenar matriz con identidad
    
    Para i Desde 0 Hasta n-1 Hacer
        pivote = matrizExtendida[i][i]
        
        Si pivote == 0 Entonces
            intercambiarFilas(matrizExtendida, i) // Intercambiar la fila con otra que tenga un pivote diferente de cero
            pivote = matrizExtendida[i][i] // Actualizar pivote
        Fin Si
        
        Si pivote == 0 Entonces
            Escribir "Error: la matriz no tiene inversa"
            error = Verdadero
            Romper
        Fin Si
        
        filaPivote = dividirFila(matrizExtendida[i], pivote) // Hacer que el pivote sea 1
        matrizExtendida[i] = filaPivote
        
        Para j Desde 0 Hasta n-1 Hacer
            Si i != j Entonces
                factor = matrizExtendida[j][i]
                filaActual = restarFilas(matrizExtendida[j], multiplicarFila(filaPivote, factor)) // Hacer cero el resto de la columna
                matrizExtendida[j] = filaActual
            Fin Si
        Fin Para
    Fin Para
    
    Si no(error) Entonces
        inversa = extraerMatrizInversa(matrizExtendida, n) // Extraer la matriz inversa de la matriz extendida
        Escribir "La matriz inversa es: "
        MostrarMatriz(inversa) // Mostrar el resultado
    Fin Si

Fin Algoritmo

Funcion matriz <- generarEntradas
    // Lógica para leer y generar las entradas de la matriz
    Leer entradas // Ingresar los valores de la matriz
    matriz = [valores ingresados por el usuario]
Fin Funcion

Funcion matriz <- crearMatrizIdentidad(n)
    // Lógica para crear una matriz identidad de tamaño n
    matriz = [matriz identidad de n x n]
Fin Funcion

Funcion matriz <- unirMatrices(matrizA, matrizB)
    // Lógica para concatenar dos matrices
    matriz = matrizA + matrizB
Fin Funcion

Funcion intercambiarFilas(matriz, fila)
    // Lógica para intercambiar la fila con otra si el pivote es cero
    Si hay una fila con valor != 0 en la columna i Entonces
        Intercambiar las filas
    SiNo
        Error: matriz no tiene inversa
    Fin Si
Fin Funcion

Funcion fila <- dividirFila(fila, pivote)
    // Lógica para dividir todos los elementos de la fila entre el pivote
    Para cada elemento de la fila Hacer
        fila[elemento] = fila[elemento] / pivote
    Fin Para
Fin Funcion

Funcion filaResultado <- restarFilas(filaOriginal, filaMultiplicada)
    // Lógica para restar una fila multiplicada por un factor de otra fila
    Para cada elemento en filaOriginal Hacer
        filaResultado[elemento] = filaOriginal[elemento] - filaMultiplicada[elemento]
    Fin Para
Fin Funcion

Funcion filaMultiplicada <- multiplicarFila(fila, factor)
    // Lógica para multiplicar una fila por un factor
    Para cada elemento en la fila Hacer
        filaMultiplicada[elemento] = fila[elemento] * factor
    Fin Para
Fin Funcion

Funcion inversa <- extraerMatrizInversa(matrizExtendida, n)
    // Lógica para extraer la matriz inversa de la parte extendida (las columnas n a 2n)
    Para i Desde 0 Hasta n-1 Hacer
        Para j Desde n Hasta 2*n-1 Hacer
            inversa[i][j-n] = matrizExtendida[i][j]
        Fin Para
    Fin Para
Fin Funcion

Funcion limpiar
    // Lógica para limpiar los valores de la matriz y entradas
    Limpiar todas las entradas de la matriz
    Escribir "Se ha limpiado la matriz y las entradas para un nuevo cálculo"
Fin Funcion

Funcion MostrarMatriz(matriz)
    // Lógica para mostrar la matriz en pantalla
    Escribir matriz
Fin Funcion