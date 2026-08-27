from db.models import Base, engine


print("Creating application tables...")


Base.metadata.create_all(
    bind=engine
)


print("Application tables created successfully!")