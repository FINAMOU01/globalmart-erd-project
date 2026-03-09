GlobalMart E-Commerce System Documentation
1. Introduction

GlobalMart est une plateforme e-commerce internationale qui permet aux clients d’acheter des produits provenant de différents vendeurs et entrepôts à travers le monde.

Le système est composé de plusieurs sous-systèmes principaux :

Customer System

Order System

Product and Inventory System

Currency System

Ces sous-systèmes travaillent ensemble pour gérer :

les comptes clients

les commandes

le catalogue de produits

la gestion du stock

les devises internationales

2. Customer System
Overview

Le Customer System gère tous les comptes utilisateurs de la plateforme GlobalMart.

Il stocke les informations des clients, leur niveau de fidélité et leur historique de commandes.

Entities
Customers

La table Customers contient les informations des utilisateurs enregistrés.

Attributes:

customer_id (Primary Key)

first_name

last_name

email

phone

password_hash

tier_id (Foreign Key)

created_at

status

Chaque client peut passer plusieurs commandes.

Customer_Tiers

La table Customer_Tiers définit les différents niveaux de fidélité.

Attributes:

tier_id (Primary Key)

tier_name

discount_rate

benefits

Exemples de niveaux :

Bronze

Silver

Gold

Ces niveaux permettent d’offrir des réductions et avantages différents aux clients.

Relationships

Customer_Tiers → Customers
One-to-Many

Un niveau peut être attribué à plusieurs clients.

Customers → Orders
One-to-Many

Un client peut passer plusieurs commandes.

System Explanation

Lorsqu’un utilisateur s’inscrit sur la plateforme :

Un enregistrement est créé dans la table Customers.

Un niveau de fidélité lui est attribué.

Lorsqu’il effectue un achat, une commande est créée dans la table Orders.

3. Order System
Overview

Le Order System gère les achats effectués par les clients sur GlobalMart.

Il enregistre :

qui a passé la commande

quels produits ont été achetés

la quantité de chaque produit

Tables
Customers (Referenced)

Cette table contient les informations des clients.

Fields:

customer_id

name

email

tier_id

created_at

Chaque commande doit être liée à un client.

Orders

La table Orders représente une commande effectuée par un client.

Fields:

order_id

customer_id

order_date

status

total_amount

Status possibles :

Pending

Shipped

Delivered

Cancelled

Order_Items

La table Order_Items contient les détails des produits dans chaque commande.

Fields:

order_item_id

order_id

product_id

quantity

unit_price

Cela permet de gérer plusieurs produits dans une même commande.

Relationships

Customers → Orders
One-to-Many

Un client peut passer plusieurs commandes.

Orders → Order_Items
One-to-Many

Une commande peut contenir plusieurs produits.

Products → Order_Items
Many-to-One

Chaque item correspond à un produit spécifique.

How Orders Work

Le processus de commande suit ces étapes :

Le client sélectionne les produits à acheter.

Une commande est créée dans la table Orders.

Chaque produit devient une entrée dans Order_Items.

Le système calcule le montant total.

Le statut de la commande est mis à jour selon l’avancement.

4. Product and Inventory System
Product Definition

Le système de produits repose sur l’entité Products.

Chaque produit possède :

un identifiant unique

un nom

un prix de base

une devise associée

Cela permet au système de gérer un catalogue de produits international.

Flexible Product Attributes

Les produits peuvent avoir des caractéristiques différentes.

Par exemple :

un laptop → RAM, stockage

un vêtement → taille, couleur

Pour gérer cela, GlobalMart utilise un système flexible basé sur :

Attributes
Product_Attributes

Cela permet d’ajouter facilement de nouveaux types de produits sans modifier la structure de la base de données.

Inventory Management

Le système Inventory suit la quantité disponible de chaque produit.

Fields importants :

quantity_on_hand

reorder_threshold

Lorsque le stock descend sous le seuil minimum, le système peut déclencher un réapprovisionnement automatique.

Multi-Warehouse Management

GlobalMart possède plusieurs entrepôts.

La table Warehouses stocke :

la localisation

la capacité de stockage

