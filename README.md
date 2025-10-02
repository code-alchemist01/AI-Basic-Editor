# 🤖 AI Basic Editor

Expert-level code writing assistant! Write professional code using the power of Gemini AI with a modern Streamlit-based interface.

## ✨ Features

- 🎨 **Modern Streamlit Interface**: Gradient colors and responsive design
- 🔗 **Gemini API Integration**: Google's most advanced AI model
- 📊 **PostgreSQL Database**: Chat history and knowledge storage
- 🤖 **Expert Code Editor**: Professional code writing with customized AI prompts
- 💬 **Real-time Chat**: Message history and cleanup features
- 🔧 **Easy Setup**: Run with a single command

## 🚀 Quick Start

### 1. Clone the Project
```bash
git clone https://github.com/code-alchemist01/AI-Basic-Editor.git
cd AI-Basic-Editor
```

### 2. Setup Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Edit .env file and add your credentials
```

### 3. Run the Application
```bash
python run.py
```

The application will automatically install required packages and start at `http://localhost:8501`.

## ⚙️ Configuration

### .env File
Set the following variables in your `.env` file:

```env
# PostgreSQL Database URL
DATABASE_URL=postgresql://username:password@localhost:5432/ai_editor

# Gemini API Key (https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here

# Gemini Model
GEMINI_MODEL=gemini-2.0-flash
```

### Supported Models
- `gemini-2.0-flash` (Recommended - Fast and powerful)
- `gemini-1.5-pro` (Most advanced model)
- `gemini-1.5-flash` (Quick response)

## 📋 Usage Examples

### Web Development
```
"Create a responsive navbar component with React"
"Write REST API with Node.js Express"
"Design modern layout with CSS Grid"
```

### Python Development
```
"Write a blog application with Python Flask"
"Create data analysis script with Pandas"
"Write async web service with FastAPI"
```

### Database
```
"Optimize PostgreSQL performance"
"Write MongoDB aggregation pipeline"
"Create SQL injection protected queries"
```

### DevOps
```
"Write Docker multi-stage build file"
"Create Kubernetes deployment yaml"
"Write CI/CD pipeline with GitHub Actions"
```
<img width="1890" height="822" alt="Ekran görüntüsü 2025-10-02 235629" src="https://github.com/user-attachments/assets/c2eb7233-24db-4b48-a49e-bb328aa1558e" />
<img width="1895" height="892" alt="Ekran görüntüsü 2025-10-02 224708" src="https://github.com/user-attachments/assets/df8107bc-f8cd-41cb-b8ce-bfaca5069977" />
<img width="1891" height="910" alt="Ekran görüntüsü 2025-10-02 224716" src="https://github.com/user-attachments/assets/63867e47-82fd-4436-b3b4-a710dd46f948" />
<img width="1887" height="886" alt="Ekran görüntüsü 2025-10-02 235721" src="https://github.com/user-attachments/assets/d48611bf-6574-4ff1-8e6a-b1d496642934" />
<img width="1873" height="885" alt="Ekran görüntüsü 2025-10-02 235812" src="https://github.com/user-attachments/assets/048c5f0e-dde9-4061-89a0-54bf95a46d63" />
<img width="1869" height="914" alt="Ekran görüntüsü 2025-10-02 224813" src="https://github.com/user-attachments/assets/e58b972d-9488-41e5-ac38-3f273b498812" />
<img width="1857" height="881" alt="Ekran görüntüsü 2025-10-02 224801" src="https://github.com/user-attachments/assets/e50146cf-e5c3-464f-8fe7-e68db2a3107a" />



## 🛠️ Development

### Project Structure
```
AI-Basic-Editor/
├── app.py              # Main Streamlit application
├── database.py         # PostgreSQL database management
├── gemini_client.py    # Gemini API integration
├── run.py             # Run script
├── requirements.txt   # Python dependencies
├── database_schema.sql # Database schema
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore file
└── README.md          # This file
```

### Manual Installation
```bash
# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start the application
streamlit run app.py
```

## 🔒 Security

- ✅ API keys are securely stored in `.env` file
- ✅ `.env` file is excluded from Git via `.gitignore`
- ✅ Manual API key input for secure usage
- ✅ Database connections are managed securely

## 📦 Dependencies

- `streamlit` - Web interface
- `psycopg2-binary` - PostgreSQL connection
- `google-generativeai` - Gemini API
- `python-dotenv` - Environment variables
- `sqlalchemy` - ORM

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter issues:

1. Make sure your `.env` file is properly configured
2. Check that PostgreSQL database is running
3. Verify your Gemini API key is valid
4. Check terminal for error messages

## 🎯 Future Features

- [ ] Code syntax highlighting
- [ ] File upload/download
- [ ] Theme options
- [ ] Multi-language support
- [ ] Plugin system
- [ ] Code versioning
