# Migration notes

Rebuilt directly in the E: repository from the current public Wix source. The captures contain 22 event entries, 24 homepage slideshow photos, and 16 profiles. The captured content and original spelling are preserved.

Current leadership is grouped into Co-Presidents, Vice Presidents, Directors, then Officers & Assistants. Past leaders follow, grouped by 2025 and 2024. Profiles appear two per row above 600 px and one per row on phones.

The Wix banner and runtime are omitted. Contact validates input and prepares an email draft; the visitor must send it using their own email app. Chat opens contact options rather than a Wix live chat session. Enrollment retains the original Google Form. Photo controls without an original album destination open the event's cover image; external Canva and WeChat album links remain unchanged.

Hidden Search and Schedule pages are retained, with local search implemented. The unlinked Event Details & Registration page is the Wix sample template; RSVP stays on the original site.

The repeatable checker verifies local links/fragments, CSS and content asset paths, and member preservation. Deployment still requires enabling GitHub Pages or uploading `dist/` to a static host.

## Local verification

All eight pages were checked at 1280 px and 390 px, with no horizontal overflow. Current leadership has 13 profiles, past leadership has 3, and the first two cards share the same row on desktop. Slideshow navigation, photo viewing, local search, and the email draft preview passed. JavaScript syntax and all local references passed. No email or enrollment was submitted.
