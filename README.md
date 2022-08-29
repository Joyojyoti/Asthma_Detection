## Asthma Detection Prototype!

### Run Command:

To Run the Streamlit app in browser, located to the base folder where all the files are being stored.

Give the below command.

```
streamlit run app.py
``` 

To train the model, locate to the base folder where all the files are being stored.

Give the below command.

```
python train_model.py
```

Then give your choice of model and train+save the model.



***********************************************************************

train_model.py will train the model given dataset in 'data/' folder.

It will generate Proper Evaluation measures for the dataset and save the trained model.

Trained model name = pretrained_model.joblib

*********************************************************************** 

use_model.py will use the pre-trained model and apply Explainable AI algorithms

The output of XAI algorithms will be stored as "explained_data.html"

***********************************************************************

app.py is the main streamlit app which will host the app in web browser.

It will internally call use_model.py and display XAI data.

***********************************************************************
