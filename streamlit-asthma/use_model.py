from importables import *
from train_model import get_data 
warnings.filterwarnings('ignore')
#callmodel function will get data from streamlit UI and use here.
def callmodel(age, gender, outdoorjob, outdooractivity, smoking, humidity, pressure, temp, uv, wind):
	
	#loading pretrained model
	filename = "pretrained_model.joblib"
	loaded_model = joblib.load(filename)

	#loading data
	X_train, X_test, y_train, y_test = get_data()

	# setup of test data
	test_data = {
	    "Age": [int(age)],
	    "Gender": [int(gender)],
	    "OutdoorJob": [int(outdoorjob)],
	    "OutdoorActivities": [int(outdooractivity)],
	    "SmokingHabit": [int(smoking)],
	    "Humidity": [int(humidity)],
	    "Pressure": [int(pressure)],
	    "Temperature": [float(temp)],
	    "UVIndex": [int(uv)],
	    "WindSpeed": [float(wind)]
	}
	test_dataframe = pd.DataFrame(test_data)

	# explainable AI setup
	lime_explainer = lime_tabular.LimeTabularExplainer(np.array(X_train),
		mode="classification",
		feature_names=X_train.columns,
		categorical_features=[0,1,2,3,4,5,9],
		class_names=['High','Low','Moderate']
		)

	exp = lime_explainer.explain_instance(data_row=test_dataframe.iloc[0], 
	    predict_fn=loaded_model.predict_proba,
	    top_labels=3)

	# Saving XAI output
	exp.save_to_file('explained_data.html')

	
	predicted_output = loaded_model.predict(test_dataframe)

	return predicted_output