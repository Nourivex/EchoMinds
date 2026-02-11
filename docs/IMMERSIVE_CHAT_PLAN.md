# 🎭 Immersive Chat System - Technical Planning

## 📋 Overview

Transformasi chat system dari **flat text** menjadi **structured narrative** yang immersive seperti Character AI/Chai.

**Current State:**
```
"Kakak! Halo juga! Aku lagi main sama bonekaku... | [EN] Hey! Hello too! I'm playing with my doll..."
```
❌ Panjang, cluttered, terasa "debug mode"

**Target State:**
```
*Aiko sedang duduk di lantai, memainkan boneka kecilnya.*

"Kakak! Halo juga! Kakak lagi apa nih?"

*Ia tersenyum lebar.*

🌐 Show translation
```
✅ Immersive, natural, clean

---

## 🎯 Goals

1. **Structured Message Format** - Pisahkan dialogue, action, thought, emotion
2. **Optional Translation** - Toggle subtle, tidak default visible
3. **Scene Awareness** - Activity, location, mood context
4. **Immersive Rendering** - Different styles untuk different message types
5. **Consistency** - Standardized writing rules untuk AI responses

---

## 🏗️ Architecture Changes

### 1. Message Schema Enhancement

**Current:**
```typescript
type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}
```

**New (Structured):**
```typescript
type StructuredMessage = {
  id: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  
  // Structured content
  dialogue?: string;          // "Kakak! Halo juga!"
  action?: string;            // "sedang duduk sambil memainkan boneka"
  thought?: string;           // "semoga kakak nggak pergi lagi"
  emotion?: string;           // "tersenyum lebar", "memiringkan kepala"
  
  // Optional translation
  translation?: {
    dialogue?: string;
    action?: string;
    thought?: string;
  };
  
  // Legacy fallback
  rawContent?: string;        // For parsing old messages
}
```

### 2. Scene Context System

**New State:**
```typescript
type SceneContext = {
  activity: 'idle' | 'playing' | 'walking' | 'cooking' | 'studying' | 'sleeping';
  location: 'bedroom' | 'living-room' | 'park' | 'office' | 'cafe' | 'unknown';
  mood: 'happy' | 'shy' | 'sad' | 'excited' | 'calm' | 'anxious';
  timeOfDay: 'morning' | 'afternoon' | 'evening' | 'night';
}
```

**Injection to Prompt:**
```
[Scene Context]
Location: bedroom
Activity: playing with dolls
Mood: happy, excited
Time: afternoon

[Character State]
You are sitting on the floor in your bedroom...
```

### 3. Writing Format Standards

| Type       | Format                              | Example                                      |
|------------|-------------------------------------|----------------------------------------------|
| **Dialogue** | Quoted text `"..."`               | "Kakak! Halo juga!"                         |
| **Action**   | Italic with asterisks `*...*`     | *sedang duduk di lantai*                    |
| **Thought**  | Parentheses `(...)`               | (semoga kakak nggak pergi lagi)             |
| **Emotion**  | Often combined with action        | *tersenyum lebar*, *memiringkan kepala*     |

---

## 🎨 UI/UX Design

### Message Rendering (Different Styles)

```svelte
<!-- Action/Narration -->
<div class="text-slate-500 italic text-sm mb-2">
  *{message.action}*
</div>

<!-- Dialogue -->
<div class="text-slate-900 dark:text-slate-100 text-base mb-2">
  "{message.dialogue}"
</div>

<!-- Thought (subtle) -->
<div class="text-slate-400 text-sm">
  ({message.thought})
</div>

<!-- Translation Toggle -->
{#if message.translation}
  <button 
    class="mt-2 text-xs text-purple-600 hover:text-purple-700"
    onclick={() => showTranslation = !showTranslation}
  >
    🌐 {showTranslation ? 'Hide' : 'Show'} translation
  </button>
  
  {#if showTranslation}
    <div class="mt-2 p-2 bg-purple-50 dark:bg-purple-900/20 rounded text-sm">
      {message.translation.dialogue}
    </div>
  {/if}
{/if}
```

### Translation Options

**Option A: Toggle inside bubble (Recommended)**
```
┌─────────────────────────────────────┐
│ *Aiko sedang bermain boneka*        │
│ "Kakak! Halo juga!"                 │
├─────────────────────────────────────┤
│ 🌐 Show English translation         │  ← Click to expand
└─────────────────────────────────────┘
```

**Option B: Globe icon (More subtle)**
```
┌─────────────────────────────────────┐
│ *Aiko sedang bermain boneka*        │
│ "Kakak! Halo juga!"              🌐 │  ← Hover/click
└─────────────────────────────────────┘
```

---

## 🔧 Implementation Plan

### Phase 1: Backend Updates

**1.1. Update ChatResponse Schema**
- File: `backend/models/schemas.py`
- Add `StructuredMessageContent` model
- Maintain backward compatibility with `rawContent`

