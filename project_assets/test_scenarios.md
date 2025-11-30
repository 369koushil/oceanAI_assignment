# Test Scenarios for E-Shop Checkout

## Document Information
- **Version:** 1.0
- **Date:** January 2025
- **Purpose:** Comprehensive test scenarios for QA automation

---

## Test Scenario Categories

### 1. Product Display and Cart Management

#### Scenario 1.1: Add Single Product to Cart
**Given:** User is on the checkout page  
**When:** User clicks "Add to Cart" for Wireless Headphones  
**Then:** 
- Product appears in shopping cart
- Cart shows "Wireless Headphones" with quantity 1
- Subtotal shows $79.99
- Cart is no longer empty

#### Scenario 1.2: Add Multiple Different Products
**Given:** Cart is empty  
**When:** User adds Wireless Headphones, Smart Watch, and Bluetooth Speaker  
**Then:**
- All three products appear in cart
- Cart shows 3 different items
- Subtotal equals $79.99 + $199.99 + $49.99 = $329.97

#### Scenario 1.3: Increase Product Quantity
**Given:** Wireless Headphones (qty: 1) is in cart  
**When:** User changes quantity input to 3  
**Then:**
- Cart displays quantity as 3
- Line total updates to $239.97 (79.99 × 3)
- Subtotal recalculates correctly

#### Scenario 1.4: Remove Product by Setting Quantity to Zero
**Given:** Smart Watch is in cart with quantity 2  
**When:** User sets quantity to 0  
**Then:**
- Smart Watch is removed from cart
- Subtotal decreases by $399.98
- Cart recalculates total

#### Scenario 1.5: Empty Cart State
**Given:** All products have been removed  
**Then:**
- Cart displays "Your cart is empty"
- Subtotal shows $0.00
- Total shows $0.00

---

### 2. Discount Code Functionality

#### Scenario 2.1: Apply Valid Discount Code SAVE15
**Given:** 
- Cart subtotal is $249.99
- No discount is currently applied  
**When:** User enters "SAVE15" and clicks Apply  
**Then:**
- Success message displays: "Discount applied: 15% off!"
- Discount shows -$37.50 (15% of $249.99)
- Total is reduced by discount amount
- Message appears in green color

#### Scenario 2.2: Apply Invalid Discount Code
**Given:** Cart has items totaling $100  
**When:** User enters "INVALID" and clicks Apply  
**Then:**
- Error message displays: "Invalid discount code"
- Error message appears in red text
- No discount is applied
- Discount amount remains $0.00

#### Scenario 2.3: Submit Empty Discount Code
**Given:** Discount code field is empty  
**When:** User clicks Apply button  
**Then:**
- Error displays: "Please enter a discount code"
- Error appears in red text
- No discount is applied

#### Scenario 2.4: Case Insensitive Discount Code
**Given:** Cart subtotal is $100  
**When:** User enters "save15" (lowercase)  
**Then:**
- Code is accepted (converted to uppercase internally)
- Discount applies correctly at 15%

#### Scenario 2.5: Discount Calculation with Multiple Items
**Given:** 
- Cart contains: Wireless Headphones ($79.99) + Smart Watch ($199.99)
- Subtotal: $279.98  
**When:** User applies "SAVE15"  
**Then:**
- Discount calculates as $42.00 (15% of $279.98)
- Total becomes $237.98 (before shipping)

---

### 3. Shipping Method Selection

#### Scenario 3.1: Default Shipping Method
**Given:** Page loads for first time  
**Then:**
- Standard Shipping is selected by default
- Shipping cost shows $0.00
- Delivery time displays "5-7 business days"

#### Scenario 3.2: Select Express Shipping
**Given:** Standard shipping is currently selected  
**When:** User selects Express Shipping radio button  
**Then:**
- Express Shipping becomes selected
- Shipping cost updates to $10.00
- Total increases by $10.00
- Delivery time shows "2-3 business days"

