from argon2 import PasswordHasher

ph = PasswordHasher()

new_password = "priyansh"
new_hash = ph.hash(new_password)

print(new_hash)