**1.2. Enhance System Prompt**
- File: `backend/services/chat_service.py`
- Inject scene context into prompt
- Add formatting instructions:
  ```
  Format your response using:
  - Actions in *asterisks*
  - Dialogue in "quotes"
  - Thoughts in (parentheses)
  ```

**1.3. Message Parser (Optional)**
- Create `parse_message()` function
- Regex-based parsing for legacy responses:
  - Action: `/\*(.*?)\*/g`
  - Dialogue: `/"(.*?)"/g`
  - Thought: `/\((.*?)\)/g`

**1.4. Scene Context Manager**
- New service: `backend/services/scene_service.py`
- Track conversation state (activity, location, mood)
- Update based on user input
- Inject into prompts

### Phase 2: Frontend Updates

**2.1. Update Message Type**
- File: `src/lib/types.ts`
- Add `StructuredMessage` interface
- Create `MessagePart` component variants

**2.2. Create Message Components**
```
src/components/chat/message-parts/
├── DialoguePart.svelte       // Quoted dialogue
├── ActionPart.svelte         // Italic narration
├── ThoughtPart.svelte        // Subtle thoughts
├── EmotionIndicator.svelte   // Visual emotion cues
└── TranslationToggle.svelte  // Collapsible translation
```

**2.3. Update ChatInterface**
- Parse structured messages
- Render different parts with different styles
- Add translation toggle state per message
- Smooth animations for expand/collapse

**2.4. Scene Indicator (Optional)**
```svelte
<!-- Subtle scene indicator -->
<div class="text-xs text-slate-400 mb-4">
  📍 Bedroom • 🎮 Playing • 😊 Happy
</div>
```

### Phase 3: Advanced Features

**3.1. Idle Messages**
- Detect user inactivity (>30s)
- Generate contextual idle message
- Example: *Aiko melihat ke arah pintu* "Kakak... masih di sana?"

**3.2. Emotional Drift**
- Track conversation tone over time
- Adjust character mood dynamically
- Reflect in scene context

**3.3. Activity Memory**
- Remember what character was doing
- Maintain continuity across messages
- Example: If playing → mention toy later

**3.4. Visual Enhancements**
- Animated typing effect for dialogue
- Fade-in for actions
- Pulse effect for new thoughts
- Avatar expressions based on emotion

---

## 📊 Testing Strategy

### Unit Tests
- Message parser (regex extraction)
- Scene context manager
- Translation toggle logic

### Integration Tests
- End-to-end chat flow with structured messages
- Scene context injection
- Backward compatibility with old messages

### UX Testing
- Translation toggle usability
- Message readability
- Immersion vs information balance

---

## 🚧 Migration Strategy

### Backward Compatibility

**Old messages:**
```json
{
  "role": "assistant",
  "content": "Kakak! Halo juga! Aku lagi main sama bonekasku..."
}
```

**Auto-parse to structured:**
```typescript
function migrateMessage(old: Message): StructuredMessage {
  const parsed = parseMessage(old.content);
  return {
    ...old,
    dialogue: parsed.dialogue,
    action: parsed.action,
    thought: parsed.thought,
    rawContent: old.content // Keep original
  };
}
```

### Graceful Degradation

If parser fails → fallback to `rawContent` display

---

## 📈 Success Metrics

- **Immersion Score**: User feedback on "feels alive"
- **Clarity**: Message readability rating
- **Translation Usage**: % of users who expand translations
- **Scene Continuity**: AI maintains context across 5+ messages
- **Response Quality**: Structured format compliance rate

---

## 🔗 Related Issues

- **CORS Error**: `/api/config` missing CORS headers (blocking Settings page)
- **Message Length**: Current bilingual display too long
- **Persona Consistency**: AI sometimes breaks character format

---

## 📅 Timeline Estimate

| Phase | Task | Estimate | Status |
|-------|------|----------|--------|
| 1 | Backend schema updates | 2 hours | Pending |
| 1 | System prompt enhancement | 1 hour | Pending |
| 1 | Message parser | 2 hours | Pending |
| 1 | Scene context service | 3 hours | Pending |
| 2 | Frontend types | 1 hour | Pending |
| 2 | Message components | 3 hours | Pending |
| 2 | ChatInterface refactor | 2 hours | Pending |
| 2 | Translation toggle | 1 hour | Pending |
| 3 | Idle messages | 2 hours | Pending |
| 3 | Visual enhancements | 2 hours | Pending |

**Total Estimate:** ~19 hours (~2-3 work sessions)

---

## 🎯 Next Steps (Priority Order)

1. ✅ **Document planning** (this file)
2. 🔧 **Fix CORS issue** (Settings page blocked)
3. 📝 **Create backend schema** for structured messages
4. 🎨 **Build message components** (UI prototypes)
5. 🧪 **Test with simple examples** (proof of concept)
6. 🚀 **Gradual rollout** (feature flag?)

---

**Created:** 2025-01-XX  
**Last Updated:** 2025-01-XX  
**Status:** Planning Phase  
**Owner:** EchoMinds Team
