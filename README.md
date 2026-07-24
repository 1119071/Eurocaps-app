# Eurocaps — Raw Material \& Order Management System

A desktop application for managing raw material inventory, placing supplier orders, and generating reports, built for **Eurocaps**, a supplement manufacturer.

This was my final IT project for **Year 1 of Business IT \& Management (HBO)**. The app was built together with AI assistance (Claude), and scored a **9.8/10**.

## Features

* 🔐 **Login screen** to access the system
* 📦 **Inventory overview** — searchable table of all raw materials, with live stock/status statistics (OK vs. Low stock)
* 🛒 **Place orders** — select a material, quantity and supplier, with an optional rush-order flag; keeps an order history
* 🏭 **Supplier management** — view, edit and delete suppliers
* ✏️ **Stock updates** — adjust the current stock level of any material
* 📊 **Reports** — generate and preview an inventory or orders report, and export it as a `.txt` file



## Tech Stack

* **Python 3** (standard library only — no external packages required)
* **Tkinter** for the GUI (included with standard Python installs)
* **CSV files** as the data store (no database needed)



## Project Structure

```
Eurocapsapp\_english/
├── app.py            # main application
├── inventory.csv     # raw material stock data
├── orders.csv        # order history
├── suppliers.csv     # supplier contact data
└── README.md
```

The app locates the CSV files relative to `app.py` itself, so the whole folder can be moved, renamed, or downloaded anywhere on your computer and it will still work — as long as `app.py` and the three `.csv` files stay together in the same folder.



## Requirements

* Python 3.10 or newer
* Tkinter (bundled with Python on Windows and macOS; on Linux, install it separately if missing, e.g. `sudo apt install python3-tk`)

No `pip install` is required — the project only uses Python's standard library.



## How to Run

1. Make sure Python 3 is installed. Check with:

```
   python --version
   ```

2. Download or clone this repository.
3. Open a terminal in the project folder and run:

```
   python app.py
   ```

4. Log in with:

   * **Username:** `123`
   * **Password:** `123`

   (This is a demo login for the school project — replace it with real authentication before using this in production.)



   ## Notes

* All data is stored in plain CSV files (`inventory.csv`, `orders.csv`, `suppliers.csv`). Editing these files outside the app (e.g. in Excel) is possible, but make sure to keep them **comma-separated** and keep the header row unchanged, or the app won't be able to read them correctly.
* This project was developed as a school assignment; the login system, data storage, and error handling are intentionally simple and are not meant for production use.



  ## Acknowledgements

  This application was developed with the help of AI (Claude by Anthropic) as part of the development process, as agreed for this assignment.

