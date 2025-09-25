# It's Hot - AI Coffee Shop Assistant

A sophisticated multi-agent conversational AI system for a coffee shop that handles customer inquiries, order taking, and recommendations with personality and flair.

## 🎯 Project Overview

"It's Hot" is an intelligent chatbot system designed for a coffee shop that provides:
- Natural conversation with customers
- Order management and processing  
- Menu information and recommendations
- Flirty, playful personality matching the brand
- Multi-agent architecture for specialized tasks

## 🏗️ Architecture

### Multi-Agent System
The system uses a modular multi-agent architecture where specialized agents handle different aspects of customer interaction:

```
User Input → Guard Agent → Classification Agent → Specialized Agent → Response
```

### Agent Components

#### 1. **Guard Agent** (`guard_agent.py`)
- **Purpose**: Content filtering and validation
- **Function**: Determines if user queries are appropriate for the coffee shop context
- **Output**: Allows/blocks requests and provides appropriate responses

#### 2. **Classification Agent** (`classification_agent.py`)
- **Purpose**: Route user queries to appropriate specialized agents
- **Function**: Analyzes user intent and selects the best agent to handle the request
- **Agents**: `details_agent`, `order_taking_agent`, `recommendation_agent`

#### 3. **Details Agent** (`details_agent.py`)
- **Purpose**: Handle informational queries about the coffee shop
- **Features**: 
  - RAG (Retrieval-Augmented Generation) with Pinecone vector database
  - Menu details, hours, location, ingredients
  - HuggingFace embeddings for semantic search

#### 4. **Order Taking Agent** (`order_taking_agent.py`)
- **Purpose**: Manage the complete order process
- **Features**:
  - Multi-step order workflow
  - Order validation against menu
  - Price calculation and order summary
  - Integration with recommendation agent

#### 5. **Recommendation Agent** (`recommendation_agent.py`)
- **Purpose**: Provide personalized recommendations
- **Features**:
  - Apriori algorithm for "frequently bought together" recommendations
  - Popularity-based recommendations
  - Category-specific suggestions
  - Machine learning-driven suggestions

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **LLM Integration**: OpenAI-compatible API (HuggingFace endpoints)
- **Vector Database**: Pinecone
- **Embeddings**: HuggingFace Transformers (sentence-transformers/all-MiniLM-L6-v2)
- **Data Processing**: Pandas
- **Web Framework**: Streamlit (for UI)
- **Environment Management**: python-dotenv

## 📁 Project Structure

```
project/
├── main.py                          # HuggingFace API deployment entry point
├── streamlit_app.py                 # Streamlit web interface
├── agent_controler.py               # Main orchestrator
├── development_code.py              # Local testing interface
├── agent/
│   ├── __init__.py
│   ├── agent_protocol.py            # Protocol definitions
│   ├── guard_agent.py               # Content filtering
│   ├── classification_agent.py      # Intent classification
│   ├── details_agent.py             # Information queries
│   ├── order_taking_agent.py        # Order management
│   ├── recomendation_agent.py       # ML recommendations
│   └── utils.py                     # Shared utilities
├── recommendation_objects/
│   ├── apriori_recommendations.json # Apriori rules data
│   └── popularity_recommendation.csv # Popularity data
├── requirements.txt
├── .env                            # Environment variables
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- HuggingFace account and API token
- Pinecone account and API key
- OpenAI-compatible model endpoint

### 1. Clone Repository
```bash
git clone <repository-url>
cd its-hot-coffee-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:

```env
# Model Configuration
BASE_URL=https://your-hf-endpoint.com/v1
HF_TOKEN=your_huggingface_token
MODEL_NAME=your_model_name

# Vector Database
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
```

### 4. Prepare Data Files
Ensure these files exist in `recommendation_objects/`:
- `apriori_recommendations.json` - Association rules for recommendations
- `popularity_recommendation.csv` - Product popularity data

#### CSV Format Requirements
`popularity_recommendation.csv` should contain:
```csv
product,product_category,number_of_transactions
Latte,Coffee & Espresso,150
Cappuccino,Coffee & Espresso,120
...
```

## 🎮 Usage

### Option 1: Command Line Interface
```bash
python development_code.py
```

### Option 2: Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```
Access at: `http://localhost:8501`

### Option 3: API Deployment (HuggingFace)
```bash
python main.py
```

### API Input Format
```json
{
  "input": {
    "messages": [
      {"role": "user", "content": "I would like one Latte please"}
    ]
  }
}
```

