# AI Live Commerce Operator

## One-Line Concept

A SaaS operator console that lets small brands run an AI digital-human livestream host for product selling, customer Q&A, replay clips, and campaign scripts.

## Target Users

- Small and midsize ecommerce brands
- Live commerce agencies
- Solo merchants selling through Douyin, TikTok Shop, Xiaohongshu, Taobao Live, or similar channels
- Teams that need more livestream coverage than human hosts can provide

## Market Thesis

Live commerce and social commerce remain large, high-frequency workflows, especially in China and cross-border ecommerce. Merchants want more selling hours, lower host cost, faster script iteration, and reusable short video content.

This is the strongest fit for the current LiveTalking repo because the repo already supports real-time digital-human rendering, WebRTC preview, RTMP-style output, TTS, interruption, recording, and custom action states.

Reference signals:

- NIQ 2026 commerce trends report discusses the scale and continued growth of live commerce and social commerce in China.
- Public reporting on AI avatar livestreaming shows increasing adoption and platform regulation, which suggests demand but also a need for compliance controls.

## Core User Story

A merchant uploads a product catalog, selects an avatar and voice, starts a preview, sends approved selling scripts to the avatar, handles buyer questions, interrupts when needed, and records useful moments as short clips.

## MVP Scope

- Product catalog upload or manual product cards
- Script queue for product intros, objection handling, limited-time offers, and closing prompts
- WebRTC preview using the LiveTalking engine
- Echo-mode script playback
- Manual interrupt and resume
- RTMP/live output configuration
- Session status panel
- Recording and clip download
- Basic help/tutorial page

## Example Workflows

### Product Launch

1. Merchant adds a new product with price, benefits, specs, and common objections.
2. SaaS generates 10 short livestream scripts.
3. Operator clicks "Start Preview".
4. Operator sends scripts one by one to the avatar.
5. When a viewer asks about shipping, the operator sends a prepared response.
6. Operator records the best 60-second pitch as a reusable clip.

### Flash Sale

1. Merchant sets a sale window and coupon terms.
2. SaaS prepares countdown lines and urgency copy.
3. Avatar repeats the offer every few minutes.
4. Operator interrupts with updated stock or price changes.

## Differentiators

- Built for live selling, not generic avatars
- Human-in-the-loop script approval
- Product-aware prompts and answer templates
- Record once, reuse for short video
- China-aware workflows and platform-specific templates

## Pricing Ideas

- Starter: one avatar, preview, limited clip generation
- Pro: live streaming hours, product catalog, script library
- Agency: multiple brands, multiple operators, team review
- Usage add-ons: GPU minutes, TTS minutes, avatar generation, storage

## Technical Fit With This Repo

Use directly:

- `app.py` server entry
- WebRTC `/offer`
- `/human` text driver
- `/record` and `/record/{sessionid}`
- `streamout/rtmp.py` for live output direction
- `tts/` plugins
- `data/avatars/` avatar assets
- `web/` as the first operator-console prototype

Needs new platform work:

- Auth and tenancy
- Product catalog database
- Script approval workflow
- Stream destination management
- Observability for live sessions
- Billing and usage metering

## Main Risks

- Platform policy and AI-avatar labeling requirements
- Live stream reliability and GPU capacity planning
- Quality of product Q&A grounding
- Voice/avatar licensing and user-uploaded asset rights

## Build Later In Its Own Repo

Suggested repo name:

`ai-live-commerce-operator`

Suggested first milestone:

Build a single-tenant local operator console around LiveTalking with product cards, script queue, WebRTC preview, interrupt, and recording.
