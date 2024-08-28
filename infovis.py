import matplotlib.pyplot as plt
import json

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def visualize_sales(items):
    names = [item['name'] for item in items]
    quantities = [item['quantity'] for item in items]

    plt.figure(figsize=(10, 6))
    plt.bar(names, quantities)
    plt.title('Sales by Item')
    plt.xlabel('Item Name')
    plt.ylabel('Quantity Sold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def main():
    data = load_data('sales_data.json')
    visualize_sales(data['items'])

if __name__ == "__main__":
    main()

def visual():

def load():
    