La table Inventory connecte :

Products ↔ Warehouses

Cela permet de savoir dans quel entrepôt se trouve chaque produit.

5. Currency System
Overview

Le Currency System permet à GlobalMart de supporter plusieurs devises pour les transactions internationales.

Il permet :

d’enregistrer les devises utilisées

de convertir les prix

de gérer les taux de change

Entities
Currencies

La table Currencies contient les devises supportées par la plateforme.

Fields:

currency_code (Primary Key)

currency_name

symbol

Exemples :

currency_code	currency_name	symbol
USD	US Dollar	$
EUR	Euro	€
XAF	Central African CFA Franc	FCFA
Exchange_Rates

La table Exchange_Rates stocke les taux de conversion des devises.

Fields:

rate_id

currency_code

rate_to_usd

date_updated

Cela permet au système de convertir les prix dans différentes devises.

Relationships

Currencies → Products
One-to-Many

Une devise peut être utilisée par plusieurs produits.

Products → Currencies
Many-to-One

Chaque produit possède une devise pour son prix.

Currencies → Exchange_Rates
One-to-Many

Une devise peut avoir plusieurs taux de change au fil du temps.

Example

Products

product_id	product_name	base_price	currency_code
1	Laptop	900	USD
2	Jacket	120	EUR
3	Traditional Cloth	25000	XAF

Exchange Rates

currency_code	rate_to_usd
EUR	1.09
XAF	0.0016
6. System Integration

Les différents sous-systèmes de GlobalMart travaillent ensemble :

Customers
→ passent des
Orders

Orders
→ contiennent
Order_Items

Order_Items
→ référencent
Products

Products
→ ont des
Attributes

Products
→ sont stockés dans
Warehouses via Inventory

Products
→ utilisent
Currencies

Currencies
→ possèdent
Exchange_Rates

Cette architecture modulaire permet à GlobalMart d’être :

évolutif

flexible

adapté à un marché international

✅ Si tu veux, je peux aussi te faire :

un diagramme ERD complet de tout GlobalMart (très propre pour ton rapport)

la structure SQL complète de la base de données

la structure Django models.py correspondant à toute cette documentation.

je veux cette documentation en anglais

Voici la documentation complète de GlobalMart en anglais, bien organisée pour un rapport ou un fichier globalmart_system.md dans GitHub.

GlobalMart E-Commerce System Documentation
1. Introduction

GlobalMart is an international e-commerce platform designed to allow customers to browse products, place orders, and manage purchases across multiple regions.

The system is organized into several subsystems that work together to support the platform’s operations:

Customer System

Order System

Product and Inventory System

Currency System

These subsystems allow GlobalMart to manage:

customer accounts

product catalogs

inventory and warehouses

customer orders

international currencies and exchange rates

Together, they create a scalable and flexible architecture for a global marketplace.

2. Customer System
Overview

The Customer System manages all user accounts in the GlobalMart platform. It stores customer information, assigns loyalty tiers, and connects customers to their orders.

This subsystem ensures that each customer can register, place orders, and benefit from loyalty programs.

Entities
Customers

The Customers entity stores information about users who register on the platform.

Attributes:

customer_id (Primary Key)

first_name

last_name

email

phone

password_hash

tier_id (Foreign Key)

created_at

status

Each customer is assigned a loyalty tier and can place multiple orders.

Customer_Tiers

The Customer_Tiers entity defines the loyalty levels available to customers.

Attributes:

tier_id (Primary Key)

tier_name

discount_rate

benefits

Examples of tiers include:

Bronze

Silver

Gold

These tiers allow the system to provide different benefits or discounts to customers.

Relationships

Customer_Tiers → Customers
One-to-Many relationship

One tier can be assigned to many customers.

Customers → Orders
One-to-Many relationship

One customer can place multiple orders.

System Explanation

When a user registers on the platform, a record is created in the Customers table. Each customer is assigned a tier that determines their benefits or discounts.

When the customer purchases products, orders are recorded in the Orders table and linked to the customer through the customer_id.

This structure ensures proper management of customer accounts and purchase history.

3. Order System
Overview

