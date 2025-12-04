# Astrological Insight Generator
Build a service that takes a user's birth details (name, date, time, and location of birth) and returns a personalized daily astrological insight, using a combination of zodiac logic and LLM-based language generation.

## ⚛️ Horoscope Generation Service Architecture

The system is structured as a pipeline with three major layers: **Interface**, **Intelligence (Core Logic & Context Retrieval)**, and **Generation**.

---

### 1. 🌐 The Interface Layer (FastAPI & Caching)

This layer handles the request lifecycle, input validation, and initial caching strategy to ensure speed and reliability.

* **User/Client:** Initiates the process by sending a **POST request** containing user data (like date of birth) to the API.
* **FastAPI Entrypoint (`/predict`):** The primary entry point for the service.
    * **Validator:** The first point of logic. It checks if the input data is valid.
        * **No:** Returns an **Error Response** to the client.
        * **Yes:** Proceeds to the cache check.
    * **Cache Check (Redis Cache):** Immediately checks the high-speed **Redis Cache** (or an equivalent in-memory store) for a result for the exact same user/date combination.
        * **Cache Hit:** Directly returns the stored **JSON Response** to the User, bypassing the entire intelligence and generation pipeline.
        * **Cache Miss:** Proceeds to the Core Logic Layer.

---

### 2. 🧠 The Intelligence Layer (Core Logic & Context Retrieval)

This layer executes the necessary business logic to gather all inputs required for the LLM prompt.

#### A. Core Logic
* **Zodiac Engine:** Takes the date from the input and calculates the precise **Astrological Sign** (e.g., **Leo**).

#### B. Context & Retrieval (RAG)
The calculated Sign is used to **parallelize** the retrieval of contextual data:
* **Context Retriever:** Uses the calculated Sign (e.g., 'Leo') to query the **Vector Store / Knowledge Base (KB)**.
    * **Vector Store:** Returns relevant astrological context (e.g., specific **Planetary Alignment** rules) needed for the prediction.
* **User Profile DB:** The Sign is also used to fetch **User Preferences** (e.g., "User prefers career advice," language setting) from the User Profile Database.

---

### 3. ✨ The Generation Layer (Prompting & Output)

This final layer aggregates the context, generates the insight, and prepares the final output, including translation and final caching.

* **Prompt Builder:** Aggregates the three main components into a single, comprehensive **Complete Prompt**:
    1.  Calculated **Sign**.
    2.  Retrieved **Context** (Planetary Alignment).
    3.  **User Preferences** (Personalization).
* **LLM (Large Language Model):** Receives the Complete Prompt and generates the **Raw Insight** (the horoscope prediction text).
* **Translator Service:** Receives the Raw Insight and applies **multilingual support**. If the user's preferred language (e.g., Hindi) is set, it translates the text into the **Final Text**.
* **Final API Handling:**
    1.  The **Final Text** is saved back into the **Redis Cache** to serve future identical requests (Cache Hit).
    2.  The **API Entrypoint** receives the final result and sends the complete **JSON Response** back to the **User**.

***

Would you like to explore the specific schema for the JSON request/response in the **Interface Layer**?

```mermaid
flowchart TD
    %% --- NEW BRIGHTER STYLING ---
    %% Palette: Hot Pink, Electric Blue, Lime, Yellow, Orange, Violet
    %% Stroke color changed from #333 (grey) to #2E004F (Deep Indigo) for color consistency
    
    classDef client fill:#FF6EC7,stroke:#2E004F,stroke-width:2px,color:black;
    classDef api fill:#4D96FF,stroke:#2E004F,stroke-width:2px,color:black;
    classDef logic fill:#6BCB77,stroke:#2E004F,stroke-width:2px,color:black;
    classDef storage fill:#FFD93D,stroke:#2E004F,stroke-width:2px,color:black;
    classDef external fill:#FF9F43,stroke:#2E004F,stroke-width:2px,color:black;
    classDef decision fill:#C780FA,stroke:#2E004F,stroke-width:2px,color:black;
    classDef info fill:#00E0FF,stroke:#2E004F,stroke-width:2px,color:black;
    
    %% Subgraph Styling (Pastel backgrounds to replace white/grey)
    style Core_Logic fill:#E8FFEA,stroke:#6BCB77,stroke-width:2px,color:black
    style RAG_Personalization fill:#FFFBE6,stroke:#FFD93D,stroke-width:2px,color:black
    style External_Services fill:#FFE5D9,stroke:#FF9F43,stroke-width:2px,color:black
    %% ---------------------------

    %% Nodes
    User(["👤 User / Client"]):::client
    API["⚡ FastAPI Entrypoint /predict"]:::api
    
    subgraph Core_Logic [🧠 Core Logic Layer]
        Validator{Input Valid?}:::decision
        Cache{Check Cache}:::decision
        Zodiac[Zodiac Engine]:::logic
        Prompt[Prompt Builder]:::logic
        Translator[Translator Service]:::logic
    end

    subgraph RAG_Personalization [🔍 Context & Retrieval]
        VectorStore[("Vector Store / KB")]:::storage
        UserProfile[("User Profile DB")]:::storage
        Retriever[Context Retriever]:::logic
    end

    subgraph External_Services [☁️ External Services]
        LLM["🤖 LLM (OpenAI/HF)"]:::external
        Redis[("Redis Cache")]:::storage
    end

    %% Flow
    User -->|POST JSON| API
    API --> Validator
    Validator -- No --> Err([Error Response]):::client
    Validator -- Yes --> Cache
    
    Cache -- Hit --> User
    Cache -- Miss --> Zodiac
    
    Zodiac -->|Date/Time| Sign([Calculated Sign: Leo]):::info
    
    %% Parallel Context Gathering
    Sign --> Retriever
    Sign --> UserProfile
    
    Retriever -->|Query: 'Leo'| VectorStore
    VectorStore -->|Context: 'Planetary Alignment'| Prompt
    
    UserProfile -->|Context: 'Preferences'| Prompt
    
    %% Generation
    Prompt -->|Complete Prompt| LLM
    LLM -->|Raw Insight| Translator
    
    Translator -->|Final Text| Redis
    Redis -->|Save| API
    API -->|JSON Response| User
```
