## Authentication Setup
This project uses **Djoser** for user authentication and **Token Authentication** for securing API endpoints.

### Available endpoints:
- `/auth/users/` - Register a new user
- `/auth/token/login/` - Obtain authentication token
- `/auth/token/logout/` - Invalidate token
- `/auth/users/me/` - View/update authenticated user profile
- `/auth/users/deposit/` - Replenishment of the balance of uthenticated user profile

## Token Authentication
To access protected API endpoints, include the token in the request header:
```
Authorization: Token <your-token>
```

### Example request format for a protected endpoint:
```json
GET http://127.0.0.1:8000/api/your-endpoint/
Authorization: Token <your-token>
```

### Possible Responses:
- **Errors:**
  - `"detail"`: "Invalid token."

## Example: Register a User
```json
POST http://127.0.0.1:8000/auth/users
Content-Type: application/json
{
	"username": "",
	"email": "",
	"password": ""
}
```

### Possible Responses:
- **Errors:**
  - `"username"`:
    - "This field is required.".
    - "A user with that username already exists."
  - `"email"`:
    - "This field may not be blank."
    - "Enter a valid email address."
    - "An user with this email already exists."
  - `"password"`:
    - "This field may not be blank."
    - "Password must be at least 8 characters long with at least one capital letter and symbol."
- **Success:**
  - `"message"`: "User registered successfully!"

## Example: Login
```json
POST http://127.0.0.1:8000/auth/jwt/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "Testpassword123!"
}
```

### Possible Responses:
- **Errors:**
  - `"detail"`: "No active account found with the given credentials"
- **Success:**
  - `sets refresh token in cookies`
  - `"refresh"`: ```<token>```
  - `"access"`: ```<token>```

## Example: Refresh
```json
POST http://127.0.0.1:8000/auth/jwt/refresh/
Cookie: refresh=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MjMyNjg3MywiaWF0IjoxNzYyMjQwNDczLCJqdGkiOiI1ZjJiMzBiZTMwNTA0MjY0OTU4ODY5ZmY5ZjYwODg2OCIsInVzZXJfaWQiOjF9.i109kBPAqnzUkrV4UW29jv1Xkmpyr5RPkj2AfhnKKck
```

### Possible Responses:
- **Errors:**
  ```json
  {
  "detail": "Token is blacklisted",
  "code": "token_not_valid"
  }
  ```
  ```json
  {
  "detail": "Token is invalid",
  "code": "token_not_valid"
  }
  ``` 
- **Success:**
  - `sets refresh token in cookies`
  - `"refresh"`: ```<token>```
  - `"access"`: ```<token>```

## Example: Logout
```
POST http://127.0.0.1:8000/auth/logout/
```

## Example: User information
```json
GET http://localhost:8000/auth/users/me/
```

### Possible Responses:
```json
{
  "id": 1,
  "email": "admin@admin.com",
  "username": "admin",
  "profile": {
    "balance": "26500.00"
  }
}
```

## Example: Deposit
```json
GET http://localhost:8000/auth/user/deposit

or 

POST http://localhost:8000/auth/users/deposit/
Content-Type: application/json

{
	"deposit": "100"
}
```

### Possible responses
- GET method:
  ```json
  {
    "balance": // current balance
  }
  ```
- POST method:
  - Success:
    ```json
    {
      "balance": // current balance
      "deposit": // number 
    }
    ```
  - Errors:
    - `"deposit"`: "A deposit must be more than 0"


## Game Modes
It is a template for other games. Other games can include not only `"bet"` field and include  additional fields in the request.

## Example of the game
```json
POST http://localhost:8000/<game-name>/
Content-Type: application/json

{
	"bet": 2000.00,
    ...
}
```

### Possible responses

- **Errors**:
  - `"balance"`: "Current balance is not enough"
  - `"bet"`: "Bet cannot be negative"
- **Success**: 
  ```json
  {
    "bet": // number
    "is_win": // true or false
    "payout": // number
    "result": // result of the game
  }
  ```

## Game history
There is an endpoint in order to get history of the last 20 games of the user:
```json
GET http://localhost:8000/<game-name>/
```

