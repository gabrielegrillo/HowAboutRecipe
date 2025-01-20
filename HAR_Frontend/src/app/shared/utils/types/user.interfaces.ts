
// Interfaces for Users & Correlated Objects

// User
export interface UserInterface {
    "id": string,
    "firstName": string,
    "lastName": string,
    "emailAddress": string,
    "password": string
}

export interface Author {
    "id": string,
    "username": string
}

export interface UserLoginAuthInterface {
    "username": string,
    "password": string
}
export interface UserRegisAuthInterface {
    "first_name": string,
    "last_name": string,
    "username": string,
    "email": string,
    "password": string
}

export interface UserAuth {
    "username": string,
    "password": string
}

export interface UserToken extends UserLoggedInfo {
    "refresh": string,
    "access": string
}

export interface UserLoggedInfo {
    "first_name": string,
    "last_name": string,
    "username": string,
    "email": string
}