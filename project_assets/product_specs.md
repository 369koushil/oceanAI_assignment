# Product Specifications - E-Shop Checkout
Version: 1.0
Updated: Jan 2025

## Product Catalog
Products shown in HTML:

1. Wireless Headphones
   - ID: WH-001
   - Price: $79.99
   - Description: Premium noise-cancelling headphones

2. Smart Watch
   - ID: SW-002
   - Price: $199.99
   - Description: Track your fitness and stay connected

3. Bluetooth Speaker
   - ID: BS-003
   - Price: $49.99
   - Description: Portable speaker with amazing sound

## Cart Functionality
- Add to cart increases quantity by 1
- Quantity can be edited (min 0)
- If quantity = 0 → remove item
- Cart shows:
  * Product name
  * Quantity
  * Line total
- Auto recalculates:
  * Subtotal
  * Shipping
  * Discount
  * Total

## Shipping Methods
Standard Shipping:
- Cost: $0
- Delivery: 5–7 business days (default)

Express Shipping:
- Cost: $10
- Delivery: 2–3 business days

## Discount Code Rules
Valid Code: SAVE15  
- Discount: 15% of subtotal  
- Applies before shipping  
- Error messages:
  * Invalid: "Invalid discount code"
  * Empty: "Please enter a discount code"

## Required Fields:
- Full Name
- Email
- Address
- Shipping Method
- Payment Method

## Form Validation Rules
Full Name:
- Not empty → error: “Please enter your full name”

Email:
- Regex: /^[^@\s]+@[^@\s]+\.[^@\s]+$/  
- Error: “Please enter a valid email address”

Address:
- Not empty → error: “Please enter your shipping address”

## Payment Success Conditions
ALL must be true:
1. Cart not empty  
2. Name valid  
3. Email valid  
4. Address valid  

On success:
- Show success message
- Disable Pay Now button
- Change text → “Payment Complete”