#### Scenario 3.3: Switch Back to Standard Shipping
**Given:** Express shipping is selected ($10 shipping cost)  
**When:** User selects Standard Shipping  
**Then:**
- Shipping cost returns to $0.00
- Total decreases by $10.00
- Delivery time changes to "5-7 business days"

#### Scenario 3.4: Shipping Cost with Discount
**Given:**
- Subtotal: $100
- Discount (SAVE15): -$15
- Express Shipping: $10  
**Then:**
- Total calculation: $100 - $15 + $10 = $95.00
- Shipping is added AFTER discount is applied

---

### 4. Form Validation

#### Scenario 4.1: Submit Form with All Valid Fields
**Given:**
- Name: "John Doe"
- Email: "john@example.com"
- Address: "123 Main St, New York"
- Cart has items
- Shipping method selected
- Payment method selected  
**When:** User clicks "Pay Now"  
**Then:**
- Form submits successfully
- Success message displays: "✅ Payment Successful! Thank you for your order."
- "Pay Now" button text changes to "Payment Complete"
- Button becomes disabled

#### Scenario 4.2: Submit with Empty Name Field
**Given:** Name field is empty, other fields valid  
**When:** User clicks "Pay Now"  
**Then:**
- Error displays below name field: "Please enter your full name"
- Error text is red
- Form does not submit
- Success message does not appear

#### Scenario 4.3: Submit with Invalid Email Format
**Given:** Email field contains "invalid-email" (no @ symbol)  
**When:** User clicks "Pay Now"  
**Then:**
- Error displays below email: "Please enter a valid email address"
- Error text is red color
- Form does not submit

#### Scenario 4.4: Submit with Empty Address
**Given:** Address field is blank, other fields valid  
**When:** User submits form  
**Then:**
- Error shows: "Please enter your shipping address"
- Error appears in red below address field
- Form validation fails

#### Scenario 4.5: Multiple Field Validation Errors
**Given:**
- Name: empty
- Email: "invalid"
- Address: empty  
**When:** User clicks "Pay Now"  
**Then:**
- All three error messages display simultaneously
- Each error appears below its respective field
- All errors are in red text
- Form does not submit

#### Scenario 4.6: Valid Email Format Variations
**Test Cases for Valid Emails:**
- "user@example.com" - Should be accepted
- "test.user@domain.co.uk" - Should be accepted
- "john.doe+tag@example.org" - Should be accepted

**Test Cases for Invalid Emails:**
- "user@" - Should show error
- "@domain.com" - Should show error
- "userdomain.com" - Should show error
- "user @example.com" - Should show error

---

### 5. Payment Method Selection

#### Scenario 5.1: Default Payment Method
**Given:** Page loads  
**Then:**
- Credit Card is selected by default
- PayPal is not selected

#### Scenario 5.2: Switch to PayPal
**Given:** Credit Card is currently selected  
**When:** User clicks PayPal radio button  
**Then:**
- PayPal becomes selected
- Credit Card is deselected
- Payment method value is "paypal"

#### Scenario 5.3: Switch Back to Credit Card
**Given:** PayPal is selected  
**When:** User selects Credit Card  
**Then:**
- Credit Card is selected
- Payment method value is "credit-card"

---

### 6. Payment Submission

#### Scenario 6.1: Submit Payment with Empty Cart
**Given:** Cart is empty (no items)  
**When:** User fills all form fields and clicks "Pay Now"  
**Then:**
- Alert displays: "Your cart is empty. Please add items before checkout."
- Payment does not process
- Success message does not appear

#### Scenario 6.2: Successful Payment Complete Flow
**Given:**
- Cart: Wireless Headphones ($79.99)
- Discount: SAVE15 (-$12.00)
- Shipping: Express ($10.00)
- All form fields valid  
**When:** User clicks "Pay Now"  
**Then:**
- Success message appears with green background
- Message text: "✅ Payment Successful! Thank you for your order."
- Button text changes to "Payment Complete"
- Button is disabled
- Total paid: $77.99