### API Response Format
```json
{
  "generated_text": "Response content",
  "role": "assistant",
  "memory": {
    "agent": "order_taking_agent",
    "step_number": 2,
    "order": [{"item": "Latte", "quantity": 1, "price": 275}]
  },
  "status": "success"
}
```

## 🏪 Menu & Pricing

### Coffee & Espresso
- Cappuccino - ₹250
- Espresso Shot - ₹150  
- Latte - ₹275
- Ouro Brasileiro Shot - ₹200

### Drinking Chocolate
- Dark Chocolate - ₹300
- Chili Mayan - ₹350

### Tea Selection
- Traditional Blend Chai - ₹180
- Serenity Green Tea - ₹200
- English Breakfast - ₹190
- Earl Grey - ₹200
- Morning Sunrise Chai - ₹180
- Peppermint - ₹180
- Lemon Grass - ₹180
- Spicy Eye Opener Chai - ₹220

### Bakery & Pastries
- Oatmeal Scone - ₹160
- Jumbo Savory Scone - ₹200
- Chocolate Chip Biscotti - ₹150
- Ginger Biscotti - ₹150
- Chocolate Croissant - ₹220
- Hazelnut Biscotti - ₹150
- Cranberry Scone - ₹180
- Scottish Cream Scone - ₹200
- Croissant - ₹180
- Almond Croissant - ₹250
- Ginger Scone - ₹180

### Flavours & Syrups
- Chocolate Syrup - ₹120
- Hazelnut Syrup - ₹120  
- Caramel Syrup - ₹130
- Sugar Free Vanilla Syrup - ₹120

## 🧠 AI Features

### Natural Language Processing
- Intent classification and routing
- Context-aware responses
- Multi-turn conversation handling
- Memory management across conversation

### Recommendation Engine
- **Apriori Algorithm**: "Customers who bought X also bought Y"
- **Popularity-Based**: Top-selling items
- **Category-Specific**: Recommendations within product categories
- **Order-Based**: Suggestions based on current order

### Personality & Tone
- Flirty, playful, and engaging personality
- Brand-consistent "It's Hot" themed responses  
- Contextual humor and wordplay
- Professional yet entertaining customer service

## 🔧 Configuration & Customization

### Adding New Menu Items
Update the menu in `order_taking_agent.py` system prompt and CSV files.

### Modifying Agent Behavior
Each agent's personality and responses are controlled via system prompts in their respective files.

### Recommendation Tuning
- Adjust `top_k` parameters in recommendation functions
- Modify confidence thresholds in apriori rules
- Update popularity weightings

### Vector Database Management
- Index management via Pinecone dashboard
- Embedding model can be changed in `utils.py`
- Namespace configuration in `details_agent.py`

## 🚀 Deployment

### HuggingFace Spaces
1. Create new Space on HuggingFace
2. Upload project files
3. Set environment variables in Space settings
4. Deploy using `main.py` as entry point

### Local Development
```bash
# Test individual components
python -m pytest tests/

# Run development interface
python development_code.py

# Launch web interface
streamlit run streamlit_app.py
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Missing Environment Variables
```
ValueError: Missing environment variables for OpenAI client
```
**Solution**: Verify all required environment variables in `.env` file

#### 2. CSV Column Errors
```
KeyError: 'number_of_transactions'
```
**Solution**: Check CSV file structure matches expected format

#### 3. Pinecone Connection Issues
```
PineconeException: Invalid API key
```
**Solution**: Verify Pinecone API key and index configuration

#### 4. Model Endpoint Issues
```
Connection error to model endpoint
```
**Solution**: Check BASE_URL and HF_TOKEN configuration

### Debug Mode
Enable debug mode in Streamlit interface or add logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Considerations

- **Response Time**: ~2-3 seconds per query (depends on model endpoint)
- **Concurrent Users**: Limited by model endpoint rate limits
- **Memory Usage**: ~500MB for full system with embeddings
- **Vector Search**: Sub-second retrieval from Pinecone

## 🔒 Security & Privacy

- API keys stored in environment variables
- No persistent user data storage (except conversation memory)
- Content filtering via Guard Agent
- Input validation and sanitization

## 🤝 Contributing

### Development Setup
1. Fork repository
2. Create feature branch
3. Install development dependencies
4. Run tests before submitting PR

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings for all functions
- Include type hints where appropriate
- Write unit tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution  
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## 👥 Team

**ASISH BAIDYA** - Lead Developer & AI Engineer
- Project Architecture & Implementation
- Multi-Agent System Design
- Machine Learning Integration

## 📞 Support

For issues and questions:
- Create GitHub issue
- Check troubleshooting section
- Review environment configuration

---

**"It's Hot" - Where AI meets the perfect cup of coffee! ☕**