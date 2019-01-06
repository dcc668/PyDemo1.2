import pandas as pd
import numpy as np

df1=pd.DataFrame([[1,2,3],[4,5,6]],columns=["col1","col2","col3"])
df2=pd.DataFrame([[3,4,5],[1,5,6]],columns=["col1","col2","col3"])

print(df1)
print(df2)

res=df1/df2
print(res)

res=[]
df1=pd.DataFrame([[1,2,3],[4,5,6]],columns=["col1","col2","col3"])
df2=pd.DataFrame([[3,4,5],[1,5,6]],columns=["col1","col2","col3"])
res.append(df1.values)
res.append(df2.values)

print(res)
print(np.array(res).shape)

