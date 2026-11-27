# Framework Party

A mobile-friendly IT0049 study space for CodeIgniter and Laravel.

## Reviewer Notes

Open [`reviewer.html`](reviewer.html) from the **Reviewer Notes** tab for a continuous reading version: roughly 17,000 words including code, 55 sections covering all 300 PDF pages, 11 figures, 107 code examples, highlighted takeaways, tables, and original PDF page links. Each module adds term-and-meaning lists and three worked situations. The notes preserve the original explanations while separating dense text into lists and steps. All eight chapters remain open; there are no quizzes, answer reveals, or study-state controls in this document. The existing study website and original slides are preserved.

The notes are static HTML, readable without JavaScript, mobile friendly, and styled for browser printing. They follow the classroom PDFs and explicitly label corrections, prerequisites, and additional explanations. Official documentation links support those clarifications.

## A quieter interface

The home screen offers Study and Practice. The lesson library shows one module at a time. Additional practice modes, references, progress, appearance, and the timer are available on demand. All 31 lessons, 93 recall prompts, 480 practice questions, and 300 original slides remain intact.

## Study your way

- **Original slides:** all 300 pages of the eight course modules, with enlarged screenshots, extracted text, bookmarks, and studied-page marks.
- **Guided study:** 31 rewritten lessons with small explanations, memory cues, worked examples, and 93 self-assessed recall checks. An in-app review list returns topics after increasing intervals.
- **Practice:** 480 questions with explanations and original PDF page references, including 24 applied checks per module, across practice quizzes, typed recall, flashcards, training loops, timed rehearsals, and an ordered practice path.
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

The editable note chapters are in notes-source/. Rebuild reviewer.html with python tools/build_reviewer.py. The generator requires Python markdown-it-py and Node.js. It applies syntax colors during generation, so the complete notes remain readable without JavaScript.

Each module contains 60 questions. The Practice screen permits 1–60 questions per new session, including the optional practice modes. Revised questions receive versioned IDs. Previous answers do not count as attempts on a changed question. The app keeps session history, original-slide progress, and unchanged question records. A saved session that contains a retired question closes safely.

## Application practice and code colors

The questions test concepts and decisions. They do not ask students to remember arbitrary slide labels, demo credentials, or the number of sample records. Situations cover request routing, query results, validation failures, missing records, file replacement, access checks, and notification conditions. The notes explain the same reasoning with new examples. The supplied modules define the course scope.

The canonical bank is `tools/question-bank.json`. Rebuild the deployed data with `python tools/expand_questions.py`. The script preserves the module data and uses the reviewed bank instead of generating slide-recall questions.

Code examples use locally bundled PrismJS 1.30.0. The MIT license is in `assets/prism/LICENSE`. The shared renderer supports PHP, Blade, HTML, SQL, shell commands, environment settings, and Apache configuration. Syntax tokens distinguish keywords, variables, functions, strings, numbers, and comments. Both appearance modes use readable token contrast. Normal answer text uses the body font; code uses a monospace font.

Run the content checks after edits:

```sh
node tools/check_question_bank.cjs
node tools/check_code_format.cjs
python tools/check_reviewer.py
```

The checks verify the canonical bank, 60 questions and 24 applied checks per module, unique answers, PDF references, code escaping, Blade tokens, and exact source text in all 107 rendered code examples. Browser checks cover answer feedback, session completion, the 60-question limit, retired sessions, retained slide progress, dynamic lesson code colors, and mobile code scrolling.
