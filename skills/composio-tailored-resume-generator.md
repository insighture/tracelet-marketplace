---
name: tailored-resume-generator
description: Analyzes job descriptions and generates tailored resumes that highlight relevant experience, skills, and achievements — optimized for ATS and human reviewers.
kind: skill
---

# Tailored Resume Generator

Customizes your resume for specific job postings, emphasizing relevant experience and optimizing for ATS (Applicant Tracking Systems).

## When to Use This Skill

- Applying for a specific job position
- Customizing your resume for different industries or roles
- Highlighting relevant experience for career transitions
- Optimizing your resume for ATS keyword matching
- Creating multiple resume versions for different applications

## How to Use

### Basic Usage

```
I'm applying for this job:

[paste job description]

Here's my background:
- 5 years as software engineer at TechCorp
- Led team of 3 developers on mobile app project
- Expert in Python, JavaScript, React
- Computer Science degree from State University
```

### With Existing Resume

```
Please tailor my resume for this position:

Job Description: [paste job description]
My Current Resume: [paste resume]
```

### Career Transition

```
I'm transitioning from marketing to product management.
Here's the job I'm applying for: [paste job description]
My transferable experience: [describe relevant experience]
```

## How This Skill Works

### 1. Analyze Job Requirements

Extracts and prioritizes:
- **Must-have qualifications**: Years of experience, required skills, education
- **Key skills**: Technical tools, methodologies, competencies
- **ATS keywords**: Repeated terms and phrases for optimization
- **Company values**: Cultural fit indicators

### 2. Map Experience to Requirements

For each job requirement:
- Identifies matching experience
- Finds transferable skills if no direct match
- Notes gaps to address or de-emphasize

### 3. Structure the Tailored Resume

**Professional Summary**: Leads with years of experience, top skills, industry fit

**Skills Section**: Groups by category matching job requirements, exact terminology from job description

**Professional Experience**: 
- Emphasizes responsibilities aligned with job requirements
- Quantifies achievements (numbers, percentages, scale)
- Uses action verbs: Led, Developed, Implemented, Optimized, Analyzed
- Format: `[Action Verb] + [What] + [How] + [Result]`

### 4. Optimize for ATS

- Standard section headings
- Keywords from job description woven in naturally
- Both acronyms and full terms (e.g., "SQL (Structured Query Language)")
- Plain formatting — no tables, graphics, headers/footers

## Example

**Input**: Senior Data Analyst role requiring SQL, Python, visualization, A/B testing, healthcare preferred. Candidate has 5 years at RetailCo plus 1-year healthcare internship.

**Output excerpt**:
```markdown
# JOHN DOE
john.doe@email.com | (555) 123-4567

## PROFESSIONAL SUMMARY
Results-driven Data Analyst with 5+ years leveraging SQL, Python, and
advanced visualization tools to deliver actionable insights. Proven track
record in statistical analysis, A/B testing, and cross-functional
collaboration. Healthcare industry experience.

## TECHNICAL SKILLS
- **Analysis & Programming**: SQL, Python, Statistical Analysis, A/B Testing
- **Visualization**: Tableau, Power BI, Dashboard Development

## PROFESSIONAL EXPERIENCE

**Data Analyst** | RetailCo | 2019-2024
- Designed 50+ SQL queries and Python automation scripts, reducing
  manual processing time by 60%
- Conducted A/B testing and statistical analysis improving campaign ROI by 35%
- Presented analytical findings to executive leadership quarterly
```

## After the Resume

Also provides:
- **Strengths analysis**: What makes this candidate competitive
- **Gap analysis**: Requirements not fully met + how to address them
- **Interview preparation tips**: Key talking points and stories to prepare
- **Cover letter hooks**: 2-3 suggested opening lines

## Special Considerations

| Profile | Approach |
|---------|---------|
| Career changers | Functional format, transferable skills, compelling narrative |
| Recent graduates | Lead with education, include projects and GPA if 3.5+ |
| Senior executives | Executive summary, strategic impact, revenue growth |
| Technical roles | Prominent skills section, GitHub/portfolio links |

## Best Practices

- Be truthful — never fabricate experience
- Quantify achievements with specific metrics
- Keep to 1 page (<10 years) or 2 pages (10+ years)
- Generate separate tailored versions for each role

*Source: github.com/ComposioHQ/awesome-claude-skills*
