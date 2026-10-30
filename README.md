# 🛒 ProcurementCopilot

### 🤖 Smarter Procurement. Faster Purchase Orders. AI-Powered Assistance.

**ProcurementCopilot** is a Python-based AI assistant designed to simplify procurement workflows by leveraging Azure OpenAI. It aims to help users streamline purchase order generation and make procurement-related tasks more efficient.

> 💡 Less manual work. Smarter workflows. Simplified procurement.

---

## ✨ Features

- 🧠 **AI-Powered Assistance** — Integrates with Azure OpenAI for intelligent text generation.
- 📄 **Purchase Order Generation** — Supports generating purchase order content.
- ⚙️ **Environment-Based Configuration** — Loads configuration securely from environment variables.
- 🔐 **Credential Safety** — Keeps API keys and sensitive configuration outside source code.
- 📋 **Dependency Management** — Uses `requirements.txt` to manage Python packages.

---

## 🏗️ Project Structure

```text
ProcurementCopilot/
│
├── procurement_copilot.py   # Main application
├── requirements.txt         # Python dependencies
├── generated_po.txt         # Generated purchase order output
├── .gitignore               # Excludes secrets and local files
├── .env                     # Local configuration (not committed)
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Azure OpenAI | AI-powered text generation |
| Semantic Kernel | AI integration and orchestration |
| python-dotenv | Loading environment variables |
| Git & GitHub | Version control and collaboration |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/amitha052003/ProcurementCopilot.git
cd ProcurementCopilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure your Azure OpenAI settings:

```dotenv
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_CHAT_DEPLOYMENT=your_chat_deployment_name
AZURE_OPENAI_API_VERSION=2024-10-21
```

Replace the example values with your actual Azure configuration.

🔒 **Security reminder:** Never commit `.env` or publish API keys. Keep `.env` listed in `.gitignore`.

### 5. Run the application

```bash
python procurement_copilot.py
```

Follow the application's prompts or output to use its available procurement features.

---

## 📂 Output

The application includes `generated_po.txt`, which can be used to store generated purchase order content, depending on the application's implementation.

Example purchase order fields might include:

- Purchase order number
- Supplier details
- Item descriptions
- Quantities and pricing
- Delivery information

*These are illustrative fields; actual output depends on the implementation.*

---

## 🔐 Security Best Practices

- Store API keys in environment variables.
- Never upload `.env` to a public repository.
- Avoid committing real supplier information or confidential purchase orders.
- Use `.gitignore` to exclude virtual environments and generated sensitive files.
- Rotate credentials immediately if they are accidentally exposed.

---

## 🗺️ Future Enhancements

- [ ] Add a user-friendly web interface.
- [ ] Support structured purchase order generation.
- [ ] Export purchase orders to PDF or Excel.
- [ ] Add input validation and error handling.
- [ ] Maintain purchase order history.
- [ ] Add automated tests.

---

## 👩‍💻 Author

**Amitha**

GitHub: [@amitha052003](https://github.com/amitha052003)

---

## ⭐ Support

If you find this project interesting, consider giving the repository a star on GitHub!

<p align="center">
  <b>Built with 🐍 Python and ☁️ Azure OpenAI</b>
</p>
