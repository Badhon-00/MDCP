# security.md: cryptography standards

Use vetted libraries. Never invent a cipher, mode or key format.

- Passwords: Argon2id (`argon2` package), per-hash salt, tune cost to ~250ms on the server. Optional server-side pepper from env.
- Encryption at rest: AES-256-GCM, random 12-byte IV per message, never reuse an IV with a key. See crypto-vault.md.
- Signing: HMAC-SHA256 or Ed25519. Compare with `timingSafeEqual`.
- Tokens: random 32 bytes from `crypto.randomBytes`; store only a hash server-side.
- JWT: pin the algorithm, check `exp`, `iss`, `aud`. Short access token, rotating refresh token in an httpOnly, Secure, SameSite cookie.
- Keys: in a secret manager or env, never in the repo. Support rotation by storing a key ID with each ciphertext.
- TLS 1.2+ everywhere; HSTS on.
