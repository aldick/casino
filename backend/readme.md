# It is documentation for using OquEasy API

## Register

/api/account/register/

### JSON request

```json
{
"email": "",
"password": "",
"first_name": "",
"last_name": ""
}
```

### Possible responses:
- "email":
	- "This field may not be blank.",
	- "Enter a valid email address.",
	- "An user with this email already exists."
- "password":
	- "This field may not be blank.",
	- "Password must be at least 8 characters long with at least one capital letter and symbol.",
- "message": "User registered successfully!"


## Login

/api/account/login/

### JSON request

```json
{
"email": "",
"password": ""
}
```

### Possible responses:
- "access"
- "refresh"
- "message":
  - "Invalid email or password",
  - "User is inactive"
- "email":
	- "This field may not be blank.",
- "password":
	- "This field may not be blank.",


## Logout

/api/account/logout/

### JSON request
```json
Authorization: Bearer <access_token>

{
"refresh": ""
}
```

### Possible responses:
- "message":
  - "Successfully logged out"
- "detail":
  - 'Authentication credentials were not provided.'
- "error":
  - "Invalid token"

## Refresh

/api/account/refresh/

This url is needed to refresh token. Access token and refresh token have 5 minutes and 7 days lifetime respectively. If their lifetime expired, this error would be seen:

```json
{
"detail": "Given token not valid for any token type",
"code":"token_not_valid",
"messages": [{
	"token_class":"AccessToken",
	"token_type":"access",
	"message":"Token is expired"
	}]
}
```

### JSON request
```json
{
"refresh": ""
}
```

### Possible responses:
- "access"
- "refresh"

## Reset password request

/api/account/reset-password-request/

### JSON request

```json
{
"email": ""
}
```

### Possible responses

- "success": "We have sent you a link to reset your password"
- "error": "User with credentials not found"

## Reset password

/api/account/reset-password/.../

### JSON request

```json
{
    "new_password": "",
    "confirm_password": ""
}
```

### Possible responses
- "new_password": ["Password must be at least 8 characters long with at least one capital letter and symbol"]
- "success": "Password updated"
- "error": "Passwords do not match"
- "new_password": ["This field may not be blank."]
- "confirm_password": ["This field may not be blank."]
