from db.checkpointer import checkpointer


print("Checkpointer object:")
print(checkpointer)

print("\nRunning PostgreSQL setup...")

checkpointer.setup()

print("PostgreSQL checkpointer setup successful!")