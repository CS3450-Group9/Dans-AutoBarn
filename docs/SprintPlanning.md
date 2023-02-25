# Milestone Planning

## 02/14/2023
### Needs of app
* Apps
  * UserAuth
    * landing page
    * signup
    * password change
  * customer
    * search for reservation
    * create reservation
    * view registrations
      * cancel reservation
        * refund user
      * see past reservations
    * user profile page
      * add balance
        * add money to account
      * link to page with registrations
      * show name
      * password change
    * form for broken down car
  * Employee
    * log hours
    * view pay history
    * check in reservation
    * till worker
      * check out reservation
      * sell insurance
      * view current reservations
        * lowjack button
    * car retrieval specialist
      * access to lowjacked location from customer form
  * Manager
    * viewing cars in inventory
      * add cars to inventory
      * remove cars from inventory
    * view all customers and employees (able to filter)
      * promotes customers to employees or employees to manager
      * demotes in opposite direction of above
      * customers only
        * pays people/approves time card

* Models
  * User
    * methods
      * balance set/get
      * change auth level
  > The following models should be in the customer app
  * Car
  * Reservation
    * property
      * has_insurance
      * total_cost

* Unit Test Cases
* add these as we go

### Documentation
* sprint planning docs
  * screenshot of backlog view
* standup reports
* retrospective
  * same as before but with...
  * specific action items for improvement
  * measurement criteria for improvement
  * percentage of contribution of each team member
* updated build instructions and unit test instructions
* 75% of application completed
* revised documentation from milestone 1

### shoulds
* color scheme
  * demo page with color scheme
* cache request for reservation for unauthed user
  * hold reservation until authenticated

### Planning sprints
#### Sprint 3
Focus on front end, development of views
#### Sprint 4
Focus on DB, development of models
#### Sprint 5
Focus on integration and touch up, everything should look nice