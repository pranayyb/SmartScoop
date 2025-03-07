# SmartScoop - AI Shopping Assistant

A sophisticated shopping assistant that leverages AI to provide personalized shopping experiences, powered by LangChain and various machine learning components.

## Features

### Core Shopping Features

- Multi-platform product search (Amazon, eBay)
- Personalized product recommendations
- Budget management
- Seasonal shopping optimization

### Technical Features

- Asynchronous operations for better performance
- Persistent storage with SQLite
- LangChain integration for natural language processing
- Modular and extensible architecture
- Comprehensive error handling and logging

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Required API Keys

You'll need the following API keys:

- Amazon Product API
- eBay API
- Groq API

### Installation

1. Clone the repository:

```bash
git clone https://github.com/pranayyb/SmartScoop.git
cd SmartScoop
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
DB_NAME=shopping_assistant.db
AMAZON_API_KEY=your_amazon_api_key
EBAY_API_KEY=your_ebay_api_key
GROQ_API_KEY=your_openai_api_key
```

### Running the Application

```bash
python main.py
```

## API Endpoints

### Chat with Shopping Assistant

**Endpoint:**  
`POST /chat`

**Description:**  
Send a message to the shopping assistant and receive a response.

**Request Body:**

```json
{
  "user_id": "string",
  "message": "string"
}
```

**Response:**

```json
{
  "response": "string"
}
```

**Example Request:**

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": "12345",
           "message": "Find me the best budget smartphones."
         }'
```

**Example Response:**

```json
{
  "response": "Here are some budget smartphones available on Amazon..."
}
```

**Error Response:**

- `500 Internal Server Error`: If there is an issue processing the request.

## Usage Examples

### Basic Product Search

```python
async def search_products():
    app = ShoppingAssistantApp(config)
    response = await app.handle_message(
        user_id="user123",
        message="Find me a gaming laptop under $1500"
    )
    print(response)
```

## Project Structure

```
SmartScoop/
├── main.py                         # Main application file
├── requirements.txt                # Project dependencies
├── .env                            # Environment variables
├── README.md                       # Project documentation
├── .gitignore                      # Git-Ignore files
├── shopping_assistant.db
├── table_data/
    ├── data.py
    ├── users.csv                   # csv containing user information
    ├── seasonal_discounts.csv      # csv containing discount in the table
└── SmartScoop/
    ├── __init__.py
    ├── database.py                 # Database management
    ├── product_search.py           # Product search implementations
    ├── recommendation.py           # Recommendation engine
    ├── user_profile.py             # User profile management
    ├── agent.py                    # Agent management
    ├── seasonal_discount.py        # Seasonal discount
    └── app.py                      # Application
```

## Configuration

The application can be configured through environment variables or a configuration file. Key configuration options include:

- `DB_NAME`: Database file name
- `AMAZON_API_KEY`: Amazon Product API key
- `EBAY_API_KEY`: eBay API key
- `GROQ_API_KEY`: OpenAI API key

## Security

- All API keys are stored securely in environment variables
- User data is encrypted at rest
- Regular security updates and dependency scanning
- Input validation and sanitization
- Rate limiting on API endpoints

## Future Enhancements

- Integration with more e-commerce platforms
- Enhanced AR capabilities for virtual try-on
- Machine learning-based price prediction
- Social media integration
- Mobile application support
- Real-time chat support
- Voice command integration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Pranay Buradkar

## Acknowledgments

- GROQ for GPT models
- LangChain community
- Contributors and testers

## Support

For support, please:

1. Check the documentation
2. Search existing issues
3. Open a new issue if needed
