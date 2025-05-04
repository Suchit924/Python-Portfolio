from app import create_app, db
from app.models import Product

# Create the Flask app and initialize the database
app = create_app()

# Open an application context
with app.app_context():
    def add_product(name, price, description, image):
        product = Product(name=name, price=price, description=description, image=image)
        db.session.add(product)
        db.session.commit()
        print(f"Product '{name}' added successfully!")


    def delete_product_by_name(product_name):
        product = Product.query.filter_by(name=product_name).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            print(f"Product '{product.name}' deleted successfully!")
        else:
            print(f"No product found with the name '{product_name}'.")

    while True:
        print("\nChoose an option:")
        print("1. Add a Product")
        print("2. Delete a Product")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            name = input("Enter product name: ")
            price = int(input("Enter product price (in cents): "))
            description = input("Enter product description: ")
            image = input("Enter image file path (relative to static folder): ")

            add_product(name, price, description, image)

        elif choice == '2':
            product_name = input("Enter product name to delete: ")
            delete_product_by_name(product_name)


        elif choice == '3':
            print("Exiting the script.")
            break

        else:
            print("Invalid choice. Please try again.")
