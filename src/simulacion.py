import simpy
import numpy as np
import random

# Parámetros del modelo 
A0 = 1000       # Capital inicial
c = 10          # Prima por asegurado (por día)
nu = 5          # Tasa de llegada de nuevos asegurados (por día)
mu = 0.2        # Tasa de salida (por día, tiempo de estancia ~ 5 días)
lam = 0.1       # Tasa de generación de reclamaciones por asegurado (por día)
mean_claim = 100  # Monto medio de reclamación (para distribución exponencial)
T = 365         # Horizonte de simulación (días)

# Variables globales
capital = A0
n_insured = 0
last_event_time = 0  # para actualizar ingresos acumulados


def update_capital(env):
    global capital, n_insured, last_event_time, c
    dt = env.now - last_event_time
    capital += c * n_insured * dt
    last_event_time = env.now

def new_insured_arrivals(env):
    global n_insured
    while env.now < T:
        yield env.timeout(random.expovariate(nu))
        update_capital(env)
        env.process(insured_process(env))

def insured_process(env):
    global n_insured, capital, lam, mu, mean_claim
    # Registro de llegada del asegurado:
    update_capital(env)
    n_insured += 1
    lifetime = random.expovariate(mu)
    # Inicia un proceso interno para generar reclamaciones
    claim_process = env.process(generate_claims(env, lifetime))
    # Espera hasta que expire la vida del asegurado
    yield env.timeout(lifetime)
    update_capital(env)
    n_insured -= 1
    # Si el proceso de reclamaciones aún no ha finalizado, se cancela
    claim_process.interrupt()

def generate_claims(env, lifetime):
    global capital, lam, mean_claim
    try:
        # Mientras no se cumpla el lifetime (se ejecuta hasta que el asegurado se retira)
        while True:
            # Tiempo hasta la siguiente reclamación
            yield env.timeout(random.expovariate(lam))
            update_capital(env)
            # Genera el monto de la reclamación. Usamos la distribución exponencial para F.
            claim_amount = np.random.exponential(mean_claim)
            capital -= claim_amount
            print(f'Tiempo {env.now:.2f}: Reclamación de {claim_amount:.2f}, Capital: {capital:.2f}')
    except simpy.Interrupt:
        # El proceso se interrumpe cuando el asegurado sale
        return
    
# Para hacer el analisis de sensibilidad
def simular(A0_param, c_param, nu_param, mu_param, lam_param, mean_claim_param ,T_param):
    global capital, n_insured, last_event_time, c, nu, mu, lam, mean_claim, T
    # Reinicializar variables globales al comienzo de la simulación:
    capital = A0_param
    n_insured = 0
    last_event_time = 0
    c = c_param
    nu = nu_param
    mu = mu_param
    lam = lam_param
    mean_claim = mean_claim_param
    T = T_param
    
    env = simpy.Environment()
    env.process(new_insured_arrivals(env))
    env.run(until=T)
    update_capital(env)
    
    return capital 


def run_simulation():
    global capital, last_event_time
    last_event_time = 0
    env = simpy.Environment()
    env.process(new_insured_arrivals(env))
    env.run(until=T)
    # Actualiza capital para el tiempo final
    update_capital(env)
    print(f'Fin de simulación en el tiempo {env.now:.2f}, Capital Final: {capital:.2f}')

if __name__ == "__main__":
    run_simulation()
