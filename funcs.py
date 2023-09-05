import numpy as np
from numpy import exp,pi,sin,cos,tan,arcsin,arccos,arctan,arctan2,sinh,cosh,tanh,mod,log,floor,ceil,sqrt,maximum,minimum,ones,zeros,angle,sign,where,logical_and
from math import pow as mpow
import matplotlib.pyplot as plt

iter = 10

#utility
iterate = lambda f,n: (lambda x: x) if n == 0 else lambda x: f(iterate(f,n-1)(x))
chi = lambda f,a,b: lambda x: where(logical_and(x>=a,x<b),f(x),0)
#
bump = chi(lambda x: exp(1/(x*(x-1))+4),0,1)
digit = lambda x,b,i: floor(x*pow(b,-i))-b*floor(x*pow(b,-i-1))
tri = lambda x: abs(mod(x-1,2)-1)
part = lambda x,n,k: 1-ceil(mod(digit(x,n,-1)-k,n)/n)
tw = lambda x: 1-abs(x-1/2)*2
gthf = lambda x: mod(floor(x*2),2.0)
kron = lambda x: maximum(floor(1-abs(x)),0)
m1 = lambda x: mod(x,1.0)
zaz = lambda f: lambda x: (1-kron(x))*f(x+kron(x)/100)
zalist = lambda f,list: lambda x: np.prod([(1-kron(x-y)) for y in list],axis = 0)*f(x+sum([kron(x-y) for y in list])/100)
zaints = lambda f: lambda x: (1-kron(m1(x)))*f(x+kron(m1(x))/100)
sna = zaz(lambda x: exp(1-1/x))
dot = lambda x: 1-minimum(floor(abs(x)),1)
mink0 = zaints(lambda x: 1/mod(x,1))
scho0 = lambda x: maximum(0,minimum(1,3*tri(mod(x,2.0))-1))
arg = lambda z: 1-angle(z)/(2*pi)

switch = lambda f: lambda x: (1-gthf(x))*(f(x+1/2)-1/2)+gthf(x)*(f(x-1/2)+1/2)
bolz0 = lambda f: lambda x: ((f(x*3)*2)*part(x,3,0)+(f(x*(-3)+2)+1)*part(x,3,1)+(f(x*3-2)*2+1)*part(x,3,2))/3
cant0 = lambda f: lambda x: (f(x*3)*part(x,3,0)+part(x,3,1)+(f((x-2/3)*3)+1)*part(x,3,2))/2

cant2 = iterate(cant0,iter)(lambda x: x)

cant_pl = [[1/3,1/3],[2/3,1/2]]
oka_pl = [[1/3,2/3],[2/3,1/3]]

def bolz(pl):
    pl = pl.append([1,1])
    pl = pl.insert(0,[0,0])
    return lambda x: sum([chi(lambda y: ((y-pl[i][0])/(pl[i+1][0]-pl[i][0]))*(pl[i+1][1]-pl[i][1])+pl[i][1],pl[i][0],pl[i+1][0]) (x) for i in range(len(pl))])

smooth = lambda x: sna(x)/(sna(x)+sna(1-x))
cant = lambda x: floor(x)+sum([(1-(((digit(x,3,-k)+1)%3)%2))*np.prod([1-digit(x,3,-j)%2 for j in range(k)],axis=0)/pow(2,k) for k in range(iter)])
mink = zaz(lambda x: floor(x)+2*sum([pow(-1,i+1)*pow(2,-sum([floor(iterate(mink0,j+1)(x)) for j in range(i)])) for i in range(1,iter)]))
oka = lambda x: iterate(bolz0,iter)(lambda x: x)(x)
scho = lambda x: sum([scho0(mpow(3,mpow(2,k))*x/3)/mpow(2,k) for k in range(iter)])/2
blanc = lambda x: (sum(tri(x*mpow(2,k))*mpow(2,-k) for k in range(iter))-x)*3/2

soli = (lambda f: lambda x,t=0: f(x+t)+1/2)(zalist(lambda x: bump(x)*(1-2*x)/((x**2)*((x-1)**2))/(6*sqrt(2)),[0,1]))
rie = lambda x,t=0: sum(sin(mpow(k,2)*x*2*pi+t*2*pi*sign(mod(k,2)-1/2))/mpow(k,2) for k in range(1,iter))*4/10+1/2
wei = lambda x,t=0: sum([sin(2*pi*x*mpow(2,k)+t*2*pi*sign(mod(k,2)-1/2))*mpow(1/2,k) for k in range(iter)])*3/8+1/2
wen = lambda x,t=0: np.prod([1+sin((x/3+1/4)*pi*mpow(sqrt(6),k*(k+1))+2*pi*t*sign(mod(k,2)-1/2))/mpow(2,k) for k in range(1,iter)],axis = 0)/2-1/6
sin2pi = lambda x,t=0: sin(2*pi*(x+t))/2+1/2

step2hill = lambda f: lambda x: f(tw(x))
step2wave = lambda f: lambda x: f(tw(mod(x+1/4,1)))
step2wave2 = lambda f: lambda x: (f(x)-x)/np.max(abs(f(x)-x))/2+1/2
hill2wave = lambda f: lambda x: (1-gthf(x))*(f(2*x)/2+1/2)+gthf(x)*(1/2-f(2*x-1)/2)

b = lambda x: sqrt(bump(mod(x,1)))
trip = lambda x: (x,x,x)
gray = lambda x: trip(bump(mod(x,1)))
prism = lambda x:(b(x),b(x+1/3),b(x+2/3))



step = [lambda x: x,smooth,cant,switch(cant),mink,switch(mink),bolz,scho]
hill = [bump,blanc]
wave = [soli,wei,rie,sin2pi,wen]
