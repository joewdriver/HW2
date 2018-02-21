# this is the k nearest nodes algorithm we'll use on the processed data files.
import pandas

# First we'll pull in the processed data sets from our previous script
training = pandas.read_csv('training_processed.csv', header=None)
testing = pandas.read_csv('testing_processed.csv', header=None)

# now we need to get the value of k from the user and ensure it is an integer
k = int(input("Enter an Integer:"))

# k will indicate how many of our neighbor nodes we will look at when trying to classify new data nodes.

# before we dive into the algorithm, however, we'll need to normalize the numerical data using the
# z-scaling method dictated by the assignment.  This will prevent larger numbers from outweighing smaller ones
# when there is no true difference in their weight.  String values we will leave alone.

def normalize(csv):
    c = 0
    for column in csv:
        r = 0
        if type(csv[column][1]) is not str:

            # for numeric values we calculate the mean and standard deviation of the column
            mean = csv[column].mean()
            std = csv[column].std()

            # next we subtract the mean from the value itself and divide by the std

        c = c + 1

normalize(training)
