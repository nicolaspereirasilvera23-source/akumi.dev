#DETERMINA SI UN NUMERO ES PRIMO

def es_primo(numero):
    """
    Determina si un número es primo de manera optimizada.
    
    Optimizaciones aplicadas:
    - Solo verifica hasta la raíz cuadrada del número
    - Maneja casos especiales (números <= 1, números pares)
    """
    if numero <= 1:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    
    # Solo verificar números impares hasta la raíz cuadrada
    for i in range(3, int(numero**0.5) + 1, 2):
        if numero % i == 0:
            return False
    return True

print(es_primo(11))