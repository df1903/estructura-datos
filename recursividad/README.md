# Recursividad

Taller de recursividad 2021-1 (enunciado: [`docs/enunciados/taller_recursividad_2021-1.pdf`](../docs/enunciados/taller_recursividad_2021-1.pdf)).

| Ejercicio | Función | Nivel |
|-----------|---------|-------|
| 1 | `saludar(x)` | básico (sin backtracking) |
| 2 | `productos(num, n)` tabla de multiplicar | básico |
| 3 | `invertir(ordenada, invertida)` | básico |
| 4 | `ordenar(lista)` | básico |
| 5-6 | `listaInvertida`, `listaDirecta` | básico |
| 7 | `sumaParesHastaDos(N)` suma pares y guarda un error por cada impar | fácil (con backtracking) |
| 8 | `sumaArreglo` | fácil |
| 9-11 | `invertirLista`, `invertirNumero`, `sumaLista` | medio |
| 12-13 | `menor`, `sumaVector` | medio |
| 14 | `esPrimo` | medio |
| 15-22 | factorial, Fibonacci, potencia, MCD, suma de dígitos, palíndromo, binario, Hanoi | complemento |

**Sin backtracking:** el trabajo se hace al *entrar* a cada ambiente. **Con backtracking:** el resultado se arma al *regresar*, cuando los ambientes se cierran.

```bash
python -m recursividad.ejercicios
```

*Autor: Daniel Felipe Franco Rincón*
