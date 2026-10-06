import pandas as pd
import plotly.express as px 
import matplotlib.pyplot as plt
import statsmodels.api as sm 
import scipy as ss
from scipy import stats
import numpy as np


df = pd.read_excel("C:\\Users\\Usuario\\Desktop\\Master big data\\4. Estadistica\\docs tarea\\tablas_para_python.xlsx")

grupo1_basal = df[df['Grupo de control'] == 1]['Basal']
grupo1_min60 = df[df['Grupo de control'] == 1]['Min60']
grupo2_basal = df[df['Grupo de control'] == 2]['Basal']
grupo2_min60 = df[df['Grupo de control'] == 2]['Min60']

#EJERCICIO 1
#a)	Obtener, usando algún programa estadístico, las medidas de centralización y dispersión
# para cada uno de los dos grupos de control para el nivel de glucosa basal, especificando 
# para cada uno de los casos si la media es o no representativa.

print("Apartado a ejercicio 1")
def mostrar_estadisticas_centralizacion(nombre, datos):
    print(f"  Media: {datos.mean():.2f}")
    print(f"  Mediana: {datos.median():.2f}")
    print(f"  Moda: {datos.mode().values}")

def mostrar_estadisticas_dispersion(nombre, datos):
    print(f"  Desviación estándar: {datos.std()}")
    print(f"  Mínimo: {datos.min()}")
    print(f"  Máximo: {datos.max()}")
    print(f"  Rango: {datos.max() - datos.min()}")
    print(f"  Varianza: {datos.var()}")
    print(f"  Coeficiente de variación: {(datos.std() / datos.mean())}") 
                                         
print("=" * 50)
print("MEDIDAS DE CENTRALIZACIÓN GRUPO 1 BASAL:")
mostrar_estadisticas_centralizacion("GRUPO 1 - Basal", grupo1_basal)

print("=" * 50)
print("MEDIDAS DE DISPERSIÓN GRUPO 1 BASAL:")
mostrar_estadisticas_dispersion("GRUPO 1 - Basal", grupo1_basal)


print("=" * 50)
print("MEDIDAS DE CENTRALIZACION DEL GRUPO 2 BASAL:")
mostrar_estadisticas_centralizacion("GRUPO 2 - Basal", grupo2_basal)

print("=" * 50)
print("MEDIDAS DE DISPERSIÓN GRUPO 2 BASAL:")
mostrar_estadisticas_dispersion("GRUPO 2 - Basal", grupo2_basal)

#b)	Estudiar la simetría y la curtosis del nivel de glucosa basal
#  en los adultos ( grupo de control 2)

print("Apartado b ejercicio 1")
print("=" * 50)
print("SIMETRÍA:")
print(f"Grupo 2 Basal: {grupo2_basal.skew():.4f}")

print("\nCURTOSIS:")
print(f"Grupo 2 Basal: {grupo2_basal.kurtosis():.4f}")

#c)	Indicar para cada una de las variables de estudio (nivel glucosa basal y nivel glucosa pasados 60 min)
# y en el grupo de  control 1 el valor de los cuartiles y su significado 
# y obtener el box- plot ( diagrama de cajas) correspondiente. 
# Estudiar la presencia de valores atípicos.

print("Apartado c ejercicio 1")
print("CUARTILES:")
print("\nGrupo 1 - Basal:")
print(f"Q1: {grupo1_basal.quantile(0.25):.2f}")
print(f"Q2 (Mediana): {grupo1_basal.quantile(0.50):.2f}")
print(f"Q3: {grupo1_basal.quantile(0.75):.2f}")

print("RANGO INTERCUARTÍLICO GRUPO BASAL (IQR):")
IQR_basal= grupo1_basal.quantile(0.75) - grupo1_basal.quantile(0.25)
print
print("Limites para valores atípicos:")
limite_inferior_basal = grupo1_basal.quantile(0.25) - 1.5 * IQR_basal
limite_superior_basal = grupo1_basal.quantile(0.75) + 1.5 * IQR_basal
print("Limite inferior Basal:", limite_inferior_basal)      
print("Limite superior Basal:", limite_superior_basal)


print("\nGrupo 1 - Min60:")
print(f"Q1: {grupo1_min60.quantile(0.25):.2f}")
print(f"Q2 (Mediana): {grupo1_min60.quantile(0.50):.2f}")
print(f"Q3: {grupo1_min60.quantile(0.75):.2f}")

