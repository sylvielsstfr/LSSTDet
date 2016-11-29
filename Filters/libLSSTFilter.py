
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits
import os
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import interp1d

#---------------------------------------------------------------------------------
detdatafilename='transmissions-LSST.dat'

class Filter:
    """
    class Filter
    =============
    Variables :
    ----------
     wl : wavelength 1d array
     u  : u filter 1d array
     g  : g filter 1d array
     r  : r filter 1d array
     i  : i filter 1d array
     z  : z filter 1d array
     y4 : y4 filter 1d array
     topt
     tccd
     atm
    Methods :
    ---------
    
    """
    wl=0
    u=0
    g=0
    r=0
    i=0
    z=0
    y4=0
    topt=0
    tccd=0
    atm=0
    
    def __init__(self):
        df=pd.read_csv(detdatafilename,names=['wl','Topt','Tccd','U','G','R','I','Z','Y4','atm'],sep='\t')
        self.wl=np.asarray(df['wl'])
        self.u=np.asarray(df['U'])*0.01
        self.g=np.asarray(df['G'])*0.01
        self.r=np.asarray(df['R'])*0.01
        self.i=np.asarray(df['I'])*0.01
        self.z=np.asarray(df['Z'])*0.01
        self.y4=np.asarray(df['Y4'])*0.01
        self.atm=np.asarray(df['atm'])
        print 'init Filter size=',self.wl.shape
    def wavelength_to_u_spl(self):
        #return UnivariateSpline(self.wl,self.u)
        return interp1d(self.wl,self.u,kind='cubic')
    def wavelength_to_g_spl(self):
        #return UnivariateSpline(self.wl,self.g)   
        return interp1d(self.wl,self.g,kind='cubic') 
    def wavelength_to_r_spl(self):
        return interp1d(self.wl,self.r,kind='cubic')  
    def wavelength_to_i_spl(self):
        return interp1d(self.wl,self.i,kind='cubic')          
    def wavelength_to_z_spl(self):
        return interp1d(self.wl,self.z,kind='cubic')
    def wavelength_to_y4_spl(self):
        return interp1d(self.wl,self.y4,kind='cubic')
    


#---------------------------------------------------------------------------------
def MakeSED(lambda_min=300.,lambda_max=1200.,dlambda=1.,slope=0):
    """
     MakeSED(lambda_min=300,lambda_max=1200,dlambda=1,power=0)
     =============================================
     
     input :
     -----
         lambda_min : minimum of SED spectra in nm
         lambda_max : maximum of SED spectra in nm
         dlambda    : bin width of SED in nm
         power      : power in wavelength
     
     output :
     --------
         wl         : wavelength 1D array
         sed        : SED 1D array
    
    """
    
    #NBINS=(lambda_max-lambda_min=300.)/dlambda
    wl=np.arange(lambda_min,lambda_max+dlambda,dlambda)
    nbins=wl.shape[0]
    bincenter=nbins/2
    
    
    sed=np.power(wl,slope)
    sedcenter=sed[bincenter]
    sed=sed/sedcenter
        
    return wl,sed  
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
def MakeFilters():
    df=pd.read_csv(detdatafilename,names=['wl','Topt','Tccd','U','G','R','I','Z','Y4','atm'],sep='\t')

    return df['wl'],df['U']*0.01,df['G']*.01,df['R']*0.01,df['I']*0.01,df['Z']*0.01,df['Y4']*0.01
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
detdatafilename='transmissions-LSST.dat'
#---------------------------------------------------------------------------------
if __name__ == "__main__":

    df=pd.read_csv(detdatafilename,names=['wl','Topt','Tccd','U','G','R','I','Z','Y4','atm'],sep='\t')
    df.head()
    plt.figure()
    colors = ['blue','green','red', 'orange','grey','black'] 
    df.plot(x='wl', y=['U','G','R','I','Z','Y4'],color=colors)
    plt.ylim([0,100])
    plt.xlabel("$\lambda$")
    plt.ylabel("Filter transmission")
    plt.title("Filters")

    # create a SED
    wl,sed=MakeSED(lambda_min=300.,lambda_max=1200.,dlambda=10.,slope=-1)
    
    print wl.shape
    plt.figure()
    plt.plot(wl,sed,'-')
    
    #wl,u,g,r,i,z,y4=MakeFilters()
    #plt.plot(wl,y4)
    flt=Filter()
    
    # get interpolation function
    wl_to_u= flt.wavelength_to_u_spl()
    wl_to_g= flt.wavelength_to_g_spl()
    wl_to_r= flt.wavelength_to_r_spl()
    wl_to_i= flt.wavelength_to_i_spl()
    wl_to_z= flt.wavelength_to_z_spl()
    wl_to_y4= flt.wavelength_to_y4_spl()
    
    tu=wl_to_u(wl)*sed
    tg=wl_to_g(wl)*sed
    tr=wl_to_r(wl)*sed
    ti=wl_to_i(wl)*sed
    tz=wl_to_z(wl)*sed
    ty4=wl_to_y4(wl)*sed
    
    plt.figure()
    plt.plot(wl,tu)
    plt.plot(wl,tg)
    plt.plot(wl,tr)
    plt.plot(wl,ti)
    plt.plot(wl,tz)
    plt.plot(wl,ty4)