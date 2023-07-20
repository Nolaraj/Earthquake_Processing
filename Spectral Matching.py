# REQPY MOdule for Spectral Matching
from REQPY_Module import REQPY_single, load_PEERNGA_record
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

def ConstantInterpolation(File, RPath, DesiredInt, OutFile):
    from scipy.interpolate import interp1d
    import os

    record_path = RPath   # Folder on current directory
    InputFile = File

    interval_desired = DesiredInt
    arr1 = np.loadtxt(os.path.join(os.getcwd(), record_path, InputFile), skiprows=0, delimiter="\t", dtype="float")
    # os.chdir(record_path)

    periods = []
    values = []
    for arr2 in arr1:
        periods.append(arr2[0])
        values.append(arr2[1])
    x = np.array(periods)
    y = np.array(values)

    interp_func = interp1d(x, y)
    new_x = np.arange(x[0], x[-1], interval_desired)
    new_y = interp_func(new_x)

    index = 1
    with open(f'{OutFile}', 'w') as f:
        f.write("X ")
        f.write("\t")
        f.write("Y")
        f.write("\n")
        for x, y in zip(new_x, new_y):
            f.write(str(x))
            f.write("\t")
            f.write(str(y))
            f.write("\n")
    return new_x, new_y


DesiredInt = 0.001
RPath = "Data"
File = 'Target Response Spectrum.txt'
OutFile = "Interpolated.txt"

# General Informations
seed = 'Input.txt'    # seeed record [g]
# target   = 'ASCE7.txt'                        # target spectrum (T,PSA)
dampratio = 0.05                              # damping ratio for spectra
TL1 = 0.05
TL2 = 6                           # define period range for matching   # (T1=T2=0 matches the whole spectrum)

dt = 0.005
OutputFile = "Ïnterpolated.txt"


s = np.loadtxt(os.path.join(os.getcwd(), RPath , seed), skiprows=0, delimiter=",", dtype="float")
fs   = 1/dt                         # sampling frequency (Hz)
new_X, new_Y = ConstantInterpolation(File, RPath, DesiredInt, OutFile)
To =  new_X
dso = new_Y
ccs,rms,misfit,cvel,cdespl,PSAccs,PSAs,T,sf = REQPY_single(s,fs,dso,To,
                                                    T1=TL1,T2=TL2,zi=dampratio,
                                                    nit=15,NS=100,
                                                    baseline=1,plots=1)
# Writer
headerinfo = 'accelerations in g, dt = ' + str(dt)
np.savetxt(OutputFile,ccs,header=headerinfo)