print("RANGO INTERCUARTÍLICO GRUPO MIN60 (IQR):")
IQR_min60 = grupo1_min60.quantile(0.75) - grupo1_min60.quantile(0.25)
print
print("Limites para valores atípicos:")
limite_inferior_min60 = grupo1_min60.quantile(0.25) - 1.5 * IQR_min60
print("Limite inferior Min60:", limite_inferior_min60)
limite_superior_min60 = grupo1_min60.quantile(0.75) + 1.5 * IQR_min60
print("Limite superior Min60:", limite_superior_min60)

plt.boxplot(grupo1_basal)
plt.title("Grupo 1 - Basal")
plt.ylabel("Glucosa")
plt.show()

plt.boxplot(grupo1_min60)
plt.title("Grupo 1 - Min60")
plt.ylabel("Glucosa")
plt.show()


#d)	Estudiar la normalidad de los datos de cada uno de los grupos de control 
# estudiados para el nivel de glucosa pasados 60 minutos. 

print("Apartado d ejercicio 1")
print("Estudio de normalidad con test de Shapiro-Wilk:")
grupo1_min60_normalidad = ss.stats.shapiro(grupo1_min60)
print(grupo1_min60_normalidad)

grupo2_min60_normalidad = ss.stats.shapiro(grupo2_min60)
print(grupo2_min60_normalidad)


#EJERCICO 2
#Con los datos del fichero anterior, se quiere estudiar la relación existente entre el nivel basal
#  y el nivel de glucosa que tienen los pacientes sanos jóvenes(grupo 1) una hora después
#  de tomar el preparado de glucosa. Se pide:

#a)	Estudiar la relación lineal existente entre estas dos variables de estudio gráficamente y mediante
#  algún valor estadístico de forma razonada.
#diagrama de dispersion hecho en excel 

print("apartado a ejercicio 2")
cov = grupo1_basal.cov(grupo1_min60)
print("Covarianza:", cov)
corr = grupo1_basal.corr(grupo1_min60)
print("Correlación:", corr)
print("corr entre 0,6-0,8 indica relación alta")

plt.scatter(grupo1_basal, grupo1_min60)
plt.xlabel("Nivel glucosa basal")
plt.ylabel("Nivel glucosa pasados 60 min")
plt.title("Diagrama de dispersión Grupo 1")
plt.show()

#b)	Obtener un modelo lineal que explica el nivel de glucosa en sangre a los 60 minutos en función del nivel
#  basal del paciente y realizar la estimación para un paciente cuyo nivel basal es 83 mg/Dl
print("apartado b ejercicio 2")
X=grupo1_basal
Y=grupo1_min60
X_mean = np.mean(X) 
Y_mean = np.mean(Y)

b1 = np.cov(X, Y, ddof=1)[0,1] / np.var(X, ddof=1)  
b0 = np.mean(Y) - b1 * np.mean(X) 
print(f"Y = {b0:.2f} + {b1:.3f}·X  → Para 83: {b0 + b1*83:.1f}")

#c)	¿Qué tanto por ciento del nivel de glucosa en sangre pasados 60 minutos queda no queda explicado por el anterior modelo?
print("apartado c ejercicio 2" )
coeficiente_determinacion = corr**2
print("Coeficiente de determinación R²:", coeficiente_determinacion)
porcentaje_no_explicado = (1 - coeficiente_determinacion) * 100
print(f'Porcentaje no explicado: {porcentaje_no_explicado:.2f}%')


#d)	Si aumentásemos el nivel basal de un paciente en 5 mg/Dl ¿Qué variación experimentaría
#  su nivel de glucosa al cabo de 60 minutos?
print("apartado d ejercicio 2")
print(f"Variación para un aumento de 5 mg/Dl en el nivel basal: {b1 * 5:.1f}")

#Ejercicio 3 
#a)	Se quiere estudiar si se puede admitir que el nivel medio de glucosa en sangre en el momento de la ingestión
#  en los jóvenes es 88 mg/Dl. Obtener el intervalo de confianza al 95% y al 99% para el nivel medio de glucosa
#  en sangre de los jóvenes y posteriormente contesta a la cuestión planteada con los resultados obtenidos o
#  con un contraste de hipótesis.

print("Apartado a ejercicio 3")
print("CONTRASTE AL 95% DE CONFIANZA:")
t_stat, p_value = stats.ttest_1samp(grupo1_basal, popmean=88)
alpha = 0.05  # nivel de significancia 95%
print("t-statistic:", t_stat)
print("p-value:", p_value)

