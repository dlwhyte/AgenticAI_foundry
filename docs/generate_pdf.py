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
from reportlab.lib.enums import TA_CENTER

NAVY   = colors.HexColor('#1B2A4A')
ORANGE = colors.HexColor('#F5A623')
LGREY  = colors.HexColor('#F5F5F5')
MGREY  = colors.HexColor('#CCCCCC')
YELLOW = colors.HexColor('#FFF3CD')

def s(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, leading=13,
             textColor=colors.black, spaceAfter=4)
    d.update(kw)
    return ParagraphStyle(name, **d)

TITLE = s('T',  fontName='Helvetica-Bold', fontSize=28, textColor=colors.white, alignment=TA_CENTER, spaceAfter=4)
SUB1  = s('S1', fontSize=14, textColor=colors.white, alignment=TA_CENTER)
SUB2  = s('S2', fontName='Helvetica-BoldOblique', fontSize=11, textColor=colors.white, alignment=TA_CENTER)
H1    = s('H1', fontName='Helvetica-Bold', fontSize=15, textColor=NAVY, spaceBefore=14, spaceAfter=4)
H2    = s('H2', fontName='Helvetica-Bold', fontSize=12, textColor=NAVY, spaceBefore=10, spaceAfter=3)
BODY  = s('B')
BOLD  = s('Bb', fontName='Helvetica-Bold')
CODE  = s('C',  fontName='Courier', fontSize=8.5, backColor=LGREY, borderPadding=4, leading=12)
NOTE  = s('N',  fontName='Helvetica-Oblique', textColor=NAVY, leftIndent=10)
FOOT  = s('F',  fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
BITEM = s('Bu', leftIndent=15, bulletIndent=5)

def mktbl(data, widths):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0), NAVY),
        ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
        ('FONTNAME',      (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),(-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGREY]),
        ('GRID',          (0,0),(-1,-1), 0.5, MGREY),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 6),
    ]))
    return t

def p(text, style=None):
    return Paragraph(str(text), style or BODY)

