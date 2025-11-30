# ai-startup-validator - Startup Idea Validation Tool

A comprehensive AI-powered platform that validates startup ideas through intelligent market analysis, competitor research, risk assessment, and strategic advice. Built with FastAPI backend and Streamlit frontend, ai-startup-validator uses LangGraph workflows and advanced language models to provide data-driven insights for entrepreneurs.

## Features

- **AI-Powered Market Analysis**: Deep market insights using a Hugging Face endpoint model (configurable; default `openai/gpt-oss-120b`)
- **Competitive Intelligence**: Automated competitor research and positioning analysis  
- **Risk Assessment**: Multi-dimensional risk evaluation across market, technical, operational, regulatory, and financial factors
- **Strategic Advisory**: Go/No-Go recommendations with actionable next steps
- **Web Search Integration**: Real-time market data via DuckDuckGo, invoked through a tool-enabled flow with robust fallbacks
- **Workflow Orchestration**: LangGraph-powered, tools-first agent coordination with automatic fallbacks
- **User-Friendly Interface**: Clean Streamlit web interface for easy interaction

##  Architecture

ai-startup-validator follows a modular microservices architecture with clear separation of concerns:

```
├── main.py                     # FastAPI backend server
├── app.py                      # Streamlit frontend application
├── config.py                   # Configuration and model parameters
├── graphs/
│   └── workflow.py            # LangGraph workflow orchestration
├── nodes/                     # Analysis agents
│   ├── market_analyst.py      # Market analysis agent
│   ├── competitor_analysis.py # Competitor research agent
│   ├── risk_assessor.py       # Risk assessment agent
│   └── advisor.py             # Strategic advisor agent
├── state/
│   └── agent_state.py         # Shared state management
├── models/
│   └── chat_model.py          # Hugging Face model configuration
├── tools/
│   └── web_search_tool.py     # DuckDuckGo search integration
└── prompts/                   # Agent-specific prompts
    ├── market_analyst.txt
    ├── competitor_analyst_prompt.txt
    ├── risk_assessor.txt
    └── advisor.txt
```

## Prerequisites

- **Python 3.11+**
- **Hugging Face API Token** (for the configured Hugging Face endpoint model)
- **Internet connection** for web search functionality

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/TAK1EDD1NE/ai-startup-validator.git
cd ai-startup-validator
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here
```

**To obtain a Hugging Face API token:**
1. Visit [Hugging Face](https://huggingface.co/)
2. Create an account or log in
3. Navigate to Settings → Access Tokens
4. Create a new token with appropriate permissions

## Usage

ai-startup-validator requires running both the backend API and frontend interface:

### Method 1: Manual Startup (Recommended for Development)

**Terminal 1 - Start the FastAPI Backend:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start the Streamlit Frontend:**
```bash
streamlit run app.py
```

### Method 2: Production Deployment
```bash
# Backend (production mode)
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (in separate terminal)
streamlit run app.py --server.port 8501
```

### 3. Access the Application
- **Frontend Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000

### 4. Validate Your Startup Idea
1. Open the Streamlit interface in your browser
2. Enter your startup idea in the text area
3. Click "Validate" to initiate the analysis
4. Review the comprehensive validation report including:
   - Market analysis and opportunities
   - Competitive landscape assessment
   - Risk evaluation and mitigation strategies  
   - Strategic recommendations and next steps

## Configuration

Customize the analysis behavior in `config.py`:

```python
# Model Configuration
REPO_ID = "openai/gpt-oss-120b"  # Language model
TEMPERATURE = 0.7                          # Response creativity (0-1)
MAX_NEW_TOKENS = 512                      # Maximum response length

