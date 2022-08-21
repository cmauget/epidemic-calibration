#regroup different EDO solvers
import numpy as np

def RK4(dt,Times,y0,f):
    sol=[y0];
    p0=y0*1
    p1=y0*0
    for t in Times:
        k1 = f(t,p0)
        k2 = f(t+(dt/2),p0+(dt/2)*k1)
        k3 = f(t+(dt/2),p0+(dt/2)*k2)
        k4 = f(t+dt,p0+dt*k3)
        p1 = p0 + (dt/6) * (k1+2*k2+2*k3+k4)
        sol.append(p1)
        p0=p1*1.0

    sol.pop()

    return sol

def AB3(dt,Times,y0,f):
    sol=[y0];

    # Initialisation :
    soltmp = RK4(dt,np.array([0,dt,2*dt]),y0,f)

    p0 = y0*1.0
    p1 = soltmp[1]*1.0
    sol.append(p1)
    p2 = soltmp[2]*1.0
    sol.append(p2)
    p3 = y0*0
    t=3*dt


    while(t<=Times[-1]):
        f0 = f(t-3*dt,p0)
        f1 = f(t-2*dt,p1)
        f2 = f(t-dt,p2)
        p3 = p2 + dt *(  float(23/12) * f2 - float(16/12) *  f1 + float(5/12) * f0 )
        sol.append(p3)
        p0=p1*1.0
        p1=p2*1.0
        p2=p3*1.0
        t+=dt



    return sol