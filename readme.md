# Casino

It is a fake casino game with games like crash, coinflip, roulette and others. 

*Features*: 
- Backend: Django Rest Framework
- Frontend: ...
- Database: PostgreSQL or sqlite3

## Installation

### 1. Clone the Repository
```bash
https://github.com/aldick/casino.git
cd casino
```

### 2. Configure Environment Variables
Create a `.env` file in the project root and add the following:
```env
SECRET_KEY=your-django-secret-key
DJANGO_ENV=prod

DATABASE_DB=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

### 3. Run Server Using Docker Compose
- Developer server
  ```bash
  docker-compose up -d --build
  ```

- Production server
  ```bash
  docker-compose -f docker-compose.prod.yml up -d --build
  ```

The application will be available at `http://127.0.0.1:8000`.

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a pull request