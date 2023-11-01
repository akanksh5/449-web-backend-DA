# 449-web-backend-DA
## Movie Ratings System
- A simple movie ratings system that supports creation, updation and deletion of movie rating entries.
- Has support for JWT Authentication with /register and /login endpoints.
- Application developed using Flask as the backend framework and MySQL for the relational database.
### Installation
- Install and source the virtual env => https://docs.python.org/3/library/venv.html
- Install all the python3 libraries required for this application using the following command
 => pip3 install -r requirements.txt
-  Install MySQL => https://dev.mysql.com/downloads/installer/
- Create a .env file and source the following environment Variables<br>
  **SQLALCHEMY_DATABASE_URI<br>   SQLALCHEMY_TRACK_MODIFICATIONS<br>
  UPLOAD_FOLDER<br>
  JWT_SECRET_KEY**
- Connect to the database and create a database based on the configuration value.
- Run the following command - ```flask --app movieratings run ```
- Using Postman, hit the respective endpoints
- Project Contributors - **Dhanush KJ & Akanksh Jagadish**