# crypto-vault.md

AES-256-GCM with Node's built-in crypto. `key` is a 32-byte Buffer from env or a secret manager.

```ts
import { randomBytes, createCipheriv, createDecipheriv } from 'node:crypto'

export function encrypt(key: Buffer, plaintext: string): string {
  const iv = randomBytes(12)
  const c = createCipheriv('aes-256-gcm', key, iv)
  const ct = Buffer.concat([c.update(plaintext, 'utf8'), c.final()])
  return Buffer.concat([iv, c.getAuthTag(), ct]).toString('base64')
}

export function decrypt(key: Buffer, b64: string): string {
  const b = Buffer.from(b64, 'base64')
  const d = createDecipheriv('aes-256-gcm', key, b.subarray(0, 12))
  d.setAuthTag(b.subarray(12, 28))
  return Buffer.concat([d.update(b.subarray(28)), d.final()]).toString('utf8')
}
```

Password hashing:

```ts
import argon2 from 'argon2'
const hash = await argon2.hash(password, { type: argon2.argon2id })
const ok = await argon2.verify(hash, password)
```

Rotation: prefix each ciphertext with a key ID and keep old keys for decrypt only. Add a unit test that round-trips and that a tampered ciphertext throws.
