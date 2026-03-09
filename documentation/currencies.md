Name:  TCHANGO NODUOU  JOSEPH
Matricule: ICTU20233955


GlobalMart E-Commerce Platform
Currency & Exchange Rate System

1. Introduction
   
The Currency System is the sub-module (in the GlobalMart E-commerce platform) responsible for managing all currency-related data in GlobalMart. It covers two main concerns: maintaining a master list of all currencies the platform supports, and storing the exchange rates used to convert prices between those currencies.
This document contains analysis, entity design, business rules, and ERD description for this module. It serves as the reference file for the currency-system branch of the team's GitHub repository.

3. System Context and Motivation

A simple e-commerce system typically operates in a single currency. GlobalMart is different — it targets an international customer base where people expect to see prices in their local currency and pay in it too. This means the system needs to know what currencies exist, what the conversion rate between any two currencies is on any given day, and which rate was active at the exact moment an order was placed.
For example, consider a customer in Cameroon who wants to buy a product priced at $150 USD. The system must look up the current USD to XAF (CFA Franc) exchange rate, which is approximately 655.957, and compute the local price: 150 × 655.957 = 98,393.55 XAF. The order then records both figures — 98,393.55 XAF as the amount the customer paid in their currency, and 150.00 USD as the base currency equivalent used for internal financial reporting.
This dual-storage approach is a fundamental design principle of the GlobalMart currency system. All financial reports are consolidated in USD, while customers always see amounts in their own currency.

4. Entities and Attributes
The Currency System involves two entities: Currencies and Exchange_Rates.

3.1 Entity: Currencies
The Currencies table is the master reference for every currency supported on the platform. Each row represents one world currency, identified by its internationally standardised three-letter ISO 4217 code.

Attribute	Data Type	Constraints	Description
currency_code	CHAR(3)	PRIMARY KEY	ISO 4217 three-letter code, e.g. USD, EUR, XAF, GBP
currency_name	VARCHAR(50)	NOT NULL	Full name of the currency, e.g. US Dollar, Euro
symbol	VARCHAR(10)	—	Display symbol used in the user interface, e.g. $, €, FCFA


3.2 Entity: Exchange_Rates
The Exchange_Rates table stores the conversion factor between pairs of currencies. Every row links a source currency to a target currency and records the rate that was valid from a specific date onward. This date-based design means the system keeps a full history of rate changes — old records are never deleted, and new rates are always added as new rows with a new effective date.

Attribute	Data Type	Constraints	Description
from_currency	CHAR(3)	PK, FK → Currencies	The source currency, e.g. USD
to_currency	CHAR(3)	PK, FK → Currencies	The target currency, e.g. EUR
effective_date	DATE	PK, NOT NULL	The date from which this rate applies
rate	DECIMAL(18,6)	NOT NULL, CHECK > 0	Conversion factor: 1 unit of from_currency equals this many units of to_currency

The composite primary key consisting of from_currency, to_currency, and effective_date is a key design decision. It enforces that only one rate per currency pair per date can exist, while naturally preserving the full history of every rate change the platform has ever recorded.

4. Relationships
The Currency System involves one main relationship between the two entities.
The Currencies table relates to Exchange_Rates in two ways simultaneously — a currency can appear as the source (from_currency) in many exchange rate records, and it can also appear as the target (to_currency) in many exchange rate records. Both directions are one-to-many: one currency, many rate records.
Every row in Exchange_Rates always references exactly two currencies — one as the source and one as the target. Both foreign keys point back to the same Currencies table.

Relationship	Type	Meaning
Currencies → Exchange_Rates (via from_currency)	1 : N	One currency is the source in many rate records
Currencies → Exchange_Rates (via to_currency)	1 : N	One currency is the target in many rate records

5. ERD Description
The ERD for the Currency System contains two entity boxes connected by two foreign keys.
The Currencies entity holds three attributes: currency_code as the primary key, currency_name, and symbol.
The Exchange_Rates entity holds four attributes: from_currency as a foreign key, to_currency as a foreign key, effective_date as a primary key, and rate.
One lines connect Currencies to Exchange_Rates — Indicating the relationship: From currency_code to from_currency, and from currency_code to to_currency. Both carry a one-to-many notation: one currency record on the Currencies side, many records on the Exchange_Rates side.
The ERD diagram is drawn separately and saved as a .JPG file in the ERD folder of the repository under the filename currency_system_erd.JPG.
