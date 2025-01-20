
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
    "firstName": string,
    "lastName": string,
    "username": string,
    "email": string,
    "password": string
}

export interface UserAuth {
    "username": string,
    "password": string
}

export interface UserToken {
    "refresh": string,
    "access": string
}