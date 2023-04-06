import sys
from pyspark.sql.functions import avg
from pyspark.sql import SparkSession

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: dataframe_example.py <input folder> ")
        exit(-1)

    appName = "DataFrame Lab 8"
    input_folder = sys.argv[1]

    spark = SparkSession.builder.appName(appName).getOrCreate()

    dataset = spark.read \
                  .option("inferSchema", True) \
                  .option("header", True) \
                  .csv(input_folder)

    dataset.show(10, False)
    dataset.printSchema()

    # Compute the Average Humidity of all stations (group by stations)
    filtered_data = dataset.filter(dataset["Air Temperature"] > 20)
    result = filtered_data.groupBy("Station Name").agg(avg("Humidity").alias("Average Humidity"))

    print("\n\n\nResults:")
    result.show(20, False)
    result.printSchema()

    result.write.format("csv") \
        .option("header", True) \
        .option("compression", "gzip") \
        .save("output")

    spark.stop()
