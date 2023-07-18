# OO Parking System Backend
Backend API for a parking system. Built with FastAPI.
## Requirements
Python 3.10
## How to run locally
1. Clone the repository
```
git clone https://github.com/Saliovin/OOParkingSystem.git
```
2. Change directory to the backend app
```
cd OOParkingSystem/OOParkingSystem-Backend
```
3. Install pipenv
```
pip install pipenv
```
4. Install packages
```
pipenv installo
```
5. Run DB migrations
```
pipenv run alembic upgrade head
```
6. Run the ASGI server
```
pipenv run uvicorn app.main:app --reload
```