# Program Requirements
Requirements are scored by their priority with a letter symbol in four categories:
- A) Must include
- B) Should include
- C) Could include
- D) Won't include
## Functional Requirements 
All Functional Requirements fall under the A) Must include category unless otherwise specified  
### 1 - User Account Creation
    1.1 - User will be prompted to create their own login credentials for account authorization
    1.2 - Upon creation, user is a "customer" by default
    1.3 - Upon creation, user has a starting account balance
### 2 - Car Rentals
    2.1 - 3 categories for vehicle type:
       1. $10 a day for a basic rental
       2. $50 a day for an upgraded rental
       3. $100 a day for a luxury rental
    2.2 - Insurance
       2.2.1 - Provided for a $50 dollar fee
       2.2.2 - If insurance isn't bought by the customer and the rental breaks down, a $300 fee will be deduced from the customer
       2.2.3 - The cheaper vehicle type categories are more likely to break down
       2.2.4 - There may be other terms that cost other amounts
    2.3 - Availabilty Constraint
    2.4 - Limited Inventory of Rentals
       2.4.1 - Have a library of photos so that each rental has a corresponding photo
    2.5 - If a customer has insufficient funds to make a reservation, they are notified and asked if they would like to deposit more funds
       2.5.1 - If so, they will be prompted to enter an amount to deposit in their account
    2.6 - An account is required in order to make a reservation
### 3 - User Types
    3.1 - Customer
       3.1.1 - Default account type
       3.1.2 - Can only reserve a rental
       3.1.3 - Funds are deducted from their account balance when a reservation is made
    3.2 - Till Worker
       3.2.1 - Verifies customer has the correct reservation at time of pick-up
       3.2.2 - Sells insurance to the customer at time of pick-up
       3.2.3 - Has option to "low-jack" the rental to make a break-down more likely
       3.2.4 - Is paid a wage of $15/hour from the manager
    3.3 - Car Retrieval Specialist (Could be blended with the Till Worker role) -> Prioritized in category C
       3.3.1 - Retrieves a broken-down rental
       3.3.2 - Is paid a wage of $15/hour from the manager
    3.4 - Manager
       3.4.1 - Customer payments are allotted into manager's account
       3.4.2 - Has ability to promote a customer to the role of Till Worker/Car Retrieval Specialist
       3.4.3 - Has ability to purchase a new vehicle to add to the inventory
## Non-Functional Requirements
### 1 - User Account Creation
    1.1 - A) Login credentials will be cached and stored in a database
    1.2 - A) Account balance for the user will be stored in their database model as well
    1.3 - B) Views for a customer and a user who is not logged in should be differentiated
    1.4 - B) Other than the manager, newly-created accounts will be assigned as customers with the appropriate corresponding view. Therefore, the manager and their view should be created as a special case
### 2 - Car Rentals
    2.1 - A) Each car rental must have an ID associated with it so that reservations don't overlap
    2.2 - A) An Availabilty Constraint must be applied so that two customers don't reserve the same rental. This may be done with the use of a database or some form of data structure
    2.3 - A) There is a limited inventory of rentals, but more can be added to the rental model by the manager
    2.4 - A) Have a library of photos so that each rental in the inventory has a corresponding photo
    2.5 - A) A rental can only be reserved by a registered user who is signed in
    2.5 - B) If a user doesn't have enough funds to make a reservation, re-direct the user to a separate view in order to deposit funds and then return them to the original reservation page
    2.6 - B) If a reservation is made, a code should be generated for the user to provide to the Till worker at time of pick-up. This may be done with a function that randomly generates a string of characters.
    2.7 - B) If a customer does not purchase insurance and the car is "low-jacked", a field for the in-use rental should indicate if it has broken down.
    2.8 - C) A rental could have its own model in the database that contains its id, photo, availabilty, cost, amount of gas in its tank, etc.
### 3 - User Types
    3.1 - A) Each user type will have separate views. A Django views file will be used to determine which view the user should see based on their user-type.
    3.2 - A) The manager is the only one who has the option to update a user's position to that of a till worker or car retrieval specialist
    3.3 - B) The manager adds funds into their employees' account balances to pay them. Therefore, there should be a function to deduct an amount from the manager's account and deposit it into the employee's account.
    3.4 - B) The manager should have some way to add a new rental to the inventory. In their view they may be able to view a catalog of cars to add to the rental database.
    3.5 - B) Till Workers should be able to see the same code that the customer acquired upon making a successful reservation
    3.6 - B) The Till worker's view should include a checklist of items for the insurance that they can sell to the customer. The amount thechecklisted items sum to should be deducted from the customer's account when it is submitted/beginning of the reservation.
    3.7 - C) The till worker and car retrieval specialist could be merged into one position unless more duties can be thought of for the retrieval specialist
    