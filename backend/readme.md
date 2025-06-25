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
POST http://127.0.0.1:8000/auth/token/login/
Content-Type: application/json
{
  "username": "testuser",
  "password": "Testpassword123!"
}
```

### Possible Responses:
- **Errors:**
  - `"non_field_errors"`: "Unable to log in with provided credentials."
- **Success:**
  - `"auth_token"`: ```<token>```

## Example: Logout
```
POST http://127.0.0.1:8000/auth/token/logout/
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
    "stop_value": 2.50
  }
  ```

## Example: Roulette
```json
POST http://localhost:8000/roulette/
Content-Type: application/json

{
  "bet": 2000.00,
  "bet_type": // "color", "even_odd", or "number"
  "bet_value": // "red" or "black" for color;
               // "even" or "odd" for even_odd; 
               // 0-36 for number
}
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
    "bet": 2000.00,
    "is_win": // true or false
    "payout": // number
    "result": // random integer between 0 and 36
    "bet_type": "color",
    "bet_value": "red"
  }
  ```
