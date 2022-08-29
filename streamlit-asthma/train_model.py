from importables import *
warnings.filterwarnings('ignore')
# get_data function will fetch data from dataset
# preprocess the dataset and provide train test split.
def get_data():
	df = pd.read_csv("data/dataset.csv")
	df = df.drop(['UserNo.','UserID','Location'],axis=1)

	# changing the continuous target variable to categorical target variable.
	df['ACTScore'] = pd.cut(df.ACTScore,bins=[0,15,19,25],labels=['High','Moderate','Low'])

	#label order encoding to all the categorical feature points
	df['Age'] = LabelEncoder().fit_transform(df.Age)
	df['Gender'] = LabelEncoder().fit_transform(df.Gender)
	df['OutdoorJob'] = LabelEncoder().fit_transform(df.OutdoorJob)
	df['OutdoorActivities'] = LabelEncoder().fit_transform(df.OutdoorActivities)
	df['SmokingHabit'] = LabelEncoder().fit_transform(df.SmokingHabit)
	df['UVIndex'] = LabelEncoder().fit_transform(df.UVIndex)

	# Oversampling to the lower count targets.
	sm = SMOTE(sampling_strategy='auto', random_state=42)
	X, Y = sm.fit_resample(df.drop('ACTScore', axis=1), df['ACTScore'])
	df = pd.concat([pd.DataFrame(Y), pd.DataFrame(X)], axis=1)

	# Dividing the dataset to training points and target variable
	Y = df["ACTScore"]
	X = df[["Age","Gender","OutdoorJob","OutdoorActivities","SmokingHabit","Humidity","Pressure","Temperature","UVIndex","WindSpeed"]]

	return train_test_split(X, Y, random_state=42, test_size = 0.3)

print("Started Training your model!...")
X_train, X_test, y_train, y_test = get_data()

# Taking model choice from user.
flag = False
# while not flag:
	# i = str(input("Press 0: RandomForestClassifier & Press 1: LogisticRegression: "))
	# if i == '0':
	# 	model = RandomForestClassifier(n_estimators = 15, random_state = 0)
	# 	flag = True
	# elif i == '1':
	# 	model = LogisticRegression()
	# 	flag = True
	# else:
	# 	print("Invalid Input, Try Again!")
	

#training model
model = RandomForestClassifier(n_estimators = 15, random_state = 0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

precision, recall, fscore, support = score(y_test, y_pred)
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))


filename = "pretrained_model.joblib"
joblib.dump(model, filename)
print("Model Trained and Saved Successfully!")