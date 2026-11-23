# Framework Party

A mobile-friendly IT0049 study space for CodeIgniter and Laravel.

## Reviewer Notes

Open [`reviewer.html`](reviewer.html) from the **Reviewer Notes** tab for a continuous reading version: roughly 13,900 words including code, 55 sections covering all 300 PDF pages, 11 figures, highlighted takeaways, tables, explained code, and original PDF page links. All eight chapters remain open; there are no quizzes, answer reveals, or study-state controls in this document. The existing study website and original slides are preserved.

The notes are static HTML, readable without JavaScript, mobile friendly, and styled for browser printing. They follow the classroom PDFs and explicitly label corrections, prerequisites, and additional explanations. Official documentation links support those clarifications.

## A quieter interface

The home screen offers Study and Practice. The lesson library shows one module at a time. Additional practice modes, references, progress, appearance, and the timer are available on demand. All 31 lessons, 93 recall prompts, 128 practice questions, and 300 original slides remain intact.

## Study your way

- **Original slides:** all 300 pages of the eight course modules, with enlarged screenshots, extracted text, bookmarks, and studied-page marks.
- **Guided study:** 31 rewritten lessons with small explanations, memory cues, worked examples, and 93 self-assessed recall checks. An in-app review list returns topics after increasing intervals.
- **Practice:** 128 questions with explanations and original PDF page references, across practice quizzes, typed recall, flashcards, training loops, timed rehearsals, and an ordered practice path.
- **Your progress:** saved sessions, a daily question goal, and badges earned from real activity.

Use the palette button in the header to choose **Daydream**, **Lagoon**, or **Peach Club**, with **Light**, **Dark**, or **Auto** appearance. Roomier reading and quiet motion are available there too.

The original course files and the independently written teaching version are kept separate. These materials are a study aid rather than an official examination.

## Run locally

There is no build step or backend dependency. Open `index.html`, or serve this directory:

```sh
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Publishing

This repository is a static GitHub Pages site. Publish `main` from the repository root. `.nojekyll` lets GitHub serve the files directly. All app links and assets use relative paths so deployment under a repository subpath works.

## Progress and preferences

Study activity and appearance preferences are stored in the current browser. Publishing makes the course available on different devices; it does not automatically synchronize their progress. **My progress → Export / Import** transfers a backup, including guided recall drafts and review dates.

The focus timer stays within the page. Guided review dates create an in-app due list, not external notifications. Timed rehearsals continue counting elapsed time while away from the tab.

## Content and assets

Course PDFs are in `modules/`, their rendered slide screenshots are in `slides/`, and teaching content is in the JavaScript data files. Fonts are served locally. Bricolage Grotesque and DM Sans are distributed under the SIL Open Font License; licenses are included in `assets/fonts/`.

## Validation

The practice, guided-study, slide-reader, appearance, and mobile navigation flows were exercised in the browser. All six palette/mode combinations were checked for automated accessibility violations on the home screen. Phone layouts were checked for overflow, readable lesson text, and accessible module selection. Reduced motion and native system appearance are respected.

The editable note chapters are in notes-source/. Rebuild reviewer.html with python tools/build_reviewer.py. The generator requires Python markdown-it-py and Node.js.
