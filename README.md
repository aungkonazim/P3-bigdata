# P3-bigdata
Sparse Matrix Vector Multiplication - CSR

**Configuration**

We used apache spark prebuilt version from pip.  

Please run `pip install -r requirements.txt` to install the dependencies

The spark context that we used had the following properties

[('spark.rdd.compress', 'True'),
 ('spark.serializer.objectStreamReset', '100'),
 ('spark.ui.showConsoleProgress', 'true'),
 ('spark.submit.deployMode', 'client'),
 ('spark.app.name', 'pyspark-shell')]

**Note**

Please note that you need to change the environment variable with the version of python you are using
 
` import os
 os.environ["PYSPARK_PYTHON"]="python3.6"` (assuming python3.6 is your version)

Change these two lines of code accordingly

**Exceution**

Main code is in "main3.py" file

Please run the code in terminal with the filepaths as input arguments

Paste the data files in the data folder and Run the following line in terminal 

`python3.6 main3.py ./data/data ./data/rindx ./data/cindx ./data/xvector
`

**Algorithm Description**

Since data in each input file is given in a space separated single line the input was taken sequentially through numpy library
(Using spark functions to read the data would not improve the load on a single node)

After reading the data sequentially I partition the data according to the '`rindx`' values and parallelize them with '`cindx`'
information stored alongside each plus the row index as we determined from processing the '`rindx`' file

Read the '`xvector`' file along with the index of each number on the line

First multiply each number in the sparse matrix with a number from xvector where the column index of the number matches 
with the row index of the xvector.

Next sum each row using the row indices as keys

Find out the missing row indices and fill them with 0

save the output   



 