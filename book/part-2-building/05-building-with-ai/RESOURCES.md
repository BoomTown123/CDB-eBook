# Chapter 5: Building with AI -- Resources

> Curated resources for deeper exploration of topics covered in this chapter.

## Frameworks from This Chapter

- [8 Patterns for Effective AI Coding](../../../frameworks/8-patterns-for-ai-coding.md) -- Context first, concrete examples, iterative refinement, architecture ownership, test-driven prompting, error escalation, checkpoint commits, and ruthless review.

## Tools & Platforms

### AI Coding Tools -- Inline Autocomplete (Level 1)
- [GitHub Copilot](https://github.com/features/copilot) -- 88% of accepted suggestions survive to production; 30% acceptance rate; 55% faster task completion.
- [JetBrains AI](https://www.jetbrains.com/ai/) -- AI assistant integrated into IntelliJ, PyCharm, and other JetBrains IDEs.

### AI Coding Tools -- IDE Integration (Level 3)
- [Cursor](https://www.cursor.com/) -- AI-native code editor; supports Claude, GPT, and Gemini; Cursor 2.0 supports 8 simultaneous agents.
- [Windsurf (Codeium)](https://codeium.com/) -- AI-native code editor with conversational refinement capabilities.

### AI Coding Tools -- Agentic (Level 4)
- [Claude Code](https://code.claude.com/) -- Terminal-based agentic coding; plan mode, subagents for parallel execution, hooks for review checkpoints.
- [Devin (Cognition Labs)](https://www.cognition.ai/) -- Autonomous AI software engineer; used by Goldman Sachs, Santander, Nubank; 20x efficiency on security fixes.

### AI Coding Tools -- Orchestration (Level 5)
- [GitLab Duo Agent Platform](https://about.gitlab.com/) -- Multi-agent orchestration; went GA in January 2026.

### AI Coding Infrastructure
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) -- 10,000+ active servers, 97 million monthly SDK downloads; standard for AI-tool integration.
- [AGENTS.md](https://github.com/anthropics/claude-code/blob/main/AGENTS.md) -- Convention for AI agent instructions; appears in 60,000+ open source projects.
- [Supabase MCP](https://supabase.com/) -- Database operations through MCP; create branches, test migrations, apply to production in a single conversation.
- [Remotion](https://www.remotion.dev/) -- React video creation; Claude Code skill teaches animation APIs for programmatic video generation.

### Chat Interfaces
- [Claude.ai](https://claude.ai/) -- Architecture discussions and learning new frameworks.
- [ChatGPT](https://chat.openai.com/) -- General AI conversations and code generation.

## Further Reading

- [Accenture Developer Productivity Report 2025](https://www.accenture.com/us-en/insights/technology/developer-productivity-ai) -- 50,000 developers; 8.69% increase in pull requests, 84% more successful builds.
- [Builder.io: AI-Assisted Development Workflows](https://www.builder.io/blog/ai-coding-workflows) -- "Plan, Test, Code, Review" cycle with human checkpoints every 10-15 minutes.
- [Cognition Labs: Enterprise Deployment Case Studies](https://www.cognition.ai/blog/enterprise-results) -- Goldman Sachs, Santander, Nubank: 5-10% developer time savings; 20x efficiency on security fixes.
- [Anthropic: Claude Code Agent Skills Standard](https://code.claude.com/docs/en/skills) -- Open standard for cross-platform skill definitions (December 2025); SKILL.md format.
- [GitHub Blog: OpenAI GPT-4.1 in Copilot](https://github.blog/changelog/2025-04-14-openai-gpt-4-1-now-available-in-public-preview-for-github-copilot-and-github-models/) -- How established tools migrate between models transparently.

## Research & Data

- [METR AI Coding Tool Productivity Study](https://metr.org/research/) -- Developers 19% slower with AI tools on mature codebases; 55% report worse understanding of agent-generated code.
- [GitHub Copilot Impact Study](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/) -- 88% of accepted characters make it into final code; 78% task completion rate.
- [McKinsey: Unleashing Developer Productivity with Generative AI](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai) -- Teams without training saw 60% lower productivity gains from AI coding tools.
- [Deloitte AI Institute: State of Agentic AI 2025](https://www2.deloitte.com/us/en/insights/focus/tech-trends.html) -- 95% of enterprise multi-agent pilots fail to meet stated objectives.
- [Contrary Research: AI Coding Tools Analysis](https://research.contrary.com/reports/ai-coding) -- Level 4 agents: 35% task correctness improvement, 50% effort reduction, 60% task completion rate.
- [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/) -- 49% of organizations use multiple AI coding tools; 26% pair Copilot with Claude.
- Security data: Only 55% of AI-generated code is secure; 86% XSS vulnerability rate in AI-generated code.
- Technical debt: Code blocks with 5+ duplicated lines increased 8x since AI adoption; code churn doubled from 3-4% to 7%.
- Hallucinated dependencies: Of 2.23 million code references analyzed, 440,445 contained hallucinated dependencies; 43% repeated enough for attackers to exploit.

## Community & Learning

- [ZoomInfo AI Development](https://www.zoominfo.com/) -- 400+ developers seeing 6,500 daily suggestions with 33% acceptance rate.
- [Skywork AI](https://skywork.ai/) -- Turned a 6-month roadmap into 3 weeks using the Human-AI Development Loop.

### The 5 Levels of AI-Assisted Development

| Level | Name | Example Tools | Key Metric |
|-------|------|---------------|------------|
| 1 | Autocomplete | GitHub Copilot inline | 88% survive to production |
| 2 | Generation | Chat interfaces | 8.69% more PRs (Accenture) |
| 3 | Iteration | Cursor, Windsurf | 10-15 min human checkpoints |
| 4 | Agents | Claude Code, Devin | 20x efficiency on targeted tasks |
| 5 | Orchestration | GitLab Duo, Cursor 2.0 | 95% of enterprise pilots fail |

### Progression Guidance

- Progress one level every 2-4 weeks for durable capability
- Jumping two levels in a week causes regression within a month
- Level 3 to Level 4 is the biggest jump -- requires shift from implementer to architect/reviewer
- Invest 6-12 weeks accepting slower initial output to build review skills at Level 4
