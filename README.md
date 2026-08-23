#  TravelMind AI — Intelligent Multi-Agent Trip Planning Platform

> **Voice-enabled AI trip planner powered by a multi-agent LangGraph pipeline with real-time flight, hotel, and weather data.**

---

##  Live Demo
*Deployment in progress — backend agents built, frontend coming soon*

---

##  What is TravelMind AI?

TravelMind AI is a full-stack agentic AI application that plans personalized trips end-to-end. Speak or type your travel preferences — destination, dates, budget, group size — and a multi-agent system powered by LangGraph researches real flights, hotels, weather forecasts, and attractions, then generates a detailed day-by-day itinerary with direct booking links.

**The real problem it solves:** Planning a trip involves hours of research across 10+ websites. TravelMind AI collapses this into a 60-second conversation.

---

##  Features

-  **Voice input** — speak your trip details using Web Speech API
-  **Multi-agent orchestration** — Orchestrator supervises Research, Planner, and Writer agents via LangGraph
-  **Real flight data** — live prices and schedules via SerpApi Google Flights
-  **Real hotel data** — availability and pricing via SerpApi Google Hotels
-  **Train options** — Indian Railways data via RapidAPI
-  **Weather-aware planning** — OpenWeatherMap integration with dynamic replanning if bad weather detected
-  **Day-by-day itinerary** — personalized based on budget, group size, and preferences
-  **Two-way WhatsApp** — receive itinerary on WhatsApp, reply to modify it (Twilio)
-  **Google Calendar sync** — automatically creates calendar events for each activity
-  **Long-term memory** — remembers user preferences across sessions (LangGraph MemorySaver)
-  **PDF export** — download full itinerary as PDF
-  **Budget tracker** — real-time budget breakdown with Recharts visualization
-  **Deep booking links** — pre-filled MakeMyTrip, IRCTC, Booking.com links

---

## Architecture

```
User Input (Voice / Text)
          ↓
    React Frontend
          ↓
    FastAPI Backend
          ↓
  ┌─────────────────────────────────┐
  │     LangGraph Agent Pipeline    │
  │                                 │
  │  ┌─────────────────────────┐   │
  │  │    Orchestrator Node    │   │
  │  │  (Supervisor LLM)       │   │
  │  └────────────┬────────────┘   │
  │               │ routes to      │
  │    ┌──────────┼──────────┐     │
  │    ▼          ▼          ▼     │
  │ Research   Planner    Writer   │
  │  Agent      Agent     Agent    │
  │    │          │          │     │
  │    └──────────┴──────────┘     │
  │               │ reports back   │
  │          Orchestrator          │
  └─────────────────────────────────┘
          ↓
  Integrations Layer
  WhatsApp + Google Calendar
          ↓
    React UI displays
    itinerary + booking links
```

**Orchestrator pattern:** The Orchestrator LLM supervises all three agents — evaluating output quality, routing dynamically, and retrying with specific feedback if any agent produces poor results. Maximum 2 retries per agent.

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | LangGraph |
| LLM | Groq API (llama-3.1-8b-instant) |
| Web Search | Tavily API |
| Flights + Hotels | SerpApi Google Flights / Hotels |
| Trains | RapidAPI Indian Railways |
| Weather | OpenWeatherMap API |
| WhatsApp | Twilio API (two-way webhook) |
| Calendar | Google Calendar API |
| Backend | FastAPI + Python |
| Frontend | React + Vite + Tailwind CSS |
| Charts | Recharts |
| Voice | Web Speech API |
| PDF Export | html2pdf.js |
| Deployment | Docker + Docker Compose + AWS EC2 |
| Observability | LangSmith |

---

##  Project Structure

