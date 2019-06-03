import pandas as pd

list_csv=[
    "config_bdd15000-20000.csv",
    "config_bdd20000-30000.csv",
    "config_bdd30000-40000.csv",
    "config_bdd40000-60000.csv",
    "config_bdd60000-90000.csv",
    "config_bdd90000-100000.csv",
    "config_bdd100000-1265000.csv",
]

for csv in list_csv:

    df = pd.read_csv(csv)

    basic_head = ["cid", "time", "date"] # "compile"
    size_methods = ["vmlinux", "GZIP-bzImage", "GZIP-vmlinux", "GZIP", "BZIP2-bzImage", 
                  "BZIP2-vmlinux", "BZIP2", "LZMA-bzImage", "LZMA-vmlinux", "LZMA", "XZ-bzImage", "XZ-vmlinux", "XZ", 
                  "LZO-bzImage", "LZO-vmlinux", "LZO", "LZ4-bzImage", "LZ4-vmlinux", "LZ4"]
    compilation_status_column_name = 'kernel_size'

    #Filtering out X86_32 configuration
    df.query("X86_64 == 'y'", inplace=True)
    
    def nbyes(row):
        return sum(row == "y")                    
    df['nbyes'] = df.apply(nbyes, axis=1)

    #Filtering out specific cid
    df.query("cid != 74459", inplace=True)
    df.query("cid != 30698", inplace=True)

    #tri state step
    tri_state_values = ['y', 'n', 'm']

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
            freqy = 0
            freqn = 0
            freqm = 0
            if ('y' in freq.index):
                freqy = freq['y']
            if ('n' in freq.index):
                freqn = freq['n']
            if ('m' in freq.index):
                freqm = freq['m']
            freq_ymn_features.append((col, freqy, freqm, freqn))
        else:
            if not (col in size_methods): 
                non_tristate_options.append(col)

    from sklearn.preprocessing import LabelEncoder
    def encode_data_compilation(df):
        lae = LabelEncoder()
        # we save quantitative values we want (here vmlinux, TODO: generalize)
        # the key idea is that the labelling encoder should not be applied to this kind of values (only to predictor variables!)
        # vml = rawtuxdata['LZO'] # rawtuxdata['vmlinux'] 
        o_sizes = df[size_methods]
        cid = df["cid"]
        # we may remove non tri state options, but TODO there are perhaps some interesting options (numerical or string) here
        #tuxdata = rawtuxdata.drop(columns=non_tristate_options).drop(columns=['vmlinux']).apply(le.fit_transform)
        df_encoded = df.drop(columns=non_tristate_options).drop(columns=size_methods).apply(lae.fit_transform)

        #tuxdata['vmlinux'] = vml 
        #df_encoded[size_methods] = o_sizes
        # we can ue vmlinux since it has been restored thanks to previous line
        df_encoded[size_methods] = o_sizes[size_methods]
        df_encoded["cid"]=cid
        return df_encoded

    df_encoded = encode_data_compilation(df)

    df_encoded.to_csv(csv.split(".")[0]+"_encoded_all_size.csv", index=False)