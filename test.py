 
import numpy as np
import pandas as pd
from ipdb import set_trace

df = pd.DataFrame({'a':[1,2],'b':[2,3],'c':[3,4], 'd':[5,6]})
#
#dic = {1:10,2:20,3:30}
#df.set_index(['a', 'b'],inplace = True)
#df['new'] = df.index[1]
#df['new'] = df['new'].apply(lambda x: dic[x])
#print(df)
#print(dict)
a = list()
b = list()
c = list()
df.set_index(['a'],inplace = True)
print(df)
set_trace()
print(df.index[0])
set_trace()
for i in df.b:
    a.append(i)
    ad = i*i
    b.append(ad)

print(a)
print(b)
