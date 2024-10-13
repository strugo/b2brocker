Project Setup Guide
===

Running the Project
---

1. Build the containers: 
``` docker compose build ```

2. Start the project with default settings: 
``` docker compose up ```

3. Run tests and see the coverage report:
``` docker compose run test ```

4. Stop the project: 
``` docker compose down ```

5. Remove the volume with the database:
``` docker volume rm b2brocker_mysql_data ```

Environment Variables
---
The env.example file contains a list of environment variables that can be configured.

Database Configuration
---
By default, Django connects to the database with the root user, which is convenient for development. However, it is recommended to use a user with limited privileges in a production environment.

Wallet Balance Restrictions
---
The wallet balance is calculated based on transactions and cannot be less than zero. Due to this restriction, deleting and editing transactions is disabled.

Changing Wallet Label
---
You can change the wallet label, but changing the balance directly is not allowed.

---

Task
===

Develop a REST API server using Django REST Framework with pagination, sorting, and filtering for two models:

Transaction (id, wallet_id (foreign key), txid, amount);
Wallet (id, label, balance);

Where txid is a required unique string field, amount is a number with 18-digit precision, label is a string field, balance is a summary of all transactions’ amounts. Transaction amount may be negative. Wallet balance should NEVER be negative

Tech Stack:

Python - 3.11+
Database - MySQL
API specification - JSON:API — A specification for building APIs in JSON (you are free to use the plugin https://django-rest-framework-json-api.readthedocs.io/en/stable/)

Advantages:

Test coverage
SQLAlchemy migrations is an option
Any linter usage
Quick start app guide if you create your own docker-compose or Dockerfiles
Comments in non-standard places in code
Use database indexes if you think it’s advisable
Leave a GitHub link to the repo. Please delete the repo after HR feedback

[execution time limit] 4 seconds (sh)

[memory limit] 1 GB
