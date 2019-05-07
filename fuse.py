import pandas as pd

df1 = pd.read_csv("config_bdd15000-20000_encoded.csv")
df2 = pd.read_csv("config_bdd20000-30000_encoded.csv")
df3 = pd.read_csv("config_bdd30000-40000_encoded.csv")
df4 = pd.read_csv("config_bdd40000-60000_encoded.csv")
df5 = pd.read_csv("config_bdd60000-90000_encoded.csv")
df6 = pd.read_csv("config_bdd90000-100000_encoded.csv")
df7 = pd.read_csv("config_bdd100000-1265000_encoded.csv")

df = pd.concat([df1,df2,df3,df4,df5,df6,df7])

#Save some memory
del(df1)
del(df2)
del(df3)
del(df4)
del(df5)
del(df6)
del(df7)

basic_head = ["cid", "time", "date"] # "compile"
size_methods = ["vmlinux", "GZIP-bzImage", "GZIP-vmlinux", "GZIP", "BZIP2-bzImage", 
              "BZIP2-vmlinux", "BZIP2", "LZMA-bzImage", "LZMA-vmlinux", "LZMA", "XZ-bzImage", "XZ-vmlinux", "XZ", 
              "LZO-bzImage", "LZO-vmlinux", "LZO", "LZ4-bzImage", "LZ4-vmlinux", "LZ4"]
compilation_status_column_name = 'compile_success'

#Find tri state options
#tri state step
tri_state_values = [0, 1, 2]

ftuniques = []
freq_ymn_features = []
non_tristate_options = []

for col in df:
    ft = df[col]    
    # eg always "y"
    if len(ft.unique()) == 1:
        ftuniques.append(col)
    # only tri-state values (y, n, m) (possible TODO: handle numerical/string options)    
    elif all(x in tri_state_values for x in ft.unique()):     #len(ft.unique()) == 3: 
        freq = ft.value_counts(normalize=True)
        freq0 = 0
        freq1 = 0
        freq2 = 0
        if (0 in freq.index):
            freq0 = freq[0]
        if (1 in freq.index):
            freqn = freq[1]
        if (2 in freq.index):
            freqm = freq[2]
        freq_ymn_features.append((col, freq0, freq1, freq2))
    else:
        if not (col in size_methods): 
            non_tristate_options.append(col)
        


print(str(len(df)) + " before the removal of some entries (those with same configurations)")
#Dropping duplicates
df.drop_duplicates(subset=df.columns.difference(ftuniques).difference(size_methods).difference(basic_head).difference(non_tristate_options), inplace=True)
print(str(len(df)) + " after the removal of some entries (those with same configurations)")

df.to_csv("dataset_encoded.csv", index=False)