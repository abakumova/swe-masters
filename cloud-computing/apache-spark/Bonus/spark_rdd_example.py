import sys
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name


# Custom function for computing a sum.
# Inputs: a and b are values from two different RDD records/tuples.
def customSum(a, b):
    sum = a + b

    return sum


def split_words(line):
    file_name, line_text = line
    words = re.findall(r'\b[a-z]+\b', line_text.lower())
    return [(file_name, word) for word in words]


def top_five(records):
    sorted_records = sorted(records, key=lambda x: x[1], reverse=True)
    return sorted_records[:5]


def get_word_count(record):
    ((file_name, word), count) = record
    return (file_name, (word, count))


def get_total_word_count(record):
    (file_name, count) = record
    return (file_name, count)


if __name__ == "__main__":
    # Check the number of arguments
    if len(sys.argv) != 2:
        print("Usage: wordcount <file>", file=sys.stderr)
        exit(-1)

    # Set a name for the application
    appName = "PythonWordCount"

    # Set the input folder location to the first argument of the application
    # NB! sys.argv[0] is the path/name of the script file
    input_folder = sys.argv[1]

    # Create a new Spark application and get the Spark session object
    spark = SparkSession.builder.appName(appName).getOrCreate()

    # Get the spark context object.
    sc = spark.sparkContext

    # Load input RDD from the data folder
    # lines = sc.textFile(input_folder)
    lines = spark.read.text(input_folder).select(input_file_name(), "value").rdd.map(tuple)

    # Take 5 records from the RDD and print them out
    #records = lines.take(5)
    #for record in records:
    #    print(record)

    # Apply RDD operations to compute WordCount
    # lines RDD contains lines from the input files.
    # Lets split the lines into words and use flatMap operation to generate an RDD of words.
    # words = lines.flatMap(lambda line: line.split(' '))
    words = lines.flatMap(split_words)

    word_counts = words.map(lambda word: ((word[0], word[1]), 1)).reduceByKey(lambda a, b: a + b)
    file_word_counts = word_counts.map(lambda x: (x[0][0], x[1])).reduceByKey(lambda a, b: a + b)
    total_word_counts = file_word_counts.mapValues(lambda x: 1 / x)

    file_word_frequencies = word_counts.map(lambda x: (x[0][0], (x[0][1], x[1]))).join(total_word_counts).map(
        lambda x: (x[0], (x[1][0][0], x[1][0][1] * x[1][1])))

    top_five_frequencies = file_word_frequencies.groupByKey().mapValues(
        lambda x: sorted(x, key=lambda y: y[1], reverse=True)[:5])

    top_five_frequencies.saveAsTextFile("output_bonus")

    # Transform words into (word, 1) Key & Value tuples
    #pairs = words.map(lambda word: (word, 1))

    # Apply reduceBy key to group pairs by key/word and apply sum operation on the list of values inside each group
    # Apply our of customSum function as the aggregation function, but we could also have used "lambda x,y: x+y" function
    #counts = pairs.reduceByKey(customSum)

    # Read the data out of counts RDD
    # Output is a Python list (of (key, value) tuples)
    #output = counts.map(get_word_count).groupByKey().mapValues(top_five)

    #output.saveAsTextFile("output")
    # Print each key and value tuple inside output list
    # for (word, count) in output:
    #    print(word, count)

    # Stop Spark session. It is not required when running locally through PyCharm.
    # spark.sparkContext.stop()
    # spark.stop()
