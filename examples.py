from rpy2_wrapper import R

def main():
    rinst = R()
    rinst.import_csv("sample_data.csv")
    print(type(rinst.p_df))
    rinst.p_df
    print(type(rinst.r_df))
    rinst.r_df
    rinst.aov(data_column="data.5",label_column="category")
    rinst.tukeyHSD(data_column="data.5",label_column="category")
    rinst.oneway(data_column="data.5",label_column="category")
    rinst.dunnett_test(data_column="data.5",label_column="category")
    rinst.close()
    rinst2 = R()
    rinst2.import_csv("sample_data2.csv",index_col=0)
    rinst2.p_df
    rinst2.fisher_test()
    rinst2.close()
    rinst3 = R()
    rinst3.import_csv("sample_data3.csv")
    rinst3.steeldwass(data_column="data.5",label_column="category")
    rinst3.close()

if __name__=="__main__":
    main()
    print("complete")