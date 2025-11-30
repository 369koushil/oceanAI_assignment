# E-Shop Checkout - Product Specifications

## Document Version: 1.0
**Last Updated:** January 2025  
**Owner:** Product Team

---

## Overview
This document outlines the functional specifications for the E-Shop checkout system. All features described here must be implemented and tested according to these requirements.

---

## Product Catalog

### Available Products

1. **Wireless Headphones**
   - Product ID: WH-001
   - Price: $79.99
   - Description: Premium noise-cancelling headphones
   - Stock Status: In Stock
   - Category: Electronics

2. **Smart Watch**
   - Product ID: SW-002
   - Price: $199.99
   - Description: Track your fitness and stay connected
   - Stock Status: In Stock
   - Category: Electronics

3. **Bluetooth Speaker**
   - Product ID: BS-003
   - Price: $49.99
   - Description: Portable speaker with amazing sound
   - Stock Status: In Stock
   - Category: Electronics

---

## Shopping Cart Functionality

### Cart Operations
- Users can add products to cart using the "Add to Cart" button
- Each product can have a quantity from 1 to 99
- Users can modify quantity using the quantity input field
- Setting quantity to 0 removes the item from cart
- Cart displays item name, quantity, and line total
- Cart is stored in browser memory (session-based)

### Cart Calculations
- **Subtotal**: Sum of all (item price × quantity)
- **Shipping Cost**: Calculated based on selected shipping method
- **Discount**: Applied from valid discount codes
- **Total**: Subtotal + Shipping - Discount

---

## Discount Code System

### Valid Discount Codes

#### SAVE15
- **Discount Type**: Percentage
- **Discount Amount**: 15% off subtotal
- **Validity**: Active
- **Conditions**: 
  - Applies to subtotal before shipping
  - Cannot be combined with other codes
  - No minimum purchase required
- **Expected Behavior**: When "SAVE15" is entered and applied, the discount should show 15% reduction on the subtotal

### Invalid Discount Code Behavior
- Any code other than "SAVE15" should display error: "Invalid discount code"
- Empty discount code submission should display: "Please enter a discount code"
- Discount can only be applied once per session
- If invalid code is entered, no discount should be applied

---

## Shipping Methods

### Standard Shipping
- **Cost**: FREE ($0.00)
- **Delivery Time**: 5-7 business days
- **Default Selection**: Yes
- **Availability**: All addresses

### Express Shipping
- **Cost**: $10.00
- **Delivery Time**: 2-3 business days
- **Default Selection**: No
- **Availability**: All addresses

### Shipping Calculation Rules
- Shipping cost is added to subtotal after discount
- Changing shipping method recalculates total immediately
- Standard shipping is selected by default on page load

---

## Form Validation Requirements

### Required Fields
All fields marked with * are mandatory:
1. Full Name
2. Email Address
3. Shipping Address
4. Shipping Method (radio button - one must be selected)
5. Payment Method (radio button - one must be selected)

### Field-Specific Validation

#### Full Name
- **Validation**: Must not be empty
- **Error Message**: "Please enter your full name"
- **Error Display**: Red text below the input field
- **Trigger**: On form submission

#### Email Address
- **Validation**: Must match email format (contains @ and domain)
- **Error Message**: "Please enter a valid email address"
- **Error Display**: Red text below the input field
- **Valid Examples**: user@example.com, test.user@domain.co.uk
- **Invalid Examples**: user@, @domain.com, userdomain.com
- **Trigger**: On form submission

#### Shipping Address
- **Validation**: Must not be empty
- **Error Message**: "Please enter your shipping address"
- **Error Display**: Red text below the input field
- **Trigger**: On form submission

---

## Payment Processing

### Payment Methods

#### Credit Card
- **Label**: "💳 Credit Card"
- **Value**: credit-card
- **Default**: Yes
- **Processing**: Client-side validation only (no actual payment processing in demo)

#### PayPal
- **Label**: "🅿️ PayPal"
- **Value**: paypal
- **Default**: No
- **Processing**: Client-side validation only (no actual payment processing in demo)

### Payment Submission Rules

#### Successful Payment Conditions
All of the following must be true:
1. Cart contains at least one item
2. All required fields are valid
3. Email format is correct
4. Name is not empty
5. Address is not empty

#### Payment Success Behavior
When all conditions are met:
- Display message: "✅ Payment Successful! Thank you for your order."
- Success message appears with green background
- "Pay Now" button changes to "Payment Complete"
- "Pay Now" button becomes disabled

#### Payment Failure Behavior
If conditions are not met:
- Show specific error messages for each invalid field
- Do not display success message
- Keep "Pay Now" button enabled
- Do not process payment

### Edge Cases
- **Empty Cart**: If user tries to pay with empty cart, show alert: "Your cart is empty. Please add items before checkout."
- **Partial Form Completion**: Show errors only for empty/invalid fields, allow user to correct

---

## Business Rules Summary

1. **Minimum Order**: No minimum order value required
2. **Maximum Quantity**: 99 items per product
3. **Discount Limits**: Only one discount code per order
4. **Shipping Options**: Must select exactly one shipping method
5. **Payment Options**: Must select exactly one payment method
6. **Form Validation**: All validation happens on form submission
7. **Session Handling**: Cart data persists only during browser session

---

## Testing Priority Areas

### High Priority
- Discount code "SAVE15" applies 15% discount correctly
- Form validation for all required fields
- Payment success message displays when all conditions met
- Cart quantity updates and calculations

### Medium Priority
- Shipping method selection updates total
- Invalid discount codes show appropriate errors
- Email format validation

### Low Priority
- UI/UX animations and transitions
- Hover effects
- Responsive design

---

## Known Limitations
- This is a demo checkout system without actual payment processing
- No backend server integration
- No user authentication
- No order history
- Cart resets on page refresh

---

**End of Document**