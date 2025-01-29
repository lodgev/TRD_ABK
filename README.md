
# Sport Betting Microservices Application
### Authors : 
Oleksandra KUKSA
Olha ALIEINIK
Doriane BEDIER

## Project Overview

This is a **sport betting application** built using a **microservices architecture**. The platform allows users to:

-   **Manage their profile** 
-   **View matches and odds**
-   **Place single and combined bets**
-   **Manage transactions and wallets**
-   **Read sports news**

##  Setup & Installation

### How to execute the python notebooks

#### Prerequisites:
-  Python 3 or more
#### Libraries:
- pandas
- numpy
- scikit-learn
- torch 

You can execute this command to install them :

```pip install pandas numpy scikit-learn torch torchvision torchaudio```

Then you can execute each cell one by one

### How to Access the Site

#### Prerequisites:

-   Docker Desktop
-   Ubuntu Terminal

#### 1 - Clone the repository

```bash
git clone https://github.com/lodgev/TRD_ABK.git

```

#### 2 - Start the Services

Use **Docker Compose** to run all microservices together: Navigate to the project folder and execute the following commands:

```bash
cd backEnd/services
docker-compose up --build

```

On a browser, go to the address: `http://localhost:8501`

You are now on the homepage.

## Using the Application

Once everything is running, navigate to `http://localhost:8501` to access the Streamlit frontend.

## Some Details

### Authentication

-   You can create an account. You will have to verify your email via a mail sent to your inbox, so enter a valid address.
-   Or you can use a test account: **Login**: [john@doe.com](mailto:john@doe.com) **Password**: password123

### Recommendation

-   You have to place a bet first before getting news recommendations.
-   After placing your first bet, you can browse the articles on the News page.
-   You can mark articles as "not interested" or rate them.
-   Clicking on "Read the article" will take you to an external website that published the article.

## Architecture

The system is composed of several microservices. All endpoints are testable using an API client. We recommend using **Bruno** as it is what we used. In almost every service, there is a folder containing Bruno files.

 You can open them as a collection in Bruno, and you will have all the requests available directly. If you don't have Bruno, we describe the different endpoints below, and you can find test request bodies in the previously mentioned folders.

### **Gateway & Frontend** (`streamlit-app`)

Acts as the frontend and gateway for all services, providing the user interface via **Streamlit**.

-   **Features:**
    -   User authentication and profile management
    -   Match listing with real-time odds
    -   Single and combined bet creation
    -   Wallet and transaction management

### **Recommendation Service** (`recommender-service`)

Manages recommendations for users.

-   **Endpoints:**
    -   `GET /feedback/{user_id}` → Get feedback by user
    -   `GET /feedback` → Get all feedback
    -   `GET /recommendations/{user_id}` → Get recommendations for a user
    -   `POST /feedback` → Post feedback for an article

### **Authentication Service** (`auth-service`)

Manages user authentication.

-   **Endpoints:**
    -   `GET /auth/forgot-password` → Forgot password request
    -   `GET /auth/login` → Login request
    -   `POST /auth/logout` → Logout request
    -   `PUT /auth/register` → Register request
    -   `DELETE /auth/reset-password/` → Reset password request
    -   `GET /auth/verify/{user_id}` → Email verification request

### **User Management Service** (`usermanagement-service`)

Manages user authentication, profile updates, and account deletion.

-   **Endpoints:**
    -   `GET /UserManagementService/users` → Get all users
    -   `GET /UserManagementService/users/{user_id}` → Get user by ID
    -   `POST /UserManagementService/users` → Create a new user
    -   `PUT /UserManagementService/users/{user_id}` → Update user profile
    -   `DELETE /UserManagementService/users/{user_id}` → Delete user

### **Match Management Service** (`match-service`)

Handles match listings, club information, and odds calculation.

#### Matches :

-   **Endpoints:**
    -   `GET /matches` → Fetch all matches
    -   `GET /matches/{match_id}` → Get match details by ID
    -   `POST /matches` → Add a new match
    -   `PUT /matches/{match_id}` → Update match details
    -   `DELETE /matches/{match_id}` → Cancel a match
    -   `GET /matches/{date}` → Show matches by date

#### Clubs :

-   **Endpoints:**
    -   `GET /clubs` → Get all clubs
    -   `GET /clubs/{club_id}` → Get a club by its ID

#### Odds :

-   **Endpoints:**
    -   `GET /odds/{match_id}` → Get odds for a match
    -   `GET /odds` → Get odds for all matches
    -   `PUT /odds/{match_id}` → Update odds for a match
    -   `PUT /odds` → Update odds for all matches
    -   `DELETE /odds/{match_id}` → Delete odds for a match

### **Betting Service** (`betting-service`)

Handles user bets, both **single and combined bets**.

-   **Endpoints:**
    -   `POST /betts/create-bet` → Place a single bet
    -   `POST /combined-betts/create-combined-bet` → Place a combined bet
    -   `GET /betts/get-all-bets` → Get all user bets
    -   `PUT /betts/update-bet/{bet_id}` → Update a bet
    -   `GET /betts/get-bet/{bet_id}` → Get a bet by ID
    -   `DELETE /betts/cancel-bet/{bet_id}` → Cancel a bet

### **Deposit Service** (`deposit-service`)

Handles **deposits** into users' wallets.

-   **Endpoints:**
    -   `POST /create-deposit` → Deposit a certain amount into the user's wallet

### **Withdrawal Service** (`withdrawal-service`)

Handles **withdrawals** from users' wallets.

-   **Endpoints:**
    -   `POST /withdrawal` → Withdraw a certain amount from the user's wallet
    -   `GET /withdrawal/{wallet_id}` → Withdraw from a wallet with a specific ID

### **Usage Service** (`usage-service`)

Handles the usage of wallet funds for betting.

-   **Endpoints:**
    -   `GET /wallet/{wallet_id}/balance` → Get the balance of a user's wallet

### **Notification Service** (`notification-service`)

Handles email notifications.

-   **Endpoints:**
    -   `POST /change-password` → Change password notification
    -   `POST /change-password-success` → Change password success notification
    -   `POST /verify-email` → Verify email notification



