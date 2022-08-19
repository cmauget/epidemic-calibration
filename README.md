# epidemic-calibration

 A simple epidemic calibration tool, created by Clément Mauget and Roxane Leduc during an internship ar NYU.

We have built our GitHub mainly around two directories. A "dev" directory and a "calibration" directory. 

The "dev" directory contains our first codes (as well as programs allowing the reading of the JHU data) and allowed us to perform the analysis of the different methods using data frames taking into account the minimum value of the MAE for each method and train size. 

The "calibration" directory is the final version of this project and contains all the generalized codes. As seen above, the "model_gen.py" program allows the automatic generation of simulated data sets according to the user’s needs.

The "calib_test.py" programs together with  config json show to examples of the running program.

The "calibration.py" program, composed of two models, the "calibModel" which runs based on a edge matrix given by the user, and the "calibModelEdo" which can take as input a custom ODE defined by the user. 

And finally the "data_load.py", whose role is to decode the values contained in the config files.
