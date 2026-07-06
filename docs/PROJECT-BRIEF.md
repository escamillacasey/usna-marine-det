# USNA Marine Detachment Website — Project Brief

## Background

Modernization of the United States Naval Academy (USNA) Marine Detachment website. Development happens locally with modern practices, then finished HTML/CSS/JavaScript is pasted into Hannon Hill Cascade CMS for publishing.

**Live sites being merged:**
- https://www.usna.edu/Marines (detachment hub — leadership, training, mentors)
- https://www.usna.edu/MarineCorps (Marine Corps roles, mission, benefits)

Eventually these will be a single site; one URL will be pruned.

## Goals

1. Clean, responsive homepage as the foundation
2. Reusable navigation, layout, and styling components
3. Semantic HTML5, modern CSS, lightweight vanilla JavaScript
4. Mobile-friendly and accessible
5. Cascade CMS–compatible (paste-in ready, minimal modification)
6. Consistent styling site-wide
7. Performance and simplicity over unnecessary frameworks

## Constraints

- Published through Cascade CMS
- Cascade may strip custom attributes or JavaScript
- Static site only — no server-side processing
- Minimize external dependencies
- Graceful degradation when Cascade limits features
- **Prefer inline HTML over attachments** — do not link to PDF or Word downloads; migrate document content into the page

## Stack

- HTML5, CSS3, vanilla JavaScript (ES6+)
- Bootstrap only when it meaningfully simplifies layouts
- No React, Angular, Vue, or SPA frameworks

## Design Philosophy

Professionalism, Marine Corps heritage, leadership, academic excellence, simplicity, fast loading, strong typography, responsive layouts, clean navigation. Modern but appropriate for an official DoD/academic organization.

## Cascade Notes

When pasted into Cascade, the USNA global header/footer template typically wraps page content. Local files include a standalone header/footer for preview; mark sections with `<!-- CASCADE: page content start/end -->` comments for copy boundaries.
