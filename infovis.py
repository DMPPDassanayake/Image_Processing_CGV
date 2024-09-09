import matplotlib.pyplot as plt
import json

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def visualize_sales(items):
    names = [item['name'] for item in items]
    quantities = [item['quantity'] for item in items]

    max_quantity = max(quantities)

    plt.figure(figsize=(10, 6))
    for name, quantity in zip(names, quantities):  # Fixed indentation here
        if quantity == max_quantity:
            plt.bar(name, quantity, color='r')  # red color for the highest quantity
        else:
            plt.bar(name, quantity, color='b')  # blue color for the rest
    plt.title('Sales by Item')
    plt.xlabel('Name of Item')
    plt.ylabel('Quantity Sold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def main():
    data = load_data('sales_data.json')
    visualize_sales(data['items'])

if __name__ == "__main__":
    main()