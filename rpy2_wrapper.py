import pandas as pd
#import numpy as np
import rpy2.robjects as ro
#from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

class R:
    def __init__(self):
        self.r = ro.r
        #numpy2ri.activate()
        pandas2ri.activate()
        multcomp = importr("multcomp")
        stats = importr("stats")
        NSM3 = importr('NSM3')
        self.anova_results = {}
        self.oneway_results = {}
        self.data_columns = []
        self.tukeyhsd_results = []
        
    def import_csv(self,csv_path="",header='infer',index_col=None):
        self.csv_path = csv_path
        try:
            self.p_df = pd.read_csv(self.csv_path,header=header,index_col=index_col)
            self.r_df = pandas2ri.py2ri(self.p_df)
            print("succeed")
        except:
            print("failed")
        
    def aov(self,data_column="",label_column=""):
        self.data_column = data_column
        self.label_column = label_column
        label_data = ro.FactorVector(self.r_df.rx2(self.label_column))
        ro.globalenv["label_data"] = label_data
        ro.globalenv[self.data_column] = self.r_df.rx2(self.data_column)

        try:
            lm_name = "{} ~ label_data".format(self.data_column)
            #print(lm_name)
            lm_D = self.r.lm(lm_name)
            self.anova_result = self.r.aov(lm_D)
            self.anova_results[self.data_column]= self.anova_result
            print(self.r.anova(self.anova_result))
        except:
            print("failed")
    
    def oneway(self,data_column="",label_column="",var=False):
        self.data_column = data_column
        self.label_column = label_column
        label_data = ro.FactorVector(self.r_df.rx2(self.label_column))
        ro.globalenv["label_data"] = label_data
        ro.globalenv[self.data_column] = self.r_df.rx2(self.data_column)

        try:
            lm_name = "{} ~ label_data".format(self.data_column)
            #print(lm_name)
            fmla = ro.Formula(lm_name)
            #lm_D = self.r.lm(lm_name)
            onewayf = self.r("oneway.test")
            self.oneway_result = onewayf(fmla,**{"var.equal":var})
            self.oneway_results[self.data_column]= self.oneway_result
            print(self.oneway_result)
        except:
            print("failed")
            
    def tukeyHSD(self,data_column="",label_column=""):
        self.aov(data_column=data_column,label_column=label_column)
        self.anova_result = self.anova_results[self.data_column]
        self.tukeyhsd_result = self.r.TukeyHSD(self.anova_result)
        self.tukeyhsd_results.append(self.tukeyhsd_result[0])
        print(self.tukeyhsd_result[0])
    
    def steeldwass(self,data_column="",label_column=""):
        self.data_column = data_column
        self.label_column = label_column
        data = self.r_df.rx2(self.data_column)
        label_data = ro.FactorVector(self.r_df.rx2(self.label_column))
        print(self.r.pSDCFlig(data, label_data, method="Monte Carlo"))
        
    def fisher_test(self):
        data_to_matrix = self.r("data.matrix")
        matrix = data_to_matrix(self.r_df)
        fisher = self.r("fisher.test")
        print(fisher(matrix))
        
    def rsource_file_import(self,file_path=""):
        r_source = self.r['source']
        r_source(file_path)
        
    def close(self):
        #numpy2ri.deactivate()
        pandas2ri.deactivate()