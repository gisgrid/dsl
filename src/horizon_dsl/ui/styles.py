from __future__ import annotations


def app_styles() -> str:
    return """
<style>
.fdx-section {padding: 0.6rem 0 1.2rem 0;}
.fdx-kicker {text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.74rem; font-weight: 700; color: #3b82f6;}
.fdx-hero-title {font-size: 2.6rem; font-weight: 800; line-height: 1.05; margin-bottom: 0.15rem;}
.fdx-hero-subtitle {font-size: 1.2rem; color: var(--text-color); opacity: 0.85; margin-bottom: 0.8rem;}
.fdx-intro {font-size: 1.02rem; max-width: 52rem; color: var(--text-color); opacity: 0.9;}
.fdx-card, .fdx-value, .fdx-layer-card, .fdx-coverage-card, .fdx-target-card {
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 18px;
  padding: 1rem 1rem 0.95rem 1rem;
  background: rgba(248, 250, 252, 0.72);
}
.fdx-layer-card {padding: 0.9rem 1rem;}
.fdx-layer-title {font-size: 1.02rem; font-weight: 700; margin-bottom: 0.1rem;}
.fdx-layer-desc {font-size: 0.93rem; opacity: 0.9; margin-bottom: 0.25rem;}
.fdx-layer-list {font-size: 0.88rem; opacity: 0.85; margin: 0.35rem 0 0 1rem;}
.fdx-connector {margin: 0.45rem 0 0.55rem 1rem; font-size: 0.85rem; opacity: 0.78; padding-left: 0.8rem; border-left: 2px dashed rgba(100, 116, 139, 0.45);}
.fdx-grid-gap {gap: 0.8rem; display: grid;}
.fdx-value {display: flex; gap: 0.8rem; align-items: flex-start; min-height: 100%;}
.fdx-value-num {flex: 0 0 2rem; height: 2rem; border-radius: 999px; display: flex; align-items: center; justify-content: center; font-weight: 700; background: rgba(59, 130, 246, 0.12); color: #2563eb;}
.fdx-value-title {font-weight: 700; margin-bottom: 0.2rem;}
.fdx-value-copy {font-size: 0.92rem; opacity: 0.9;}
.fdx-coverage-item {display: flex; justify-content: space-between; gap: 0.8rem; padding: 0.35rem 0; border-bottom: 1px solid rgba(148, 163, 184, 0.18);}
.fdx-coverage-item:last-child {border-bottom: none;}
.fdx-pill {display: inline-block; border-radius: 999px; padding: 0.1rem 0.55rem; font-size: 0.72rem; font-weight: 700;}
.fdx-pill-covered {background: rgba(22, 163, 74, 0.14); color: #15803d;}
.fdx-pill-preview {background: rgba(37, 99, 235, 0.14); color: #2563eb;}
.fdx-pill-future {background: rgba(217, 119, 6, 0.14); color: #b45309;}
.fdx-pill-scope {background: rgba(107, 114, 128, 0.16); color: #4b5563;}
.fdx-status-line {display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap; margin-bottom:0.35rem;}
.fdx-muted {opacity: 0.78; font-size: 0.9rem;}
.fdx-action-group {border: 1px solid rgba(148, 163, 184, 0.32); border-radius: 18px; padding: 1rem; height: 100%;}
.fdx-badge {display:inline-block; padding:0.18rem 0.55rem; border-radius:999px; font-size:0.72rem; font-weight:700; background:rgba(37,99,235,0.14); color:#1d4ed8;}
.fdx-stale {border-left: 4px solid #f59e0b; padding-left: 0.8rem;}
@media (prefers-color-scheme: dark) {
  .fdx-card, .fdx-value, .fdx-layer-card, .fdx-coverage-card, .fdx-target-card, .fdx-action-group {
    background: rgba(15, 23, 42, 0.6);
    border-color: rgba(148, 163, 184, 0.28);
  }
  .fdx-value-num {background: rgba(96, 165, 250, 0.18); color: #93c5fd;}
  .fdx-pill-covered {background: rgba(74, 222, 128, 0.18); color: #86efac;}
  .fdx-pill-preview {background: rgba(96, 165, 250, 0.18); color: #93c5fd;}
  .fdx-pill-future {background: rgba(251, 191, 36, 0.18); color: #fcd34d;}
  .fdx-pill-scope {background: rgba(148, 163, 184, 0.18); color: #cbd5e1;}
  .fdx-badge {background: rgba(96, 165, 250, 0.18); color: #bfdbfe;}
}
</style>
"""
