"""
Vehicle Damage Detection AI Module
FREE - Uses Hugging Face model (no API costs)
Model: beingamit99/car_damage_detection
"""

import logging
from PIL import Image
import io
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# Global model instance (loaded once at startup)
_damage_detector = None

def load_damage_detection_model():
    """
    Load AI model at startup (downloads once, then cached)
    Call this in FastAPI startup event
    """
    global _damage_detector
    
    if _damage_detector is not None:
        return _damage_detector
    
    try:
        logger.info("Loading vehicle damage detection AI model...")
        from transformers import pipeline
        
        _damage_detector = pipeline(
            "image-classification",
            model="beingamit99/car_damage_detection"
        )
        
        logger.info("✅ AI model loaded successfully!")
        return _damage_detector
        
    except Exception as e:
        logger.debug(f"⚠️ AI model not available: {e}")
        return None


def analyze_vehicle_damage(image_bytes: bytes) -> Dict[str, Any]:
    """
    Analyze vehicle image for damage using AI
    
    Args:
        image_bytes: Image file bytes
    
    Returns:
        {
            "ok": bool,
            "has_damage": bool,
            "damage_type": str or None,
            "confidence": float,
            "all_predictions": list,
            "verdict": str
        }
    """
    global _damage_detector
    
    # Load model if not loaded
    if _damage_detector is None:
        _damage_detector = load_damage_detection_model()
        
    if _damage_detector is None:
        return {
            "ok": False,
            "error": "AI model not available"
        }
    
    try:
        # Load image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run AI prediction
        predictions = _damage_detector(image)
        
        # Parse results
        top_prediction = predictions[0]
        damage_type = top_prediction['label']
        confidence = top_prediction['score']
        
        # Determine if damaged
        # Known damage types: GLASS SHATTER, DENT, LAMP BROKEN, SCRATCH, CRACK
        damage_types = ['GLASS SHATTER', 'DENT', 'LAMP BROKEN', 'SCRATCH', 'CRACK']
        
        has_damage = False
        verdict = "NO DAMAGE"
        
        if damage_type in damage_types and confidence > 0.5:
            has_damage = True
            verdict = f"{damage_type} DETECTED"
        elif damage_type in damage_types and confidence > 0.3:
            verdict = f"POSSIBLE {damage_type} (needs review)"
        
        return {
            "ok": True,
            "has_damage": has_damage,
            "damage_type": damage_type if has_damage else None,
            "confidence": round(confidence, 4),
            "confidence_percent": round(confidence * 100, 2),
            "verdict": verdict,
            "all_predictions": [
                {
                    "type": p['label'],
                    "confidence": round(p['score'], 4),
                    "confidence_percent": round(p['score'] * 100, 2)
                }
                for p in predictions[:5]  # Top 5
            ]
        }
        
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "ok": False,
            "error": str(e)
        }


def get_damage_summary(predictions: List[Dict]) -> str:
    """
    Generate human-readable summary from predictions
    """
    if not predictions or not predictions[0].get('has_damage'):
        return "✅ No damage detected"
    
    damage_type = predictions[0].get('damage_type', 'Unknown')
    confidence = predictions[0].get('confidence_percent', 0)
    
    if confidence > 70:
        return f"🔴 {damage_type} detected ({confidence:.1f}% confidence)"
    elif confidence > 50:
        return f"🟡 {damage_type} detected ({confidence:.1f}% confidence)"
    else:
        return f"⚠️ Possible {damage_type} ({confidence:.1f}% confidence - needs review)"


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python vehicle_damage_ai.py image.jpg")
        sys.exit(1)
    
    # Load model
    print("Loading model...")
    load_damage_detection_model()
    
    # Analyze image
    image_path = sys.argv[1]
    print(f"Analyzing: {image_path}")
    
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    result = analyze_vehicle_damage(image_bytes)
    
    print("\nResult:")
    print(f"  Has damage: {result.get('has_damage')}")
    print(f"  Damage type: {result.get('damage_type')}")
    print(f"  Confidence: {result.get('confidence_percent')}%")
    print(f"  Verdict: {result.get('verdict')}")
    
    print("\nAll predictions:")
    for pred in result.get('all_predictions', []):
        print(f"  - {pred['type']}: {pred['confidence_percent']}%")
