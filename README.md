# Prompt Engineering Web Application

This is a proof of concept web application designed to help users create, improve, and refine their prompts for AI models. The application provides a user-friendly interface for structuring prompts with key components such as goals, format requirements, warnings, and context.

## Features

- Interactive web interface built with Streamlit
- Prompt structure guidance with separate sections for different components
- AI-powered prompt enhancement using Groq API
- Clean, modern UI with intuitive controls

## Prerequisites

- Python 3.12 or higher
- Groq API key (set in `.env` file)

## Installation

### Setting up a Virtual Environment

#### Linux/macOS

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install -U pip
```

#### Windows

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Upgrade pip
pip install -U pip
```

### Installing Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

## Configuration

To configure the application, create a `.env` file in the root directory and set the following environment variables:

- **GROQ_API_KEY**: Your Groq API key for accessing the Groq API.
- **DEBUG**: Set to `True` for development mode or `False` for production mode.
- **ADMIN_USERNAME**: Username for the admin user (optional).
- **ADMIN_PASSWORD**: Password for the admin user (optional).

Example:

```
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin_password
```

## Running the Application

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Deployment with Coolify

This application can be deployed using Coolify, a self-hostable PaaS solution:

1. Set up a Coolify server or use an existing one
2. Create a new service in Coolify
3. Connect your repository or upload the code
4. Configure the build settings:
   - Use the included Dockerfile
   - Set environment variables (GROQ_API_KEY)
5. Deploy the application

## Project Structure

```
├── app.py              # Main Streamlit application
├── groq_ai.py          # Groq API integration
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── TODO.md             # Development tasks and roadmap
├── sanitize.py         # Data sanitization utilities
└── .env                # Environment variables (not tracked in git)
```

## Best Practices

This project follows these Python best practices:

- Environment variables for sensitive information
- Virtual environment for dependency isolation
- Requirements file with pinned versions
- Clean code structure with separation of concerns
- Proper error handling and input validation
- Docker containerization for consistent deployment

## Image

![Project Structure](https://i.imgur.com/xFxQmgD.png)

## License

This project is open source and available for educational and personal use.

## Contributing

As this is a proof of concept, contributions are welcome to enhance functionality and usability.