# Training and Onboarding Video Generator

## One-Line Concept

A SaaS tool that turns onboarding scripts, training lessons, and sales enablement content into digital-human presenter videos.

## Target Users

- HR and people teams
- Sales enablement teams
- Customer success teams
- Compliance and operations teams
- Course creators and internal trainers

## Market Thesis

Organizations are using AI to create learning content faster, localize training, and keep internal enablement material current. Compared with live streaming, batch video generation is easier to operate because users can wait for rendering and review output before publishing.

This is a lower-risk SaaS path from the LiveTalking repo because recording/export is already present, and real-time perfection is less critical than in live support or live commerce.

## Core User Story

A trainer pastes a script, selects an avatar and voice, previews the result, records a video, downloads the MP4, and shares it with employees or customers.

## MVP Scope

- Script editor with sections
- Avatar and voice selection
- WebRTC preview
- Generate or play section-by-section narration
- Record and download MP4
- Template library for onboarding, product training, compliance, and sales scripts
- Basic project list
- Export status and history

## Example Workflows

### New Employee Onboarding

1. HR selects the "First Day Welcome" template.
2. HR pastes company-specific policies and links.
3. Avatar records a 3-minute welcome video.
4. HR downloads the MP4 and adds it to the onboarding portal.

### Product Update Training

1. Product marketing pastes release notes.
2. SaaS converts them into a short presenter script.
3. Sales enablement reviews and edits the script.
4. Avatar generates a 90-second training clip.
5. Team records variants for English and Chinese.

### Compliance Refresher

1. Operations uploads a policy summary.
2. SaaS creates a plain-language training script.
3. Avatar records the lesson.
4. Optional quiz questions are generated for the LMS.

## Differentiators

- Script-first workflow for non-video teams
- Faster than booking presenters and editors
- Multi-language and multi-voice versions
- Reusable avatar brand presence
- Review-before-publish workflow avoids live failure risk

## Pricing Ideas

- Free trial: limited exports with watermark
- Creator: monthly export minutes
- Team: shared projects and brand templates
- Enterprise: custom avatars, SSO, private deployment
- Usage add-ons: video minutes, TTS minutes, extra storage

## Technical Fit With This Repo

Use directly:

- `/human` for script playback
- `/record` and `/record/{sessionid}` for MP4 export
- TTS plugins
- Avatar generation API
- Admin/session monitoring
- Static web pages as an initial prototype surface

Needs new platform work:

- Project persistence
- Script editor and templates
- Render job queue
- Storage for exported videos
- Review and approval flow
- Multi-language script generation
- Optional LMS integrations

## Main Risks

- Output quality needs review tools
- Long-form recording stability
- Voice and avatar licensing
- Storage and GPU cost control
- Need clear watermarking and content provenance

## Build Later In Its Own Repo

Suggested repo name:

`training-onboarding-video-generator`

Suggested first milestone:

Build a script-to-video prototype with one avatar, section-based playback, recording, download, and a small template library.
