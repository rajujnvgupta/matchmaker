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

# 3 deactivate virtual environment after testing completed and server stopped
deactivate
