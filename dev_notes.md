# Developer Notes for Niner Miner Web Application
This document provides a brief overview of the technical aspects of
the Niner Miner Webapp.
## Basic File Structure
This diagram shows the basic directory structure for the application.

```mermaid
flowchart TD
  A[repo] --> B[src];
  A[repo] --> C[README];
  A[repo] --> D[Dev Notes];
  A[repo] --> E[requirements.txt];
  B[src] -- all backend --> F[main.py];
  B[src] --> G[static];
  B[src] -- edit HTML --> H[templates];
  G[static] -- edit CSS --> I[CSS];
  G[static] -- add fonts --> J[Fonts];
  G[static] -- add images --> K[Images];
```
