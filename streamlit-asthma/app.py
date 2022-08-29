from importables import *
from use_model import callmodel

# show_weather function will call API to get weather data and show specific parameters.
def show_weather():
	user_api = "78d93dd790c8f2244c2325b9ddd7b7ca"
	complete_api_link = "https://api.openweathermap.org/data/2.5/onecall?lat=" + st.session_state.latitude + "&lon=" + st.session_state.longitude+"&appid="+user_api
	api_link = requests.get(complete_api_link)
	data = api_link.json()

	#api variables:
	st.session_state.humidity = data["current"]["humidity"]
	st.session_state.pressure = data["current"]["pressure"]
	st.session_state.temp = data["current"]["temp"] - 273.15
	st.session_state.uvi = 1 if data["current"]["uvi"] < 5 else 0 
	st.session_state.wind = data["current"]["wind_speed"]

	new_title = '<p style="font-family:fantasy; color:Green; font-size: 28px;">Weather Report:</p>'
	st.markdown(new_title, unsafe_allow_html=True)
	
	col1, col2 = st.columns(2)
	with col1:
		st.write("**Weather Type:** ",data['current']['weather'][0]['main'])
		st.write("**Actual Temperature:** {0:.2f} C".format(data['current']['temp'] - 273.15))
		st.write("**Feels Like:** {0:.2f} C".format(data["current"]["feels_like"] - 273.15))
		st.write("**Humidity:** {}%".format(data["current"]["humidity"]))
		st.write("**Pressure:** {} hPa".format(data["current"]["pressure"]))
	with col2:
		st.write("**UV Index:** " + str(data["current"]["uvi"]))
		st.write("**Wind Speed:** {} mt/sec.".format(data["current"]["wind_speed"]))
		st.write("**Clouds:** {}% ".format(data["current"]["clouds"]))
		st.write("**Visibility:** {} mt.".format(data["current"]["visibility"]))
		st.write("**Timezone:** " + str(data["timezone"]))

# run_model calls the pretrained model to get output and show features of Explainable AI.
def run_model():
	result = callmodel(age=st.session_state.age,
		gender=st.session_state.gender,
		outdoorjob=st.session_state.outdoorjob,
		outdooractivity=st.session_state.outdooractivity,
		smoking=st.session_state.smoking,
		humidity=st.session_state.humidity,
		pressure=st.session_state.pressure,
		temp=st.session_state.temp,
		uv=st.session_state.uvi,
		wind=st.session_state.wind
		)

	if result[0]=='High':
		st.error("Asthma Alert is High! Prefer to stay Indoors.!")
	elif result[0]=='Low':
		st.success("Congrats! Asthma Alert is Low.!")
	elif result[0]=='Moderate':
		st.warning("Asthma Alert is Moderate! Prefer NOT to Stay Outside for a Long Time.!")


	# XAI html report will pop up in the streamlit screen.
	st.header("Explainabe Report for the given features.!")
	HtmlFile = open("explained_data.html", 'r', encoding='utf-8')
	source_code = HtmlFile.read() 
	components.html(source_code,height=1000)

#Page Headers
st.set_page_config(page_title='Asthma Alert Prototype')
st.title("Welcome to Streamlit Weather App and Asthma Detection Prototype!")
st.write("We will provide Personalized Asthma Alert.")
st.write("But! Before that help us with your data.")

#dictionaries
age_dict = {"19-30 (0)":0, "31-40 (1)":1, "41-50 (2)":2, "Above 50 (3)":3}
gender_dict = {"Male (1)":1, "Female (0)":0}
outdoorjob_dict = {"Occasionally (1)":1, "Frequently (0)":0, "Rarely (2)":2}
outdooractivity_dict = {"Extremely Likely (0)":0, "Not at all Likely (2)":2, "Neither Likely nor Dislikely (1)":1} 
smoking_dict = {"Yes (1)":1,"No (0)":0}
target = {0:"High", 1:"Low", 2:"Moderate"}

#sidebar inputs
age = st.sidebar.selectbox("What is your Age?",["19-30 (0)", "31-40 (1)", "41-50 (2)", "Above 50 (3)"])
gender = st.sidebar.selectbox("What is your Gender?",["Female (0)","Male (1)"])
outdoorjob = st.sidebar.selectbox("How often do you go for Outdoor Job?",["Frequently (0)","Occasionally (1)", "Rarely (2)"])
outdooractivity = st.sidebar.selectbox("How likely do you go for an Outdoor Activity?",["Extremely Likely (0)", "Neither Likely nor Dislikely (1)", "Not at all Likely (2)"])
smoking = st.sidebar.selectbox("Do you have smoking habit?",["No (0)", "Yes (1)"])

#final variables:
st.session_state.age = age_dict[age]
st.session_state.gender = gender_dict[gender]
st.session_state.outdoorjob = outdoorjob_dict[outdoorjob]
st.session_state.outdooractivity = outdooractivity_dict[outdooractivity]
st.session_state.smoking = smoking_dict[smoking]

#radio button for detecting Manual Place or Automatic Place
ques = st.radio("Do You Want to Manually Input Place?",("Yes","No"))
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.warning("Choosing 'NO' will detect Your Location Automatically!")


if 'latitude' not in st.session_state:
	st.session_state.latitude = ""
if 'longitude' not in st.session_state:
	st.session_state.longitude = ""



if ques == 'Yes':
	title = st.text_input('Enter Your Location: ')
	if st.button('Validate Location and Run Model'):
		geolocator = Nominatim(user_agent="MyApp")
		location = geolocator.geocode(title)
		if location:
			st.session_state.latitude = str(location.latitude)
			st.session_state.longitude = str(location.longitude)
			st.write("Your Location is Validated Successfully.")
			st.write("Detected Latitude: " + st.session_state.latitude + " and Longitude: " + st.session_state.longitude)
			show_weather()
			run_model()

		else:
			st.write("Invalid Location, Please Try Again.")
			st.session_state.latitude = ""
			st.session_state.longitude = ""
else:
	#for automatic location, location will be detected from IP address.
	g = geocoder.ip('me')
	st.session_state.latitude = str(g.latlng[0])
	st.session_state.longitude = str(g.latlng[1])
	geolocator = Nominatim(user_agent="geoapiExercises")
	location = geolocator.geocode(st.session_state.latitude+","+st.session_state.longitude)
	st.write("Detected Latitude: " + st.session_state.latitude + " and Longitude: " + st.session_state.longitude)
	st.write("Detected Location: ", location)
	show_weather()
	run_model()
