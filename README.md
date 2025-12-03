# AstrologicalInsightGenerator
Build a service that takes a user's birth details (name, date, time, and location of birth) and returns a personalized daily astrological insight, using a combination of zodiac logic and LLM-based language generation.

# Architecture
```mermaid
flowchart TD
    %% --- GLOBAL STYLING ---
    %% 1. Replaced Black/Grey text/borders with Deep Navy Blue (#000080)
    %% 2. Used highly saturated "Candy" colors for backgrounds
    
    classDef client fill:#FF85C0,stroke:#000080,stroke-width: 2px,color:#000080;
    classDef api fill:#40E0D0,stroke:#000080,stroke-width: 2px,color:#000080;
    classDef logic fill:#7CFC00,stroke:#000080,stroke-width: 2px,color:#000080;
    classDef storage fill:#FFD700,stroke:#000080,stroke-width: 2px,color:#000080;
    classDef external fill:#FF7F50,stroke:#000080,stroke-width: 2px,color:#000080;

    %% Nodes
    User(["👤 User / Client"]):::client
    API["⚡ FastAPI Entrypoint /predict"]:::api
    
    subgraph Core_Logic [🧠 Core Logic Layer]
        %% Subgraph styling (border)
        style Core_Logic fill:#E0FFFF,stroke:#000080,stroke-width: 2px,color:#000080
        
        Validator{Input Valid?}:::logic
        Cache{Check Cache}:::logic
        Zodiac[Zodiac Engine]:::logic
        Prompt[Prompt Builder]:::logic
        Translator[Translator Service]:::logic
    end

    subgraph RAG_Personalization [🔍 Context & Retrieval]
        style RAG_Personalization fill:#FFFACD,stroke:#000080,stroke-width: 2px,color:#000080
        
        VectorStore[("Vector Store / Knowledge Base")]:::storage
        UserProfile[("User Profile DB")]:::storage
        Retriever[Context Retriever]:::logic
    end

    subgraph External_Services [☁️ External Services]
        style External_Services fill:#FFE4E1,stroke:#000080,stroke-width: 2px,color:#000080
        
        LLM["🤖 LLM (OpenAI/HuggingFace)"]:::external
        Redis[("Redis/In-Memory Cache")]:::storage
    end

    %% Flow
    User -->|POST JSON| API
    API --> Validator
    Validator -- No --> Err([Error Response]):::client
    Validator -- Yes --> Cache
    
    Cache -- Hit --> User
    Cache -- Miss --> Zodiac
    
    Zodiac -->|Date/Time| Sign([Calculated Sign: Leo])
    
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

    %% --- LINK STYLING (To remove grey lines) ---
    %% Applies Deep Navy Blue to all connecting lines
    linkStyle default stroke:#000080,stroke-width: 2px,color:#000080;
```
