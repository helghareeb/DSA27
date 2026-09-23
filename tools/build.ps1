<#
.SYNOPSIS
    Build the DSA27 course PDFs from their Markdown sources.

.DESCRIPTION
    Markdown in docs/ is the source of truth; everything in docs/pdf/ is generated.

    Lecture 01 is written once and built twice: a reading handout and a
    presentation deck. Two Lua filters decide what belongs in which --
    ::: {.handout-only} blocks are dropped from the slides, and
    ::: {.slides-only} blocks are dropped from the handout.

    Requires pandoc and a LaTeX installation providing xelatex (MiKTeX).

.EXAMPLE
    pwsh tools/build.ps1
    pwsh tools/build.ps1 -Only lecture01-slides
#>
[CmdletBinding()]
param(
    # Build only one target. Omit to build everything.
    [ValidateSet('lecture01-handout', 'lecture01-slides',
                 'lecture02-handout', 'lecture02-slides',
                 'lecture03-handout', 'lecture03-slides',
                 'lecture04-handout', 'lecture04-slides',
                 'lecture05-handout', 'lecture05-slides',
                 'lecture06-handout', 'lecture06-slides', 'course-guide',
                 'study-plan', 'coverage', 'regulations',
                 'lab01', 'lab02', 'lab03', 'lab-ta-guide', 'question-bank')]
    [string]$Only
)

$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$Docs = Join-Path $Root 'docs'
$Dist = Join-Path $Docs 'pdf'
$Tmpl = Join-Path $PSScriptRoot 'templates'

# winget installs pandoc per-user; a shell opened before the install will not
# have it on PATH yet.
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    $local = Join-Path $env:LOCALAPPDATA 'Pandoc'
    if (Test-Path (Join-Path $local 'pandoc.exe')) {
        $env:Path = "$env:Path;$local"
    }
}

foreach ($exe in 'pandoc', 'xelatex') {
    if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) {
        throw "$exe was not found on PATH. See tools/README.md."
    }
}

New-Item -ItemType Directory -Force -Path $Dist | Out-Null

$Common = @(
    '--from=markdown+fenced_divs+definition_lists+pipe_tables+tex_math_dollars'
    '--pdf-engine=xelatex'
    '--lua-filter', (Join-Path $PSScriptRoot 'arabic.lua')
    '-V', 'mainfont=Segoe UI'
    '-V', 'monofont=Consolas'
    '-V', 'colorlinks=true'
    '-V', 'linkcolor=[HTML]{C8860D}'
    '-V', 'urlcolor=[HTML]{C8860D}'
    '-V', 'toccolor=[HTML]{233A3E}'
)

$HandoutOpts = $Common + @(
    '--lua-filter', (Join-Path $PSScriptRoot 'strip-slides-only.lua')
    '--lua-filter', (Join-Path $PSScriptRoot 'unwrap-divs.lua')
    '--include-in-header', (Join-Path $Tmpl 'handout-header.tex')
    '--syntax-highlighting=tango'
    '-V', 'documentclass=article'
    '-V', 'geometry:a4paper,margin=2.4cm'
    '-V', 'fontsize=11pt'
    '-V', 'linestretch=1.15'
)

$SlideOpts = $Common + @(
    '--to=beamer'
    '--slide-level=2'
    '--lua-filter', (Join-Path $PSScriptRoot 'strip-handout-only.lua')
    '--lua-filter', (Join-Path $PSScriptRoot 'unwrap-divs.lua')
    '--include-in-header', (Join-Path $Tmpl 'beamer-header.tex')
    '--syntax-highlighting=tango'
    '-V', 'aspectratio=169'
    '-V', 'fontsize=10pt'
)

function Build {
    param([string]$Name, [string]$Source, [string]$Output, [string[]]$Options)

    if ($Only -and $Only -ne $Name) { return }

    Write-Host "  $Name " -NoNewline -ForegroundColor Cyan
    # Image paths in the Markdown are relative to the source file, but pandoc
    # resolves them against the working directory unless told otherwise.
    $args = $Options + @("--resource-path=$(Split-Path -Parent $Source)",
                         '-o', $Output, $Source)
    & pandoc @args
    if ($LASTEXITCODE -ne 0) { throw "pandoc failed for $Name (exit $LASTEXITCODE)" }

    $kb = [math]::Round((Get-Item $Output).Length / 1KB)
    Write-Host "-> $(Split-Path -Leaf $Output)  (${kb} KB)" -ForegroundColor Green
}

Write-Host "Building DSA27 PDFs" -ForegroundColor White

$lecture01 = Join-Path $Docs 'lectures\01-why-this-course\lecture.md'

Build 'lecture01-handout' $lecture01 `
      (Join-Path $Dist 'DSA27-L01-handout.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'lecture01-slides'  $lecture01 `
      (Join-Path $Dist 'DSA27-L01-slides.pdf')  $SlideOpts

$lecture02 = Join-Path $Docs 'lectures\02-complexity-and-arrays\lecture.md'

