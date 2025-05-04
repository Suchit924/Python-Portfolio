import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
service = Service("chromedriver")  # Path to your chromedriver

def mark_attendance():
    try:
        status_label.config(text="Launching browser...")
        root.update()

        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://your-course-platform.com/login")  # Change to your login page

        # Log in
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
        time.sleep(5)

        # Go to session page
        driver.get("https://your-course-platform.com/my-courses")  # Adjust as needed
        time.sleep(3)

        # Attempt to mark attendance
        try:
            attendance_button = driver.find_element(By.XPATH, '//button[text()="Mark Attendance"]')
            attendance_button.click()
            messagebox.showinfo("Success", "Attendance marked successfully!")
        except:
            messagebox.showinfo("Info", "No session found or already marked.")

        driver.quit()
        status_label.config(text="Done ✅")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
        status_label.config(text="Error ❌")

# Build GUI
root = tk.Tk()
root.title("Attendance Bot")
root.geometry("300x200")

title_label = tk.Label(root, text="Online Class Attendance Bot", font=("Helvetica", 14))
title_label.pack(pady=10)

mark_button = tk.Button(root, text="Mark Attendance", command=mark_attendance, font=("Helvetica", 12), bg="#4CAF50", fg="white")
mark_button.pack(pady=20)

status_label = tk.Label(root, text="Status: Idle", fg="gray")
status_label.pack(pady=5)

root.mainloop()
