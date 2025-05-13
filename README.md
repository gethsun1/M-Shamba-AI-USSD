# 📱 M-Shamba USSD Integration
*USSD-powered crop trading for 10M Kenyan farmers with basic phones*

## 🌾 Problem: The Middlemen Trap
**82% of farmers rely on exploitative middlemen**

USSD solves 3 key barriers:
1. **No smartphones** (USSD works on all handsets)
2. **Low literacy** (menu-driven interface)
3. **Trust gaps** (real-time transaction logging)

---

## ⚡ USSD Workflow (Safaricom Example)

| Farmer Action               | System Response                          | Blockchain Event               |
|-----------------------------|------------------------------------------|--------------------------------|
| Dial `483*1#`               | "1. Sell 2. Prices 3. Wallet"            | -                              |
| Select `1` → Enter crop code `401` | "Enter quantity (kg):"            | -                              |
| Type `100` → Confirm        | "Best market price: 50 KES/kg (Unga Ltd)"| Price oracle queries Chainlink |
| Accept offer                | "Payment: 1. M-Pesa 2. USDC"             | Escrow contract deployed       |
| Choose `2`                  | "5,000 USDC pending delivery"            | Base blockchain tx initiated   |
| SMS `DELIVERED 123ABC`      | "Payment released! +10 M-SHM tokens"     | Smart contract executes        |


```bash

## Getting Started

1. Run `npm install`
2. Run `npm run dev`
```

## 2. Smart Contract Clauses

| Clause                     | Enforcement Mechanism                     |
|----------------------------|-------------------------------------------|
| 24hr payment guarantee     | Escrow penalty smart contract             |
| Data ownership             | NFT-gated access control                  |
| Dispute resolution         | Crowdsourced voting via token staking     |

---

## 🛠️ Integration Guide

### Telco Partners

| Provider   | API Docs                          | Key Endpoint   |
|------------|-----------------------------------|----------------|
| Safaricom  | [Africa's Talking](https://africastalking.com) | `POST /ussd`   |
| Airtel     | [Airtel Africa](https://developer.airtel.com)   | `GET /gateway` |
