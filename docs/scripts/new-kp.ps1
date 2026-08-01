#requires -Version 5.1
<#
.SYNOPSIS
  Создаёт новое КП из шаблона docs/kp/_template.

.EXAMPLE
  .\docs\scripts\new-kp.ps1 -Slug roza-spb -Title "Bloom CRM — Роза СПб" -Client "Роза СПб"
#>
param(
  [Parameter(Mandatory = $true)]
  [ValidatePattern('^[a-z0-9]+(?:-[a-z0-9]+)*$')]
  [string]$Slug,

  [Parameter(Mandatory = $true)]
  [string]$Title,

  [Parameter(Mandatory = $true)]
  [string]$Client,

  [string]$Summary = "КП и демо для заказчика."
)

$ErrorActionPreference = 'Stop'
$Root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$Kp = Join-Path $Root 'docs\kp'
$Template = Join-Path $Kp '_template'
$Target = Join-Path $Kp $Slug
$Registry = Join-Path $Kp 'index.json'

if (-not (Test-Path $Template)) {
  throw "Нет шаблона: $Template"
}
if (Test-Path $Target) {
  throw "Уже есть: $Target"
}

Copy-Item -Path $Template -Destination $Target -Recurse -Force

$created = Get-Date -Format 'yyyy-MM-dd'
$clientJson = [ordered]@{
  slug    = $Slug
  title   = $Title
  client  = $Client
  status  = 'draft'
  created = $created
  contact = @{
    telegram = 'https://t.me/vanyasvetlov'
    whatsapp = 'https://wa.me/79111472928'
    max      = ''
  }
  pages = @{
    kp        = 'index.html'
    demo      = 'demo.html'
    questions = 'questions.html'
    landing   = 'landing.html'
    roles     = 'test-dynamic.html'
    security  = 'security.html'
  }
  notes = "Создано new-kp.ps1 из _template."
}
$clientJson | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $Target 'client.json') -Encoding UTF8

$reg = Get-Content $Registry -Raw -Encoding UTF8 | ConvertFrom-Json
$exists = $reg.clients | Where-Object { $_.slug -eq $Slug }
if ($exists) {
  throw "slug уже в index.json: $Slug"
}

$entry = [pscustomobject]@{
  slug    = $Slug
  title   = $Title
  client  = $Client
  status  = 'draft'
  created = $created
  summary = $Summary
  entry   = 'index.html'
}
$reg.clients = @($reg.clients) + @($entry)

# Preserve readable JSON
$out = [ordered]@{
  version     = 1
  product     = $reg.product
  description = $reg.description
  clients     = @($reg.clients | ForEach-Object {
      [ordered]@{
        slug    = $_.slug
        title   = $_.title
        client  = $_.client
        status  = $_.status
        created = $_.created
        summary = $_.summary
        entry   = $_.entry
      }
    })
}
($out | ConvertTo-Json -Depth 6) | Set-Content -Path $Registry -Encoding UTF8

Write-Host "OK: docs/kp/$Slug/"
Write-Host "    entry: docs/kp/$Slug/index.html"
Write-Host "    registry updated: docs/kp/index.json"
Write-Host "Дальше: правьте HTML под клиента, status → active, деплой."