The Order System keeps track of how customers purchase products on GlobalMart. It records who placed the order, what products were purchased, and the quantity of each product.

Tables
Customers (Referenced)

This table stores information about users who can place orders.

Fields:

customer_id

name

email

tier_id

created_at

Why it matters:
Every order must be linked to a customer.

Orders

The Orders table represents an order placed by a customer.

Fields:

order_id

customer_id

order_date

status

total_amount

Order status can be:

Pending

Shipped

Delivered

Cancelled

Why it matters:
It stores the main information about the order and connects it to the customer.

Order_Items

The Order_Items table stores the details of each product within an order.

Fields:

order_item_id

order_id

product_id

quantity

unit_price

Why it matters:
It allows the system to track multiple products within one order and calculate the total cost.

Products (Referenced)

The Products table is referenced but managed by another subsystem.

Fields:

product_id

name

price

Why it matters:
Order items need to know which product was purchased and its price.

Relationships

Customers → Orders
One customer can place many orders, but each order belongs to one customer.

Orders → Order_Items
One order can contain many order items.

Products → Order_Items
Each order item corresponds to one product.

How Orders Work

The order process follows these steps:

The customer selects products to purchase.

A new order is created and linked to the customer.

Each selected product becomes an entry in Order_Items with its quantity and price.

The system calculates the total order amount.

The order status is updated as it moves through processing.

4. Product and Inventory System
Product Definition and Identification

The Product entity is the foundation of the GlobalMart catalog.

Each product is uniquely identified to prevent confusion between similar items. Important product information includes:

product name

base price

currency code

Because GlobalMart operates internationally, products are linked to a currency to support pricing across different regions.

Managing Flexible Product Attributes

Products can have very different characteristics.

For example:

laptops may have RAM, processor, and storage

clothing may have size, color, and material

To manage this flexibility, GlobalMart uses a dynamic attribute system composed of:

Attributes

Product_Attributes

This design allows the system to add new product characteristics without modifying the main product table.

Inventory Tracking and Stock Levels

The Inventory system tracks the quantity of each product available in stock.

Important fields include:

quantity_on_hand

reorder_threshold

If stock levels fall below the reorder threshold, the system can trigger a restocking process.

Multi-Warehouse Management

GlobalMart stores products in multiple warehouses.

The Warehouses table stores:

warehouse location

storage capacity

The Inventory table links products with warehouses and records the quantity available at each location.

This allows the system to:

track product location

distribute stock efficiently

fulfill orders from the nearest warehouse.

5. Currency System
Overview

The Currency System allows GlobalMart to support international transactions using multiple currencies.

This subsystem ensures that product prices can be stored, displayed, and converted between different currencies.

Entities
Currencies

The Currencies table stores the list of supported currencies in the platform.

Fields:

currency_code (Primary Key)

currency_name

symbol

Example:

currency_code	currency_name	symbol
USD	US Dollar	$
EUR	Euro	€
XAF	Central African CFA Franc	FCFA
Exchange_Rates

The Exchange_Rates table stores the conversion rates between currencies.

Fields:

rate_id

currency_code

rate_to_usd

date_updated

This allows the system to convert prices between currencies.

Relationships

Currencies → Products
One-to-Many

A currency can be used by many products.

Products → Currencies
Many-to-One

Each product is associated with a single currency.

Currencies → Exchange_Rates
One-to-Many

A currency can have multiple exchange rates over time.

Example

Products

product_id	product_name	base_price	currency_code
1	Laptop	900	USD
2	Jacket	120	EUR
3	Traditional Cloth	25000	XAF

Exchange Rates

currency_code	rate_to_usd
EUR	1.09
XAF	0.0016
6. System Integration

The GlobalMart system connects all subsystems together:

Customers
→ place
Orders

Orders
→ contain
Order_Items

Order_Items
→ reference
Products

Products
→ have
Attributes

Products
→ are stored in
Warehouses via Inventory

Products
→ use
Currencies

Currencies
→ maintain
Exchange_Rates

This modular architecture allows GlobalMart to remain scalable, flexible, and suitable for a global e-commerce environment.