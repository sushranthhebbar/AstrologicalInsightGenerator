# AstrologicalInsightGenerator
Build a service that takes a user's birth details (name, date, time, and location of birth) and returns a personalized daily astrological insight, using a combination of zodiac logic and LLM-based language generation.

# Architecture
flowchart TD
    %% Styling
    classDef client fill:#f9f,stroke:#333,stroke-width:2px;
    classDef api fill:#bbf,stroke:#333,stroke-width:2px;
    classDef logic fill:#dfd,stroke:#333,stroke-width:2px;
    classDef storage fill:#ff9,stroke:#333,stroke-width:2px;
    classDef external fill:#ddd,stroke:#333,stroke-width:2px;

    %% Nodes
    User([👤 User / Client]):::client
    API[⚡ FastAPI Entrypoint /predict]:::api
    
    subgraph Core_Logic [🧠 Core Logic Layer]
        Validator{Input Valid?}
        Cache{Check Cache}
        Zodiac[Zodiac Engine]:::logic
        Prompt[Prompt Builder]:::logic
        Translator[Translator Service]:::logic
    end

    subgraph RAG_Personalization [🔍 Context & Retrieval]
        VectorStore[(Vector Store / Knowledge Base)]:::storage
        UserProfile[(User Profile DB)]:::storage
        Retriever[Context Retriever]:::logic
    end

    subgraph External_Services [☁️ External Services]
        LLM[🤖 LLM (OpenAI/HuggingFace)]:::external
        Redis[(Redis/In-Memory Cache)]:::storage
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
