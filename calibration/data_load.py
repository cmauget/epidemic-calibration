import os
import pandas as pd
import numpy as np
import json

class dataModel:

    @staticmethod
    def load_config(name_json):

        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open(dir_path+"/config/"+name_json, "r") as read_file:
            d = json.load(read_file)

        guess = d["guess"]
        nb_comp = d["nb_comp"]
        name_comp = d["name_comp"]
        cor_tab = d["cor_tab"]
        name_params = d["name_params"]
        fit_tab = d["fit_tab"]

        N = d["N"]
        y0 = d["y0"]

        name_fic = d["name_fic"]
        data = pd.read_csv("calibration/data/"+name_fic)

        n = len(data)

        t = np.linspace(0, n, n)

        return guess, N, t, data, y0, cor_tab, nb_comp, name_comp, name_params, fit_tab

    @staticmethod
    def load_config_edo(name_json):

        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open(dir_path+"/config/"+name_json, "r") as read_file:
            d = json.load(read_file)

        guess = d["guess"]
        nb_comp = d["nb_comp"]
        name_comp = d["name_comp"]
        name_params = d["name_params"]
        fit_tab = d["fit_tab"]

        N = d["N"]
        y0 = d["y0"]

        name_fic = d["name_fic"]
        data = pd.read_csv("calibration/data/"+name_fic)

        n = len(data)

        t = np.linspace(0, n, n)

        return guess, N, t, data, y0, nb_comp, name_comp, name_params, fit_tab
