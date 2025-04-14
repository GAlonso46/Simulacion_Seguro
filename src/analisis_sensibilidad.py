from simulacion import simular
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def analizar_sensibilidad_lam(valores_lam, repeticiones):
    resultados = []  

    for lam_val in valores_lam:
        capitales = []
        for i in range(repeticiones):
            cap_final = simular(1000, 10, 5, 0.2, lam_val, 100, 365)
            capitales.append(cap_final)
        
        promedio = np.mean(capitales)
        desviacion = np.std(capitales)
        quiebras = sum(1 for cap in capitales if cap < 0)
        porcentaje_quiebra = 100 * quiebras / repeticiones

        resultados.append((lam_val, promedio, desviacion, porcentaje_quiebra))
        print(f"lam = {lam_val:.3f} | Prom = {promedio:.2f} | Desv = {desviacion:.2f} | Quiebra = {porcentaje_quiebra:.1f}%")
    
    return resultados

def analizar_sensibilidad_nu(valores_nu, repeticiones):
    resultados = []  

    for nu_val in valores_nu:
        capitales = []
        for i in range(repeticiones):
            cap_final = simular(1000, 10, nu_val, 0.2, 0.095, 100, 365)
            capitales.append(cap_final)

        promedio = np.mean(capitales)
        desviacion = np.std(capitales)
        quiebras = sum(1 for cap in capitales if cap < 0)
        porcentaje_quiebra = 100 * quiebras / repeticiones

        resultados.append((nu_val, promedio, desviacion, porcentaje_quiebra))
        print(f"nu = {nu_val:.2f} | Prom = {promedio:.2f} | Desv = {desviacion:.2f} | Quiebra = {porcentaje_quiebra:.1f}%")
    
    return resultados

def analizar_sensibilidad_mu(valores_mu, repeticiones):
    resultados = []  

    for mu_val in valores_mu:
        capitales = []
        for i in range(repeticiones):
            cap_final = simular(1000, 10, 3, mu_val, 0.095, 100, 365)
            capitales.append(cap_final)

        promedio = np.mean(capitales)
        desviacion = np.std(capitales)
        quiebras = sum(1 for cap in capitales if cap < 0)
        porcentaje_quiebra = 100 * quiebras / repeticiones

        resultados.append((mu_val, promedio, desviacion, porcentaje_quiebra))
        print(f"mu = {mu_val:.2f} | Prom = {promedio:.2f} | Desv = {desviacion:.2f} | Quiebra = {porcentaje_quiebra:.1f}%")
    
    return resultados

def analizar_sensibilidad_mean_claim(valores_mean_claim, repeticiones):
    resultados = []  

    for mc_val in valores_mean_claim:
        capitales = []
        for i in range(repeticiones):
            cap_final = simular(1000, 10, 3, 0.4, 0.095, mc_val, 365)
            capitales.append(cap_final)

        promedio = np.mean(capitales)
        desviacion = np.std(capitales)
        quiebras = sum(1 for cap in capitales if cap < 0)
        porcentaje_quiebra = 100 * quiebras / repeticiones

        resultados.append((mc_val, promedio, desviacion, porcentaje_quiebra))
        print(f"mean_claim = {mc_val:.1f} | Prom = {promedio:.2f} | Desv = {desviacion:.2f} | Quiebra = {porcentaje_quiebra:.1f}%")
    
    return resultados



def graficar_sensibilidad_lam(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df['lam'], df['Capital_Promedio'], marker='o', linestyle='-')
    plt.xlabel('Tasa de Reclamaciones (lam)')
    plt.ylabel('Capital Promedio Final')
    plt.title('Análisis de Sensibilidad: Capital vs. lam')
    plt.grid(True)
    plt.savefig('data/sensibilidad_lam.png')
    plt.show()

def graficar_sensibilidad_nu(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df['nu'], df['Capital_Promedio'], marker='o', linestyle='-')
    plt.xlabel('Tasa de llegada de nuevos asegurados (nu)')
    plt.ylabel('Capital Promedio Final')
    plt.title('Análisis de Sensibilidad: Capital vs. nu')
    plt.grid(True)
    plt.savefig('data/sensibilidad_nu.png')
    plt.show()

def graficar_sensibilidad_mu(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df['mu'], df['Capital_Promedio'], marker='o', linestyle='-')
    plt.xlabel('Tasa de salida (mu)')
    plt.ylabel('Capital Promedio Final')
    plt.title('Análisis de Sensibilidad: Capital vs. mu')
    plt.grid(True)
    plt.savefig('data/sensibilidad_mu.png')
    plt.show()

def graficar_sensibilidad_mean_claim(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df['mean_claim'], df['Capital_Promedio'], marker='o', linestyle='-')
    plt.xlabel('Monto medio de reclamación (mean_claim)')
    plt.ylabel('Capital Promedio Final')
    plt.title('Análisis de Sensibilidad: Capital vs. mean_claim')
    plt.grid(True)
    plt.savefig('data/sensibilidad_mean_claim.png')
    plt.show()


def run_analisis_sensibilidad_lam():
    resultados = analizar_sensibilidad_lam([0.09, 0.095, 0.1, 0.105, 0.11], repeticiones=30)
    df = pd.DataFrame(resultados, columns=[
    'lam',
    'Capital_Promedio',
    'Desviacion_Estandar',
    'Porcentaje_Quiebra'
])
    df.to_csv('data/sensibilidad_lam.csv', index=False)

    graficar_sensibilidad_lam(df)

def run_analisis_sensibilidad_nu():
    resultados = analizar_sensibilidad_nu([3, 5, 7, 9], repeticiones=30)
    df = pd.DataFrame(resultados, columns=[
    'nu',
    'Capital_Promedio',
    'Desviacion_Estandar',
    'Porcentaje_Quiebra'
])
    df.to_csv('data/sensibilidad_nu.csv', index=False)

    graficar_sensibilidad_nu(df)

def run_analisis_sensibilidad_mu():
    resultados = analizar_sensibilidad_mu([0.1, 0.2, 0.3, 0.4], repeticiones=30)
    df = pd.DataFrame(resultados, columns=[
    'mu',
    'Capital_Promedio',
    'Desviacion_Estandar',
    'Porcentaje_Quiebra'
])
    df.to_csv('data/sensibilidad_mu.csv', index=False)

    graficar_sensibilidad_mu(df)

def run_analisis_sensibilidad_mean_claim():
    resultados = analizar_sensibilidad_mean_claim([90, 95, 100, 105, 110], repeticiones=30)
    df = pd.DataFrame(resultados, columns=[
    'mean_claim',
    'Capital_Promedio',
    'Desviacion_Estandar',
    'Porcentaje_Quiebra'
])
    df.to_csv('data/sensibilidad_mean_claim.csv', index=False)

    graficar_sensibilidad_mean_claim(df)


if __name__ == "__main__":
    #run_analisis_sensibilidad_lam()
    #run_analisis_sensibilidad_nu()
    #run_analisis_sensibilidad_mu()
    run_analisis_sensibilidad_mean_claim()



