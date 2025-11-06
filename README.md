# Flask Inventory Application

This project is a Flask web application that connects to a MongoDB database to manage an inventory system. It features two forms: one for creating inventory items and another for recording transactions.

## Project Structure

```
flask-inventory-app
├── src
│   ├── main.py          # Entry point of the Flask application
│   ├── models.py        # Data models for inventory items and transactions
│   ├── forms.py         # Form definitions for inventory and transactions
│   ├── config.py        # Configuration settings for the application
│   └── templates
│       ├── base.html    # Base template for the application
│       └── index.html   # Main template with links to forms
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-inventory-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up your MongoDB connection string in the `.env` file:
   ```
   MONGODB_URI=<your_mongodb_connection_string>
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

## Features

- Create inventory items with details such as ID, code, product name, shelves, floors, and packs.
- Record transactions with details such as ID, date, product name, and total amount.
- User-friendly forms with validation using Flask-WTF.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.