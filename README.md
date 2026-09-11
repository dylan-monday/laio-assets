# LA.IO Assets

The LA.IO (Louisiana Innovation Office) brand system, served as public files at https://assets.la.io. Maintained by Monday + Partners.

## What is here

+ **https://assets.la.io/ai** is the Brand Kit for AI: setup for Claude, Claude Design, Claude Code, Cowork, Lovable, and any other AI, plus the brand summary and every asset URL. Source: `ai/`.
+ **https://assets.la.io/llms.txt** is the same inventory as a plain list for agents and crawlers.
+ `fonts/`, `logos/`, `motifs/` and `colors/` hold the brand files, served with open CORS so they load on any domain.
+ `labs/` is the Louisiana Innovation Labs identity kit.
+ `/illustrator` is the Illustration Machine, a separate app proxied in from its own project.

## How it works

There is no framework and no server-side build. Vercel serves the files as they are. The pages are generated locally by `_build/gen_pages.py` and committed; `_build/` itself is not deployed.

```
python3 _build/gen_pages.py
```

Merging to `main` deploys. Work on a branch and open a pull request.

## Where to read more

+ `CLAUDE.md`: how the repo and the deployment work, the house rules, and the history. Written for anyone, person or AI, making changes.
+ `ai/README.md`: the brand kit folder, file by file.
+ `_build/README.md`: the page generator, the font build, and the Labs logo kit.
