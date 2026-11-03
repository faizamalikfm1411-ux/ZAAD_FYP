# Wireframe vs SRS Conflict List (S1-KF-05)

**Project:** ZAAD | **Compared:** SRS v1.2, Figures 3.2 to 3.5 | **Prepared by:** Khansa Farooq | **Reviewer:** Faiza Malik | **Date:** 2 Nov 2026

## ARIA name confirmed

The assistant is called **ARIA** in the UI, documents and demo. "Jim" is removed everywhere it appears: the avatar label, the chat header, the greeting "Hi, I'm Jim!", the input placeholder "Ask Jim about your food...", "Your conversations with Jim", and the Figure 3.4 caption "AI-Assistant". Owner: Hamna.

## Conflicts and proposals

| # | Wireframe element (figure) | SRS requirement | Conflict | Proposal | Owner |
|---|---|---|---|---|---|
| 1 | Assistant named "Jim" (3.3, 3.4, 3.5) | SRS 1 and 2.2 name it ARIA | Wrong name | Rename to ARIA on every screen and caption | Hamna |
| 2 | "Favourites" tab and heart icons on dish cards (3.3, 3.5) | Fig 3.1 navigation; FR-MEM-01 to 04 | No favourites feature in the SRS | Remove the tab and hearts, or raise a scope change (NFR-BR-01) | Hamna remove; Khansa scope |
| 3 | "Rs" prices on dish cards and a price filter, Low to High (3.3, 3.5) | FR-MENU-01 to 06; payments out of scope | Dish records have no price field | Remove prices and the price filter | Hamna |
| 4 | Category chips Biryani, Karahi, BBQ, Healthy (3.3, 3.5) | FR-MENU-05 | Categories are Pakistani Food, Fast Food, Desserts | Change the chips to the three SRS categories | Hamna |
| 5 | Calories-per-meal filter: Any kcal, under 600, over 750 (3.5) | Not specified | Extra control outside the SRS | Remove, or raise a scope change | Hamna; Khansa |
| 6 | Dark theme on the Urdu screen (3.5) | NFR-UI-01 | Style differs from the English screens | One theme for both languages; dark mode only after a scope change | Hamna |
| 7 | Scanner says "dish QR code" and "Enter dish code" (3.5) | FR-AR-01 | The SRS uses one table/menu QR that opens the menu overlay | Reword to "table/menu QR". Keep manual code entry as a fallback for the table code only | Hamna |
| 8 | "Continue with Google / Gmail" (3.2, 3.4) | FR-PROF-19 | Sign-in is required, but Google sign-in is not specified | Supervisor decision (affects the auth design). Default to email and password | Khansa; Faiza |
| 9 | "Permission denied" in red inside the chat screen (3.4) | NFR-UI-10 | The error does not explain what is unavailable or offer an alternative | Explain it and offer a working alternative (text input in place of voice) | Hamna |
| 10 | No SAFE / CAUTION / DANGER banners and no blocked-dish screen | FR-ALG-04 to 07; NFR-UI-02, 05, 09 | The SRS List of Figures describes Fig 3.4 as the allergen banner wireframe, but Fig 3.4 shows the chat | Design all three states plus the blocked screen (S2-HM-11); correct the List of Figures | Hamna; Khansa signs off |
| 11 | Small labels and tab text (3.3, 3.5) | NFR-UI-06, 07 | Some text looks under 11 px and some targets look under 44 x 44 px. I cannot measure this from a PDF render | Check sizes and tap targets in Figma | Hamna |
| 12 | Figure 3.2 shows a real-looking personal email in the form | Privacy | A real address is visible in the SRS | Replace with a placeholder such as name@example.com | Hamna |
| 13 | Figure 3.5 caption reads "Containers,QR-Scanner, Bilingual Menu" | Document quality | Typo and unclear caption | Retitle "Filters, QR scanner and bilingual menu" | Hamna |

## Missing screens

Hamna designs all of these (plan Section 7.3, screens 3 to 6 and 9 to 21): 4-step onboarding (language, 10 allergens, calorie goal, diet type), the three allergen banners and the blocked-dish screen, the dish AR view with nutrition sheet and ingredient highlight, "I ate this" confirm and undo with the daily intake summary, profile and language edit, a hunger-level control (1 to 5), and the error states (camera or mic denied, Urdu voice unavailable, model failed to load, data unavailable).

## Needs supervisor decision

1. Google sign-in (row 8).
2. Whether any of favourites, prices, the calorie filter or dark mode should be kept as a scope change (rows 2, 3, 5, 6). Each needs supervisor and team approval and an SRS version increment.
