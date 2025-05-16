# 📱 M-Shamba USSD Integration
*USSD-powered crop trading for 10M Kenyan farmers with basic phones*

## 🌾 Problem: The Middlemen Trap
**82% of farmers rely on exploitative middlemen**

USSD solves 3 key barriers:
1. **No smartphones** (USSD works on all handsets)
2. **Low literacy** (menu-driven interface)
3. **Trust gaps** (blockchain-based transaction logging)

## 🚀 New Features

### 1. Enhanced USSD Flow
- Redis-based session management for improved reliability
- Robust error handling and recovery
- Input validation and retry limits
- Comprehensive logging and monitoring

### 2. Base OnchainKit Integration
- Smart wallet creation for each farmer
- USDC payments on Base network
- Real-time transaction status updates
- Escrow contract integration

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Redis Server
- Base API Key

### Environment Variables
```bash
# Create .env file
REDIS_URL=redis://localhost:6379/0
BASE_RPC_URL=https://goerli.base.org
USDC_CONTRACT_ADDRESS=your_contract_address
ESCROW_CONTRACT_ADDRESS=your_escrow_address
VITE_BASE_API_KEY=your_base_api_key
```

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Django server
python manage.py runserver
```

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔄 USSD Flow

| Step | Action | Response |
|------|--------|----------|
| 1 | Dial `483*1#` | Main menu |
| 2 | Select crop | Show USDC prices |
| 3 | Enter quantity | Calculate total |
| 4 | Confirm | Initialize payment |
| 5 | Payment | Base wallet transaction |
| 6 | Confirmation | SMS with tx hash |

## 🧪 Testing

```bash
# Run backend tests
python manage.py test

# Run frontend tests
npm test
```

## 📊 Monitoring

The application includes comprehensive logging and monitoring:
- USSD session tracking
- Blockchain transaction status
- Error rates and types
- Response times
- Session completion rates

## 🔒 Security Features

1. Redis session timeout (5 minutes)
2. Input validation and sanitization
3. Rate limiting
4. Secure wallet management
5. Error recovery mechanisms

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License.

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
