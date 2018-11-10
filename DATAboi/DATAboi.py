# DATAboi

import numpy as np
import pandas as pd

class Data:
    def __init__(self):
        # txt box
        print('\n', '  DATAboi', '\n', " - - - - -", '\n')

        # load
        self.INP = np.loadtxt("inp/inp.txt", float)
        self.Q = np.loadtxt("inp/Q.txt", float)

        # get opt
        self.agg_t_inp = int(input("set agg_t_inp:          "))
        self.agg_t_Q = int(input("set agg_t_Q:            "))
        self.agg_type = np.zeros(self.INP.shape[1])
        self.t_x = np.zeros((self.INP.shape[1], 5))
        self.t_x_max = 0

        while int(input("any inp additive? :     ")):
            self.agg_type[int(input("col n? :          "))] = 1

        while int(input("any col t-x? :          ")):
            col_n = int(input("col n?:           "))
            n_t_x = int(input("n t_x?:           "))

            for i in range(n_t_x):
                self.t_x[col_n][i] = int(input("value?:           "))
                if self.t_x[col_n][i] > self.t_x_max:
                    self.t_x_max = self.t_x[col_n][i]

        self.t_x_Q = []
        for i in range(int(input("t_x_Q n?:               "))):
            self.t_x_Q.append(int(input("value?:                 ")))
            if self.t_x_Q[i] > self.t_x_max:
                self.t_x_max = self.t_x_Q[i]

        self.cons_print = int(input("\nprint output?:          "))

        # # # #
        self.agg()
        self.prep()
        self.print()

    def agg(self):  # aggregates INP and Q mtx

        # INP
        i = j = 0
        while j < self.INP.shape[1]:
            while i < self.INP.shape[0]/self.agg_t_inp:

                if self.agg_type[j] == 0:
                    self.INP[i][j] = self.INP[i*self.agg_t_inp][j]
                else:
                    sum = 0
                    for k in range(self.agg_t_inp):
                        sum += self.INP[i*self.agg_t_inp+k][j]
                    self.INP[i][j] = sum

                i += 1
            j += 1
            i = 0

        # Q
        self.Q = self.Q[::self.agg_t_Q]

        # cleanup
        self.INP = self.INP[:(int(self.INP.shape[0]/self.agg_t_inp))][:]

    def prep(self):         # prepares the out INP and EXP_OUT files

        self.out_INP = pd.DataFrame(self.INP)
        self.exp_out = pd.DataFrame(self.Q)

        l = self.out_INP.shape[1]                                                       # l = last col pointer
        for i in range(self.out_INP.shape[1]):                                      # go through t_x options and
            for j, val in enumerate(self.t_x[i]):                                   # build out_INP
                if self.agg_type[i] == 0 and val != 0:                                  # agg_type 0 shifting
                    self.out_INP[l] = self.out_INP[i].shift(int(val))
                    l+=1

        for i in range(self.agg_type.shape[0]):                                     # agg_type 1 shifting
            if self.agg_type[i] != 0:                                                   # find agg_type1 cols

                for j, val in enumerate(self.t_x[i]):                                   # get vals (t-x)
                    if val != 0:

                        self.out_INP[l+j] = self.out_INP[i]

                        for m in range(int(self.out_INP.shape[0]-val)):                 # aggregate
                            for n in range(1, int(val)):
                                self.out_INP[l+j][m] += self.out_INP[l+j][m+n]

                        self.out_INP[l+j] = self.out_INP[l+j].shift(int(val))           # shift col down
                        l+=j                                                            # update last col

        l = self.out_INP.shape[1]                                                   # Q inp shifting
        for i, val in enumerate(self.t_x_Q):
            if val != 0:
                self.out_INP[l+i] = self.exp_out.shift(val)

        self.out_INP = self.out_INP[int(self.t_x_max):]                             # cutoff
        self.exp_out = self.exp_out[int(self.t_x_max):]

        # console print
        if self.cons_print != 0:
            print('\n', self.out_INP)
            print('\n', self.exp_out)

        print('\n', '   process complete :)')


    def print(self):
        self.out_INP.to_csv('out/INP.txt', sep = " ", header = 0, index = 0)
        self.exp_out.to_csv('out/EXP_OUT.txt', sep = " ", header = 0, index = 0)



dt = Data()
