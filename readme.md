### 1. Testing POST /faucet/fund

URL: `http://localhost:8000/faucet/fund/`

   ```
   Headers:

    Key: Content-Type
    Value: application/json
   
   ```

Body:
   ```json
    JSON payload:
    {
       "wallet_address": "0xYourWalletAddressHere"
    }
   ```

**Expected Responses:**

- Success (200 OK):

  ```json
  {
      "tx_hash": "0x123...abc"
  }
  ```

- Rate Limit Exceeded (429 Too Many Requests):
  ```json
  {
      "error": "Rate limit exceeded"
  }
  ```

- Invalid Wallet (400 Bad Request):

  ```json
  {
      "error": "Invalid wallet address"
  }
  ```

### 2. Testing GET /faucet/stats

type  **GET**
URL: `http://localhost:8000/faucet/stats/`

**Expected Response (200 OK):**
```json
{
    "success": 5,
    "failed": 2
}
```

### Common Test Scenarios:

1. **Valid Request:**
   - Wallet: Valid Sepolia address
   - Expected: 200 OK with transaction hash

2. **Invalid Wallet:**
   - Wallet: "0xInvalidAddress"
   - Expected: 400 Bad Request with error message

3. **Duplicate Request:**
   - Send same wallet twice within 1 minute
   - Expected: 429 Too Many Requests on second attempt

4. **Different IP Testing:**
   - Use Postman's built-in proxy or different machines
   - Add header `X-Forwardssed-For: 1.2.3.4` to simulate different IPs

### Viewing Results:
- Check transaction status on [Sepolia Etherscan](https://sepolia.etherscan.io/) using the returned tx_hash
- Monitor Django logs for errors:
  ```bash
  docker-compose logs web
  ```

Remember to fund your sender wallet first using a Sepolia faucet like:
- https://sepoliafaucet.com/
- https://faucet.quicknode.com/ethereum/sepolia