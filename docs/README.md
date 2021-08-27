# Markdown file:

# Introduction

## General Idea

The beer game is based on supply chain and involves 4 players where each
player represents one of the four stages in the chain i.e the retailer, the man-
ufacturer, the wholesaler, the consumer.

Every week the retailer receives orders from the consumer without any time
delay. The retailer fulfills as many unit of beer order as it can and then cal-
culates the number of units that are required based on the total number of
stocks left in the inventory, the cost of each beer, and the backlog.
After some time delay, the retailer places an order to the wholesaler. The
wholesaler tries to fulfill the demand of the retailer and estimates how much
beer is needed. The wholesaler places an order to the distributor if he senses
he is in need of more stocks. This process is repeated with the manufacturer
as well.

Lastly, the manufacturer begins production according to the order demand.
When the production is over, the beer is send backwards to the distributor,
then from the distributor to the wholesaler, retailer, and finally to the con-
sumer. There are time delays in each step during the downstream process,
except between the retailer and consumer.

## Goals and Objectives

The objective of the game is to receive orders and deliver the items back
to the consumer, in a way the maximizes profits and minimizes the total
cumulative cost of all stages based the given information. Cost can be arisen
from numerous places. There is a cost for holding the inventory, a cost for
not satisfying demand so called a ”back order” which is basically a cost that
is incurred until the demand for the product is satisfied.

![FIG 1](/docs/imgs/Fig%201.png)

# Requirements

## User

The user can be logged in as a student or as an instructor. Each of these roles
have their own requirements.

### Instructor
1. The instructor acts as as an administrator of the game.
2. One should be able to modify the input parameter, record every players individual performance and see the summary of the game results.
3. The instructor must be able to set the initial values for the following parameters prior to the start of each game:
   - Number of rounds, weeks per game
   - Time delay for both upstream and downstream
   - Initial number of items in inventory of each stakeholder
   - The backlog and the cost of each item in stock
   - The amount of information available to each stakeholder can view in the game
4. The instructor must be able to supervise the current state of each game during a session.
5. The instructor must be able to change the type of demand for the players.
6. The instructor and user must be able to view a plot showing the bullwhip effect and player demand versus demand generated.

### Player
Once the lobby and game setting are initialised by the instructor players can
join the lobby.

1. A player should be able to decide on his/her role be able to choose a role of Retailer, Wholesaler, Distributor, or Factory.
2. A player shall be able to place orders to the upstream supply chain.
3. The players are not allowed to discuss or talk about their own strategies with each other. Players can only view the following:
   - The backlog of orders that couldn’t be fulfilled.
   - Incoming orders from the upstream
   - Number of stocks in the inventory
   - Updated information after the orders have been placed.

There are 24 rounds of the game and in each round the player performs the
following 4 steps.
1. Check Deliveries Check the quantity of beer units that are delivered to the downstream supplier in the supply chain within some time delay.
2. Check Incoming Orders Check the quantity of beer units that the downstream supplier has ordered within some time delay.
3. Deliver Beer To satisfy the consumer demand, deliver as many units as possible.
4. Place Out going Order This is the decision-making process where the number of units of beer needed are decided to keep the inventory going and ensure that he has sufficient units to meet future demands. The decision is based on 3 factors namely backlog, consumer needs, and current stock.
   
## System

Following are the system requirements that must be kept it when creating the
game. Please note that there maybe other requirements as well however these
are the major ones that need be talked upon and the foundation through which
the game should be created.

1. When first opening app user (who could either be a player or an instructor) should be presented with the options to login or to register.
2. A player should only be able to play a game which is has been created
by some instructor.
3. There can only be one instructor for one session or game that is happening after which he will receive a unique code only for that session.
4. User can only join the game by typing the unique code after which he
should automatically be assigned the role of a player.
5. A player should only be active in one session.
6. All players and instructor should have their own unique id to identify
them.
7. When the game reaches the maximum number of weeks, it should terminate and present players with a final interface which displays the saved
game statistics.
8. Players should be able to choose a valid role (Factory, Distributor, Whole-
saler and Retailer) that they must stick to and cannot be changed.
9. After each round the system should be able to show the player the demand from the successor, the incoming beers from the predecessor, the
number of beers in warehouse, the back log and input field to place the
order.
10. Certain settings such as holding costs or beer costs cannot be changed
by the instructor once the game has started but certain settings such as
number of rounds should be able to change once the game has instructed.
The system should be able to handle such functionalities.
11. The instructor should be able to inspect each game in the session while
it is ongoing and after the game has ended the instructor should be able
to see weekly analysis after each round.
12. When the game reaches the maximum number of weeks, it should terminate and present players with a final interface which displays the saved
game statistics.

# Design

## Use Case

![FIG 2](/docs/imgs/Fig%202.png)

The above use-case diagram provides a comprehensive overview of what
an instructor can do using the web application, from logging in the the game
to changing the properties of all the games that instructor is managing. The
diagram also captures the requirement of the software to edit the various game
parameters of a particular game that s/he is managing.

![FIG 3](/docs/imgs/Fig%203.png)

The above use-case diagram gives an overview of the functionalities that the
web service offers to the players of the beer game. It includes every action that
the user can take while playing the game, like ordering the beers and making
plots of the back order, demand or/and total cost. It also encompasses use
cases that are not necessarily involved with playing the game, like creating
one’s own game.

## Class

![FIG 4](/docs/imgs/Fig%204.png)

## Activity

![FIG 5](/docs/imgs/Fig%205.png)

## Sequence

![FIG 6](/docs/imgs/Fig%206.png)

The Stakeholder tries to login to the game with the relevant credentials-
name and password, and allowed to interact with the game only if he/she is
registered for the game.

![FIG 7](/docs/imgs/Fig%207.png)

The following sequence diagram explains how an instructor can update a
game that has been created. The instructor can change the relevant settings
of the game, for example increasing or decreasing the backlog cost.

![FIG 8](/docs/imgs/Fig%208.png)

This sequence diagram explains how the instructor is able to view the data
of a particular game.

![FIG 9](/docs/imgs/Fig%209.png)

The following sequence diagram explains how a player can join a game.
The player requires a game number that is registered, password, and the role
in which the player tends to join. The server then checks for the validity on
the basis of given information and responds whether or not the player has been
able to join the game.

![FIG 10](/docs/imgs/Fig%2010.png)

The following sequence diagram explains how the instructor can create a
game.The instructor has to configure the settings of the game that would
be displayed. Then, by providing a valid number(which also is a configuration
step), the instructor will be able to create a new game.

# Conclusion

The goal of this game is to teach students who use this software about The
Bullwhip Effect which is a supply chain phenomenon describing how small
fluctuations in demand at the retail level can cause progressively larger fluctuations in demand at the wholesale, distributor, manufacturer and raw material
supplier levels. The e↵ect is named after the physics involved in cracking a
whip. When the person holding the whip snaps their wrist, the relatively small
movement causes the whip’s wave patterns to increasingly amplify in a chain
reaction.
The purpose of this document is for developers to have a guideline to follow and know procedures about how to do your coding instead of just starting
form scratch. The ideas presented above teach you with general conceptual
modeling of the structure of the application, and for detailed modeling translating the models into programming code.

# References

1. (https://www.transentis.com/understanding-the-beer-game/en/)
2. (http://scgames.bauer.uh.edu)
3. (https://www.draw.io/)
4. (https://en.wikipedia.org/wiki/Beer_distribution_game)
5. (https://www.supplychain-academy.net/beer-game/)
6. (http://www.peter-baumann.org)
