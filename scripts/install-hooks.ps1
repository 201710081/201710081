param([Parameter(Mandatory=$true)][string]$PythonPath)
$ErrorActionPreference = 'Stop'
$repo = (git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Git repository not found.' }
$resolvedPython = (Resolve-Path -LiteralPath $PythonPath).Path
& $resolvedPython -c 'import sys; assert sys.version_info.major == 3'
if ($LASTEXITCODE -ne 0) { throw 'Python validation failed.' }
$existing = git -C $repo config --get core.hooksPath
if ($existing -and $existing -ne '.githooks') { throw 'Existing hooksPath detected. Integrate the privacy hook with existing hooks first.' }
git -C $repo config privacy.python ($resolvedPython.Replace('\','/'))
if ($LASTEXITCODE -ne 0) { throw 'Python configuration failed.' }
git -C $repo config core.hooksPath .githooks
if ($LASTEXITCODE -ne 0) { throw 'Hook installation failed.' }
Write-Output 'Privacy pre-commit and pre-push hooks enabled for this repository.'
