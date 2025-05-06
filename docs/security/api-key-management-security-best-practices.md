# API Key Management and Security Best Practices

**Last Updated:** 2023-06-12

## Table of Contents

1. [Introduction](#introduction)
2. [API Key Security Fundamentals](#api-key-security-fundamentals)
3. [Centralized API Key Management](#centralized-api-key-management)
4. [Environment File Security](#environment-file-security)
5. [API Key Rotation Strategies](#api-key-rotation-strategies)
6. [Encryption and Secure Storage](#encryption-and-secure-storage)
7. [Version Control Considerations](#version-control-considerations)
8. [Automated Solutions](#automated-solutions)
9. [Implementation Examples](#implementation-examples)
10. [Security Incident Response](#security-incident-response)
11. [References and Resources](#references-and-resources)

## Introduction

API keys are critical security credentials that grant access to services, data, and functionality. Proper management of these keys is essential to prevent unauthorized access, data breaches, and potential financial losses. This document outlines comprehensive strategies for securing API keys across development environments, with a focus on practical implementation.

## API Key Security Fundamentals

### Key Security Principles

1. **Never hardcode API keys** in source code, configuration files, or client-side code
2. **Implement the principle of least privilege** - keys should have minimal necessary permissions
3. **Treat API keys as sensitive as passwords** - they often provide direct access to paid services
4. **Use different API keys for different environments** (development, testing, production)
5. **Monitor API key usage** to detect unusual patterns that might indicate compromise

### Common API Key Vulnerabilities

1. **Exposure in public repositories** - keys committed to GitHub or other public repositories
2. **Client-side exposure** - keys embedded in mobile apps or frontend JavaScript
3. **Insecure storage** - keys stored in plaintext or weakly encrypted
4. **Overprivileged keys** - keys with more permissions than necessary
5. **Lack of rotation** - keys that remain unchanged for extended periods

## Centralized API Key Management

### Benefits of Centralization

1. **Simplified management** - one location to update when keys change
2. **Consistent security practices** - standardized approach across projects
3. **Easier auditing** - centralized logs of key access and usage
4. **Reduced risk of exposure** - fewer copies of keys means less risk

### Centralized Storage Options

#### 1. Secrets Management Services

- **[HashiCorp Vault](https://www.vaultproject.io/)** - Open-source secrets management
- **[AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)** - Cloud-based secrets management
- **[Azure Key Vault](https://azure.microsoft.com/en-us/services/key-vault/)** - Microsoft's secrets management solution
- **[Google Secret Manager](https://cloud.google.com/secret-manager)** - Google Cloud's secrets management

#### 2. Custom API Service

A custom API service for managing keys offers maximum flexibility:

```javascript
// Example API endpoint for retrieving keys
app.get('/api/keys/:service', authenticate, (req, res) => {
  const { service } = req.params;
  // Retrieve key from secure storage
  const key = getKeyFromSecureStorage(service);
  // Return key with short expiration
  res.json({ 
    key, 
    expires: new Date(Date.now() + 3600000) // 1 hour expiration
  });
});
```

#### 3. Shared Environment File

For smaller teams or projects, a shared environment file in a secure location:

```bash
# ~/.env.mcp - Centralized environment file
BRAVE_API_KEY=your-brave-api-key
PERPLEXITY_API_KEY=your-perplexity-api-key
```

## Environment File Security

### Best Practices for .env Files

1. **Always add .env files to .gitignore**
2. **Use .env.example files** with placeholder values for documentation
3. **Limit access to .env files** to only those who need it
4. **Consider encrypting .env files** when not in use
5. **Validate environment variables** on application startup

### Environment File Structure

```bash
# .env.mcp - MCP Server Environment Variables
# Last updated: 2023-06-12

# Search APIs
BRAVE_API_KEY=your-brave-api-key-here
PERPLEXITY_API_KEY=your-perplexity-api-key-here

# AI Service APIs
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Database Credentials
DB_PASSWORD=your-database-password-here
```

### Using Environment Files in VS Code MCP

```json
// VS Code MCP configuration using envFile
{
  "servers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "envFile": "~/.env.mcp"
    }
  }
}
```

## API Key Rotation Strategies

### Why Rotate API Keys?

1. **Limit damage from compromised keys**
2. **Comply with security policies** that require periodic rotation
3. **Revoke access** from former team members
4. **Ensure keys don't become stale** or forgotten

### Rotation Frequency Guidelines

| Risk Level | Recommended Rotation Frequency |
|------------|--------------------------------|
| Low        | Every 90 days                  |
| Medium     | Every 30-60 days               |
| High       | Every 7-30 days                |
| Critical   | Every 1-7 days                 |

### Manual Rotation Process

1. **Generate new API key** from the service provider
2. **Update the key** in your secure storage or environment files
3. **Distribute the new key** to all necessary environments
4. **Verify functionality** with the new key
5. **Revoke the old key** after confirming everything works

### Automated Rotation Script

```python
#!/usr/bin/env python3
# rotate_api_keys.py

import requests
import os
import json
import re
from dotenv import load_dotenv

# Load current keys
load_dotenv('~/.env.mcp')

# Function to rotate Brave Search API key
def rotate_brave_key():
    current_key = os.getenv('BRAVE_API_KEY')
    
    # Call Brave API to rotate key (hypothetical endpoint)
    headers = {'Authorization': f'Bearer {current_key}'}
    response = requests.post('https://api.brave.com/rotate-key', headers=headers)
    
    if response.status_code == 200:
        new_key = response.json()['new_key']
        return new_key
    else:
        print(f"Failed to rotate Brave key: {response.text}")
        return None

# Rotate keys for each service
new_keys = {}

brave_key = rotate_brave_key()
if brave_key:
    new_keys['BRAVE_API_KEY'] = brave_key

# Update .env.mcp file
if new_keys:
    with open('~/.env.mcp', 'r') as file:
        env_content = file.read()
    
    # Replace old keys with new ones
    for key, value in new_keys.items():
        env_content = re.sub(f'{key}=.*', f'{key}={value}', env_content)
    
    with open('~/.env.mcp', 'w') as file:
        file.write(env_content)
    
    print("API keys rotated successfully")
else:
    print("No keys were rotated")
```

## Encryption and Secure Storage

### Encrypting Environment Files

#### 1. Using git-crypt

[git-crypt](https://github.com/AGWA/git-crypt) allows you to encrypt specific files in your Git repository:

```bash
# Install git-crypt
brew install git-crypt  # macOS
apt-get install git-crypt  # Ubuntu/Debian

# Initialize git-crypt in your repository
git-crypt init

# Specify which files to encrypt in .gitattributes
echo ".env.mcp filter=git-crypt diff=git-crypt" > .gitattributes

# Add collaborators (optional)
git-crypt add-gpg-user USER_ID

# Now you can commit .env.mcp and it will be encrypted
```

#### 2. Using Mozilla SOPS (Secrets OPerationS)

[SOPS](https://github.com/mozilla/sops) is a tool that supports multiple encryption methods:

```bash
# Install SOPS
brew install sops  # macOS

# Encrypt your .env.mcp file
sops --encrypt --pgp YOUR_PGP_KEY_FINGERPRINT .env.mcp > .env.mcp.enc

# Decrypt when needed
sops --decrypt .env.mcp.enc > .env.mcp
```

### Secure Storage Options

1. **Hardware Security Modules (HSMs)** - Physical devices for secure key storage
2. **Encrypted Databases** - Store keys in encrypted database fields
3. **Encrypted File Systems** - Store keys on encrypted partitions
4. **Key Management Services (KMS)** - Cloud provider solutions for key management

## Version Control Considerations

### Preventing Accidental Commits

1. **Add sensitive files to .gitignore**:

```
# .gitignore
.env
.env.mcp
*.pem
*.key
```

2. **Use pre-commit hooks** to scan for sensitive data:

```bash
#!/bin/bash
# pre-commit hook to check for API keys

if git diff --cached | grep -E 'API_KEY|api_key|apikey|secret|password' > /dev/null; then
  echo "WARNING: Possible API key or secret found in commit"
  echo "Please remove sensitive data and try again"
  exit 1
fi
```

3. **Use tools like GitGuardian or TruffleHog** to scan repositories

### Handling Key Rotation in Version Control

1. **Separate commits for code and configuration changes**
2. **Use descriptive commit messages** for key rotations:

```
[Security] Rotate API keys for Brave Search

- Updated key references in documentation
- Updated example configuration
- DO NOT COMMIT ACTUAL KEYS
```

## Automated Solutions

### Centralized Key Distribution System

```bash
#!/bin/bash
# update-env-keys.sh

# Configuration
API_URL="https://your-api-service.com/api-keys"
ENV_FILE_PATH="$HOME/.env.mcp"
PROJECT_PATHS=(
  "$HOME/Documents/GitHub/project1"
  "$HOME/Documents/GitHub/project2"
)

# Function to prompt for credentials if needed
authenticate() {
  echo "Authentication required"
  read -p "Username: " username
  read -sp "Password: " password
  echo
  
  # Get JWT token
  response=$(curl -s -X POST https://your-api-service.com/login \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\",\"password\":\"$password\"}")
  
  token=$(echo $response | jq -r '.token')
  if [ "$token" == "null" ]; then
    echo "Authentication failed"
    exit 1
  fi
  
  echo $token > "$HOME/.env-api-token"
  echo "Authentication successful"
}

# Check if we have a valid token
if [ ! -f "$HOME/.env-api-token" ]; then
  authenticate
else
  token=$(cat "$HOME/.env-api-token")
  # Verify token is still valid
  curl -s -X GET "$API_URL" -H "Authorization: Bearer $token" > /dev/null
  if [ $? -ne 0 ]; then
    authenticate
  fi
fi

# Get the latest API keys
token=$(cat "$HOME/.env-api-token")
keys=$(curl -s -X GET "$API_URL" -H "Authorization: Bearer $token")

# Update the main .env.mcp file
echo "# MCP Server Environment Variables - Updated $(date)" > "$ENV_FILE_PATH"
echo "$keys" | jq -r 'to_entries[] | "\(.key | ascii_upcase)_API_KEY=\(.value)"' >> "$ENV_FILE_PATH"

# Copy to all project directories
for project in "${PROJECT_PATHS[@]}"; do
  if [ -d "$project" ]; then
    cp "$ENV_FILE_PATH" "$project/.env.mcp"
    echo "Updated .env.mcp in $project"
  fi
done

echo "All .env.mcp files have been updated successfully"
```

### Symbolic Link Approach

For a simpler solution, use symbolic links to a central file:

```bash
# Create a central .env.mcp file
touch ~/.env.mcp

# Create symbolic links in each project
ln -s ~/.env.mcp /path/to/project1/.env.mcp
ln -s ~/.env.mcp /path/to/project2/.env.mcp
```

## Implementation Examples

### VS Code MCP Configuration

```json
// settings.json or .vscode/mcp.json
{
  "servers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "envFile": "~/.env.mcp"
    },
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-perplexity-ask"],
      "envFile": "~/.env.mcp"
    }
  }
}
```

### Node.js API Service for Key Management

```javascript
// server.js - A simple Express.js API server
const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const fs = require('fs');
const app = express();
app.use(express.json());

// Secret keys stored in encrypted format
let encryptedKeys = {
  'brave-search': 'encrypted-key-here',
  'perplexity': 'encrypted-key-here'
};

// Encryption/decryption functions
function encrypt(text, masterKey) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', masterKey, iv);
  const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]).toString('hex');
}

function decrypt(encryptedText, masterKey) {
  const buffer = Buffer.from(encryptedText, 'hex');
  const iv = buffer.slice(0, 16);
  const tag = buffer.slice(16, 32);
  const encrypted = buffer.slice(32);
  const decipher = crypto.createDecipheriv('aes-256-gcm', masterKey, iv);
  decipher.setAuthTag(tag);
  return decipher.update(encrypted) + decipher.final('utf8');
}

// Authentication middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).send('Access denied');
  
  try {
    const verified = jwt.verify(token, process.env.JWT_SECRET);
    req.user = verified;
    next();
  } catch (err) {
    res.status(400).send('Invalid token');
  }
};

// Login endpoint
app.post('/login', (req, res) => {
  // Validate username and password (use a secure method)
  if (req.body.username === 'admin' && req.body.password === 'secure-password') {
    const token = jwt.sign({id: 'admin'}, process.env.JWT_SECRET, {expiresIn: '1d'});
    res.json({token});
  } else {
    res.status(401).send('Invalid credentials');
  }
});

// Get all API keys
app.get('/api-keys', authenticate, (req, res) => {
  // Decrypt keys before sending
  const masterKey = Buffer.from(process.env.MASTER_KEY, 'hex');
  const decryptedKeys = {};
  
  for (const [service, encryptedKey] of Object.entries(encryptedKeys)) {
    decryptedKeys[service] = decrypt(encryptedKey, masterKey);
  }
  
  res.json(decryptedKeys);
});

// Update an API key
app.put('/api-keys/:service', authenticate, (req, res) => {
  const { service } = req.params;
  const { key } = req.body;
  
  // Encrypt the new key
  const masterKey = Buffer.from(process.env.MASTER_KEY, 'hex');
  encryptedKeys[service] = encrypt(key, masterKey);
  
  res.json({success: true});
});

// Rotate an API key (if the service supports it)
app.post('/rotate-key/:service', authenticate, async (req, res) => {
  const { service } = req.params;
  
  try {
    // Call service-specific rotation logic
    const newKey = await rotateKeyForService(service);
    
    // Encrypt and store the new key
    const masterKey = Buffer.from(process.env.MASTER_KEY, 'hex');
    encryptedKeys[service] = encrypt(newKey, masterKey);
    
    res.json({success: true, message: `Key for ${service} rotated successfully`});
  } catch (error) {
    res.status(500).json({success: false, message: error.message});
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

## Security Incident Response

### If an API Key is Compromised

1. **Immediately revoke the compromised key**
2. **Generate a new key** and update all necessary locations
3. **Investigate the breach** to understand how the key was exposed
4. **Monitor for unauthorized usage** of the compromised key
5. **Document the incident** and implement measures to prevent recurrence

### Monitoring for Exposed Keys

1. **Set up alerts** for unusual API usage patterns
2. **Use services like GitGuardian** to monitor for exposed keys
3. **Implement rate limiting** to minimize damage from key exposure
4. **Review access logs regularly** for suspicious activity

## References and Resources

### Tools

- [git-crypt](https://github.com/AGWA/git-crypt) - Transparent file encryption in git
- [SOPS](https://github.com/mozilla/sops) - Secrets management with multiple encryption methods
- [HashiCorp Vault](https://www.vaultproject.io/) - Secrets management platform
- [GitGuardian](https://www.gitguardian.com/) - Secrets detection and remediation
- [TruffleHog](https://github.com/trufflesecurity/trufflehog) - Searches for secrets in git repositories

### Best Practices Documentation

- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x00-introduction/)
- [NIST Guidelines for Managing API Keys](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204.pdf)
- [Google Cloud API Key Best Practices](https://cloud.google.com/docs/authentication/api-keys)
- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)

### Articles and Tutorials

- [The Definitive Guide to API Key Management](https://auth0.com/blog/the-definitive-guide-to-api-key-management/)
- [How to Handle API Keys in Your Projects](https://dev.to/bearer/how-to-handle-api-keys-in-your-projects-49li)
- [Secure API Key Storage for Node.js Applications](https://www.freecodecamp.org/news/how-to-securely-store-api-keys-4ff3ea19ebda/)

---

**Note**: This document should be reviewed and updated regularly as security best practices evolve. Always consult with security professionals when implementing sensitive systems.
