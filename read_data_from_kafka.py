from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, col
from elasticsearch import Elasticsearch

spark = SparkSession.builder.appName("Read From Kafka") \
    .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:7.12.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
    .getOrCreate()

# Set up Elasticsearch connection
es = Elasticsearch(hosts=["localhost:9200"])

es.indices.delete(index='office-index', ignore=[400, 404])

# Define index settings and mapping
office_index = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "custom_edge_ngram", "asciifolding"]
                    }
                },
                "filter": {
                    "custom_edge_ngram": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 10
                    }
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "event_ts_min": {"type": "date"},
            "ts_min_bignt": {"type": "integer"},
            "room": {"type": "keyword"},
            "co2": {"type": "integer"},
            "light": {"type": "float"},
            "temperature": {"type": "float"},
            "humidity": {"type": "float"},
            "pir": {"type": "float"}
        }
    }
}

# Create the index with the mapping
es.indices.create(index="office-index", body=office_index)




df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092,localhost:9292") \
    .option("subscribe", "office-input") \
    .option("failOnDataLoss", "false") \
    .load()



df2 = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "topic","partition","offset", "timestamp")
df3 = df2.withColumn("event_ts_min", F.split(F.col("value"), ",")[0].cast(TimestampType())) \
.withColumn("ts_min_bignt", F.split(F.col("value"), ",")[1].cast(IntegerType())) \
.withColumn("room", F.split(F.col("value"), ",")[2].cast(StringType())) \
.withColumn("co2", F.split(F.col("value"), ",")[3].cast(IntegerType())) \
.withColumn("light", F.split(F.col("value"), ",")[4].cast(FloatType())) \
.withColumn("temperature", F.split(F.col("value"), ",")[5].cast(FloatType())) \
.withColumn("humidity", F.split(F.col("value"), ",")[6].cast(FloatType())) \
.withColumn("pir", F.split(F.col("value"), ",")[7].cast(FloatType())) \
.drop("value")


# Write the data to Elasticsearch
def writeToElasticsearch(df, epoch_id):

    df.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", "localhost") \
        .option("es.port", "9200") \
        .option("es.resource", "office-index") \
        .mode("append") \
        .save()



checkpointDir = "file:///tmp/streaming/read_from_kafka_write_to_elastic2"

streamingQuery = df3.writeStream \
    .trigger(processingTime="1 second") \
    .option("numRows", 4) \
    .option("truncate", False) \
    .outputMode("append") \
    .option("checkpointLocation", checkpointDir) \
    .foreachBatch(writeToElasticsearch) \
    .start()

streamingQuery.awaitTermination()

