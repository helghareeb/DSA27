<#
.SYNOPSIS
    Build the DSA27 course PDFs. A thin wrapper around tools/build.py.

.DESCRIPTION
    Markdown in docs/ is the source of truth; everything in docs/pdf/ is generated.
    The real build lives in tools/build.py so that Windows, Linux and macOS run
    one build. Requires Python, pandoc and xelatex (MiKTeX or TeX Live) on PATH.

.EXAMPLE
    pwsh tools/build.ps1                       # everything
    pwsh tools/build.ps1 -Only lecture01-slides
    pwsh tools/build.ps1 -Only book            # the students' book
#>
[CmdletBinding()]
param([string]$Only)

$ErrorActionPreference = 'Stop'

# winget installs pandoc per-user; a shell opened before the install will not
# have it on PATH yet.
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    $local = Join-Path $env:LOCALAPPDATA 'Pandoc'
    if (Test-Path (Join-Path $local 'pandoc.exe')) { $env:Path = "$env:Path;$local" }
}

$py = Join-Path $PSScriptRoot 'build.py'
if ($Only) { & python $py $Only } else { & python $py }
if ($LASTEXITCODE -ne 0) { throw "build failed (exit $LASTEXITCODE)" }
