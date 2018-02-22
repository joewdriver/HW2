# this is the k nearest nodes algorithm we'll use on the processed data files.
import pandas, math

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
            for row in csv[column]:
                csv.iat[r,c] = (csv.iat[r,c] - mean)/std
                r = r + 1

        c = c + 1

# since our normalization has introduced negativity into our dataset we can see the added value of squaring the
# distances when we run the k-NN algorithm.

normalize(training)
normalize(testing)

# now we dive into the k-NN algorithm.  This bit is fairly straightforward, but unfortunately computation-heavy.  For
# each of the values in the test database we calculate their distance from all the values in the training database.
# We do this using an extended pythagorean formula.  Once that is done, we identify the k lowest distances and poll them
# to see which class they belong to.  Majority wins.  In case of a tie, we'll let the k+1 next value decide.

def nearest_neighbor(training, testing, k):
    test_rows = testing.shape[0]
    columns = testing.shape[1]
    training_rows = testing.shape[0]

    # we need to add a column to the dataframe to track distances.  the initial value will be replaced, but is left
    # unreasonably high in case for some reason it is not.
    distance_column = columns
    training['Distance'] = 1000.0
    testing['Predictions'] = "!"

    # for each row in the test data set
    for test_row in range(0,test_rows):
        # look at every row in the training data set
        for training_row in range(0,training_rows):
            # set a variable to track the pre-root distance
            sum = 0
            # review the columns with the exception of the last one, which holds the classification
            for column in range(0,columns-1):
                # if numeric, subtract training from testing, square it, and add it to the sum
                if type(testing.iat[test_row,column]) is not str:
                    x = (testing.iat[test_row,column] - training.iat[training_row,column])**2
                    sum = sum + x
                # if it is a string and they are different, the distance is 1.
                if type(testing.iat[test_row, column]) is str:
                    if __name__ == '__main__':
                        if testing.iat[test_row,column] != training.iat[training_row,column]:
                            sum = sum +1
            # after viewing each of the columns for a given row, we take the square root of the sum.  This will
            # be the value that informs our ultimate solution.  We will add this value as a new column at the end
            # of the dataset
            distance = math.sqrt(sum)
            training.iat[training_row, distance_column] = distance
        # Once we have added a distance value for every row in the training dataset, we need to identify the k lowest
        # we pull the min out k + 1 times
        lowest_indexes = []
        for i in range(0,k + 1):
            index = training.ix[:,distance_column].idxmin()
            lowest_indexes.append(index)
            training.iat[index,distance_column] = 1000
        # now that we have the k+1 nearest neighbors, we poll them
        vote = 0
        for neighbor in range(0,k):
            if training.iat[neighbor,distance_column - 1] == '+':
                vote = vote + 1
            if training.iat[neighbor, distance_column - 1] == '-':
                vote = vote - 1
        # once the votes are in we assign the value accordingly
        if vote > 0:
            testing.iat[test_row, columns] = "+"
        elif vote < 0:
            testing.iat[test_row, columns] = "-"
        else:
            testing.iat[test_row, columns] = training.iat[lowest_indexes[k],distance_column - 1]
        # finally, we do it again for every row in the test database

    # our final output is the testing dataset with an added column of expected values (+,-) next to the actual ones.
    testing.to_csv("Results", header=False, index=False)

    # we can then take these two columns and compare them to measure our accuracy.  Since this is being done in python
    # instead of Matlab I am unable to generate a table (or I just don't know how), but I can report the rough results
    # below -- feel free to add different values of k when running the program.
    matches = 0
    for i in range(0, test_rows):
        if testing.iat[i, distance_column - 1] == testing.iat[i, distance_column]:
            matches = matches + 1
    success_rate = matches/(test_rows)
    print("The success rate of our classifier is " + str(success_rate))

    # k = 2, accuracy = .602
    # k = 3, accuracy = .601
    # k = 4, accuracy = .695

nearest_neighbor(training, testing, k)
