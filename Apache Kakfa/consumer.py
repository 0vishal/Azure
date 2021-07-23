'''
@Author: Vishal Salaskar
@Date: 2021-06-26
@Last Modified by: Vishal Salaskar
@Last Modified time: 2021-06-26
@Title : Program to perform  apache kafa to read from consumer
'''
from kafka import KafkaConsumer, consumer
import os

class Consumer:


    def __init__(self):
        """
        Description : required connection to Kafka server and topic 
        """
        TOPIC_NAME = os.getenv('TOPIC_NAME')
        KAFKA_SERVER = os.getenv('SERVER')
        self.consumer = KafkaConsumer(TOPIC_NAME,auto_offset_reset='earliest',bootstrap_servers=[KAFKA_SERVER],api_version=(0, 10))

    def read_data(self):
        """
        description : to read the twitter tweets data
        """
        try:
            for message in self.consumer:
                message = message.value
                print(message)
        except:        
            print("error")        

if __name__ == "__main__":

    get_data = Consumer()
    get_data.read_data()

