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
        
    def import_csv(self,csv_path="",header='infer',index_col=None):
        self.csv_path = csv_path
        try:
            self.p_df = pd.read_csv(self.csv_path,header=header,index_col=index_col)
            self.r_df = pandas2ri.py2ri(self.p_df)
            self.colnames = np.array(self.r_df.names).tolist()
            print("column names:")
            print(self.colnames)
            print("Import was succeeded")
        except:
            print("Import was failed")
            
    def _savemode(self):
        if len(self.save_file)!=0:
            self.save_mode = True
        else:
            self.save_mode = False
        
    def _preprocessing(self,data_column="",label_column="",save_file=""):
        data = self.r_df.rx2(data_column)
        label_data = ro.FactorVector(self.r_df.rx2(label_column))
        lm_name = f"{data_column} ~ label_data"
        self.save_file = save_file
        self._savemode()
        return label_data, data, lm_name
        
    def print_func(self,result):        
        if self.save_mode:
            with open(self.save_file,"a") as f:
                print(*result,file=f)
        else:
            print(*result)
    
    def aov(self,data_column="",label_column="",save_file=""):
        label_data, data, lm_name = self._preprocessing(data_column=data_column,
                                                        label_column=label_column,
                                                        save_file=save_file)
        ro.globalenv["label_data"] = label_data
        ro.globalenv[data_column] = data

        lm_D = self.r.lm(lm_name)
        anova_result = self.r.aov(lm_D)
        result = ["-------------Result of ANOVA-------------\n",
                 self.r.anova(anova_result)]
        self.print_func(result)
            
        return anova_result, label_data, data, lm_name
    
    def oneway(self,data_column="",label_column="",var=False,save_file=""):
        label_data, data, lm_name = self._preprocessing(data_column=data_column,
                                                                   label_column=label_column,
                                                                   save_file=save_file)
        ro.globalenv["label_data"] = label_data
        ro.globalenv[data_column] = data

        fmla = ro.Formula(lm_name)
        onewayf = self.r("oneway.test")
        self.oneway_result = onewayf(fmla,**{"var.equal":var})
        result = ["-------------Result of Welch's ANOVA-------------\n",
                  self.oneway_result]
        self.print_func(result)
            
    def tukeyHSD(self,data_column="",label_column="",save_file=""):
        anova_result, label_data, data, lm_name = self.aov(data_column=data_column,
                                                           label_column=label_column,
                                                           save_file=save_file)
        self.tukeyhsd_result = self.r.TukeyHSD(anova_result)
        result = ["-------------Result of TukeyHSD test-------------\n\n",
                  self.tukeyhsd_result[0]]
        self.print_func(result)
        
    def dunnett_test(self,data_column="",label_column="",save_file=""):
        anova_result, label_data, data, lm_name = self.aov(data_column=data_column,
                                                           label_column=label_column,
                                                           save_file=save_file)
        
        dunnett = self.r.mcp(label_data="Dunnett")
        dunnett_result = self.r.glht(anova_result, linfct=dunnett)
        dunnett_result_summary = (self.r.summary(dunnett_result))
        names = self.r("names")
        columns = np.array(names(dunnett_result_summary[-1][2]))
        dunnett_result_summary_df = pd.DataFrame([np.array(i) for i in dunnett_result_summary[-1][2:-1]],
                                      index=["Estimate","Std. Error", "t value", "Pr(>|t|)"],
                                      columns=columns)
        result = ["-------------Result of Dunnett's test-------------\n\n",
                  dunnett_result_summary_df.T,"\n"]
        self.print_func(result)

    def fisher_test(self,save_file=""):
        self.save_file = save_file
        self._savemode()
        data_to_matrix = self.r("data.matrix")
        matrix = data_to_matrix(self.r_df)
        fisher = self.r("fisher.test")
        result = ["-------------Result of Fisher's Exact test-------------\n",
                  fisher(matrix)]
        self.print_func(result)
        
    def steeldwass(self,data_column="",label_column="",save_file=""):
        label_data, data, lm_name = self._preprocessing(data_column=data_column,
                                                        label_column=label_column,
                                                        save_file=save_file)
        result = ["-------------Result of Steel-Dwass test-------------\n\n",
                  self.r.pSDCFlig(data, label_data)]
        self.print_func(result)
        
    def rsource_file_import(self,source_file="",save_file=""):
        r_source = self.r["source"]
        r_source(source_file)
        
    def close(self):
        numpy2ri.deactivate()
        pandas2ri.deactivate()