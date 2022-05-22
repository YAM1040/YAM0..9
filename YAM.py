from os import read
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from HeBERT.src.HebEMO import *
from csv import writer
import os 
#Requirements: Torch, TensorFlow, Flax, python 3.8.10, pandas, bs4 ,HeBert

class Main:
  def Request():
    try:#send get request
      URL = (input("please enter a specific FXP forums URL: "))
      page = requests.get(URL)
      soup = BeautifulSoup(page.content, 'html.parser')
      page_body = soup.find_all('p', {'threaddesc'})  
      with open('output.csv', 'w+', newline ='') as file:   
          write = csv.writer(file)
          write.writerows(page_body)     
    except requests.exceptions.RequestException as e:
      print("Access denied please check your internet configuration, using another IP address might help")
      print("closing YAM...")
      quit()
    except:
      print("Unknown error. Please check your connectivity and installed dependencies")
      print("closing YAM...")
      quit()
    
    
  def AnalyzingFunc():
    try:#read line by line and process witb HeBert
      print("HeBERT is analyzing the data this may take a while, please wait.")
      with open('output.csv','r') as file2:
        reader_obj = csv.reader(file2)
        for i in reader_obj:
            HebEMO_model = HebEMO()
            hebEMO_df = HebEMO_model.hebemo(i)
            hebEMO_df.to_csv('non_filter_id.csv', mode='a') 
    except:
      print("Unknown error. Please check your connectivity and installed dependencies")
      print("closing YAM...")
      quit()

    try:#filter the results for negative emotions
      df = pd.read_csv('non_filter_id.csv')
      df_fear = df[df['fear'] == '1']
      df_fear.to_csv('fear_id_results.csv', mode = 'a')
      df_anger = df[df['anger'] == '1']
      df_anger.to_csv('anger_id_results.csv', mode = 'a')
      df_sadness = df[df['sadness'] == '1']
      df_sadness.to_csv('sadness_id_results.csv', mode = 'a')
      os.remove('output.csv')
    except:
      print("Unknown error. Please check your connectivity and installed dependencies")
      print("closing YAM...")
      quit()
    else:
      print("successfull operation!")
      print("output files are located under the YAM's folder")
      print("thank you for using YAM")

  Request()
  AnalyzingFunc()