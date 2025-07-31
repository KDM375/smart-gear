## API Documentation

## Table of Contents
1. [Overview](#overview)
2. [BaseURL](#base_url)
3. [Models Overview](#models-overview)
4. [Endpoints](#endpoints)
5. [Authentication](#authentiation)

## Overview
Smart Gear is an online e commerce website that specializes in selling electronic gadgets with the convenience of the products arriving right at your doorsteps. Smart Gear's backend technology focuses on providing a safe and convenient experience when making purchases online.

## BaseURL


## Models Overview
# Product:
    name: Char
    description: Text
    price: Decimal
    stock: PositiveInteger
    created_at: DateTime
    image: Image
# Cart:
    owner: FK to User
    items: Text
    total_price: Decimal
    created_at: DateTime
# Transaction:
    transaction_id: PK
    owner: FK to User
    amount: Decimal
    transaction_type: Char
    status: Char
    created_at: DateTime

## Endpoints
# Users
# Products
# Payment
