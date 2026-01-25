# PROJECT RESTRUCTURE DIRECTIVE

**From:** CEO  
**To:** CTO Autonomous Brain Team  
**Date:** January 25, 2026  
**Priority:** HIGH  
**Status:** IMMEDIATE ACTION REQUIRED

---

## Reference Project

The project must follow the format and structure of the **QuickNoteJournal** Replit project:

**Reference URL:** https://replit.com/@rhuam/QuickNoteJournal

---

## Required Project Structure

The apex-trade project must be restructured to match the following format:

### Core Application Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application entry point |
| `main.py` | Application bootstrap and initialization |
| `orchestrator.py` | Multi-agent orchestration and coordination |
| `database.py` | Local database operations |
| `firebase_db.py` | Firebase cloud database integration |
| `scoring.py` | Scoring and evaluation logic |

### Required Directories

| Directory | Purpose |
|-----------|---------|
| `.streamlit/` | Streamlit configuration files |
| `neurons/` | AGI/Neural network components |
| `attached_assets/` | Static assets and resources |

### Configuration Files

| File | Purpose |
|------|---------|
| `agi_local_data.json` | Local AGI state and data persistence |
| `pyproject.toml` | Python project dependencies |
| `.replit` | Replit configuration |
| `replit.md` | Project documentation |

---

## Technology Stack Requirements

The restructured project must use:

1. **Python** as the primary language
2. **Streamlit** for the web interface
3. **Firebase** for cloud database
4. **UV package manager** for dependency management
5. **Neural/AGI components** for intelligent processing

---

## Deployment Target

The project must be deployable on **Replit** with:

- Autoscale configuration (4 vCPU / 8 GiB RAM / 3 Max)
- Public visibility
- Production-ready deployment

---

## Action Items

1. Reorganize existing code to match the required structure
2. Implement Streamlit-based UI in `app.py`
3. Create orchestrator for multi-agent coordination
4. Set up Firebase integration
5. Configure for Replit deployment
6. Ensure all components are functional and integrated

---

## Deadline

**This restructure should already be completed.** The project must be in the specified format immediately.

---

## Notes

- All existing functionality must be preserved
- The CTO Autonomous Brain capabilities must be integrated into the new structure
- Cross-session persistence must continue to work
- CEO approval workflows must remain intact

---

*Directive issued by CEO*  
*Compliance is mandatory*
