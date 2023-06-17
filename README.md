# CS3450-Group9
## Usage information
> IMPORTANT:  
> Site should only be viewed from a desktop environment  
> Site is not available over HTTPS due to django errors  
> Due to the nature of the site, a user with malintent can delete the manager account and lock out functionality, this will be prevented by perdiodically wiping the database and recreating users  
> If you are unable to log in with an account higher than customer (you can create a customer account by going to dansautobarn.com/signup) wait approx 24hrs for the above to happen  

Live site available [here](http://dansautobarn.com)  
Login information is as follows  
| Username   | Password | Auth Level   |
|------------|----------|--------------|
| admin      | password | Manager      |
| carperson  | password | Employee     |
| Tillperson | password | Employee     |
| customer   | hello    | Customer     |

## Use Case Videos
To view the functionality without using the site yourself you can watch use case videos [here](https://www.youtube.com/playlist?list=PLY7a540W2V3Uface3frI61mU53oRxRQO-)

## Organization & Name Scheme
### File Structure
All documentation will be located in the /docs/ folder   
Files will be UpperCamelCase  
Directories will be lowerCamelCase  
Other structure determined as needed
### Team Organization
One member will be selected as the scrum master  
Discorse will be through Discord  
Standup meetings will be held on Discord Voice Chat   
All issues will be tracked on Jira  
## Version-Control procedures
### Git Branches
#### main
Main is for "version releases"/completed Project Milestones  
Main will need four approvals for the pull request to be merged  
#### dev
Dev will be merged to main for upon completion of a Project Milestone/Sprint.  
Merges to dev will need at least one approval  
Pull requests should only be made when program is functional  
#### documentation
The documentation branch is used to update sprint retrospectives and standup meeting documentation  
#### other development branches
All other branches should have dev as the source and will require a pull request to merge to dev.  
All branches will be made through Jira and associated with a ticket, format should be as follows "G9-'ticket number'-'ticket title'".  
When setup, a pull request will need a functioning build from Jenkins to merge. 
## Tool Stack
The tool stack will use Django for the backend  
The Database will be the default Django SQLite Database  
The front end will use Vue.js  
### Setup Procedure
#### Install/Configuration for Django
1. Install Django  
2. Create Django project using ```$ django-admin startproject DansAutoBarn ```
3. Create Django app using ```$ python manage.py startapp <<app_name>> ```  
4. Modify necessary parts of the project to have app be recognized throughout    
   1. Add app to installed apps in ```<<project>>/settings.py```  
5. Install [python-decouple](https://pypi.org/project/python-decouple/)
#### Configuration for Vue.js
1. Create a regular js file for the app you'd like to use vue with  
2. File should be created in ```<<app_name>>/static/<<app_name>>/<<view>>.js```
#### Resources
[Offical Django Install Guide](https://vuejs.org/guide/quick-start.html#creating-a-vue-application)  
## Build instructions
1. Have python installed
2. In a command line navigate to ```/web```  
3. Run the command ```$ python manage.py runserver```  
## Unit testing instructions
All developers involved in a PR will test functionality of systems implemented  
[Unit Testing Documentation](https://github.com/CS3450-Group9/CS3450-Group9/tree/documentation/docs/unitTests)
## System testing instructions
When setup, Jenkins will do all system/integration testing  
Until that point, the all developers involved in the PR should verify changes don't affect unwanted systems  
## Other development notes, as needed
