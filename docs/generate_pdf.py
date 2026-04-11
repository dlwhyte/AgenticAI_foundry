#!/usr/bin/env python3
"""
Generate Student_Quick_Start.pdf for AgenticAI Foundry
Run from repo root: python docs/generate_pdf.py
Requires: pip install reportlab
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

NAVY   = colors.HexColor('#1B2A4A')
ORANGE = colors.HexColor('#F5A623')
LGREY  = colors.HexColor('#F5F5F5')
MGREY  = colors.HexColor('#CCCCCC')
YELLOW = colors.HexColor('#FFF3CD')

def s(name, **kw):
    defaults = dict(fontName='Helvetica', fontSize=9, leading=13,
                    textColor=colors.black, spaceAfter=4)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

TITLE  = s('T',  fontName='Helvetica-Bold', fontSize=28, textColor=colors.white,
           alignment=TA_CENTER, spaceAfter=4)
SUB1   = s('S1', fontSize=14, textColor=colors.white, alignment=TA_CENTER)
SUB2   = s('S2', fontName='Helvetica-BoldOblique', fontSize=11,
           textColor=colors.white, alignment=TA_CENTER)
H1     = s('H1', fontName='Helvetica-Bold', fontSize=15, textColor=NAVY,
           spaceBefore=14, spaceAfter=4)
H2     = s('H2', fontName='Helvetica-Bold', fontSize=12, textColor=NAVY,
           spaceBefore=10, spaceAfter=3)
BODY   = s('B')
BOLD   = s('Bb', fontName='Helvetica-Bold')
CODE   = s('C',  fontName='Courier', fontSize=8.5, backColor=LGREY,
           borderPadding=4, leading=12)
NOTE   = s('N',  fontName='Helvetica-Oblique', textColor=NAVY, leftIndent=10)
FOOT   = s('F',  fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
BULLET = s('Bu', leftIndent=15, bulletIndent=5)

def tbl(data, widths, header_bg=NAVY):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), header_bg),
        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGREY]),
        ('GRID',         (0,0), (-1,-1), 0.5, MGREY),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
    ]))
    return t

def p(text, style=None):
    return Paragraph(text, style or BODY)

def build(filename='Student_Quick_Start.pdf'):
    doc = SimpleDocTemplate(filename, pagesize=letter,
        rightMargin=0.75*inch, leftMargin=0.75*inch,
        topMargin=0.5*inch,  bottomMargin=0.5*inch,
        author='MIT Professional Education',
        subject='Applied Generative AI for Digital Transformation',
        title='AgenticAI Foundry - Student Quick Start Guide')

    W = 7*inch
    story = []

    # ── PAGE 1: Cover + Module Overview ──────────────────────────────────────
    hdr = Table([
        [p('AgenticAI Foundry', TITLE)],
        [p('Student Quick Start Guide', SUB1)],
        [p('MIT Professional Education  |  Applied Generative AI for Digital Transformation', SUB2)],
    ], colWidths=[W])
    hdr.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), NAVY),
        ('BACKGROUND',(0,1),(-1,2), ORANGE),
        ('TOPPADDING',(0,0),(-1,0), 18), ('BOTTOMPADDING',(0,0),(-1,0), 14),
        ('TOPPADDING',(0,1),(-1,1),  8), ('BOTTOMPADDING',(0,1),(-1,1),  4),
        ('TOPPADDING',(0,2),(-1,2),  4), ('BOTTOMPADDING',(0,2),(-1,2), 12),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ]))
    story += [hdr, Spacer(1, 0.2*inch),
              p('This guide gets you from zero to running the course demos in the shortest possible time.'),
              Spacer(1, 0.05*inch), p("What's Included", H1)]

    modules = [
        ['Demo', 'Module', 'What You Will Learn', 'API Key?'],
        ['LLM Cost Explorer',      'Module 1', 'Why the same AI task can cost $1 or $230 depending on model choice', 'No'],
        ['Multi-Agent Demo',       'Module 2', 'How three AI agents collaborate like a team (CrewAI)',               'Optional'],
        ['LangChain Agent Demo',   'Module 2', 'How a single agent uses tools to answer questions in real time',     'Optional'],
        ['MCP Explorer',           'Module 3', 'How AI agents connect to external tools (calendars, CRMs, etc.)',   'No'],
        ['Agent Security Demo',    'Module 4', 'Prompt injection attacks and defense-in-depth guardrails',           'Demo: No / Live: Optional'],
        ['Human-in-the-Loop Demo', 'Module 5', 'Patterns for keeping humans in control of AI decisions',            'No'],
    ]
    story.append(tbl([[p(c, BOLD if i==0 else BODY) for c in r] for i,r in enumerate(modules)],
                     [1.4*inch, 0.85*inch, 3.35*inch, 1.4*inch]))
    story += [Spacer(1,0.08*inch),
              p('<i>Modules 1, 3, 4, and 5 work immediately - no account, no API key. '
                'Module 2 needs Ollama (free, local) or an OpenAI API key.</i>', NOTE),
              Spacer(1,0.12*inch),
              p('Step 0 - Get the Code (Both Paths)', H1),
              p('You need a copy of this repository on your computer before doing anything else.'),
              Spacer(1,0.05*inch)]

    get_code = [
        [p('<b>Option 1: Download ZIP</b> (easiest)', BOLD), p('<b>Option 2: Clone with Git</b>', BOLD)],
        [p('1. Click the green &lt;&gt; Code button on GitHub<br/>'
           '2. Click Download ZIP<br/>'
           '3. Find it in Downloads and extract it'),
         p('<font name="Courier" size="8">git clone https://github.com/dlwhyte/AgenticAI_foundry.git</font>')],
    ]
    gc = Table(get_code, colWidths=[3.5*inch, 3.5*inch])
    gc.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.5,MGREY),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),
    ]))
    story += [gc, Spacer(1,0.08*inch),
              p('<b>Which path?</b> "Have I used Docker before, or am I comfortable installing a new app?"'),
              p('Yes -> Path A: Docker (recommended)     No -> Path B: Python'),
              p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 1', FOOT)]

    # ── PAGE 2: Path A - Docker ───────────────────────────────────────────────
    story.append(PageBreak())
    story += [p('Path A: Docker (Recommended)', H1),
              p('Docker packages the entire app into a self-contained box. Runs identically on Windows, Mac, '
                'and Linux. Time: ~20 minutes first time, under 1 minute after that.')]

    docker = [
        ['Step', 'Action', 'Command / Detail'],
        ['1', 'Install Docker Desktop',
         'Windows/Mac: docker.com/products/docker-desktop
Linux: see docs/DOCKER_GUIDE.md'],
        ['2', 'Open a Terminal',
         'Windows: Win+R > powershell
Mac: Cmd+Space > Terminal
Linux: Ctrl+Alt+T'],
        ['3', 'Navigate to project folder',
         'cd path/to/AgenticAI_foundry
(Tip: drag the folder onto the terminal window)'],
        ['4', 'Build the app (one-time)',
         'docker build -t agenticai-foundry .'],
        ['5', 'Run the app',
         'docker run -p 8501:8501 agenticai-foundry'],
        ['6', 'Open in browser',
         'http://localhost:8501'],
        ['7', 'Stop the app',
         'Press Ctrl+C in the terminal'],
    ]
    story.append(tbl(
        [[p(r[0],BOLD if i==0 else BODY), p(r[1],BOLD if i==0 else BOLD),
          p(r[2].replace('\n','<br/>'), BOLD if i==0 else BODY)]
         for i,r in enumerate(docker)],
        [0.45*inch, 1.6*inch, 4.95*inch]))

    story += [Spacer(1,0.1*inch), p('Docker Troubleshooting', H2)]
    trouble = [
        ['Problem', 'Solution'],
        ['"Docker command not found"',     'Make sure Docker Desktop is open and running'],
        ['"Cannot connect to daemon"',     'Open Docker Desktop; wait for the whale icon to stop animating'],
        ['"Port 8501 is already in use"',  'Run: docker run -p 8502:8501 agenticai-foundry  then open :8502'],
        ['Build seems stuck',              'Wait - first build downloads ~500MB, can take 5+ min on slow connections'],
    ]
    story.append(tbl([[p(c, BOLD if i==0 else BODY) for c in r] for i,r in enumerate(trouble)],
                     [2.5*inch, 4.5*inch]))
    story += [Spacer(1,0.06*inch),
              p('For more detail see docs/DOCKER_GUIDE.md in the repo.', NOTE),
              p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 2', FOOT)]

    # ── PAGE 3: Path B - Python ───────────────────────────────────────────────
    story.append(PageBreak())
    story += [p('Path B: Python', H1),
              p('Run the app directly. More steps involved but full code visibility. Time: ~15 minutes.'),
              p('<b>Check Python first:</b> run <font name="Courier">python3 --version</font> in a terminal. '
                'If 3.9 or lower - use Docker instead. CrewAI (Module 2) needs Python 3.10+.'),
              Spacer(1,0.06*inch)]

    pysteps = [
        ['Step', 'Action', 'Detail'],
        ['1', 'Install Python 3.10+',
         'Check: python3 --version
If 3.9 or lower: download from python.org/downloads
Windows: check "Add Python to PATH" during install'],
        ['2', 'Open terminal & navigate',
         'See Docker Path Steps 2-3 for how to open a terminal and cd to the folder'],
        ['3', 'Install dependencies
(REQUIRED)',
         'pip3 install -r requirements.txt
pip3 install -r requirements-crewai.txt
(Run BOTH commands. Takes 2-5 minutes each.)'],
        ['4', 'Run the app',
         'python3 -m streamlit run Home.py
Browser opens to http://localhost:8501 automatically'],
        ['5', 'Stop the app', 'Press Ctrl+C'],
    ]
    story.append(tbl(
        [[p(r[0].replace('\n','<br/>'),BOLD if i==0 else BODY),
          p(r[1].replace('\n','<br/>'),BOLD if i==0 else BOLD),
          p(r[2].replace('\n','<br/>'),BOLD if i==0 else BODY)]
         for i,r in enumerate(pysteps)],
        [0.65*inch, 1.55*inch, 4.8*inch]))

    warn = Table([[p('<b>Important:</b> Step 3 requires running TWO pip commands, not one. '
                    'The second file (requirements-crewai.txt) contains CrewAI, LangChain, and agent '
                    'dependencies. Skipping it will cause Module 2 to crash with ModuleNotFoundError.')]], 
                 colWidths=[W])
    warn.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),YELLOW),
        ('BOX',(0,0),(-1,-1),1,ORANGE),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    story += [Spacer(1,0.08*inch), warn, Spacer(1,0.1*inch), p('Python Troubleshooting', H2)]

    pytrouble = [
        ['Problem', 'Solution'],
        ['"pip not found"',              'Try pip3 install -r requirements.txt instead'],
        ['"streamlit not found"',        'Try python -m streamlit run Home.py'],
        ['"Permission denied"',          'Add --user: pip install --user -r requirements.txt'],
        ['Browser does not open',        'Manually go to http://localhost:8501'],
        ['Module 2 crashes on import',   'Make sure you ran BOTH pip install commands in Step 3'],
    ]
    story.append(tbl([[p(c,BOLD if i==0 else BODY) for c in r] for i,r in enumerate(pytrouble)],
                     [2.5*inch, 4.5*inch]))
    story.append(p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 3', FOOT))

    # ── PAGE 4: Module 2 Setup + What to Expect ───────────────────────────────
    story.append(PageBreak())
    story += [p('Setting Up the Agent Demos (Module 2)', H1),
              p('Modules 1, 3, 4, and 5 work immediately with no setup. '
                'For Module 2 (Multi-Agent and LangChain Agent demos) you need an AI model:'),
              Spacer(1,0.06*inch), p('Option A: Ollama - Free, runs locally, no account needed', H2)]

    ollama = [
        ['Step', 'Command'],
        ['1. Install Ollama',    'Download from ollama.ai'],
        ['2. Download a model',  'ollama pull llama3.2  (2GB one-time download)'],
        ['3. Start Ollama',      'ollama serve  (keep this terminal open)'],
        ['4. Run the app',       'Use Docker or Python path, then select Ollama in the app sidebar'],
    ]
    story.append(tbl([[p(r[0],BOLD if i==0 else BOLD), p(r[1],BOLD if i==0 else BODY)]
                      for i,r in enumerate(ollama)], [2.3*inch, 4.7*inch]))
    story += [p('The model download is ~2GB. Do this on a good internet connection.', NOTE),
              Spacer(1,0.08*inch),
              p('Option B: OpenAI - Paid, faster results (~$0.01 per demo run)', H2),
              p('Create an account at platform.openai.com and get an API key. '
                'Enter it in the app sidebar - no environment setup needed.'),
              Spacer(1,0.1*inch),
              HRFlowable(width='100%', thickness=0.5, color=MGREY),
              Spacer(1,0.1*inch),
              p("What to Expect When It's Working", H1),
              p('Open http://localhost:8501 - you should see the AgenticAI Foundry home with all 6 modules. '
                'Navigate between them using the left sidebar. '
                'Run python setup_check.py to verify your environment.'),
              Spacer(1,0.06*inch)]

    expect = [
        ['Module', 'What You Should See'],
        ['Module 1: LLM Cost Explorer',     'Interactive cost comparison charts - no API key needed'],
        ['Module 2: Multi-Agent Demo',       'Requires Ollama running or OpenAI key in sidebar'],
        ['Module 2: LangChain Agent Demo',   'Live crypto price lookups - requires Ollama or OpenAI key'],
        ['Module 3: MCP Explorer',           'Interactive MCP protocol diagram - no API key needed'],
        ['Module 4: Agent Security Demo',    'Prompt injection demonstrations - no API key for demo mode'],
        ['Module 5: HITL Demo',             'Human-in-the-Loop approval patterns - no API key needed'],
    ]
    story.append(tbl([[p(c,BOLD if i==0 else BODY) for c in r] for i,r in enumerate(expect)],
                     [2.6*inch, 4.4*inch]))
    story.append(p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 4', FOOT))

    # ── PAGE 5: Docs + Help ───────────────────────────────────────────────────
    story.append(PageBreak())
    story += [p('Documentation & Getting Help', H1)]

    docs = [
        ['Guide', 'What It Covers'],
        ['Student Quick Start (this PDF)',  "Screenshots walkthrough - start here if you're new"],
        ['docs/DOCKER_GUIDE.md',            'Full Docker setup with troubleshooting'],
        ['docs/BEGINNERS_GUIDE.md',         'Deep explanation of all technologies used'],
        ['docs/CREWAI_SETUP.md',            'Ollama and OpenAI setup for agent demos (Module 2)'],
        ['docs/HITL_GUIDE.md',             'Human-in-the-Loop patterns (Module 5)'],
        ['docs/LLM_COST_GUIDE.md',          'Token economics and model pricing (Module 1)'],
        ['docs/MULTI_AGENT_GUIDE.md',       'CrewAI vs LangChain patterns (Module 2)'],
        ['docs/MCP_GUIDE.md',              'Model Context Protocol explained (Module 3)'],
    ]
    story.append(tbl([[p(c,BOLD if i==0 else (BOLD if j==0 else BODY)) for j,c in enumerate(r)]
                      for i,r in enumerate(docs)], [2.8*inch, 4.2*inch]))
    story += [Spacer(1,0.12*inch), p('Getting Help', H2)]
    for item in [
        'Setup issues: Run python setup_check.py and share the output',
        'Docker problems: See docs/DOCKER_GUIDE.md troubleshooting section',
        'Agent demo issues: See docs/CREWAI_SETUP.md troubleshooting section',
        'General questions: Post in the course discussion forum with any error messages',
    ]:
        story.append(p('- ' + item, BULLET))

    story += [Spacer(1,0.12*inch),
              HRFlowable(width='100%', thickness=0.5, color=MGREY),
              Spacer(1,0.1*inch), p('Check Your Environment', H2),
              p('Not sure if everything is set up? Run from the project folder:'),
              p('python setup_check.py', CODE),
              p('Checks Python, libraries, Docker, Ollama, and API keys - reports in plain English.'),
              Spacer(1,0.15*inch)]

    foot_banner = Table([[p(
        'MIT Professional Education | Applied Generative AI for Digital Transformation<br/>'
        'Modules 1, 3, 4 and 5 work immediately with no API key  |  Module 2 requires Ollama or OpenAI<br/>'
        'MIT License - github.com/dlwhyte/AgenticAI_foundry',
        ParagraphStyle('FB', fontName='Helvetica', fontSize=8.5, textColor=colors.white,
                       alignment=TA_CENTER, leading=13))]], colWidths=[W])
    foot_banner.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),NAVY),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    story.append(foot_banner)

    doc.build(story)
    print(f'Generated: {filename}')

if __name__ == '__main__':
    import os, sys
    # Run from repo root so output goes to Student_Quick_Start.pdf
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'Student_Quick_Start.pdf')
    build(out)
