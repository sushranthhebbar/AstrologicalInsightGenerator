from fastapi import APIRouter, HTTPException
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse

# Import logic modules
from app.core.zodiac_engine import ZodiacEngine
from app.core.prompt_builder import PromptBuilder

# Import services
from app.services.cache_service import redis_cache
from app.services.retriever import ContextRetriever
from app.services.profile_service import ProfileService
from app.services.llm_client import LLMClient
from app.services.translator import TranslatorService

router = APIRouter()

# Initialize services
retriever = ContextRetriever()
profile_service = ProfileService()
llm_client = LLMClient()
translator = TranslatorService()

@router.post("/predict", response_model=PredictionResponse)
async def generate_insight(request: PredictionRequest):
    
    # 1. Calculate Zodiac (Logic Layer)
    zodiac_sign = ZodiacEngine.get_sign(request.birth_date)
    
    # 2. Check Cache (Interface Layer)
    # Cache key combines zodiac + date + language to ensure uniqueness
    cache_key = f"{zodiac_sign}_{request.birth_date}_{request.language}"
    cached_insight = await redis_cache.get(cache_key)
    
    if cached_insight:
        return PredictionResponse(
            zodiac=zodiac_sign,
            insight=cached_insight,
            language=request.language,
            context_used=["From Cache"]
        )

    # 3. Intelligence Retrieval (RAG & Personalization)
    # Query knowledge base with Zodiac and Birth Place
    retrieved_context = retriever.retrieve([zodiac_sign, request.birth_place])
    
    # Get user profile
    user_profile = profile_service.get_profile(request.name)

    # 4. Prompt Generation
    prompt = PromptBuilder.build(
        name=request.name,
        zodiac=zodiac_sign,
        context=retrieved_context,
        preferences=user_profile
    )

    # 5. LLM Call
    raw_insight = await llm_client.generate_insight(prompt)

    # 6. Post-Processing (Translation)
    final_insight = await translator.translate(raw_insight, request.language)

    # 7. Save to Cache
    await redis_cache.set(cache_key, final_insight)

    return PredictionResponse(
        zodiac=zodiac_sign,
        insight=final_insight,
        language=request.language,
        context_used=retrieved_context
    )
