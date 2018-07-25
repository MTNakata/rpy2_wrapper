from rpy2_wrapper import R

def main():
    import_data = "sample_data.csv"
    rinst = R()
    rinst.import_csv(import_data)
    data_column="data.5"
    label_column="category"
    anova_results = rinst.aov(data_column=data_column,label_column=label_column)
    rinst.tukeyHSD(data_column=data_column,label_column=label_column)
    rinst.oneway(data_column=data_column,label_column=label_column)
    rinst.dunnett_test(data_column=data_column,label_column=label_column)
    rinst.close()
    import_data = "sample_data2.csv"
    rinst2 = R()
    rinst2.import_csv(import_data,index_col=0)
    rinst2.fisher_test()
    rinst2.close()
    import_data = "sample_data3.csv"
    rinst3 = R()
    rinst3.import_csv(import_data)
    rinst3.steeldwass(data_column=data_column,label_column=label_column)
    rinst3.close()

if __name__=="__main__":
    main()
    print("OK")