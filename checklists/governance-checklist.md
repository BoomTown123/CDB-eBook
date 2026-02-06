# Checklist: AI Governance Readiness

Use this checklist when establishing or auditing your AI governance. Work through each category sequentially---permission models and risk assessment inform your governance structure, which drives compliance and monitoring.

*Derived from the [Permission Model Framework](../frameworks/permission-model-framework.md), [7 AI Risks and Mitigations](../frameworks/7-ai-risks-and-mitigations.md), and [AI Governance Framework](../frameworks/ai-governance-framework.md) --- Chapter 11: Ethics, Governance, and Risk.*

---

## Permission Model Setup

- [ ] Audit every AI system currently in operation and map each to a permission mode: Auto, Approved-Tools, or Ask-Every-Time
- [ ] For each system, evaluate the four selection questions: blast radius, recoverability, evidence base, and regulatory expectations
- [ ] Confirm that all new AI systems start at Ask-Every-Time and have documented criteria for graduating to each successive level
- [ ] Define measurable thresholds for mode transitions (e.g., financial impact under $5K for Auto, $5K--$50K for Approved-Tools, over $50K for Ask-Every-Time)
- [ ] Document each permission decision in writing: current mode, rationale, triggers for mode change (up or down), and who approves changes
- [ ] Verify that any system running with more autonomy than its risk profile warrants has a plan to add controls
- [ ] Establish an incident regression policy: on incident, regress one permission level immediately and investigate root cause before re-earning autonomy

## Risk Assessment

- [ ] **Hallucination:** Implement guardrail systems that intercept AI outputs before users see them, and deploy RAG to ground responses in verified documents
- [ ] **Bias and Discrimination:** Conduct algorithmic impact assessments before deployment and test across demographic groups using fairness metrics (target 80% parity or better)
- [ ] **Privacy Leakage:** Deploy data loss prevention integrated with AI interfaces, mandate zero-data-retention vendor contracts, and use tokenization to anonymize data before processing
- [ ] **Prompt Injection:** Implement AI firewalls analyzing prompts before they reach models, deploy canary tokens, and consider dual-model architectures for policy validation
- [ ] **Model Drift:** Deploy continuous monitoring tracking prediction distributions and outcome accuracy, with automated retraining triggered when accuracy drops below threshold (5% below baseline)
- [ ] **Security Vulnerabilities:** Implement zero-trust AI architecture (API authentication, rate limiting, input validation, model access logging) and create an AI bill of materials documenting model dependencies
- [ ] **Regulatory Non-Compliance:** Implement NIST AI RMF's four functions (Govern, Map, Measure, Manage), deploy model cards for all production systems, and schedule regular third-party audits against ISO 42001

## Governance Structure

- [ ] Establish First Line (team-level) decision rights: research leads and product managers approve low-risk experiments and internal tools without committee review
- [ ] Establish Second Line (working group) with Risk Management and Legal reviewing medium-risk deployments, bias audits, and EU AI Act compliance
- [ ] Establish Third Line (AI Ethics Board or equivalent committee) with genuine authority to approve, modify, or terminate high-risk AI projects
- [ ] Define board-level escalation for frontier AI decisions, regulatory strategy, and major incidents
- [ ] Create RACI matrices for your most common AI deployment scenarios (Responsible, Accountable, Consulted, Informed)
- [ ] Assign ethics focal points in each business unit for first-line decisions
- [ ] Document escalation thresholds by financial impact, data sensitivity, and regulatory classification before they are needed

## Compliance

- [ ] Identify all AI systems that fall under EU AI Act high-risk classifications (credit decisions, healthcare diagnostics, employment screening, law enforcement)
- [ ] Ensure high-risk classified systems require committee-level approval regardless of financial impact
- [ ] Deploy model cards documenting training data, performance metrics, and known limitations for every production AI system
- [ ] Verify human oversight requirements are met for all systems handling PII or protected-class data
- [ ] Maintain documentation sufficient to satisfy auditors, regulators, and legal review ("documented risk assessment and evidence" rather than informal judgment)
- [ ] Track regulatory landscape changes and update governance framework accordingly---annual review cycles are too slow for AI

## Monitoring and Audit

- [ ] Schedule quarterly reviews of all permission model assignments as systems and regulatory landscape evolve
- [ ] Implement continuous monitoring of model performance against baseline accuracy targets (maintain within 95% of initial deployment)
- [ ] Track false positive rates across all AI systems (target: reduce from 35% to under 5% for guardrail-equipped systems)
- [ ] Conduct regular third-party audits of AI systems against ISO 42001 and NIST AI RMF
- [ ] Monitor for over-governance signals: if governance only blocks and never enables, it isn't working
- [ ] Review whether governance committees are making timely decisions---teams spending more than 50% of time on governance activities signals process failure
- [ ] Maintain audit trail of all mode changes, incident regressions, and re-escalations
