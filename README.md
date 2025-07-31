# API Documentation

## Table of Contents
- [API Documentation](#api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [BaseURL](#baseurl)
  - [Models Overview](#models-overview)
  - [Endpoints](#endpoints)
  - [Authentication](#authentication)
  - [WebHooks](#webhooks)

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
| POST   | `/account/register/`      | Register a new user              | 
| POST   | `/account/token/`         | Obtaining the auth tokens        | 
| GET    | `/account/token_refresh/` | Refreshing access tokens         | 
| GET    | `/products/all_products/`  | Obtaining all product details    | 
| POST   | `/payment/initiate/`      | Initiating checkout in Paystack  | 
| GET    | `/payment/webhooks/`      | Handling Paystack webhooks       | 

## Authentication

## WebHooks