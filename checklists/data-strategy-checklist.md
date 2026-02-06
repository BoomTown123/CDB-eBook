# Checklist: Building Your Data Strategy

Use this checklist when designing a data strategy for an AI-first product, evaluating an existing data pipeline, or assessing whether your data creates a defensible competitive advantage. It draws from the six data strategy failure patterns, the data flywheel framework, and the data moats assessment from Chapter 9.

## Data Collection

- [ ] You have validated product-market fit before investing in data infrastructure
- [ ] Define collection targets by what improves the model, not by what's easiest to capture
- [ ] Capture signals from production systems and real user interactions, not just synthetic or test data
- [ ] You have identified the specific edge cases your collection pipeline needs to surface (e.g., Tesla's 0.01% automatic edge case detection)
- [ ] Internal users provide continuous usage data to seed the system before external launch
- [ ] Collection covers all five flywheel components: collection, storage, analysis, application, and feedback
- [ ] You know the point at which adding more data stops improving model performance

## Data Quality

- [ ] Data accuracy is measured and tracked over time (U.S. average declined from 63.5% to 26.6% between 2021-2024)
- [ ] Automated checks detect duplicates, outliers, and missing values in incoming data
- [ ] Schema changes (missing columns, altered formats) trigger alerts, not silent failures
- [ ] Data drift detection monitors shifts in input distributions
- [ ] Model performance is tracked across segments over time, not just in aggregate
- [ ] Your team spends more time training than cleaning---if not, collection standards need tightening
- [ ] AI-generated content is flagged and excluded from training sets to prevent model collapse

## Flywheel Design

- [ ] You can map your data flow through all five components: Collection, Storage, Analysis, Application, Feedback
- [ ] The break point in your flywheel is identified (typically between storage-analysis or analysis-application)
- [ ] Your system has network learning, not just individual learning (deleting one user's data would affect other users' experience)
- [ ] Insights from analysis translate into shipped product improvements, not slide decks
- [ ] Feedback loops measure whether improvements actually generate more and better data
- [ ] Deployment velocity is measured---you can ship, measure, and iterate within days, not months
- [ ] Cold start strategy is defined: expert seeding, targeting complexity over volume, or building the loop architecture before data arrives
- [ ] You have tested whether your flywheel compounds over time or plateaus after initial gains

## Moat Assessment

- [ ] Every data asset considered a competitive advantage has been run through the Moat Test:
  - [ ] Can a competitor buy this data?
  - [ ] Can they scrape it?
  - [ ] Can they partner for it?
  - [ ] Does usage generate more of it?
  - [ ] Is it embedded in customer workflows?
- [ ] You distinguish between data you possess (commodity) and data your system generates through usage (compounding advantage)
- [ ] Don't treat static datasets as durable moats---recognize them as depreciating assets
- [ ] Your moat strategy focuses on at least one of: workflow integration, execution velocity, or systems of intelligence
- [ ] The five conditions for defensible data are evaluated:
  - [ ] Continuous refreshment through usage
  - [ ] High-quality domain specificity with intelligent curation
  - [ ] Data governance that creates procurement advantage
  - [ ] Deep workflow integration that creates switching costs
  - [ ] Network effects that compound with each user

## Infrastructure

- [ ] Infrastructure complexity matches your current stage, not your aspirational scale
- [ ] You can name the specific bottleneck each infrastructure component solves
- [ ] Teams don't spend days or weeks configuring infrastructure for each new workload
- [ ] Multi-provider strategies with fallback options are in place before reaching production scale
- [ ] Systems can switch between AI providers or degrade gracefully during outages
- [ ] Data is accessible across teams, not siloed in department-specific stores
- [ ] Unit economics are viable: margins are above 40% (AI wrappers average 25-60% vs. traditional SaaS at 70-90%)

## Governance

- [ ] Data collection complies with applicable privacy regulations (EU AI Act, industry-specific requirements)
- [ ] Consent and data usage terms are clear to users and legally reviewed
- [ ] Audit trails exist for how data flows through the system and into model training
- [ ] Access controls define who can read, write, and delete training data
- [ ] Data retention and deletion policies are documented and enforced
- [ ] Governance architecture anticipates regulatory tightening rather than reacting to it
- [ ] Compliance capabilities are treated as competitive advantage in enterprise procurement, not just a cost center

---

**Source frameworks:**
- [The 6 Data Strategy Mistakes That Stall Flywheels](../frameworks/6-data-strategy-mistakes.md)
- [Building Data Flywheels](../frameworks/data-flywheel.md)
- [Data Moats: What's Defensible vs. Replicable](../frameworks/data-moats.md)

**Full chapter:** [Chapter 9: Data Strategy](../book/part-3-operating/09-data-strategy/README.md)