Build 'lecture02-handout' $lecture02 `
      (Join-Path $Dist 'DSA27-L02-handout.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'lecture02-slides'  $lecture02 `
      (Join-Path $Dist 'DSA27-L02-slides.pdf')  $SlideOpts

$lecture03 = Join-Path $Docs 'lectures\03-recursion\lecture.md'

Build 'lecture03-handout' $lecture03 `
      (Join-Path $Dist 'DSA27-L03-handout.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'lecture03-slides'  $lecture03 `
      (Join-Path $Dist 'DSA27-L03-slides.pdf')  $SlideOpts

$lecture04 = Join-Path $Docs 'lectures\04-dynamic-arrays\lecture.md'

Build 'lecture04-handout' $lecture04 `
      (Join-Path $Dist 'DSA27-L04-handout.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'lecture04-slides'  $lecture04 `
      (Join-Path $Dist 'DSA27-L04-slides.pdf')  $SlideOpts

$lecture05 = Join-Path $Docs 'lectures\05-linked-lists\lecture.md'

Build 'lecture05-handout' $lecture05 `
      (Join-Path $Dist 'DSA27-L05-handout.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'lecture05-slides'  $lecture05 `
      (Join-Path $Dist 'DSA27-L05-slides.pdf')  $SlideOpts

$lecture06 = Join-Path $Docs 'lectures\06-stacks\lecture.md'

Build 'lecture06-handout' $lecture06 `
      (Join-Path $Dist 'DSA27-L06-handout.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'lecture06-slides'  $lecture06 `
      (Join-Path $Dist 'DSA27-L06-slides.pdf')  $SlideOpts

Build 'course-guide' (Join-Path $Docs 'course\00-course-guide.md') `
      (Join-Path $Dist 'DSA27-Course-Guide.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'study-plan' (Join-Path $Docs 'course\01-study-plan.md') `
      (Join-Path $Dist 'DSA27-Study-Plan.pdf') $HandoutOpts

Build 'coverage' (Join-Path $Docs 'course\02-coverage.md') `
      (Join-Path $Dist 'DSA27-Coverage.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

Build 'regulations' (Join-Path $Docs 'course\regulations\dsa-in-your-program.md') `
      (Join-Path $Dist 'DSA27-DSA-In-Your-Program.pdf') ($HandoutOpts + @('--toc', '--toc-depth=2'))

$Labs = Join-Path $Docs 'labs'

Build 'lab01' (Join-Path $Labs 'lab01-python-basics.md') `
      (Join-Path $Dist 'DSA27-Lab01.pdf') ($HandoutOpts + @('--toc', '--toc-depth=1'))

Build 'lab02' (Join-Path $Labs 'lab02-control-flow-functions.md') `
      (Join-Path $Dist 'DSA27-Lab02.pdf') ($HandoutOpts + @('--toc', '--toc-depth=1'))

Build 'lab03' (Join-Path $Labs 'lab03-data-structures-classes.md') `
      (Join-Path $Dist 'DSA27-Lab03.pdf') ($HandoutOpts + @('--toc', '--toc-depth=1'))

Build 'lab-ta-guide' (Join-Path $Labs 'ta-guide.md') `
      (Join-Path $Dist 'DSA27-Lab-TA-Guide.pdf') ($HandoutOpts + @('--toc', '--toc-depth=1'))

# Question bank: one PDF per questions file, answers file and mock exam.
$QB = Join-Path $Docs 'question-bank'
$QBFiles = [ordered]@{
    'week01-questions'      = 'DSA27-QB-Week01-Questions.pdf'
    'week01-answers'        = 'DSA27-QB-Week01-Answers.pdf'
    'week02-questions'      = 'DSA27-QB-Week02-Questions.pdf'
    'week02-answers'        = 'DSA27-QB-Week02-Answers.pdf'
    'week03-questions'      = 'DSA27-QB-Week03-Questions.pdf'
    'week03-answers'        = 'DSA27-QB-Week03-Answers.pdf'
    'week04-questions'      = 'DSA27-QB-Week04-Questions.pdf'
    'week04-answers'        = 'DSA27-QB-Week04-Answers.pdf'
    'week05-questions'      = 'DSA27-QB-Week05-Questions.pdf'
    'week05-answers'        = 'DSA27-QB-Week05-Answers.pdf'
    'week06-questions'      = 'DSA27-QB-Week06-Questions.pdf'
    'week06-answers'        = 'DSA27-QB-Week06-Answers.pdf'
    'mock-exam-weeks01-03'  = 'DSA27-QB-Mock-Exam-Weeks01-03.pdf'
}
foreach ($entry in $QBFiles.GetEnumerator()) {
    Build 'question-bank' (Join-Path $QB "$($entry.Key).md") `
          (Join-Path $Dist $entry.Value) $HandoutOpts
}

Write-Host "Done. Output in docs/pdf/" -ForegroundColor White
