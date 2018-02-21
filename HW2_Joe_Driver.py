# this is my homework solution for the nearest neighbors problem.  The report will be submitted as code comments.
import pandas

# a bit of preprocessing needs to be done before anything else -- all numberic strings should be converted to
# numbers.

def convert_to_num(dataframe):
    rows = dataframe.shape[0]
    cols = dataframe.shape[1]
    for row in range(0,rows-1):
        for col in range(0,cols-1):
            if type(dataframe.iat[row,col]) is str:
                try:
                    dataframe.iat[row, col] = float( dataframe.iat[row, col])
                except:
                    pass
    return dataframe

# our first task is to import both files for work.  I'll be using the pandas library, which does not provide any
# machine learning functionality, but quite a bit of support with matrices.  For this submission you will have to
# alter the address of the data sets below

training = pandas.read_csv('crx.data.training', header=None)
testing = pandas.read_csv('crx.data.testing', header=None)

training = convert_to_num(training)
testing = convert_to_num(testing)

# next we have to fill in the missing values of the data set.  I'll be using a fairly simple approach--for numerical
# sets I am going to take the average of the entire column and enter that for the missing values.  In cases of text
# coding I am going to retrieve the most commonly occuring value and input that

i = 0
for column in training:
    i = i+1
    print("COLUMN " + str(i))

    # first identify the value we'll be inputting.  I'm using the second row (index 1) in the data set since it has no
    # missing values whereas the first row does and can confuse the reader.

    if type(training[column][1]) is str:
        # For strings this will retrieve the most common value and input it
        mode = training[column].value_counts().idxmax()
        # locate missing entries
        missing = 0
        for row in training[column]:
            if row == "?":
                missing = missing + 1
                row = mode
        print(str(missing) + " missing string values replaced with " + mode)

    else:
        # for numbers we will input the average of the entire column
        temp = training[column]
        sum = 0
        for row in temp:
            try:
                sum = sum + row
            except:
                pass
        mean = sum/len(temp)
        missing = 0
        for row in training[column]:
            if row == "?":
                missing = missing + 1
                row = mean
        print(str(missing) + " missing number values replaced with " + str(mean))