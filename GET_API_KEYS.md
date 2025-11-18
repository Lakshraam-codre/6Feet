# 🔑 Getting Your API Keys - Complete Guide

This guide provides exact step-by-step instructions with screenshots for getting all required API keys.

---

## 1. OpenAI API Key (5 minutes)

### Step 1: Create OpenAI Account
1. Go to: https://platform.openai.com/signup
2. Sign up with email or Google account
3. Verify your email

### Step 2: Add Payment Method (Required)
1. Go to: https://platform.openai.com/account/billing/overview
2. Click "Set up paid account"
3. Add credit card
4. Set usage limits if desired
   - Free trial credits expire after 3 months
   - Pay-as-you-go after that (~$0.002 per chat message)

### Step 3: Get API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it: `lesotho-chatbot`
4. **Copy the key immediately** (shown only once!)
   - It looks like: `sk-proj-ABC123XYZ...`
5. Click "Done"

**Save this securely!** You'll need it for the .env file.

---

## 2. Africa's Talking (SMS/USSD/Voice) - (5 minutes)

### Step 1: Create Account
1. Go to: https://africastalking.com
2. Click "Signup" (top right)
3. Fill in details:
   - Business name: "Lesotho Agriculture"
   - Email: your email
   - Password: strong password
4. Create account

### Step 2: Verify Email
1. Check email for Africa's Talking verification
2. Click verification link
3. Set up 2-factor authentication (recommended)

### Step 3: Get API Credentials
1. Go to: https://africastalking.com/app/settings/apikeys
2. You'll see:
   - **API Key**: (long string starting with `sandbox_`)
   - **Username**: usually shown as `YOUR_USERNAME`

**For Testing (Sandbox):**
- Use `sandbox_` prefixed keys
- Free SMS testing
- 10 SMS per day limit

**For Production:**
- Switch from Sandbox to Production in settings
- Purchase airtime credits
- Pay per SMS sent

### Step 4: Copy Your Credentials
```
AFRICAS_TALKING_USERNAME = Your username from dashboard
AFRICAS_TALKING_API_KEY = sandbox_abc123xyz... (for testing)
SMS_SHORTCODE = lesotho_agri (or requested code)
USSD_CODE = *384*50234# (example, check your account)
```

**Save these for .env file**

---

## 3. Weather API Key - (5 minutes)

### Option A: OpenWeatherMap (Recommended)

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (top right)
3. Fill in details and verify email
4. Go to: https://openweathermap.org/api/one-call-3
5. Click "How to start"
6. Choose FREE plan
7. Go to: https://home.openweathermap.org/api_keys
8. Copy "Default" API key
   - Looks like: `abc123def456xyz789...`

**Usage with FREE tier:**
- 1,000 calls/day limit
- Perfect for agriculture use case
- No credit card needed

### Option B: WeatherAPI (Alternative)

1. Go to: https://www.weatherapi.com
2. Click "Sign Up Free"
3. Fill email and password
4. Verify email
5. Dashboard shows API key automatically
   - Looks like: `abc123def456...`

**Usage with FREE tier:**
- 1,000,000 calls/month limit
- Better than OpenWeatherMap
- Recommended alternative

**Save your chosen key for .env file**

---

## Summary Table

Create a text file with your credentials (keep it safe!):

```
================== API KEYS ==================

1. OpenAI
   Key: sk-proj-....
   Status: ✓ Active

2. Africa's Talking  
   Username: your_username
   API Key: sandbox_abc123...
   SMS Shortcode: lesotho_agri
   USSD Code: *384*50234#
   Status: ✓ Sandbox Ready

3. Weather API
   Key: abc123xyz...
   Provider: openweathermap (or weatherapi)
   Status: ✓ Active

================================================
```

---

## Important Notes

⚠️ **SECURITY IMPORTANT:**
- Never commit API keys to GitHub
- Never share keys in emails or messages
- Regenerate keys if accidentally exposed
- Use environment variables (never hardcoded)

✅ **Testing Safe:**
- Africa's Talking has free Sandbox mode
- OpenAI has free trial credits ($5)
- Weather APIs have free tiers
- Total startup cost: $0 to test!

💡 **Production Costs (Estimated):**
- OpenAI: ~$10/month (1000 farmers, 5 messages/day each)
- Africa's Talking: ~$0.08 per SMS (~$80 for 1000 farmers)
- Weather API: Free tier sufficient
- Total: ~$90-100/month for 1000 farmers

---

## Next Step

Once you have all three API keys:
1. Open `backend/.env.example`
2. Copy it to `backend/.env`
3. Fill in the keys (see SETUP.md for details)
4. Start the application!

**Got all your keys?** Proceed to next step! ✨
