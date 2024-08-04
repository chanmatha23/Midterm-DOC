Django Installation
ตรวจสอบว่ามีการติดตั้ง Python แล้วในเครื่อง
Windows & MacOS

- Open the Command Prompt / Terminal
- Enter the command
> py --version
Results

> python --version
Python 3.9.13
สร้าง folder สำหรับใส่ project เช่น My Documents\Projects\week-2

เข้าไปที่ folder

Setup a virtual environment

Windows

# Install virtualenv
> pip install virtualenv

# Create a virtual environment
> py -m venv myvenv

# Activate virtual environment
> myvenv\Scripts\activate.bat
MacOS

# Install virtualenv
> pip install virtualenv

# Create a virtual environment
> python -m venv myvenv

# Activate virtual environment
> source myvenv/bin/activate
เมื่อทำเสร็จคุณจะเห็นว่ามี folder myvenv เพิ่มขึ้นมา

Install Django
Windows & MacOS

> pip install django
ตรวจสอบว่า install สำเร็จหรือไม่ด้วย command

> python -m django --version
4.2.13

