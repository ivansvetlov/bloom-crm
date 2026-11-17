#requires -Version 7.0
<#
.SYNOPSIS
    Локальный статический сервер для проекта.

.DESCRIPTION
    Поднимает каталог со статикой на localhost и, если попросить, в локальной сети —
    тогда его видно с телефона. Нужен потому, что часть страниц делает fetch() и при
    открытии через file:// ломается (CORS), например kp/index.json в bloom-crm.

    Каталог по умолчанию: site\, иначе docs\. Можно указать явно через -Root.

.EXAMPLE
    .\scripts\serve.ps1
    .\scripts\serve.ps1 -Port 8081 -Lan
    .\scripts\serve.ps1 -Root prototype -Lan
#>
[CmdletBinding()]
param(
    [int]$Port = 8080,
    [string]$Root = '',
    [switch]$Lan
)

$ErrorActionPreference = 'Stop'

function Resolve-Root([string]$explicit) {
    if ($explicit) {
        $p = Join-Path (Get-Location) $explicit
        if (-not (Test-Path -LiteralPath $p)) { throw "нет каталога: $p" }
        return (Resolve-Path -LiteralPath $p).Path
    }
    foreach ($candidate in 'site', 'docs', 'prototype', 'web') {
        $p = Join-Path (Get-Location) $candidate
        if ((Test-Path -LiteralPath $p) -and (Get-ChildItem -LiteralPath $p -Filter '*.html' -File -ErrorAction SilentlyContinue)) {
            return (Resolve-Path -LiteralPath $p).Path
        }
    }
    throw "не нашёл каталог со статикой (site\, docs\, prototype\, web\). Укажите -Root."
}

$static = Resolve-Root $Root

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw "нужен python в PATH" }

$inUse = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($inUse) { throw "порт $Port уже занят (PID $($inUse.OwningProcess -join ', ')). Возьмите -Port другой." }

$bind = if ($Lan) { '0.0.0.0' } else { '127.0.0.1' }

Write-Host ""
Write-Host "  каталог : $static"
Write-Host "  порт    : $Port"
Write-Host "  локально: http://localhost:$Port/"
if ($Lan) {
    $ips = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
           Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' -and $_.PrefixOrigin -ne 'WellKnown' } |
           Select-Object -ExpandProperty IPAddress -Unique
    foreach ($ip in $ips) { Write-Host "  в сети  : http://${ip}:$Port/   (открыть на телефоне)" }
    Write-Host ""
    Write-Host "  Если с телефона не открывается — Windows Firewall. Один раз, от админа:"
    Write-Host "    New-NetFirewallRule -DisplayName 'Static dev server $Port' -Direction Inbound -Action Allow -Protocol TCP -LocalPort $Port -Profile Private"
}
Write-Host ""
Write-Host "  Ctrl+C — остановить"
Write-Host ""

& $python.Source -m http.server $Port --bind $bind --directory $static
