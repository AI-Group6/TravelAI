# TravelAI
This is an AI assistant to use in travel planning. It can:
- Plan itineraries
- Compare flights
- List hotels
- Answer general travel questions

## Running the Application
1. To run the code from the command line run MainAPP.py and select option 1
   1. From command line you can currently use the database feature if you set up a postgres database
      - If you don't want to do that select option 3 to no log in
   2. Choose any of the 4 query types and ask your questions
2. To run the code from the UI run MainAPP.py and selection option 1
   1. After the flask server is running in another terminal cd into Frontend/frontend and run npm start
   2. React app should open on your device and you should be able to interact with it
      1. Note. currently you cannot log in with the UI

## Getting the Local Model Running
1. If you don't want to just be forced to use the application with the internet you can use a local model
2. 1st pip install llama-cpp-python
3. 2nd download **Phi-3-mini-4k-instruct-q4.gguf** from https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf.
4. Place that file in the root directory of the project folder

Note. If you don't want to use the local model comment out **from llama_cpp import Llama** in PhiLocalAI.py

## Getting API Keys
1. To use the LLaMa model with hugging face you need the API keys or the Aamadeus API
2. Create and .env file at the root of the project
   1. Create API keys for hugging face and Aamadeous, you can use the free tiers
   2. In that .env file place the keys in like this 
      - API_KEY="your key"
      - FLIGHT_KEY="your key"
      - FLIGHT_SECRET="your secret"
     
## Creating the Database (for command-line use)
1. Install PostgreSQL
2. Create a new server
3. Name: local
4. Hostname: localhost
5. Port: 5432
6. Username: postgres


## Necessary Imports
You may have to install some python libraries for this code to work: those could include
1. pip install llama-cpp-python
2. pip install huggingface_hub
3. pip install react
4. pip install react-cors
5. pip install pandas
6. pip install flask
7. pip install geopy
