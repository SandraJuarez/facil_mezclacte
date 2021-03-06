import matplotlib.pyplot as plt
import numpy as np
import math as mt
from scipy.special import eval_legendre
from scipy import integrate
import pandas as pd

grad=np.loadtxt("grad.txt",usecols=0,delimiter=',')

#la función g se calculó con HNC

#c2=np.loadtxt('100cm.txt',usecols=0)
#cargamos los parámetros
bt=np.loadtxt("parametros.csv",skiprows=1,usecols=0,delimiter=',')
a=np.loadtxt("parametros.csv",skiprows=1,usecols=1,delimiter=',')
k=np.loadtxt("parametros.csv",skiprows=1,usecols=2,delimiter=',')
b=np.loadtxt("parametros.csv",skiprows=1,usecols=3,delimiter=',')
al=np.loadtxt("parametros.csv",skiprows=1,usecols=4,delimiter=',')
dn=np.loadtxt("parametros.csv",skiprows=1,usecols=7,delimiter=',')

x = np.linspace(-1, 1, num=20001)
ang=np.arccos(x)
#s=np.sin(ang)
r=2*a*np.sin(ang/2)
np.place(r, r==0, [1e-9])
u=np.loadtxt("potencial.txt",skiprows=1,usecols=0)
du=-k*b*np.exp(-k*r)*(1-np.exp(-al*r))*(1.0/r)+b*np.exp(-k*r)*al*np.exp(-al*r)*(1.0/r)+b*np.exp(-k*r)*(1-np.exp(-al*r))*(-1.0/r**2)

c_dict={}
g_dict={}
gant_dict={}
gsig_dict={}
n=20
aus=0.05
si=0.1
sf=1.0+2*aus
finsc=int((sf-si)/aus)
nf=140
au=20
fin=int((nf-n)/au)
s=si
for sc in range(0,finsc):
    n=20
    for i in range(0,fin):
        name=round(s*100)
        sstr=str(name)+str(n)
        if(i<=5):
            c_dict[i]=np.loadtxt(sstr+'gmcgb.txt',skiprows=1,usecols=1,delimiter=',  ')
            g_dict[i]=np.loadtxt(sstr+'gmcgb.txt',skiprows=1,usecols=2,delimiter=',  ')
            gant_dict[i]=np.loadtxt(sstr+'gant.txt',skiprows=1,usecols=1,delimiter=',  ')
            gsig_dict[i]=np.loadtxt(sstr+'gsig.txt',skiprows=1,usecols=1,delimiter=',  ')
        if(i==6):
             c_dict[6]=c_dict[5]
             g_dict[6]=g_dict[5]
             gant_dict[6]=b_dict[5]
             gsig_dict[6]=gsig_dict[5]
        c=c_dict[i]
        g=g_dict[i]
        gant=gant_dict[i]
        gsig=gsig_dict[i]
          #para la compresibilidad
        dtc=-0.5*n*integrate.simpson(c,x,even='first')
          #para el virial
        n1=n-dn
        n2=n+dn
        f1=r*du*g
        f2=r*du*gant
        vir1=-(n1**2/8)*integrate.simpson(f1,x)
        vir2=-(n2**2/8)*integrate.simpson(f2,x)
        dtv=(vir2-vir1)/(2*dn)
        tau=-(n**2/2)*integrate.simpson(r*du*g,x)

          #escribimos los resultados en un dataframe
        df=pd.DataFrame([{'n':n,'b':b,'s':s,'camino compresibilidad':dtc,'camino virial':dtv,'presion':tau}],columns=['n','b','s','camino compresibilidad','camino virial','presion'],dtype=float)
        if((sc==0) and  (i==0)):
            df.to_csv('resultados.csv',mode='a',header=True,index=False)
        else:
            df.to_csv('resultados.csv',mode='a',header=False,index=False)
        n=n+20

    c_dict.clear()
    g_dict.clear()
    gant_dict.clear()
    gsig_dict.clear()
    s=s+0.05
