# Beer Game
The beer game is based on supply chain and involves 4 players where each player represents one of the four stages in the chain i.e the retailer, the manufacturer, the wholesaler, the consumer. The goal of this game is to teach students who use this software about The Bullwhip Efect which is a supply chain phenomenon describing how small fluctuations in demand at the retail level can cause progressively larger fluctuations in demand at the wholesale, distributor, manufacturer and raw material supplier levels.

Task list for **Sprint4**:
- [X] Restructure code to be in proper folders with tests. Improve the documentation to use markdown. Clean the flask code to use proper schemas. Add proper migration scripts. Clean the frontend react. Make sure the fronend correctly integrates with the backend
- [X] Add endpoint for play game, add more details to the get game state endpoint
- [X] Add the game logic for play game
    - Handle edge cases like the Factory should be able to play in start
    - A player should only be able to play the game if the palyer in the previous role has played
    - No player should play twice in the same week
    - A new week is considered once all the players in the week have played
- [X] Add test cases for game logic for all the above edge cases
- [X] Add game logic to get game state, including
    + Fetch user role, customer, supplier
    + If the user can currently play (again use the same logic as above to check the status of the user)
- [X] Add test for the get gamme state
- [X] Add frontend
    - Create ui elements for different sections of the screen
    - Fetch game state from the backend, make sure the order button is disabled when the user is not allowed to play the game. 
    - Handle the case when new player has not yet joined the game
    - Handle the post rquest to submit order. 


Architecture Notes
------------------
* Backend is written in Python and uses Flask as a light weight server
* For Database the system uses Sqlite for local testing and mariadb for production
* The frontend is written in js + react and served using a node.js server.
* The frontend communicates with the backend using REST architecture.
* The Authentication is done use **SESSION_KEY** which should be set in the HTTP request header. **SESSION_KEY** can be obtained by calling `authenticate/` endpoint with appropriate `email` and `passwordHash`. The **SESSION_KEY** expires in 20 mins. 


REST API Documentation
----------------------
* a YAML-style documentation can be found in the docs/ directory, you can upload this file to swagger on your account to continue developing the API
* link: https://app.swaggerhub.com/apis-docs/api-test7/group-22-modified/1.0.0/

Steps to setup & start the backend server
---------------------------------------------
* Make sure you have python virtual env installed. Create a virtual env in the root directory of the backend: `virtualenv venv`
* Switch to the venv: `source venv/bin/activate`
* Install all the python requirements: `pip3 install -r requirements.txt`
* Copy .env.sample to .env `cp .env.sample .env` (For production you need to modify the env variables appropriately to point to correct mariadb instance)
* Run the inital db migration from the root backend directory `yoyo apply`
* From the root backend directory run `python3 main.py`

Steps to run the unittests
--------------------------
* From the backend root directory run 
    - `python3 connection_test.py` (testing db operation). 
    - `python3 game_test.py` (testing game logic). 

>Tests creates a fresh db automatically every time it is run and applies all the migrations. 

Steps to setup & start the frontend server
------------------------------------------
* Make sure the backend in running!
* Make sure you have `node.js` installed. Install all the required packages using `npm install`.
* Run `npm start` to run in the development mode. 

Notes for the contributors
--------------------------
* To add any new feature please fork the repo and create a Pull Request with master
* If you find any bug please create a issue in the Github repo. For other security issue you can contact at `s.agrawal@jacobs-university.de`

