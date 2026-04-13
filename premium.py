.home-hero {
    background:
        radial-gradient(circle at top left, rgba(13, 110, 253, 0.12), transparent 34%),
        radial-gradient(circle at top right, rgba(25, 135, 84, 0.08), transparent 28%),
        linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    padding-top: 4.5rem;
    padding-bottom: 4.5rem;
    position: relative;
    overflow: hidden;
}

.home-hero::after {
    content: "";
    position: absolute;
    inset: auto -10% -120px auto;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(13, 110, 253, 0.06) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(238, 244, 255, 0.9);
    color: #0d6efd;
    border: 1px solid #d7e6ff;
    padding: 0.48rem 0.95rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    box-shadow: 0 6px 18px rgba(13, 110, 253, 0.06);
}

.hero-title {
    font-size: clamp(2.2rem, 5vw, 4.3rem);
    line-height: 1.03;
    letter-spacing: -0.045em;
    color: #101828;
    max-width: 12ch;
    font-weight: 850;
}

.hero-subtitle {
    font-size: 1.06rem;
    color: #475467;
    max-width: 60ch;
    line-height: 1.72;
}

.hero-metrics {
    display: flex;
    gap: 0.9rem;
    flex-wrap: wrap;
    margin-top: 1.7rem;
}

.hero-metric-card {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(16, 24, 40, 0.06);
    border-radius: 20px;
    padding: 0.9rem 1rem;
    min-width: 145px;
    box-shadow: 0 10px 28px rgba(16, 24, 40, 0.05);
    backdrop-filter: blur(10px);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.hero-metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 36px rgba(16, 24, 40, 0.08);
    border-color: rgba(13, 110, 253, 0.14);
}

.hero-metric-label {
    color: #667085;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.hero-metric-value {
    color: #101828;
    font-size: 1.02rem;
    font-weight: 800;
    line-height: 1.2;
}

.hero-side-card {
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(16, 24, 40, 0.06);
    box-shadow: 0 18px 45px rgba(16, 24, 40, 0.08);
    border-radius: 24px;
}

.hero-side-card .card-body {
    padding: 1.4rem;
}

.teaser-card {
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    border: 1px solid rgba(16, 24, 40, 0.05);
    border-radius: 22px;
    box-shadow: 0 10px 28px rgba(16, 24, 40, 0.05);
    background: rgba(255, 255, 255, 0.94);
}

.teaser-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 40px rgba(16, 24, 40, 0.09);
    border-color: rgba(13, 110, 253, 0.14);
}

.teaser-icon {
    font-size: 1.25rem;
}

.calculadoras-section {
    padding-top: 5rem;
    padding-bottom: 4rem;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    position: relative;
}

.quick-actions-section {
    padding-top: 1.25rem;
    padding-bottom: 3rem;
    background: #ffffff;
}

.premium-section {
    padding-top: 0.5rem;
    padding-bottom: 3.2rem;
    background: #ffffff;
}

.cta-section {
    padding-bottom: 3.2rem;
    background: #ffffff;
}

.books-section {
    padding-top: 1rem;
    padding-bottom: 3rem;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.section-eyebrow {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #0d6efd;
    background: #eef4ff;
    border: 1px solid #d7e6ff;
    padding: 0.45rem 0.82rem;
    border-radius: 999px;
    margin-bottom: 1rem;
    box-shadow: 0 6px 16px rgba(13, 110, 253, 0.05);
}

.section-title {
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    line-height: 1.06;
    letter-spacing: -0.035em;
    color: #101828;
    font-weight: 850;
}

.section-subtitle {
    color: #667085;
    font-size: 1.04rem;
    max-width: 720px;
    line-height: 1.72;
}

.calc-card {
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 10px 30px rgba(16, 24, 40, 0.06);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    border: 1px solid rgba(16, 24, 40, 0.06);
    backdrop-filter: blur(8px);
    border-radius: 24px;
    overflow: hidden;
}

.calc-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 44px rgba(16, 24, 40, 0.10);
    border-color: rgba(13, 110, 253, 0.18);
}

.calc-card-featured {
    background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.99) 0%, rgba(244, 248, 255, 0.97) 100%);
    border: 1px solid rgba(13, 110, 253, 0.18);
    box-shadow: 0 16px 44px rgba(13, 110, 253, 0.10);
}

.calc-card-icon {
    width: 54px;
    height: 54px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
    border: 1px solid #d7e6ff;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

.calc-card-badge,
.book-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.36rem 0.72rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 800;
    color: #0d6efd;
    background: #eef4ff;
    border: 1px solid #d7e6ff;
    text-align: center;
}

.calc-card-btn.btn-light {
    background: #f8fafc;
    border: 1px solid #e4e7ec;
    border-radius: 999px;
    font-weight: 700;
}

