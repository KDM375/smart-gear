# API Documentation

## Table of Contents
- [API Documentation](#api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [BaseURL](#baseurl)
  - [Models Overview](#models-overview)
  - [Endpoints](#endpoints)
  - [Authentication](#authentication)

## Overview
Smart Gear is an online e commerce website that specializes in selling electronic gadgets with the convenience of the products arriving right at your doorsteps. Smart Gear's backend technology focuses on providing a safe and convenient experience when making purchases online.

## BaseURL
This link serves as the base url for using the api. It has been hosted using render.com
    https://smart-gear-1.onrender.com/


## Models Overview
**Product**:
- Name: *char*
- Description: *text*
- Price: *decimal*
- Stock: *positiveinteger*
- Created_at: *datetime*
- Image: *image*

**Cart**:
- Owner: *FK to user*
- Items: *text*
- Total_price: *decimal*
- Created_at: *datetime*

**Transaction**:
- Transaction_id: *PK*
- Owner: *FK to user*
- Amount: *decimal*
- Transaction_type: *char*
- Status: *char*
- Created_at: *datetime*

## Endpoints

| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| POST   | `/account/register/`      | Register a new user (It takes in the new user's details as an input body)              | 
| POST   | `/account/token/`         | Obtaining the auth tokens to log in a user (It takes the user's email and password as an input body)      | 
| POST    | `/account/token_refresh/` | Refreshing access tokens (It takes the refresh tokens as an input body)        | 
| GET    | `/products/all_products/`  | Obtaining all product details    | 
| POST   | `/payment/initiate/`      | Initiating checkout in Paystack  | 
| GET    | `/payment/webhooks/`      | Handling Paystack webhooks       | 

## Authentication
User authentication uses JSON Web Token (JWT) to validate the user's credentials during login. If it is successful it gives two unique tokens, the **access** token and the **refresh** and logs in the user. The access token is passed with every request the user makes. The refresh token refreshes the access token every time it expires after every 30 mins. The user logs out only when the refresh token expires.
