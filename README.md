# Real-Time Visualization of Sensor Data with Spark Streaming, Kafka, and Kibana

## 1. Project Definition

This project aims to visualize sensor data in real-time by utilizing Spark Streaming, Kafka, and Kibana. The dataset contains data from 255 sensors in 51 rooms across 4 floors of the Sutardja Dai Hall at UC Berkeley. The data includes CO2 concentration, humidity, temperature, light, and PIR motion sensor readings. 
The project involves 
* preprocessing the dataset with PySpark, 
* producing it into a Kafka topic, 
* consuming the topic with Spark Streaming, 
* and finally visualizing the data with Kibana on ElasticSearch.

<img src="https://github.com/semihdesticioglu/Streaming_Sensor_Data_Realtime_Dashboard/blob/f1990afe1731b2495b0891c28c38f2b0705f9895/images/streaming_sensor_data.jpg" width=50% height=50%>

## 2. Usage Details

###   Step 1: Preprocessing the Dataset with PySpark
1.1. Load the dataset and convert it into the required format with PySpark.

1.2. Save the preprocessed dataset to the local disk.

Detail code for processing can be seen in notebook data_preparation.py. This part is an example from the code >

```
function test() {
  console.log("notice the blank line before this function?");
}
```

###  Step 2: Producing Data to Kafka Topic
2.1. Use the data generator to read preprocessed data from the local disk.

2.2. Produce the data into the office-input Kafka topic.

Detail code for Producing data to kafka can be seen in notebook producing_data_on_kafka.py. This part is an example from the code >

```
function test() {
  console.log("notice the blank line before this function?");
}
```
### Step 3: Consuming Data with Spark Streaming and Write it to ElasticSearch
3.1. Create a Spark Streaming application to consume the office-input Kafka topic.

3.2. Create structured data from the consumed messages.

3.3. Write the structured data as an index to Elasticsearch.

Detail code for Consuming data with Spark can be seen in notebook consuming_on_spark_write_to_es.py. This part is an example from the code >

```
function test() {
  console.log("notice the blank line before this function?");
}
```

### Step 4: Creating Kibana Visualizations
4.1. Open Kibana and connect it to the Elasticsearch index containing the sensor data.

4.2. Create visualizations according to the specifications in the `DE_Project_Kibana_Graphs.docx` document.

4.3. Configure the Kibana dashboard to refresh every few seconds to display real-time changes in the graphs.

**Instructions:**

- Access Kibana through your web browser at `http://localhost:5601`.

- Go to the "Management" tab and create an index pattern for the `sensors_data` index in Elasticsearch.

- Navigate to the "Visualize" tab and create visualizations for CO2 concentration, humidity, temperature, light, and PIR motion sensor data according to the provided specifications.

- Once the visualizations are created, go to the "Dashboard" tab and create a new dashboard.

- Add the visualizations to the dashboard and arrange them as desired.

- In the dashboard settings, set the auto-refresh interval to a few seconds (e.g., 5 seconds) to display real-time changes in the graphs.

- Save the dashboard, and it will now display the sensor data in real-time with the specified visualizations.

