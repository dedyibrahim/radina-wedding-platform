$taskWorkspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$taskArchive = Join-Path $taskWorkspace 'legacy-invitation\construction-scripts\radina-experiences'
New-Item -ItemType Directory -Force -Path $taskArchive | Out-Null
$taskResolvedArchive = (Resolve-Path -LiteralPath $taskArchive).Path
if (-not $taskResolvedArchive.StartsWith($taskWorkspace + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Archive must stay inside workspace.' }
$taskFiles = @('upgrade-contract.py','upgrade-presentations.py','connect-editor.py','extract-wedding-composables.py','split-template-presentations.mjs','split-theme-styles.mjs','polish-experiences.mjs','polish-template-css.py','finalize-experience-copy.py','finalize-upgrade-docs.py','finalize-navigation.py','preserve-floral-motion.py')
foreach ($taskFilename in $taskFiles) {
    $taskSource = Join-Path $taskWorkspace ('scripts\' + $taskFilename)
    if (-not [IO.Path]::GetFullPath($taskSource).StartsWith($taskWorkspace + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Source must stay inside workspace.' }
    Move-Item -LiteralPath $taskSource -Destination $taskResolvedArchive
}
Set-Content -LiteralPath (Join-Path $taskArchive 'README.md') -Encoding utf8 -Value 'Historical one-time construction scripts for the Radina experience upgrade. Do not run them against the current project. Runtime components and migrations are the maintained sources; npm and Artisan do not execute these scripts.'
