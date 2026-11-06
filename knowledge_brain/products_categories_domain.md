# Products & Categories Domain Model

## Overview
Manages POS catalog, product categories, pricing, item availability, and imagery.

## Models
- **`Category`**:
  - `name` (CharField, unique)
  - `icon` (CharField, default 'Coffee')
  - `status` (SmallIntegerField, default 1)
- **`Product`**:
  - `category` (ForeignKey to `Category`, CASCADE)
  - `name` (CharField)
  - `price` (DecimalField)
  - `description` (TextField, blank=True)
  - `image_url` (URLField/CharField, blank=True)
  - `is_available` (BooleanField, default True)
  - `status` (SmallIntegerField, default 1)
  - `created_at` (DateTimeField, auto_now_add=True)