.calc-card-btn.btn-light:hover {
    background: #eef2f6;
    border-color: #d0d5dd;
}

.calc-highlight-box {
    background:
        radial-gradient(circle at top right, rgba(13, 110, 253, 0.08), transparent 30%),
        linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #eaecf0;
    border-radius: 24px;
    padding: 1.3rem;
    box-shadow: 0 10px 26px rgba(16, 24, 40, 0.05);
}

.quick-card {
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    border-radius: 22px;
    border: 1px solid rgba(16, 24, 40, 0.05);
    box-shadow: 0 10px 28px rgba(16, 24, 40, 0.05);
}

.quick-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 35px rgba(16, 24, 40, 0.08);
    border-color: rgba(13, 110, 253, 0.12);
}

.premium-panel {
    background:
        radial-gradient(circle at top right, rgba(13, 110, 253, 0.10), transparent 28%),
        radial-gradient(circle at bottom left, rgba(25, 135, 84, 0.06), transparent 30%),
        linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid rgba(16, 24, 40, 0.06);
    border-radius: 28px;
    box-shadow: 0 18px 46px rgba(16, 24, 40, 0.08);
    overflow: hidden;
}

.premium-title {
    color: #101828;
    font-size: clamp(1.7rem, 3vw, 2.5rem);
    line-height: 1.08;
    letter-spacing: -0.03em;
    font-weight: 850;
}

.premium-list {
    padding-left: 1.1rem;
    color: #475467;
    line-height: 1.9;
}

.premium-list li {
    margin-bottom: 0.35rem;
}

.premium-price-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.55rem 0.95rem;
    border-radius: 999px;
    background: #101828;
    color: #ffffff;
    font-size: 0.88rem;
    font-weight: 800;
    letter-spacing: 0.01em;
    box-shadow: 0 12px 28px rgba(16, 24, 40, 0.16);
}

.premium-mini-note {
    color: #667085;
    font-size: 0.92rem;
    font-weight: 600;
}

.premium-feature-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.8rem;
    margin-top: 1.25rem;
}

.premium-feature-chip {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.85rem 0.95rem;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(16, 24, 40, 0.06);
    box-shadow: 0 8px 24px rgba(16, 24, 40, 0.04);
    color: #344054;
    font-size: 0.94rem;
    font-weight: 700;
}

.premium-feature-chip i,
.premium-feature-chip span.icon {
    color: #198754;
    font-size: 1rem;
}

.premium-cta-btn {
    border-radius: 999px;
    font-weight: 800;
    padding: 0.95rem 1.35rem;
    box-shadow: 0 14px 30px rgba(16, 24, 40, 0.12);
}

.premium-cta-btn.btn-dark:hover,
.premium-cta-btn.btn-success:hover {
    transform: translateY(-1px);
}

.cta-panel {
    background:
        radial-gradient(circle at top right, rgba(13, 110, 253, 0.09), transparent 28%),
        linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid rgba(16, 24, 40, 0.06);
    border-radius: 28px;
    box-shadow: 0 18px 46px rgba(16, 24, 40, 0.08);
}

.cta-panel .btn {
    border-radius: 999px;
    font-weight: 800;
    padding-top: 0.9rem;
    padding-bottom: 0.9rem;
}

.book-card {
    border-radius: 22px;
    border: 1px solid rgba(16, 24, 40, 0.05);
    box-shadow: 0 10px 28px rgba(16, 24, 40, 0.05);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.book-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 38px rgba(16, 24, 40, 0.08);
    border-color: rgba(13, 110, 253, 0.12);
}

.home-soft-divider {
    height: 1px;
    width: 100%;
    background: linear-gradient(90deg, transparent 0%, rgba(16, 24, 40, 0.08) 50%, transparent 100%);
    margin: 0 auto;
}

@media (max-width: 991px) {
    .home-hero {
        padding-top: 3.2rem;
        padding-bottom: 3.2rem;
    }

    .calculadoras-section {
        padding-top: 3.6rem;
        padding-bottom: 2.6rem;
    }

    .hero-title {
        max-width: none;
    }

    .premium-feature-grid {
        grid-template-columns: 1fr;
    }

    .hero-metric-card {
        min-width: calc(50% - 0.5rem);
    }
}

@media (max-width: 767px) {
    .hero-subtitle,
    .section-subtitle {
        font-size: 0.98rem;
    }

    .hero-metrics {
        gap: 0.75rem;
    }

    .hero-metric-card {
        min-width: 100%;
    }

    .calc-card,
    .premium-panel,
    .cta-panel,
    .book-card,
    .quick-card,
    .teaser-card {
        border-radius: 20px;
    }

    .premium-title,
    .section-title {
        line-height: 1.12;
    }
}
