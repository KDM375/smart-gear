### API Documentation

## Table of Contents
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
#Product:
-name: Char
-description: Text
-price: Decimal
-stock: PositiveInteger
-created_at: DateTime
-image: Image
#Cart:
-owner: FK to User
-items: Text
-total_price: Decimal
-created_at: DateTime
#Transaction:
-transaction_id: PK
-owner: FK to User
-amount: Decimal
-transaction_type: Char
-status: Char
-created_at: DateTime

## Endpoints

| Method | Endpoint                  | Description           |
|--------|---------------------------|-----------------------|
| GET    | `/api/products/`          | List all products     | 
| POST   | `/api/products/`          | Create a new product  | 
| GET    | `/api/products/<id>/`     | Get product details   | 
| PUT    | `/api/products/<id>/`     | Update a product      | 
| DELETE | `/api/products/<id>/`     | Delete a product      | 

## Authentication

## WebHooks