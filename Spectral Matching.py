import os
from REQPY_Module import REQPY_single
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

def PlotsandWrite(PSA, T, RS_Periods, RS_Sa):
    def write_file(periods, accelerations):
        with open(SpectralAccelerationFile, 'w') as f:
            f.write("Period")
            f.write("\t")
            f.write("Sa(g)")
            f.write("\n")
            for period, acceleration in zip(periods, accelerations):
                f.write(str(period))
                f.write("\t")
                f.write(str(acceleration))
                f.write("\n")


    plt.plot(T, PSA, c='b', label='Matched')

    plt.plot(RS_Periods, RS_Sa, c='r', ls='--', label='Target RS')
    plt.legend()
    plt.show()


    write_file(T, PSA)




MainFolder = "Data"

#Name the Earthquake and Response spectrum file inside of Main Folder
File = 'Target Response Spectrum.txt'
seed = 'Input.txt'
dampratio = 0.05

#Range of Scaling in Periods
TL1 = 0.05
TL2 = 6

#Time Step of Earthquake data
dt = 0.005


OutputFolder = "Out"
OutPath = os.path.join(os.getcwd(), MainFolder, OutputFolder)
if os.path.exists(OutPath) is False:
    os.makedirs(OutPath)


#Interpolation Value for the Response Spectrum (Could be any)
DesiredInt = 0.001
InterpolatedFile = os.path.join(os.getcwd(), MainFolder, OutputFolder, "Interpolated.txt")
ScaledFile = os.path.join(os.getcwd(), MainFolder, OutputFolder, "Scaled.txt")
SpectralAccelerationFile = os.path.join(os.getcwd(), MainFolder, OutputFolder, "Spectral Acc.txt")




if __name__ == '__main__':
    s = np.loadtxt(os.path.join(os.getcwd(), MainFolder , seed), skiprows=0, delimiter=",", dtype="float")
    fs   = 1/dt                         # sampling frequency (Hz)
    new_X, new_Y = ConstantInterpolation(File, MainFolder, DesiredInt, InterpolatedFile)
    To =  new_X
    dso = new_Y
    ccs,rms,misfit,cvel,cdespl,PSAccs,PSAs,T,sf = REQPY_single(s,fs,dso,To,
                                                        T1=TL1,T2=TL2,zi=dampratio,
                                                        nit=3,NS=100,
                                                        baseline=1,plots=1)
    plt.show()



    # Writer
    headerinfo = 'accelerations in m/s², dt = ' + str(dt)
    np.savetxt(ScaledFile,ccs*9.81,header=headerinfo)

    PlotsandWrite(PSAccs, T, To, dso)
