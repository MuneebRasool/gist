## Features

- 🚀 FastAPI for high-performance API development
- 🗃️ Tortoise ORM for async database operations
- 🔒 Built-in user authentication module
- 🎯 Modular project structure
- ⚡ Comprehensive error handling
- 📝 Automatic API documentatio─ config/             # Configuration settings
│   ├── __init__.py
│   └── settings.py     # Environment and app settings
├── exceptions/         # Global exception handling
│   ├── __init__.py
│   ├── database.py    # Database-specific exceptions
│   └── handlers.py    # Global exception handlers
├── models/            # Database models
│   ├── __init__.py
│   └── user.py       # User model definition
├── modules/          # Feature modules
│   └── auth/        # Authentication module
│       ├── constants.py    # Module constants
│       ├── dependencies.py # Route dependencies
│       ├── exceptions.py   # Module-specific exceptions
│       ├── router.py      # API routes
│       ├── schemas.py     # Pydantic models
│       ├── service.py     # Business logic
│       └── utils.py       # Helper functions
└── utils/           # Shared utilities
    └── common.py    # Common utility functions
```

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv sync
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
aerich init -t src.config.settings.TORTOISE_ORM
aerich init-db
```
- For new Migrations:
```bash
aerich migrate
aerich upgrade
```
6. Run the development server:
```bash
fastapi dev
```

## Development Strategies

### Adding New Features

1. Create a new module in `src/modules/`:
```
modules/
└── new_feature/
    ├── constants.py    # Module-specific constants
    ├── dependencies.py # Route dependencies
    ├── exceptions.py   # Module-specific exceptions
    ├── router.py      # API routes
    ├── schemas.py     # Pydantic models
    ├── service.py     # Business logic
    └── utils.py       # Helper functions
```

2. Add models in `src/models/` if needed
3. Register the router in `main.py`
4. Add tests in `tests/` directory

### Error Handling Strategy

- Use custom exceptions for specific error cases
- Global exception handlers ensure consistent error responses
- Database errors are automatically handled and formatted
- HTTP status codes convey the response status

### Database Operations

- Use Tortoise ORM models for database operations
- Keep database operations in service layers
- Use transactions for complex operations
- Migrations are handled by aerich

### API Response Format

#### Success Responses
- Return data directly
- HTTP status codes indicate success

#### Error Responses
```json
{
    "message": "Error description",
    "data": {
        "detail": "Additional error details"
    }
}
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:
```bash
pytest
```

## Contributing

1. Create a new branch for your feature
2. Follow the existing code structure
3. Add tests for new features
4. Update documentation as needed
5. Submit a pull request
