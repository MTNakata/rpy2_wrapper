import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

class R:
    def __init__(self):
        self.r = ro.r
        numpy2ri.activate()
        pandas2ri.activate()
        self.multcomp = importr("multcomp")
        self.NSM3 = importr("NSM3")
        self.anova_results = {}
        self.oneway_results = {}
        self.data_columns = []
        self.tukeyhsd_results = []
        self.dunnett_results = []
        
    def import_csv(self,csv_path="",header='infer',index_col=None):
        self.csv_path = csv_path
        try:
            self.p_df = pd.read_csv(self.csv_path,header=header,index_col=index_col)
            self.r_df = pandas2ri.py2ri(self.p_df)
            print("succeed")
        except:
            print("failed")
        
    def savemode(self,save_file=""):
        if len(save_file)!=0:
            self.save_file = save_file
            return True
        else:
            return False
       
    def print_func(self,result,save_mode):        
        if save_mode:
            with open(self.save_file,"a") as f:
                print(*result,file=f)
        else:
            print(*result)
    
    def aov(self,data_column="",label_column="",save_file=""):
        save_mode = self.savemode(save_file=save_file)
        self.data_column = data_column
        self.label_column = label_column
        label_data = ro.FactorVector(self.r_df.rx2(self.label_column))
        ro.globalenv["label_data"] = label_data
        ro.globalenv[self.data_column] = self.r_df.rx2(self.data_column)

        try:
            lm_name = "{} ~ label_data".format(self.data_column)
            lm_D = self.r.lm(lm_name)
            self.anova_result = self.r.aov(lm_D)
            self.anova_results[self.data_column]= self.anova_result
            result = ["-------------Result of ANOVA-------------\n",
                     self.r.anova(self.anova_result)]
            self.print_func(result,save_mode)
        except:
            print("failed")
    
    def oneway(self,data_column="",label_column="",var=False,save_file=""):
        save_mode = self.savemode(save_file=save_file)
        self.data_column = data_column
        self.label_column = label_column
        label_data = ro.FactorVector(self.r_df.rx2(self.label_column))
        ro.globalenv["label_data"] = label_data
        ro.globalenv[self.data_column] = self.r_df.rx2(self.data_column)

        try:
            lm_name = "{} ~ label_data".format(self.data_column)
            fmla = ro.Formula(lm_name)
            onewayf = self.r("oneway.test")
            self.oneway_result = onewayf(fmla,**{"var.equal":var})
            self.oneway_results[self.data_column]= self.oneway_result
            result = ["-------------Result of Welch's ANOVA-------------\n",
                      self.oneway_result]
            self.print_func(result,save_mode)
        except:
            print("failed")
            
    def tukeyHSD(self,data_column="",label_column="",save_file=""):
        save_mode = self.savemode(save_file=save_file)
        self.aov(data_column=data_column,label_column=label_column,save_file=save_file)
        self.anova_result = self.anova_results[self.data_column]
        self.tukeyhsd_result = self.r.TukeyHSD(self.anova_result)
        self.tukeyhsd_results.append(self.tukeyhsd_result[0])
        result = ["-------------Result of TukeyHSD test-------------\n\n",
                  self.tukeyhsd_result[0]]
        self.print_func(result,save_mode)
        
    def dunnett_test(self,data_column="",label_column="",save_file=""):
        save_mode = self.savemode(save_file=save_file)
        self.data_column = data_column
        self.label_column = label_column
        data = self.r_df.rx2(self.data_column)
        label_data = ro.FactorVector(self.r_df.rx2(self.label_column))

        self.aov(data_column=data_column,label_column=label_column,save_file=save_file)
        self.anova_result = self.anova_results[self.data_column]
        
        dunnett = self.r.mcp(label_data="Dunnett")
        self.dunnett_result = self.r.glht(self.anova_result, linfct=dunnett)
        self.dunnett_results.append(self.dunnett_result)
        self.result = (self.r.summary(self.dunnett_result))
        names = self.r("names")
        columns = np.array(names(self.result[-1][2]))
        self.result_df = pd.DataFrame([np.array(i) for i in self.result[-1][2:-1]],
                                      index=["Estimate","Std. Error", "t value", "Pr(>|t|)"],
                                      columns=columns)
        result = ["-------------Result of Dunnett's test-------------\n\n",
                  self.result_df.T,"\n"]
        self.print_func(result,save_mode)

    def fisher_test(self,save_file=""):
        save_mode = self.savemode(save_file=save_file)
        data_to_matrix = self.r("data.matrix")
        matrix = data_to_matrix(self.r_df)
        fisher = self.r("fisher.test")
        result = ["-------------Result of Fisher's Exact test-------------\n",
                  fisher(matrix)]
        self.print_func(result,save_mode)
        
    def steeldwass(self,data_column="",label_column="",save_file=""):
        save_mode = self.savemode(save_file=save_file)
        self.data_column = data_column
        self.label_column = label_column
        data = self.r_df.rx2(self.data_column)
        label_data = ro.FactorVector(self.r_df.rx2(self.label_column))
        result = ["-------------Result of Steel-Dwass test-------------\n\n",
                  self.r.pSDCFlig(data, label_data, method="Monte Carlo")]
        self.print_func(result,save_mode)
        
    def rsource_file_import(self,source_file="",save_file=""):
        r_source = self.r["source"]
        r_source(source_file)
        
    def close(self):
        numpy2ri.deactivate()
        pandas2ri.deactivate()