# Customer System Documentation

## 1. Introduction

The Customer System manages all user accounts in the GlobalMart e-commerce platform.
It stores customer information, assigns loyalty tiers, and connects customers to their orders.

This subsystem ensures that each customer can register, place orders, and benefit from loyalty programs.

---

## 2. Entities

### Customers

The Customers entity stores information about users who register on the platform.

Attributes:

* customer_id (Primary Key)
* first_name
* last_name
* email
* phone
* password_hash
* tier_id (Foreign Key)
* created_at
* status

Each customer is assigned a loyalty tier and can place multiple orders.

---

### Customer_Tiers

The Customer_Tiers entity defines the loyalty levels available to customers.

Attributes:

* tier_id (Primary Key)
* tier_name
* discount_rate
* benefits

Examples of tiers include Bronze, Silver, and Gold.

These tiers allow the system to provide different benefits or discounts to customers.

---

## 3. Relationships

Customer_Tiers → Customers

One tier can be assigned to many customers.

Customers → Orders

One customer can place multiple orders in the system.

---

## 4. System Explanation

When a user registers on the platform, a record is created in the Customers table.
Each customer is assigned a tier that determines their benefits or discounts.

When the customer purchases products, orders are recorded in the Orders table and linked to the customer through the customer_id.

This structure ensures proper management of customer accounts and purchase history.