if p_value < alpha:
    print("Rechazamos H0 → la media poblacional no es 88")
else:
    print("No se rechaza H0 → la media poblacional podría ser 88")

print("CONTRASTE AL 99% DE CONFIANZA:")
alpha = 0.01  # nivel de significancia 99%
print("t-statistic:", t_stat)
print("p-value:", p_value)

if p_value < alpha:
    print("Rechazamos H0 → la media poblacional no es 88")
else:
    print("No se rechaza H0 → la media poblacional podría ser 88")


n=35
desviacion = grupo1_basal.std()
media = grupo1_basal.mean()
error = desviacion / np.sqrt(n)
# IC 95%
t95 = stats.t.ppf(0.975, df=n-1)
IC95 = (media - t95*error, media + t95*error)

print(f"IC 95%: ({IC95[0]:.2f}, {IC95[1]:.2f})")

# IC 99%
t99 = stats.t.ppf(0.995, df=n-1)
IC99 = (media - t99*error, media + t99*error)
print(f"IC 99%: ({IC99[0]:.2f}, {IC99[1]:.2f})")


#b)	Obtener los intervalos de confianza al 95%  para la diferencia de medias en el nivel basal de glucosa
#  entre adultos y jovenes e interpreta los resultados. ¿Se puede concluir que el nivel basal de glucosa de 
# los jóvenes y los adultos es el mismo con nivel de significación del 5%? .Suponiendo que se cumplen las condiciones
#  iniciales teóricas para obtener los intervalos de confianza
print("APARTADO B EJERCICIO 3")

n1, n2 = len(grupo1_basal), len(grupo2_basal)
x1, x2 = grupo1_basal.mean(), grupo2_basal.mean()
s1, s2 = grupo1_basal.std(ddof=1), grupo2_basal.std(ddof=1)

# IC 95%
diferencia = x1 - x2
error = np.sqrt(s1**2/n1 + s2**2/n2)
IC = (diferencia - 1.96*error, diferencia + 1.96*error)

print(f"IC 95% = ({IC[0]:.2f}, {IC[1]:.2f})")
print(f"Incluye 0? {'SÍ' if IC[0] <= 0 <= IC[1] else 'NO'}")


#c)	Se quiere estudiar la proporción de con un nivel basal de glucosa superior a 95 mg/Dl (prediabetes la población).
#  A partir de la muestra del fichero (tomando todos los datos) obtener un intervalo de confianza al 98% y contrastar 
# la hipótesis que la proporción de la población con glucosa superior a 95 mg/Dl es 0,15 con nivel de significación del 5%.

print("APARTADO C EJERCICIO 3")
pacientes_glucosa_basal= grupo1_basal + grupo2_basal
n = len(pacientes_glucosa_basal)
print("Número total de pacientes glucosa basal:", n)

prediabetes_grupo1 = grupo1_basal > 95
prediabetes_grupo2 = grupo2_basal > 95
pacientes_prediabetes = prediabetes_grupo1.sum() + prediabetes_grupo2.sum()
print("Número de pacientes con prediabetes:", pacientes_prediabetes)

proporcion_prediabetes = pacientes_prediabetes / n
print(f"Proporción de pacientes con prediabetes: {proporcion_prediabetes}")

# IC 98%
z_98 = 2.326
error_std_ic = np.sqrt(proporcion_prediabetes * (1 - proporcion_prediabetes) / n)
IC_98 = (proporcion_prediabetes - z_98 * error_std_ic,
         proporcion_prediabetes + z_98 * error_std_ic)

print(f"\nIC 98% = ({IC_98[0]:.3f}, {IC_98[1]:.3f})")

# CONTRASTE α = 0.05
proporcion_hipotesis = 0.15
z_95 = 1.96
error_std_ic95 = np.sqrt(proporcion_prediabetes * (1 - proporcion_prediabetes) / n)
IC_95 = (proporcion_prediabetes - z_95 * error_std_ic95,
         proporcion_prediabetes + z_95 * error_std_ic95)

print(f"IC 95% = ({IC_95[0]:.3f}, {IC_95[1]:.3f})")

Z = (proporcion_prediabetes - proporcion_hipotesis) / error_std_ic95
print(f"\nZ = {Z:.3f}")
print(f"Decisión: {'Rechazar H0' if abs(Z) > z_95 else 'No rechazar H0'}")

