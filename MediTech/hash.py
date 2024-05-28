from hashlib import sha256

password = "admin123"
hashed_password = sha256(password.encode()).hexdigest()
print(hashed_password)