```
travelMind-ai/
│
├── backend/
│   ├── agents/
│   │   ├── orchestrator.py    # Supervisor LLM node
│   │   ├── research.py        # Research agent node
│   │   ├── planner.py         # Planner agent node
│   │   ├── writer.py          # Writer agent node
│   │   └── graph.py           # LangGraph graph definition
│   ├── tools/
│   │   ├── weather.py         # OpenWeatherMap tool ✅
│   │   ├── search.py          # Tavily web search tool ✅
│   │   ├── flights.py         # SerpApi Google Flights tool ✅
│   │   ├── hotels.py          # SerpApi Google Hotels tool ✅
│   │   ├── trains.py          # Indian Railways tool
│   │   └── attractions.py     # Attractions + activities tool
│   ├── integrations/
│   │   ├── whatsapp.py        # Twilio two-way WhatsApp
│   │   └── calendar.py        # Google Calendar integration
│   ├── memory/
│   │   └── store.py           # LangGraph long-term memory
│   ├── main.py                # FastAPI app + endpoints
│   ├── schemas.py             # Pydantic models
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Plan.jsx       # Main planning page
│   │   │   └── Dashboard.jsx  # Trip history + stats
│   │   └── components/
│   │       ├── VoiceInput.jsx
│   │       ├── TripForm.jsx
│   │       ├── ItineraryCard.jsx
│   │       ├── FlightCard.jsx
│   │       ├── HotelCard.jsx
│   │       ├── TrainCard.jsx
│   │       └── BudgetTracker.jsx
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

##  How to Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker + Docker Compose

### 1. Clone the repository
```bash
git clone https://github.com/Siddhesh1420/TravelMind-ai.git
cd TravelMind-ai
```

### 2. Set up environment variables
Create `backend/.env`:
```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
SERPAPI_KEY=your_key
OPENWEATHERMAP_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_key
TWILIO_AUTH_TOKEN=your_key
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key
LANGCHAIN_PROJECT=travelmind-ai
```

### 3. Run with Docker
```bash
docker compose up --build
```

Open `http://localhost:3000`

### 4. Run without Docker (development)

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

##  Agent Pipeline Details

### Orchestrator (Supervisor)
LLM-powered supervisor that evaluates output quality from each agent and routes dynamically. Uses structured JSON output to decide `next_agent` and provide `feedback` when quality is poor.

### Research Agent
- Searches real flight options via SerpApi Google Flights API
- Searches hotel availability and pricing via SerpApi Google Hotels API
- Fetches 5-day weather forecast via OpenWeatherMap
- Finds train options via Indian Railways API
- Discovers attractions, restaurants, and activities via Tavily

### Planner Agent
- Reads user long-term memory for saved preferences
- Generates weather-aware day-by-day itinerary (suggests indoor activities on rainy days)
- Calculates realistic budget breakdown across all categories
- Flags budget overflow for orchestrator to handle

### Writer Agent
- Formats final itinerary as structured markdown
- Generates concise WhatsApp message summary
- Creates Google Calendar event list
- Builds pre-filled deep links for MakeMyTrip, IRCTC, and Booking.com

---

## 🔄 Current Build Status

| Component | Status |
|-----------|--------|
| Weather tool | ✅ Complete |
| Search tool | 🔄 In Progress |
| Flights tool | 🔄 In Progress |
| Hotels tool | 🔄 In Progress |
| Trains tool | 🔄 In Progress |
| Attractions tool | 🔄 In Progress |
| Research agent | ⏳ Pending |
| Planner agent | ⏳ Pending |
| Writer agent | ⏳ Pending |
| Orchestrator | ⏳ Pending |
| FastAPI backend | ⏳ Pending |
| React frontend | ⏳ Pending |
| WhatsApp integration | ⏳ Pending |
| Google Calendar | ⏳ Pending |
| Docker deployment | ⏳ Pending |

---

## Roadmap

- [x] Project architecture design
- [x] Weather tool
- [ ] All data tools (flights, hotels, trains, attractions)
- [ ] Multi-agent LangGraph pipeline
- [ ] FastAPI REST API
- [ ] React frontend with voice input
- [ ] WhatsApp two-way integration
- [ ] Google Calendar sync
- [ ] Docker + AWS EC2 deployment

---

## Author

**Siddhesh** — DSAI Student, IIT Bhilai

- GitHub: [@Siddhesh1420](https://github.com/Siddhesh1420)
- LinkedIn: [Siddhesh](https://linkedin.com/in/your-linkedin)

---

##  Disclaimer

This project is under active development. APIs used are in test/free tier mode.
