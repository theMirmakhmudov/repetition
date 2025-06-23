import bcrypt

password = b"PDP_EDU_SECRET"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())
