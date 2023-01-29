# CS3450-Group9
## Organization & Name Scheme
### File Structure
All documentation will be located in the /docs/ folder   
Files will be UpperCamelCase  
Directorys will be lowerCamelCase
Other structure determined as needed
### Team Organization
One member will be selected as the scrum master  
Discorse will be through Discord  
Standup meetings will be held on Discord  
All issues will be tracked on Jira
## Version-Control procedures
### Git Branches
**main**  
Main is for "version releases"/completed Project Milestones  
Main will need four approvals for the pull request to be merged  
**dev**  
Dev will be merged to main for upon completion of a Project Milestone/Sprint.  
Merges to dev will need at least one approval  
Pull requests should be made when program is functional  
**other development branches**  
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
4. Modify necessary parts of django to have app be recognized throughout project.  
#### Install/Configuration for Vue.js
1. Install Vue
2. Create Vue project using  ```$ vue create <<app_name>>```
3. Configure vue.config.js inside of the vue project
#### Link Django and Vue.js 
1. Install axios to handle communication  
   Use the command ```$ npm install --save axios vue-axios```
#### Resources
[Offical Django Install Guide](https://vuejs.org/guide/quick-start.html#creating-a-vue-application)  
[Linking Django and Vue.js](https://www.webucator.com/article/connecting-django-and-vue/)  
[Vue Cli Official Site](https://cli.vuejs.org/)  
## Build instructions
1. Have python installed
2. In a command line navigate to ```/web```  
3. Run the command ```$ python manage.py runserver```  
## Unit testing instructions
All developers involved in a PR will test functionality of systems implemented  
## System testing instructions
When setup, Jenkins will do all system/integration testing  
Until that point, the all developers involved in the PR should verify changes don't affect unwanted systems  
## Other development notes, as needed
There may be some issues with the current integration of the tech stack, these will be worked out as we go along.  
