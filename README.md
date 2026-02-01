# AxionAI

AxionAI is an intelligent recruitment platform that transforms how organizations handle hiring. By combining advanced AI models with practical automation, it streamlines everything from resume analysis to interview management while keeping human decision-makers in the loop.

## Core Features

**Smart Resume Processing**
- Automatically extracts and structures data from PDF resumes
- Converts unstructured text into searchable JSON format
- Handles various resume formats and layouts

**Intelligent Candidate Matching**
- Uses semantic search to find the best candidates for any job description
- Analyzes skills, experience, and qualifications beyond simple keyword matching
- Provides detailed summaries explaining why candidates are good fits

**Automated Interview System**
- Generates relevant technical and behavioral questions
- Evaluates candidate responses with detailed scoring and feedback
- Customizable question sets for different roles and levels

**Scheduling & Communication**
- Automatically schedules interview slots based on availability
- Sends professional email invitations to candidates
- Manages candidate data and interview logistics

## Quick Start

### Requirements
- Python 3.9 or higher
- PostgreSQL (for vector embeddings)
- MySQL (for user management)
- Google AI API access

### Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   
   Create a `.env` file with your credentials:
   ```
   GOOGLE_API_KEY=your_google_api_key
   API_KEY=your_embedding_api_key
   4b=gemma-3-4b-it
   27b=gemma-3-27b-it
   Connection_String=postgresql://user:pass@host:port/db
   Collection_Name=Resume
   Host=your_mysql_host
   Port=your_mysql_port
   User=your_mysql_user
   Password=your_mysql_password
   DB_Name=your_database_name
   app_password=your_email_app_password
   ```

3. **Set up directories**
   ```bash
   mkdir resume
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## API Reference

### Resume Management
- **POST /parse** - Process PDF resumes and create searchable embeddings
- **POST /match** - Find matching candidates for a job description

### Interview Operations  
- **POST /interview1** - Get question sets (0=behavioral, 1=technical)
- **POST /interview** - Update custom question sets
- **POST /evaluate** - Score candidate responses with AI feedback

### Scheduling
- **POST /schedule** - Create interview slots and send invitations

### Authentication
- **POST /login-user** - Candidate authentication
- **POST /login-org** - Organization authentication

## How It Works

1. **Resume Ingestion**: Place PDF resumes in the `/resume` folder. The system parses them into structured JSON with fields for experience, skills, education, and more.

2. **Vector Embeddings**: Structured resumes are converted to high-dimensional vectors using Google's embedding models and stored in PostgreSQL for fast semantic search.

3. **Job Matching**: When you input a job description, it gets analyzed and embedded. The system then finds candidates with the most similar profiles using vector similarity.

4. **Interview Management**: Generate contextual questions based on the role type. The AI evaluator scores responses and provides constructive feedback.

5. **Automated Scheduling**: Create time slots, manage candidate information, and send professional email invitations automatically.

## Architecture

```
AxionAI/
├── app.py              # Flask API server
├── Models.py           # Google AI integration
├── Parser.py           # PDF processing
├── Embedder.py         # Vector search engine
├── Evaluator.py        # Interview AI
├── Scheduler.py        # Email automation
├── DB.py              # Database management
├── requirements.txt    # Dependencies
└── resume/            # Resume storage
```

## Database Configuration

The platform uses a dual-database approach:
- **PostgreSQL**: Stores vector embeddings for semantic candidate search
- **MySQL**: Manages user accounts, scores, and scheduling information

Both databases need to be configured with the connection details in your `.env` file.

## Customization

The system is designed to be flexible:
- Modify prompts in the `.env` file to adjust AI behavior
- Update question sets through the API
- Extend the JSON schema for additional resume fields
- Integrate with existing HR systems via the REST API

## Development

Built with Flask and designed for easy deployment. The modular architecture makes it straightforward to add new features or integrate with other systems.

## License

MIT License - see LICENSE file for details.

---

*AxionAI helps you make better hiring decisions faster, without replacing human judgment.*
