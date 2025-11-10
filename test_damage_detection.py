"""
Test Vehicle Damage Detection with FREE Hugging Face Model
NO API COSTS - 100% FREE!
"""

import sys
from PIL import Image

print("🔧 Testing FREE AI Vehicle Damage Detection...")
print("="*60)

# Step 1: Check if transformers is installed
print("\n1️⃣ Checking dependencies...")
try:
    from transformers import pipeline
    print("✅ transformers installed")
except ImportError:
    print("❌ transformers not installed")
    print("\n📦 Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers", "torch", "pillow"])
    from transformers import pipeline
    print("✅ Packages installed!")

# Step 2: Load model (downloads first time, then cached)
print("\n2️⃣ Loading AI model from Hugging Face...")
print("⏳ This may take a minute on first run (downloading model)...")

try:
    damage_detector = pipeline(
        "image-classification",
        model="beingamit99/car_damage_detection"
    )
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

# Step 3: Test with sample images
print("\n3️⃣ Testing model...")
print("="*60)

# Test image URL (will use a sample car image)
print("\nℹ️  To test with your own image:")
print("   python test_damage_detection.py path/to/your/car_image.jpg")
print()

if len(sys.argv) > 1:
    # User provided image path
    image_path = sys.argv[1]
    print(f"📸 Analyzing: {image_path}")
    
    try:
        image = Image.open(image_path)
        print(f"✅ Image loaded: {image.size[0]}x{image.size[1]} pixels")
        
        # Run AI prediction
        print("\n🤖 Running AI analysis...")
        result = damage_detector(image)
        
        print("\n" + "="*60)
        print("🎯 RESULTS:")
        print("="*60)
        
        for i, prediction in enumerate(result, 1):
            label = prediction['label']
            score = prediction['score']
            percentage = score * 100
            
            # Emoji based on result
            if label == 'damaged':
                emoji = "🔴" if score > 0.7 else "🟡"
            else:
                emoji = "🟢"
            
            print(f"\n{emoji} Prediction #{i}:")
            print(f"   Label: {label.upper()}")
            print(f"   Confidence: {percentage:.2f}%")
            print(f"   Score: {score:.4f}")
        
        # Final verdict
        print("\n" + "="*60)
        top_prediction = result[0]
        if top_prediction['label'] == 'damaged' and top_prediction['score'] > 0.7:
            print("⚠️  VERDICT: VEHICLE HAS DAMAGE")
            print(f"   Confidence: {top_prediction['score']*100:.1f}%")
        elif top_prediction['label'] == 'damaged' and top_prediction['score'] > 0.5:
            print("🟡 VERDICT: POSSIBLE DAMAGE (needs manual review)")
            print(f"   Confidence: {top_prediction['score']*100:.1f}%")
        else:
            print("✅ VERDICT: NO DAMAGE DETECTED")
            print(f"   Confidence: {top_prediction['score']*100:.1f}%")
        
        print("="*60)
        
    except FileNotFoundError:
        print(f"❌ Error: Image file not found: {image_path}")
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        import traceback
        traceback.print_exc()

else:
    # No image provided - show instructions
    print("ℹ️  No image provided for testing.")
    print()
    print("📋 USAGE:")
    print("   python test_damage_detection.py car_image.jpg")
    print()
    print("📝 EXAMPLE:")
    print("   python test_damage_detection.py /path/to/damaged_car.jpg")
    print()
    print("💡 TIP: Download a test image from Google Images:")
    print("   - Search: 'damaged car'")
    print("   - Save image locally")
    print("   - Run script with that image")
    print()
    print("✅ Model is loaded and ready to use!")
    print("   It will be MUCH faster on subsequent runs (cached).")

print("\n" + "="*60)
print("🎉 Test complete!")
print("="*60)
print()
print("💰 COST: €0 (100% FREE!)")
print("🚀 Ready to integrate into FastAPI!")
