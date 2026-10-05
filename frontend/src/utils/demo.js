export const DEMO_TRIP = {
  destination: "Manali",
  from_city: "Delhi",
  start_date: "2026-10-10",
  end_date: "2026-10-15",
  budget: 25000,
  group_size: 2,
  travel_mode: "train",
  preferences: ["adventure", "budget"],
  itinerary: [
    {
      day_number: 1,
      date: "2026-10-10",
      morning: "Travel from Delhi to Chandigarh by train, then local transport to Manali.",
      afternoon: "Check-in at hotel. Explore Old Manali market.",
      evening: "Dinner at Chopsticks Restaurant.",
      estimated_cost: 4200
    },
    {
      day_number: 2,
      date: "2026-10-11",
      morning: "Walk through Deodar forests and scenic trails.",
      afternoon: "Trekking in rugged terrain around Manali.",
      evening: "Dinner at Siddu — traditional Himachali cuisine.",
      estimated_cost: 1800
    },
    {
      day_number: 3,
      date: "2026-10-12",
      morning: "Visit Manu Temple on the banks of River Beas.",
      afternoon: "Back-country snow trail exploration.",
      evening: "Dinner at XO Burger.",
      estimated_cost: 2100
    },
    {
      day_number: 4,
      date: "2026-10-13",
      morning: "Visit Hadimba Devi Temple — 15th century wooden fortress.",
      afternoon: "Sightseeing tour around Manali valley.",
      evening: "Relax at hotel. Hot chocolate by the fireplace.",
      estimated_cost: 1500
    },
    {
      day_number: 5,
      date: "2026-10-14",
      morning: "Private hiking trip — scenic mountain trail.",
      afternoon: "Biking along river routes.",
      evening: "Farewell dinner at Johnson's Cafe.",
      estimated_cost: 2200
    },
    {
      day_number: 6,
      date: "2026-10-15",
      morning: "Last-minute shopping at local market.",
      afternoon: "Train back to Delhi via Chandigarh.",
      evening: "Arrive in Delhi.",
      estimated_cost: 3800
    }
  ],
  recommended_hotel: "Nomadic Den Manali — 4.4 rated, budget-friendly at ₹305/night",
  recommended_flight_or_train: "NETAJI EXPRESS 12311 — Delhi to Chandigarh, then local bus to Manali",
  budget_breakdown: {
    transport: 4800,
    hotel: 9000,
    food: 6000,
    activities: 5200,
    total: 25000
  },
  total_estimated_cost: 25000,
  weather_data: {
    "2026-10-10": { condition: "Clear", temp: 18, min_temp: 12, max_temp: 22 },
    "2026-10-11": { condition: "Partly cloudy", temp: 16, min_temp: 10, max_temp: 20 },
    "2026-10-12": { condition: "Light rain", temp: 14, min_temp: 9, max_temp: 18 },
    "2026-10-13": { condition: "Clear", temp: 17, min_temp: 11, max_temp: 21 },
    "2026-10-14": { condition: "Clear", temp: 19, min_temp: 13, max_temp: 23 },
    "2026-10-15": { condition: "Partly cloudy", temp: 16, min_temp: 10, max_temp: 20 }
  },
  booking_links: {
    train: "https://www.irctc.co.in/nget/train-search",
    hotel: "https://www.booking.com/search.html?ss=Manali"
  },
  formatted_report: `# Manali Adventure Trip 🏔️

    ## Quick Summary
    Manali is a breathtaking hill station in Himachal Pradesh, perfect for adventure seekers and nature lovers.

    ## Day by Day Plan

    ### Day 1 - Arrival
    - Morning: Travel from Delhi to Manali by train
    - Afternoon: Check into Jain Residency, explore Old Manali
    - Evening: Dinner at Chopsticks Restaurant

    ### Day 2 - Solang Valley
    - Morning: Explore Solang Valley
    - Afternoon: Trekking and adventure activities
    - Evening: Dinner at Siddu

    ## Hotel
    Jain Residency - ₹345/night, 4.8 rating

    ## Budget
    | Category | Cost |
    |----------|------|
    | Transport | ₹4,800 |
    | Hotel | ₹9,000 |
    | Food | ₹6,000 |
    | Activities | ₹5,200 |
    | Total | ₹25,000 |
    `,
  whatsapp_message: "",
  calendar_events: [
  {
    title: "Day 1 — Manali",
    date: "2026-10-10",
    description: "Morning: Travel from Delhi to Manali\nAfternoon: Visit Hadimba Devi Temple\nEvening: Dinner at Chopsticks Restaurant"
  },
  {
    title: "Day 2 — Manali",
    date: "2026-10-11",
    description: "Morning: Explore Solang Valley\nAfternoon: Lakeside picnic\nEvening: Dinner at Siddu"
  },
  {
    title: "Day 3 — Manali",
    date: "2026-10-12",
    description: "Morning: Visit Manu Temple\nAfternoon: Old Manali exploration\nEvening: Dinner at XO Burger"
  },
  {
    title: "Day 4 — Manali",
    date: "2026-10-13",
    description: "Morning: Hadimba Temple\nAfternoon: Valley sightseeing\nEvening: Hotel dinner"
  },
  {
    title: "Day 5 — Manali",
    date: "2026-10-14",
    description: "Morning: Hiking trip\nAfternoon: River biking\nEvening: Farewell dinner at Johnson's Cafe"
  },
  {
    title: "Day 6 — Manali",
    date: "2026-10-15",
    description: "Morning: Local market shopping\nAfternoon: Return to Delhi\nEvening: Arrive Delhi"
  }
]
}

export const AGENT_STEPS = [
  {
    id: 'orchestrator_start',
    name: 'Orchestrator',
    description: 'Analyzing your trip requirements and coordinating agents',
    icon: 'O'
  },
  {
    id: 'research',
    name: 'Research Agent',
    description: 'Scanning flights, hotels, weather and destination data',
    icon: 'R'
  },
  {
    id: 'orchestrator_research',
    name: 'Orchestrator',
    description: 'Evaluating research quality and routing to planner',
    icon: 'O'
  },
  {
    id: 'planner',
    name: 'Planner Agent',
    description: 'Building your personalized day-by-day itinerary',
    icon: 'P'
  },
  {
    id: 'orchestrator_planner',
    name: 'Orchestrator',
    description: 'Evaluating itinerary quality and routing to writer',
    icon: 'O'
  },
  {
    id: 'writer',
    name: 'Writer Agent',
    description: 'Crafting your final journey document',
    icon: 'W'
  }
]