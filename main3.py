import os
os.environ["PYSPARK_PYTHON"]="python3.6"
import sys
import pyspark
sc = pyspark.SparkContext('local[10]')
import numpy as np
xvector = np.loadtxt(sys.argv[4])
xvector = list(enumerate(xvector))
xvector = sc.parallelize(xvector)
data = np.loadtxt(sys.argv[1])
rindx = np.loadtxt(sys.argv[2])
cindx = np.loadtxt(sys.argv[3])
print(len(data),len(cindx),len(rindx))
temp =  [(i,data[int(rindx[i]):int(rindx[i+1])],cindx[int(rindx[i]):int(rindx[i+1])]) for i in range(len(rindx)-1)]
data2 = sc.parallelize(temp)
data3  = data2
def split_4(x):
    rindx = x[0]
    data = x[1]
    cindx = x[2]
    return [(int(cindx[i]),[float(data[i]),rindx]) for i in range(len(data))]
data4 = data3.flatMap(lambda x:split_4(x))
data5 = data4.groupByKey().map(lambda x:(x[0],list(x[1])))
# counter = sc.accumulator(0)
def split_5(x):
    value_rindx = x[0]
    value_xvector = int(x[1])
    return [(value_rindx[i][1],value_rindx[i][0]*value_xvector) for i in range(len(value_rindx))]
data6 = data5.join(xvector)
data7 = data6.flatMap(lambda x:split_5(x[1]))
data8 = data7.reduceByKey(lambda a,b:a+b).sortByKey()
rindx = np.array([int(i) for i in rindx])
diff_rindx = np.diff(rindx)
ind_diff_rindx = list(range(len(diff_rindx)))
ind_diff_rindx = np.array(ind_diff_rindx)[np.where(diff_rindx==0)[0]]
ind_rindx = list(range(len(rindx)))
output = []
for i in ind_diff_rindx:
    output.extend([(i,0)])
output = output + data8.collect()
output = np.array(output)
output = output[output[:,0].argsort()]
output = list(output[:,1])
for i in range(len(output)):
    output[i] = str(int(output[i]))
output_sentence = " ".join(output)
with open('yvector','w') as f:
    f.write(output_sentence)
    f.close()
sc.stop()