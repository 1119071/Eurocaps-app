# Eurocaps — Raw Material & Order Management System

A Python-based desktop application for managing raw material inventory, supplier orders, stock updates, and business reports.

This project was developed as my final Year 1 Business IT & Management project at Rotterdam University of Applied Sciences, based on a real-world business scenario involving Eurocaps, a supplement manufacturer.

**Final grade: 9.8/10**

**Python | Tkinter | CSV | Desktop Application | Business Process Improvement**

## Application Preview

![Eurocaps Inventory Management System](Eurocaps%20app%20inventory%20screen.png)

## Overview

The Eurocaps Inventory & Order Management System is a desktop application designed to support business operations related to raw material inventory and supplier orders.

The application provides functionality for:

- Managing raw material inventory
- Monitoring stock levels and stock status
- Placing and tracking supplier orders
- Managing supplier information
- Updating inventory levels
- Generating inventory and order reports
- Exporting reports as `.txt` files

The project combines software development with practical business process improvement, focusing on creating a simple and accessible solution for managing operational data.

## Features

### 🔐 Login System

A login screen provides access to the application.

> **Demo credentials**
>
> Username: `123`  
> Password: `123`

The login system is intended for demonstration purposes and is not designed as a production-ready authentication system.

### 📦 Inventory Management

- View all raw materials in a searchable inventory table
- Monitor current stock levels
- View stock status statistics
- Identify materials with low stock levels

### 🛒 Supplier Orders

- Select a raw material
- Specify the required quantity
- Select a supplier
- Mark orders as rush orders when necessary
- Maintain an order history

### 🏭 Supplier Management

- View supplier information
- Edit supplier details
- Delete suppliers

### ✏️ Stock Updates

- Update the current stock level of raw materials
- Keep inventory information up to date

### 📊 Reports

- Generate inventory reports
- Generate order reports
- Preview generated reports
- Export reports as `.txt` files

## Tech Stack

- **Python 3** — Application development and business logic
- **Tkinter** — Graphical user interface
- **CSV** — Data storage
- **Python Standard Library** — No external packages required

## Project Structure

```text
Eurocaps-app/
│
├── app.py
├── inventory.csv
├── orders.csv
├── suppliers.csv
├── Eurocaps app inventory screen.png
├── README.md
├── LICENSE
└── .gitignore
```

### Files

| File | Purpose |
|---|---|
| `app.py` | Main application containing the user interface and application logic |
| `inventory.csv` | Stores raw material inventory data |
| `orders.csv` | Stores supplier order history |
| `suppliers.csv` | Stores supplier information |
| `Eurocaps app inventory screen.png` | Screenshot showing the application interface |
| `README.md` | Project documentation |
| `LICENSE` | Project license |

The application locates the CSV files relative to `app.py`. This allows the complete project folder to be moved or renamed while maintaining functionality, as long as `app.py` and the three CSV files remain together.

## Requirements

- Python 3.10 or newer
- Tkinter

Tkinter is included with standard Python installations on Windows and macOS. On Linux, Tkinter may need to be installed separately.

No external Python packages are required.

## How to Run

### 1. Install Python

Make sure Python 3.10 or newer is installed.

Check your Python version with:

```bash
python --version
```

### 2. Download or Clone the Repository

Download the repository or clone it using Git:

```bash
git clone https://github.com/1119071/Eurocaps-app.git
```

Navigate to the project directory:

```bash
cd Eurocaps-app
```

### 3. Run the Application

Start the application with:

```bash
python app.py
```

### 4. Log In

Use the following demo credentials:

```text
Username: 123
Password: 123
```

## Data Storage

The application stores its data in three CSV files:

- `inventory.csv` — Raw material inventory
- `orders.csv` — Supplier order history
- `suppliers.csv` — Supplier information

The CSV files can be edited externally using applications such as Microsoft Excel. However, the comma-separated format and header rows should be preserved to ensure the application continues to read the data correctly.

## Project Context

This project was developed as my final Year 1 project for the Bachelor of Business IT & Management at Rotterdam University of Applied Sciences.

The project focuses on applying programming and information technology to a practical business scenario. The application combines a graphical user interface, data management, business logic, and operational process support.

The project received a final grade of **9.8/10**.

## Limitations

This project was developed as an educational project and is not intended for production use without further development.

Known limitations include:

- The login system uses a simple demo username and password
- Data is stored in CSV files rather than a database
- Authentication is not connected to a secure user management system
- Error handling and data validation are intentionally simple
- The application would require additional security and infrastructure for production use

These limitations were considered appropriate for the scope of the Year 1 project.

## AI Usage

AI tools were used as part of the development process, primarily to support coding, problem-solving, and clarification during development.

The application was developed with AI assistance using Claude by Anthropic. The use of AI was permitted as part of the project assignment.

The final application, implementation decisions, testing, and project documentation were reviewed and developed as part of the project work.

## License

This project is shared for portfolio and educational purposes under the MIT License.
