# This Project has been build and tested on Linux Ubuntu 20.04



# 1 create virtual environment for developement
python3 -m venv match-maker-env

# 2 activate this environment on linux
source match-maker-env/bin/activate

# 3. Install dependencies:
    pip3 install -r requirements.txt

# 4. Create the database:
    python3 -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

    pip3 install pydantic[email]

# 5. Run the FastAPI application:
    uvicorn app.main:app --reload
# 6 Below package to run pytest
    pip3 install httpx
# 7 Run the tests:
    pytest

# 8 Open Below URL in browser to TEST API listed there

http://127.0.0.1:8000/docs#/



# 3 deactivate virtual environment after testing completed and server stopped
deactivate


![alt text](<Screenshot from 2025-03-01 15-30-40.png>)
