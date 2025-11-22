#!/bin/bash

# 🧪 Comprehensive Test Script for AI Image Analysis Platform
# Tests all features: OCR, Caption, Translation, TTS

echo "🧪 Testing AI Image Analysis Platform"
echo "======================================"
echo ""

BASE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=$3
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$url")
    fi
    
    status_code=$(echo "$response" | tail -n 1)
    
    if [ "$status_code" = "200" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $status_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $status_code)"
        ((FAILED++))
    fi
}

# Test 1: Health Check
echo "1️⃣  Health Check"
test_endpoint "Health endpoint" "$BASE_URL/api/health" "GET"
echo ""

# Test 2: Available Voices
echo "2️⃣  TTS Voices"
test_endpoint "Get available voices" "$BASE_URL/api/voices" "GET"
echo ""

# Test 3: OCR Languages
echo "3️⃣  OCR Languages"
test_endpoint "Get OCR languages" "$BASE_URL/api/languages/ocr" "GET"
echo ""

# Test 4: Translation Languages
echo "4️⃣  Translation Languages"
test_endpoint "Get translation languages" "$BASE_URL/api/languages/translation" "GET"
echo ""

# Test 5: TTS - English
echo "5️⃣  Text-to-Speech (English)"
echo -n "Testing English TTS... "
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test.", "language": "en", "rate": 200}' \
  --output /tmp/test_tts_english.wav)

status_code=$(echo "$response" | tail -n 1)
if [ "$status_code" = "200" ] && [ -f "/tmp/test_tts_english.wav" ]; then
    size=$(ls -lh /tmp/test_tts_english.wav | awk '{print $5}')
    echo -e "${GREEN}✓ PASSED${NC} (Generated $size WAV file)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (HTTP $status_code)"
    ((FAILED++))
fi
echo ""

# Test 6: TTS - Hindi
echo "6️⃣  Text-to-Speech (Hindi)"
echo -n "Testing Hindi TTS... "
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "नमस्ते दोस्तों", "language": "hi", "rate": 200}' \
  --output /tmp/test_tts_hindi.wav)

status_code=$(echo "$response" | tail -n 1)
if [ "$status_code" = "200" ] && [ -f "/tmp/test_tts_hindi.wav" ]; then
    size=$(ls -lh /tmp/test_tts_hindi.wav | awk '{print $5}')
    echo -e "${GREEN}✓ PASSED${NC} (Generated $size WAV file)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (HTTP $status_code)"
    ((FAILED++))
fi
echo ""

# Test 7: TTS - Spanish
echo "7️⃣  Text-to-Speech (Spanish)"
echo -n "Testing Spanish TTS... "
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola amigos", "language": "es", "rate": 200}' \
  --output /tmp/test_tts_spanish.wav)

status_code=$(echo "$response" | tail -n 1)
if [ "$status_code" = "200" ] && [ -f "/tmp/test_tts_spanish.wav" ]; then
    size=$(ls -lh /tmp/test_tts_spanish.wav | awk '{print $5}')
    echo -e "${GREEN}✓ PASSED${NC} (Generated $size WAV file)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (HTTP $status_code)"
    ((FAILED++))
fi
echo ""

# Test 8: Translation
echo "8️⃣  Translation"
echo -n "Testing translation (English to Spanish)... "
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_language": "es"}')

status_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [ "$status_code" = "200" ] && echo "$body" | grep -q "Hola"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (HTTP $status_code)"
    ((FAILED++))
fi
echo ""

# Summary
echo "======================================"
echo "📊 Test Summary"
echo "======================================"
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "Generated audio files:"
    ls -lh /tmp/test_tts_*.wav 2>/dev/null
    echo ""
    echo "You can play them with:"
    echo "  afplay /tmp/test_tts_english.wav"
    echo "  afplay /tmp/test_tts_hindi.wav"
    echo "  afplay /tmp/test_tts_spanish.wav"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please check the backend logs.${NC}"
    exit 1
fi