# API Configuration  
BASE_URL = "http://localhost:8000/"       # Backend API endpoint
```
## Testing 
This project includes comprehensive test suites for both the frontend (Streamlit) and backend (FastAPI) components to ensure code quality and reliability.
Prerequisites
Before running tests, ensure you have the following dependencies installed:
## Running Tests
### Run All Tests
To run all tests in the project:
```bash
pytest
```
Run Frontend Tests Only
```bash
pytest test_frontend.py -v
```
Run Backend Tests Only
```bash
pytest test_backend.py -v
```


## Test Coverage
Generate Coverage Report
```bash
pytest --cov=. --cov-report=html
```

## How It Works

ai-startup-validator employs a sophisticated multi-agent workflow:

1. **Input Processing**: User submits startup idea through Streamlit interface
2. **Tools‑First Analysis Nodes**: Each analysis node (market, competition, risk) runs in tools mode by default and may emit a tool call (DuckDuckGo) when needed
3. **Tool Execution and Routing**: Tool calls are routed through a central tools node; results are fed back into the calling node
4. **Automatic Fallbacks**: If a tool fails, the router diverts execution to a chat‑only fallback node to complete that step without tools
5. **Strategic Advisory**: Final advisor aggregates prior results and returns decision plus rationale
6. **Report Generation**: Consolidated validation report is returned to the frontend

Each agent leverages web search capabilities and specialized prompts to ensure thorough, data-driven analysis.

### New Flow Strategy (Tools‑First with Fallbacks)

- **Dynamic routing**: A custom router advances through `ANALYSIS_LIST` and determines the next node based on tool outcomes.
- **Tool node**: When a model response contains a tool call, execution is routed to a shared tools node and then resumed.
- **Fallback nodes**: On tool failure, execution skips to a chat‑only fallback for the current analysis step to ensure progress.

## Dependencies

### Core Framework
- **FastAPI**: High-performance API backend
- **Streamlit**: Interactive web frontend
- **LangGraph**: Workflow orchestration
- **LangChain Community**: Agent tools and integrations

### Search & Data
- **duckduckgo-search**: Web search functionality
- **Pydantic**: Data validation and parsing

## API Endpoints

### POST /validate
Validates a startup idea through comprehensive analysis.

**Request Body:**
```json
{
  "startup_idea": "Your startup idea description"
}
```

**Response:**
```json
{
  "startup_idea": "Original idea",
  "market_analysis": "Market insights and opportunities",
  "competition_analysis": "Competitive landscape assessment", 
  "risk_assessment": "Risk factors and mitigation strategies",
  "advisor_recommendations": "Go/No-Go/Conditional Go",
  "advice": "Strategic recommendations and next steps"
}
```

## Limitations & Considerations

- **API Dependencies**: Relies on Hugging Face and DuckDuckGo services
- **Rate Limits**: Free tier API usage may have limitations
- **Search Quality**: Analysis quality depends on available web content
- **Response Time**: Initial model loading may cause delays
- **Data Privacy**: Ensure sensitive business ideas are handled appropriately

## Troubleshooting

### Common Issues

**"Unable to connect to the ai-startup-validator API"**
- Ensure FastAPI backend is running on port 8000
- Check firewall settings and port availability
- Verify BASE_URL configuration in config.py

**"Authentication Error" with Hugging Face**
- Verify HUGGINGFACEHUB_API_TOKEN in .env file
- Ensure token has appropriate model access permissions
- Check token validity on Hugging Face platform

**Slow Response Times**
- Free tier models may have longer loading times
- Consider upgrading to paid Hugging Face plan
- Monitor network connectivity for web search operations

**No Search Results**
- Verify internet connectivity
- Try alternative keyword variations
- Check DuckDuckGo service availability

### Debug Mode
Monitor console output from both FastAPI and Streamlit terminals for detailed error logging and agent decision tracking.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **[LangGraph](https://langchain-ai.github.io/langgraph/)** for workflow orchestration
- **[Hugging Face](https://huggingface.co/)** for language model infrastructure
- **[FastAPI](https://fastapi.tiangolo.com/)** for high-performance API framework
- **[Streamlit](https://streamlit.io/)** for rapid frontend development
- **[DuckDuckGo](https://duckduckgo.com/)** for privacy-focused search functionality

## Future Enhancements

- [ ] **Multi-Company Analysis**: Batch validation of multiple startup ideas
- [ ] **Sentiment Analysis**: Market sentiment tracking and analysis
- [ ] **Financial Modeling**: Revenue projections and funding recommendations
- [ ] **Industry Templates**: Specialized validation frameworks by sector
- [ ] **Export Functionality**: PDF/Word report generation
- [ ] **Collaboration Features**: Team-based validation workflows
- [ ] **Historical Tracking**: Progress monitoring and idea evolution
- [ ] **Integration APIs**: Connect with business planning tools
- [ ] **Advanced Visualizations**: Interactive charts and market maps
- [ ] **Localization**: Multi-language support for global markets

---

**Ready to validate your next big idea?** 

For support, feature requests, or contributions, please visit our [GitHub Issues](../../issues) page.