---

### 7. Calculation and Total Verification

#### Scenario 7.1: Complex Total Calculation
**Given:**
- Product 1: Wireless Headphones × 2 = $159.98
- Product 2: Bluetooth Speaker × 1 = $49.99
- Subtotal: $209.97
- Discount (SAVE15): -$31.50
- Shipping (Express): $10.00  
**Expected Total:** $188.47

**Verification:**
- Subtotal: $209.97 ✓
- Discount: -$31.50 ✓
- Shipping: +$10.00 ✓
- Final Total: $188.47 ✓

#### Scenario 7.2: Total with No Discount, Standard Shipping
**Given:**
- Single product: Smart Watch = $199.99
- No discount code
- Standard shipping (free)  
**Expected:**
- Subtotal: $199.99
- Shipping: $0.00
- Discount: $0.00
- Total: $199.99

---

### 8. UI/UX Validation

#### Scenario 8.1: Error Message Color Verification
**Requirement:** All validation errors must appear in RED text  
**Test:**
- Trigger name validation error
- Verify color is #dc3545 (red)
- Trigger email validation error  
- Verify color is #dc3545 (red)

#### Scenario 8.2: Pay Now Button Color
**Requirement:** "Pay Now" button must be GREEN  
**Test:**
- Verify button background is #28a745 (green)
- Not purple, not blue, must be green

#### Scenario 8.3: Success Message Styling
**Requirement:** Success message has green background  
**Test:**
- Submit valid payment
- Verify success message background is #28a745 (green)
- Verify text is white

---

### 9. Edge Cases and Negative Tests

#### Scenario 9.1: Maximum Quantity Test
**Given:** User enters quantity of 99 for a product  
**Then:**
- System accepts the quantity
- Calculates total correctly (price × 99)

#### Scenario 9.2: Special Characters in Name
**Test:** Enter name with special characters: "O'Brien"  
**Expected:** Should be accepted as valid

#### Scenario 9.3: Very Long Address
**Test:** Enter address with 500+ characters  
**Expected:** Should be accepted (no max length restriction specified)

#### Scenario 9.4: Rapid Quantity Changes
**Test:** Quickly change quantity multiple times  
**Expected:**
- Cart updates smoothly without errors
- No calculation errors
- Final quantity reflects last input

#### Scenario 9.5: Apply Same Discount Code Twice
**Test:** Apply "SAVE15", then try to apply "SAVE15" again  
**Expected:** 
- Discount is not doubled
- Only one 15% discount applied

---

### 10. Cross-Feature Integration Tests

#### Scenario 10.1: Complete Checkout Journey
**Steps:**
1. Add Wireless Headphones to cart
2. Add Smart Watch to cart
3. Change Wireless Headphones quantity to 2
4. Apply discount code "SAVE15"
5. Select Express Shipping
6. Fill in customer details
7. Select PayPal payment
8. Submit payment

**Expected:**
- All steps execute without errors
- Total calculates correctly at each step
- Final payment succeeds
- Success message displays

#### Scenario 10.2: Modify Cart After Applying Discount
**Steps:**
1. Add product ($100)
2. Apply SAVE15 (-$15)
3. Add another product ($50)

**Expected:**
- New subtotal: $150
- Discount recalculates: -$22.50 (15% of new subtotal)
- Total updates correctly

---

## Priority Classification

### P0 - Critical (Must Pass)
- Payment submission with valid data
- Discount code SAVE15 calculation
- Form validation errors in red text
- Empty cart prevention

### P1 - High Priority
- Cart quantity modifications
- Shipping cost calculations
- Email format validation
- Success message display

### P2 - Medium Priority
- UI color verifications
- Edge case handling
- Multiple product scenarios

### P3 - Low Priority
- Hover effects
- Animation timings
- Responsive layout

---

**End of Test Scenarios Document**