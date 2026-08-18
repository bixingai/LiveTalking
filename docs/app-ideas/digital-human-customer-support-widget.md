# Digital Human Customer Support Widget

## Product Name: Helpora

Helpora starts with the universally understood word "help" and adds a softer, more memorable brand ending. It communicates assistance without sounding like a traditional ticketing system, which fits a support experience built around a welcoming digital human, quick answers, and human handoff when needed.

## One-Line Concept

A website support widget where customers talk to a branded digital-human assistant that answers product, service, and onboarding questions from a company knowledge base.

## Target Users

- SaaS companies with self-serve onboarding
- Ecommerce brands with repetitive pre-sales questions
- Local service businesses that need guided intake
- Enterprise support teams testing AI agent front doors

## Market Thesis

Customer support teams are adopting AI agents to reduce response time, deflect repetitive tickets, and provide always-on service. A digital-human interface can be useful when the brand wants a guided, human-like experience rather than a plain chatbot.

This direction has a larger enterprise ceiling than live commerce, but it needs stronger reliability, knowledge grounding, safety controls, and human handoff before it can be production-grade.

## Core User Story

A website visitor clicks "Talk to us", connects to a branded avatar, asks a question by text or voice, receives a short answer, and can be handed off to a human if the assistant is uncertain or the issue is sensitive.

## MVP Scope

- Embeddable widget or hosted support page
- WebRTC digital-human session
- Text input to `/human`
- Knowledge-base backed answer generation
- Echo mode for scripted answers
- Human handoff request button
- Conversation transcript
- Admin FAQ manager
- Basic analytics: sessions, questions, unresolved issues

## Example Workflows

### Ecommerce Pre-Sales

1. Customer asks: "Will this work with my phone?"
2. Assistant checks product FAQ and compatibility notes.
3. Avatar answers in a short spoken response.
4. Customer asks about returns.
5. Assistant cites the return policy and offers a human handoff.

### SaaS Onboarding

1. New user asks how to import data.
2. Assistant explains the first three steps.
3. Assistant offers to open the relevant docs page.
4. If the user asks about billing, assistant escalates to support.

## Differentiators

- More guided and personal than a text-only chat widget
- Human handoff built into the experience
- Short spoken answers designed for attention-constrained users
- Branded avatar and voice
- Useful for product demos, onboarding, and support deflection

## Pricing Ideas

- Starter: one widget, limited monthly sessions
- Growth: knowledge base, transcripts, analytics
- Business: handoff integrations, team controls, custom avatar
- Usage add-ons: TTS minutes, video minutes, storage, premium voices

## Technical Fit With This Repo

Use directly:

- WebRTC session creation
- `/human` for text-driven speech
- `/humanaudio` for uploaded audio
- SSE status events
- Admin session API
- TTS plugin architecture
- Avatar plugin architecture

Needs new platform work:

- Widget SDK
- Auth, tenants, and site embeds
- Knowledge-base ingestion and retrieval
- LLM provider abstraction
- Safety filters and escalation rules
- CRM/helpdesk integrations
- Conversation storage and privacy controls

## Main Risks

- Hallucinated support answers
- Privacy and data retention
- Latency from LLM plus TTS plus avatar rendering
- Browser compatibility for embedded WebRTC
- User expectations if the avatar appears too human

## Build Later In Its Own Repo

Suggested repo name:

`digital-human-support-widget`

Suggested first milestone:

Build a single-company hosted support page with FAQ-backed answers, WebRTC avatar playback, transcript capture, and a handoff button.
