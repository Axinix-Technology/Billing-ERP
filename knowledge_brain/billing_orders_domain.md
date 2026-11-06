# Billing & Orders Domain Model

## Overview
Handles POS checkout, bill generation, payment methods (Cash, UPI, Card), and order archiving.

## Models
- **`Order`**:
  - `bill_number` (CharField, unique)
  - `customer_name` (CharField, default 'Walk-in Customer')
  - `customer_phone` (CharField, default '')
  - `subtotal` (DecimalField)
  - `tax_amount` (DecimalField, default 0.00)
  - `discount_amount` (DecimalField, default 0.00)
  - `grand_total` (DecimalField)
  - `payment_method` (CharField: 'cash', 'upi', 'card')
  - `cashier` (ForeignKey to `User`, nullable)
  - `status` (SmallIntegerField, default 1)
  - `created_at` (DateTimeField, auto_now_add=True)
- **`OrderItem`**:
  - `order` (ForeignKey to `Order`, CASCADE)
  - `product` (ForeignKey to `Product`, SET_NULL)
  - `product_name` (CharField)
  - `quantity` (IntegerField, default 1)
  - `unit_price` (DecimalField)
  - `total_price` (DecimalField)
  - `customization` (CharField, blank=True)
