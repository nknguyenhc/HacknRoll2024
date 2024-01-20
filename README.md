# parrot-germinator

Generate music parody in one step

## Development

### Backend

1. Install Python dependencies.

```
pip install -r requirements.txt
```

2. Start the development server.

```
uvicorn index:app --reload
```

3. When finished, indicate the new Python dependencies.

```
pip freeze > requirements.txt
```

WARNING: Please do not put any secrets (API key, etc) in your code!
Put secrets in a `.env` file and place the file in the root directory.
The server has been configured to load environment variables on start.

### Frontend

1. Start the backend development server (see above).

2. On a new terminal, navigate to the frontend folder.

```
cd frontend
```

3. Install the Node.js dependencies.

```
npm i
```

4. Start the React development server.

```
npm start
```