### Possible responses

```json
{
  ...
  "game_id": {
    "bet": // number
    "is_win": // true or false
    "payout": // number
    "result": // result of the game
    "balance": // current balance of the user after the game
  },
  ...
}
```

## Example: Coin Flip
```json
POST http://localhost:8000/coin-flip/
Content-Type: application/json

{
  "bet": 2000,
  "choice": // "heads" or "tails"
}
```

### Possible Responses

- **Errors**:
  - `"choice":` " `smth` is not a valid choice."
- **Success**:
  ```json
  {
    "bet": 0.0,
    "is_win": // true or false,
    "payout": 0.0,
    "result": // "heads" or "tails"
    "balance": // current balance of the user after the game
    "choice": // "heads" or "tails"
  }
  ```

## Example: Crash
```json
POST http://localhost:8000/crash/
Content-Type: application/json

{
  "bet": 2000.00,
  "stop_value": 2.50 // a positive decimal number
}
```

### Possible Responses
- **Errors**:
  - `"stop_value"`: "stop_value cannot be negative or zero"
- **Success**:
  ```json
  {
    "bet": 2000.00,
    "is_win": // true or false
    "payout": // number
    "result": // number between 0.01 and 10,
    "balance": // current balance of the user after the game
    "stop_value": 2.50
  }
  ```

## Example: Roulette
```json
POST http://localhost:8000/roulette/
Content-Type: application/json

[
  {"bet": 100, "bet_type": "color", "bet_value": "red"},
  {"bet": 50, "bet_type": "even_odd", "bet_value": "odd"},
  {"bet": 25, "bet_type": "number", "bet_value": "17"},
  ...
]
```

### Possible Responses
- **Errors**:
  - `"bet_type"`: "`smth` is not a valid choice."
  - `"bet_value"`: "Number must be between 0 and 36" (for `bet_type: "number"`)
  - `"bet_value"`: "Number must be a valid integer" (for `bet_type: "number"`)
  - `"bet_value"`: "Color must be 'red' or 'black'" (for `bet_type: "color"`)
  - `"bet_value"`: "Must be 'even' or 'odd'" (for `bet_type: "even_odd"`)
- **Success**:
  ```json
  {
  "result": 23,
  "total_bet": 175.0,
  "total_payout": 300.0,
  "balance": 33360.0,
  "bets": [
    {
      "bet": "100.00",
      "bet_type": "color",
      "bet_value": "red",
      "payout": "200.00",
      "is_win": true
    },
    {
      "bet": "50.00",
      "bet_type": "even_odd",
      "bet_value": "odd",
      "payout": "100.00",
      "is_win": true
    },
    {
      "bet": "25.00",
      "bet_type": "number",
      "bet_value": "17",
      "payout": "0",
      "is_win": false
    },
    ...
  ]
  }
  ```


## Example: Plinko

### POST Request

```
POST http://localhost:8000/plinko/
Content-Type: application/json

{
  "bet": 2000.00,
  "lines": 10 // must be an integer between 8 and 16
}
```

### GET Request
This endpoint returns the multipliers for each bottom field 

```
GET http://localhost:8000/plinko/?lines=10
```

### Possible Responses (GET)

- **Errors**:
  - `"lines"`: "Lines must be between 8 and 16"
  - `"lines"`: "Lines must be a valid integer"
- **Success**:

  ```json
  {
  "bottom_fields": [8.9, 3.2, 1.4, 0.8, 0.6, 0.5, 0.6, 0.8, 1.4, 3.2, 8.9]
  }
  ```

### Possible Responses (POST)
This endpoint returns result as a list of turns of the ball for each line where -1 is a left and 1 is a right

- **Errors**:
  - `"lines"`: "Lines must be between 8 and 16"
  - `"lines"`: "Lines must be a valid integer"
- **Success**:

  ```json
  {
    "bet": 2000.00,
    "is_win": true, // true or false
    "payout": 2400.00,
    "result": [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1], // list of -1 (left) or 1 (right) for each line
    "balance": // current balance of the user after the game
    "lines": 10
  }
  ```