def build(filename='Student_Quick_Start.pdf'):
    doc = SimpleDocTemplate(filename, pagesize=letter,
        rightMargin=0.75*inch, leftMargin=0.75*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch,
        author='MIT Professional Education',
        subject='Applied Generative AI for Digital Transformation',
        title='AgenticAI Foundry - Student Quick Start Guide')

    W = 7*inch
    story = []

    # ── PAGE 1 ────────────────────────────────────────────────────────────────
    hdr = Table([
        [p('AgenticAI Foundry', TITLE)],
        [p('Student Quick Start Guide', SUB1)],
        [p('MIT Professional Education  |  Applied Generative AI for Digital Transformation', SUB2)],
    ], colWidths=[W])
    hdr.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY), ('BACKGROUND',(0,1),(-1,2),ORANGE),
        ('TOPPADDING',(0,0),(-1,0),18), ('BOTTOMPADDING',(0,0),(-1,0),14),
        ('TOPPADDING',(0,1),(-1,1), 8), ('BOTTOMPADDING',(0,1),(-1,1), 4),
        ('TOPPADDING',(0,2),(-1,2), 4), ('BOTTOMPADDING',(0,2),(-1,2),12),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ]))
    story += [hdr, Spacer(1,0.2*inch),
              p('This guide gets you from zero to running the course demos in the shortest possible time.'),
              Spacer(1,0.05*inch), p("What's Included", H1)]

    mods = [
        [p('Demo',BOLD), p('Module',BOLD), p('What You Will Learn',BOLD), p('API Key?',BOLD)],
        [p('LLM Cost Explorer'),    p('Module 1'), p('Why the same AI task can cost $1 or $230 depending on model choice'), p('No')],
        [p('Multi-Agent Demo'),     p('Module 2'), p('How three AI agents collaborate like a team (CrewAI)'),               p('Optional')],
        [p('LangChain Agent Demo'), p('Module 2'), p('How a single agent uses tools to answer questions in real time'),     p('Optional')],
        [p('MCP Explorer'),         p('Module 3'), p('How AI agents connect to external tools (calendars, CRMs, etc.)'),   p('No')],
        [p('Agent Security Demo'),  p('Module 4'), p('Prompt injection attacks and defense-in-depth guardrails'),           p('Demo: No / Live: Optional')],
        [p('HITL Demo'),            p('Module 5'), p('Patterns for keeping humans in control of AI decisions'),             p('No')],
    ]
    story.append(mktbl(mods, [1.4*inch, 0.85*inch, 3.35*inch, 1.4*inch]))
    story += [Spacer(1,0.08*inch),
              p('<i>Modules 1, 3, 4, and 5 work immediately - no account or API key needed. '
                'Module 2 needs Ollama (free, local) or an OpenAI API key.</i>', NOTE),
              Spacer(1,0.12*inch), p('Step 0 - Get the Code (Both Paths)', H1),
              p('You need a copy of this repository on your computer before doing anything else.'),
              Spacer(1,0.05*inch)]

    gc = Table([
        [p('<b>Option 1: Download ZIP</b> (easiest)', BOLD), p('<b>Option 2: Clone with Git</b>', BOLD)],
        [p('1. Click the green &lt;&gt; Code button on GitHub<br/>'
           '2. Click Download ZIP<br/>'
           '3. Find it in Downloads and extract it'),
         p('<font name="Courier" size="8">git clone https://github.com/dlwhyte/AgenticAI_foundry.git</font>')],
    ], colWidths=[3.5*inch, 3.5*inch])
    gc.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY), ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.5,MGREY), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),
    ]))
    story += [gc, Spacer(1,0.08*inch),
              p('<b>Which path?</b> "Have I used Docker before, or am I comfortable installing a new app?"'),
              p('Yes - Path A: Docker (recommended)     No - Path B: Python'),
              p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 1', FOOT)]

    # ── PAGE 2 ────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += [p('Path A: Docker (Recommended)', H1),
              p('Docker packages the entire app into a self-contained box. '
                'Runs identically on Windows, Mac, and Linux. '
                'Time: about 20 minutes first time, under 1 minute after that.')]

    docker_rows = [
        [p('Step',BOLD), p('Action',BOLD), p('Command / Detail',BOLD)],
        [p('1'), p('Install Docker Desktop'),
         p('Windows/Mac: docker.com/products/docker-desktop<br/>Linux: see docs/DOCKER_GUIDE.md')],
        [p('2'), p('Open a Terminal'),
         p('Windows: Win+R, type powershell<br/>Mac: Cmd+Space, type Terminal<br/>Linux: Ctrl+Alt+T')],
        [p('3'), p('Navigate to folder'),
         p('cd path/to/AgenticAI_foundry<br/>(Tip: drag the folder onto the terminal)')],
        [p('4'), p('Build the app (once)'),
         p('<font name="Courier" size="8">docker build -t agenticai-foundry .</font>')],
        [p('5'), p('Run the app'),
         p('<font name="Courier" size="8">docker run -p 8501:8501 agenticai-foundry</font>')],
        [p('6'), p('Open in browser'),
         p('http://localhost:8501')],
        [p('7'), p('Stop the app'),
         p('Press Ctrl+C in the terminal')],
    ]
    story.append(mktbl(docker_rows, [0.45*inch, 1.6*inch, 4.95*inch]))
    story += [Spacer(1,0.1*inch), p('Docker Troubleshooting', H2)]
    dt = [
        [p('Problem',BOLD), p('Solution',BOLD)],
        [p('"Docker command not found"'),    p('Make sure Docker Desktop is open and running')],
        [p('"Cannot connect to daemon"'),    p('Open Docker Desktop; wait for the whale to stop animating')],
        [p('"Port 8501 already in use"'),    p('Run: docker run -p 8502:8501 agenticai-foundry  then open :8502')],
        [p('Build seems stuck'),             p('First build downloads ~500MB - can take 5+ minutes on slow connections')],
    ]
    story.append(mktbl(dt, [2.5*inch, 4.5*inch]))
    story += [Spacer(1,0.06*inch),
              p('For more detail see docs/DOCKER_GUIDE.md in the repo.', NOTE),
              p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 2', FOOT)]

    # ── PAGE 3 ────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += [p('Path B: Python', H1),
              p('Run the app directly. More steps but full code visibility. Time: ~15 minutes.'),
              p('<b>Check Python first:</b> run <font name="Courier">python3 --version</font> in a terminal. '
                'Python 3.9 or lower? Use Docker instead. CrewAI (Module 2) needs Python 3.10+.'),
              Spacer(1,0.06*inch)]

    py_rows = [
        [p('Step',BOLD), p('Action',BOLD), p('Detail',BOLD)],
        [p('1'), p('Install Python 3.10+'),
         p('Check version: python3 --version<br/>'
           'If 3.9 or lower: download from python.org/downloads<br/>'
           'Windows: check "Add Python to PATH" during install')],
        [p('2'), p('Open terminal and navigate'),
         p('See Docker Path Steps 2-3 for opening a terminal and using cd to reach the folder')],
        [p('3'), p('Install dependencies<br/>(REQUIRED - both)'),
         p('<font name="Courier" size="8">pip3 install -r requirements.txt</font><br/>'
           '<font name="Courier" size="8">pip3 install -r requirements-crewai.txt</font><br/>'
           'Run BOTH commands. Takes 2-5 minutes each.')],
        [p('4'), p('Run the app'),
         p('<font name="Courier" size="8">python3 -m streamlit run Home.py</font><br/>'
           'Browser opens to http://localhost:8501 automatically')],
        [p('5'), p('Stop the app'), p('Press Ctrl+C')],
    ]
    story.append(mktbl(py_rows, [0.65*inch, 1.55*inch, 4.8*inch]))

    warn = Table([[p('<b>Important:</b> Step 3 runs TWO pip commands, not one. '
                    'requirements-crewai.txt contains CrewAI, LangChain, and agent dependencies. '
                    'Skipping it causes Module 2 to crash with ModuleNotFoundError.')]], colWidths=[W])
    warn.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),YELLOW), ('BOX',(0,0),(-1,-1),1,ORANGE),
        ('TOPPADDING',(0,0),(-1,-1),8), ('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10), ('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    story += [Spacer(1,0.08*inch), warn, Spacer(1,0.1*inch), p('Python Troubleshooting', H2)]
    pyt = [
        [p('Problem',BOLD), p('Solution',BOLD)],
        [p('"pip not found"'),             p('Try pip3 install -r requirements.txt instead')],
        [p('"streamlit not found"'),       p('Try python -m streamlit run Home.py')],
        [p('"Permission denied"'),         p('Add --user: pip install --user -r requirements.txt')],
        [p('Browser does not open'),       p('Manually go to http://localhost:8501')],
        [p('Module 2 crashes on import'),  p('Make sure you ran BOTH pip install commands in Step 3')],
    ]
    story.append(mktbl(pyt, [2.5*inch, 4.5*inch]))
    story.append(p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 3', FOOT))

    # ── PAGE 4 ────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += [p('Setting Up the Agent Demos (Module 2)', H1),
              p('Modules 1, 3, 4, and 5 work immediately. '
                'Module 2 needs an AI model - you have two options:'),
              Spacer(1,0.06*inch), p('Option A: Ollama - Free, runs locally, no account needed', H2)]

    ol = [
        [p('Step',BOLD), p('Command',BOLD)],
        [p('1. Install Ollama'),   p('Download from ollama.ai')],
        [p('2. Download model'),   p('ollama pull llama3.2  (2GB one-time download)')],
        [p('3. Start Ollama'),     p('ollama serve  (keep this terminal open)')],
        [p('4. Run the app'),      p('Use Docker or Python path, then select Ollama in the app sidebar')],
    ]
    story.append(mktbl(ol, [2.3*inch, 4.7*inch]))
    story += [p('The model download is ~2GB. Do this on a good internet connection.', NOTE),
              Spacer(1,0.08*inch), p('Option B: OpenAI - Paid, faster results (~$0.01 per demo run)', H2),
              p('Create an account at platform.openai.com and get an API key. '
                'Enter it in the app sidebar - no environment setup needed.'),
              Spacer(1,0.1*inch), HRFlowable(width='100%', thickness=0.5, color=MGREY),
              Spacer(1,0.1*inch), p("What to Expect When It's Working", H1),
              p('Open http://localhost:8501 to see the AgenticAI Foundry home with all 6 modules. '
                'Navigate via the left sidebar. Run python setup_check.py to verify your environment.'),
              Spacer(1,0.06*inch)]

    exp = [
        [p('Module',BOLD), p('What You Should See',BOLD)],
        [p('Module 1: LLM Cost Explorer'),    p('Interactive cost comparison charts - no API key needed')],
        [p('Module 2: Multi-Agent Demo'),      p('Requires Ollama running or OpenAI key in sidebar')],
        [p('Module 2: LangChain Agent Demo'),  p('Live crypto price lookups - requires Ollama or OpenAI')],
        [p('Module 3: MCP Explorer'),          p('Interactive MCP protocol diagram - no API key needed')],
        [p('Module 4: Agent Security Demo'),   p('Prompt injection demonstrations - no API key for demo mode')],
        [p('Module 5: HITL Demo'),            p('Human-in-the-Loop approval patterns - no API key needed')],
    ]
    story.append(mktbl(exp, [2.6*inch, 4.4*inch]))
    story.append(p('MIT Professional Education | Applied Generative AI for Digital Transformation | Page 4', FOOT))

    # ── PAGE 5 ────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += [p('Documentation and Getting Help', H1)]
    docs = [
        [p('Guide',BOLD), p('What It Covers',BOLD)],
        [p('Student Quick Start (this PDF)'),  p("Screenshots walkthrough - start here if you're new")],
        [p('docs/DOCKER_GUIDE.md'),            p('Full Docker setup with troubleshooting')],
        [p('docs/BEGINNERS_GUIDE.md'),         p('Deep explanation of all technologies used')],
        [p('docs/CREWAI_SETUP.md'),            p('Ollama and OpenAI setup for agent demos (Module 2)')],
        [p('docs/HITL_GUIDE.md'),             p('Human-in-the-Loop patterns (Module 5)')],
        [p('docs/LLM_COST_GUIDE.md'),          p('Token economics and model pricing (Module 1)')],
        [p('docs/MULTI_AGENT_GUIDE.md'),       p('CrewAI vs LangChain patterns (Module 2)')],
        [p('docs/MCP_GUIDE.md'),              p('Model Context Protocol explained (Module 3)')],
    ]
    story.append(mktbl(docs, [2.8*inch, 4.2*inch]))
    story += [Spacer(1,0.12*inch), p('Getting Help', H2)]
    for item in [
        'Setup issues: Run python setup_check.py and share the output',
        'Docker problems: See docs/DOCKER_GUIDE.md troubleshooting section',
        'Agent demo issues: See docs/CREWAI_SETUP.md troubleshooting section',
        'General questions: Post in the course discussion forum with any error messages',
    ]:
        story.append(p('- ' + item, BITEM))
    story += [Spacer(1,0.12*inch), HRFlowable(width='100%', thickness=0.5, color=MGREY),
              Spacer(1,0.1*inch), p('Check Your Environment', H2),
              p('Not sure if everything is set up? Run from the project folder:'),
              p('python setup_check.py', CODE),
              p('Checks Python, libraries, Docker, Ollama, and API keys - reports in plain English.'),
              Spacer(1,0.15*inch)]

    fb = Table([[p('MIT Professional Education | Applied Generative AI for Digital Transformation<br/>'
                   'Modules 1, 3, 4 and 5 work immediately with no API key  |  Module 2 requires Ollama or OpenAI<br/>'
                   'MIT License - github.com/dlwhyte/AgenticAI_foundry',
                   ParagraphStyle('FB', fontName='Helvetica', fontSize=8.5,
                                  textColor=colors.white, alignment=TA_CENTER, leading=13))]], colWidths=[W])
    fb.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),NAVY),
        ('TOPPADDING',(0,0),(-1,-1),10), ('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    story.append(fb)
    doc.build(story)
    print('Generated: ' + filename)

if __name__ == '__main__':
    import os
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'Student_Quick_Start.pdf')
    build(out)
