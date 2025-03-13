For training the model and inference, Use the train.ipynb notebook. The dataset is also imported and preprocessed in this file as well.

To build and run both the streamlit and flask api, use the below command - 

docker-compose up –build
 
For running in detached mode -

docker-compose up -d


Access the apps on the following ports after building the containers and running them. 
Flask API → http://localhost:8000
Streamlit UI → http://localhost:8501 

When using the API, please enter the below credentials for authentication. 

Username - "admin" 
Password - "password"

While using the streamlit app, Please enter the text of your choice in the displayed text box and then click on the "Predict Entities" button to call the API and retrieve the predicted entities from the input text.