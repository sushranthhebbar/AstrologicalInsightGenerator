# AstrologicalInsightGenerator
Build a service that takes a user's birth details (name, date, time, and location of birth) and returns a personalized daily astrological insight, using a combination of zodiac logic and LLM-based language generation.

# Architecture
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
