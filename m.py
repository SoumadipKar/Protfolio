from flask import Flask, render_template_string, send_from_directory, abort, redirect, request, jsonify
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

app = Flask(__name__)
app.secret_key = "soumadip-portfolio-secret-key"

# ── Modern Single-Page HTML & CSS & JS (subhasis.me Inspired) ────────────────
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | Portfolio · Aspiring Software Developer</title>
    <meta name="description" content="Professional portfolio of {{ name }}, Computer Science Engineering student and Python Developer & Data Analyst from Kolkata, India.">
    <meta name="keywords" content="Soumadip Kar, Python Developer, Data Analyst, Portfolio, Machine Learning, Kolkata, Brainware University">
    <meta name="author" content="{{ name }}">

    <!-- Google Fonts: Outfit (Display) & Inter (Body) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

    <style>
        :root {
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.25);
            --secondary: #818cf8;
            --accent: #c084fc;
            --accent-orange: #fb923c;
            --accent-emerald: #34d399;
            --bg-deep: #030712;
            --bg-surface: #0a0f1d;
            --bg-card: rgba(15, 23, 42, 0.65);
            --bg-card-hover: rgba(22, 34, 61, 0.85);
            --border: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(56, 189, 248, 0.35);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-sub: #64748b;
            --radius-lg: 20px;
            --radius-md: 14px;
            --radius-sm: 8px;
            --font-display: 'Outfit', -apple-system, sans-serif;
            --font-body: 'Inter', -apple-system, sans-serif;
        }

        *, *::before, *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
            font-size: 16px;
        }

        body {
            background-color: var(--bg-deep);
            color: var(--text-main);
            font-family: var(--font-body);
            line-height: 1.65;
            overflow-x: hidden;
            position: relative;
            selection-background-color: rgba(56, 189, 248, 0.25);
            selection-color: #38bdf8;
        }

        ::selection {
            background: rgba(56, 189, 248, 0.25);
            color: #7dd3fc;
        }

        /* ── Subtle Background Gradients ── */
        .ambient-bg {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }

        .ambient-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.15;
            animation: orbFloat 22s ease-in-out infinite alternate;
        }

        .orb-blue {
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, #38bdf8, #2563eb);
            top: -100px;
            left: -100px;
        }

        .orb-purple {
            width: 480px;
            height: 480px;
            background: radial-gradient(circle, #a855f7, #6366f1);
            top: 40%;
            right: -120px;
            animation-duration: 28s;
        }

        .orb-cyan {
            width: 420px;
            height: 420px;
            background: radial-gradient(circle, #06b6d4, #0284c7);
            bottom: -50px;
            left: 20%;
            animation-duration: 20s;
        }

        @keyframes orbFloat {
            0% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(40px, -30px) scale(1.08); }
            100% { transform: translate(-30px, 35px) scale(0.95); }
        }

        /* ── Custom Cursor Glow ── */
        #cursor-glow {
            position: fixed;
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 65%);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 1;
            transition: opacity 0.3s ease;
        }

        /* ── Grid Pattern Overlay ── */
        .grid-overlay {
            position: fixed;
            inset: 0;
            background-image: 
                linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none;
            z-index: 0;
        }

        /* ── Modern Navigation Bar ── */
        .navbar-wrap {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            padding: 16px 6%;
            transition: all 0.3s ease;
        }

        .navbar-wrap.scrolled {
            padding: 10px 6%;
        }

        .navbar {
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(10, 15, 29, 0.75);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid var(--border);
            border-radius: 9999px;
            padding: 8px 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
        }

        .navbar-wrap.scrolled .navbar {
            border-color: rgba(56, 189, 248, 0.2);
            background: rgba(7, 12, 23, 0.9);
        }

        .logo {
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 800;
            color: var(--text-main);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 2px;
            letter-spacing: -0.5px;
        }

        .logo span {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo .dot {
            color: var(--primary);
            -webkit-text-fill-color: var(--primary);
            font-size: 24px;
            line-height: 1;
        }

        .nav-links {
            display: flex;
            align-items: center;
            list-style: none;
            gap: 4px;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-muted);
            font-size: 14px;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 9999px;
            transition: all 0.25s ease;
            position: relative;
        }

        .nav-links a:hover,
        .nav-links a.active {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.06);
        }

        .nav-links a.active::after {
            content: '';
            position: absolute;
            bottom: 4px;
            left: 50%;
            transform: translateX(-50%);
            width: 14px;
            height: 2px;
            background: var(--primary);
            border-radius: 2px;
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .btn-resume {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-body);
            font-size: 13.5px;
            font-weight: 600;
            color: #030712;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            border: none;
            padding: 8px 18px;
            border-radius: 9999px;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.25);
        }

        .btn-resume:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4);
            filter: brightness(1.1);
        }

        .mobile-toggle {
            display: none;
            background: transparent;
            border: none;
            color: var(--text-main);
            font-size: 22px;
            cursor: pointer;
            padding: 6px;
        }

        /* Mobile drawer */
        .mobile-menu {
            display: none;
            position: fixed;
            top: 76px;
            left: 5%;
            right: 5%;
            background: rgba(10, 15, 29, 0.96);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 24px;
            z-index: 999;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
            animation: mobileSlide 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .mobile-menu.open {
            display: block;
        }

        @keyframes mobileSlide {
            from { opacity: 0; transform: translateY(-12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .mobile-menu ul {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .mobile-menu a {
            color: var(--text-main);
            text-decoration: none;
            font-size: 16px;
            font-weight: 500;
            display: block;
            padding: 10px 14px;
            border-radius: var(--radius-sm);
            transition: background 0.2s;
        }

        .mobile-menu a:hover {
            background: rgba(255, 255, 255, 0.06);
            color: var(--primary);
        }

        /* ── Common Typography & Section Elements ── */
        section {
            position: relative;
            z-index: 10;
            padding: 110px 6% 90px;
            max-width: 1240px;
            margin: 0 auto;
        }

        .section-header {
            text-align: center;
            max-width: 680px;
            margin: 0 auto 60px;
        }

        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 9999px;
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.25);
            color: var(--primary);
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .pill-badge .dot-glow {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: var(--primary);
            box-shadow: 0 0 8px var(--primary);
            animation: pulseDot 2s infinite;
        }

        @keyframes pulseDot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }

        .section-title {
            font-family: var(--font-display);
            font-size: clamp(30px, 4vw, 46px);
            font-weight: 800;
            letter-spacing: -1px;
            line-height: 1.2;
            margin-bottom: 16px;
            color: var(--text-main);
        }

        .gradient-text {
            background: linear-gradient(135deg, #60a5fa 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .section-divider {
            height: 4px;
            width: 72px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 9999px;
            margin: 0 auto 20px;
        }

        .section-subtitle {
            font-size: 16px;
            color: var(--text-muted);
            line-height: 1.7;
        }

        /* ── Hero Section ── */
        .hero-section {
            min-height: 100vh;
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 40px;
            align-items: center;
            padding-top: 140px;
            padding-bottom: 80px;
        }

        .hero-content {
            position: relative;
            z-index: 2;
        }

        .hero-greeting {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 8px 18px;
            border-radius: 9999px;
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.2);
            color: var(--primary);
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 24px;
        }

        .hero-title {
            font-family: var(--font-display);
            font-size: clamp(42px, 5.2vw, 68px);
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -1.5px;
            margin-bottom: 18px;
        }

        .typed-role-container {
            font-size: clamp(20px, 2.5vw, 28px);
            font-weight: 600;
            font-family: var(--font-display);
            color: var(--text-muted);
            margin-bottom: 20px;
            min-height: 38px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .typed-role {
            color: #7dd3fc;
            border-right: 2px solid #7dd3fc;
            white-space: nowrap;
            animation: cursorBlink 0.8s infinite;
            padding-right: 4px;
        }

        @keyframes cursorBlink {
            0%, 100% { border-color: #7dd3fc; }
            50% { border-color: transparent; }
        }

        .hero-bio {
            font-size: 17px;
            color: var(--text-muted);
            max-width: 540px;
            line-height: 1.7;
            margin-bottom: 36px;
        }

        .hero-btn-row {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            margin-bottom: 48px;
        }

        .btn-primary {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 13px 28px;
            border-radius: var(--radius-md);
            font-family: var(--font-body);
            font-size: 15px;
            font-weight: 600;
            color: #030712;
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 10px 25px -5px rgba(56, 189, 248, 0.35);
            border: none;
            cursor: pointer;
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px -5px rgba(56, 189, 248, 0.5);
            filter: brightness(1.08);
        }

        .btn-secondary {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 13px 26px;
            border-radius: var(--radius-md);
            font-family: var(--font-body);
            font-size: 15px;
            font-weight: 500;
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            text-decoration: none;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .btn-secondary:hover {
            border-color: rgba(56, 189, 248, 0.4);
            background: rgba(56, 189, 248, 0.08);
            color: #ffffff;
            transform: translateY(-2px);
        }

        .hero-stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
            padding-top: 32px;
            border-top: 1px solid var(--border);
            max-width: 580px;
        }

        .stat-card {
            display: flex;
            flex-direction: column;
        }

        .stat-value {
            font-family: var(--font-display);
            font-size: 28px;
            font-weight: 800;
            color: #f8fafc;
            line-height: 1;
            margin-bottom: 4px;
        }

        .stat-value span {
            color: var(--primary);
        }

        .stat-label {
            font-size: 12px;
            font-weight: 500;
            color: var(--text-sub);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Hero Visual Frame (subhasis.me avatar aesthetic) */
        .hero-visual-wrap {
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        .avatar-glow-ring {
            position: relative;
            width: 350px;
            height: 350px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .avatar-glow-ring::before {
            content: '';
            position: absolute;
            inset: -8px;
            border-radius: 50%;
            background: conic-gradient(from 0deg, #38bdf8, #818cf8, #c084fc, #38bdf8);
            animation: spinRing 7s linear infinite;
            filter: blur(12px);
            opacity: 0.7;
        }

        .avatar-glow-ring::after {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 50%;
            background: conic-gradient(from 0deg, #38bdf8, #818cf8, #c084fc, #38bdf8);
            animation: spinRing 7s linear infinite;
        }

        @keyframes spinRing {
            to { transform: rotate(360deg); }
        }

        .avatar-inner {
            position: relative;
            width: 342px;
            height: 342px;
            border-radius: 50%;
            overflow: hidden;
            background: var(--bg-surface);
            border: 6px solid var(--bg-deep);
            z-index: 2;
        }

        .avatar-inner img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform 0.5s ease;
        }

        .avatar-inner:hover img {
            transform: scale(1.05);
        }

        /* Floating badges around photo */
        .floating-badge {
            position: absolute;
            z-index: 10;
            background: rgba(10, 15, 29, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13.5px;
            font-weight: 600;
            color: var(--text-main);
            box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.5);
            animation: badgeFloat 4s ease-in-out infinite alternate;
        }

        .badge-pos-1 {
            top: 20px;
            right: -20px;
            border-color: rgba(56, 189, 248, 0.3);
        }

        .badge-pos-2 {
            bottom: 30px;
            left: -25px;
            animation-delay: -2s;
            border-color: rgba(129, 140, 248, 0.3);
        }

        .badge-pos-3 {
            bottom: -15px;
            right: 40px;
            animation-delay: -1s;
            border-color: rgba(192, 132, 252, 0.3);
        }

        @keyframes badgeFloat {
            0% { transform: translateY(0); }
            100% { transform: translateY(-10px); }
        }

        .badge-icon {
            font-size: 18px;
        }

        /* ── About Section ── */
        .about-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 50px;
            align-items: start;
        }

        .about-story-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 36px;
            backdrop-filter: blur(16px);
            transition: all 0.3s ease;
        }

        .about-story-card:hover {
            border-color: var(--border-hover);
        }

        .about-story-card h3 {
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 16px;
            color: var(--text-main);
        }

        .about-story-card p {
            color: var(--text-muted);
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 20px;
        }

        .story-highlights {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-top: 24px;
        }

        .highlight-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 18px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            font-size: 14px;
            font-weight: 500;
            color: #e2e8f0;
            transition: all 0.25s ease;
        }

        .highlight-item:hover {
            border-color: rgba(56, 189, 248, 0.3);
            background: rgba(56, 189, 248, 0.04);
            transform: translateX(3px);
        }

        .highlight-emoji {
            font-size: 20px;
        }

        /* Education & Journey timeline */
        .timeline-card-group {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .timeline-box {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 26px 28px;
            backdrop-filter: blur(16px);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .timeline-box::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(180deg, var(--primary), var(--secondary));
            opacity: 0.8;
        }

        .timeline-box:hover {
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.35);
            box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
        }

        .timeline-badge {
            font-size: 11.5px;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .timeline-title {
            font-family: var(--font-display);
            font-size: 19px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 4px;
        }

        .timeline-institute {
            font-size: 14.5px;
            color: #7dd3fc;
            font-weight: 500;
            margin-bottom: 10px;
        }

        .timeline-desc {
            font-size: 13.5px;
            color: var(--text-muted);
            line-height: 1.6;
        }

        /* ── Skills Section ── */
        .skills-filter-row {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 44px;
        }

        .filter-btn {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            color: var(--text-muted);
            font-family: var(--font-body);
            font-size: 13.5px;
            font-weight: 500;
            padding: 8px 20px;
            border-radius: 9999px;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .filter-btn:hover,
        .filter-btn.active {
            background: rgba(56, 189, 248, 0.12);
            border-color: rgba(56, 189, 248, 0.4);
            color: #ffffff;
            transform: translateY(-1px);
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }

        .skill-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 20px 22px;
            backdrop-filter: blur(16px);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        .skill-card:hover {
            transform: translateY(-5px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.5);
            background: var(--bg-card-hover);
        }

        .skill-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }

        .skill-meta {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .skill-logo-wrap {
            width: 38px;
            height: 38px;
            background: #ffffff;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 5px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }

        .skill-logo-wrap img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .skill-name {
            font-family: var(--font-display);
            font-size: 16px;
            font-weight: 700;
            color: #f8fafc;
        }

        .skill-category-tag {
            font-size: 11px;
            color: var(--text-sub);
            font-weight: 500;
        }

        .skill-pct {
            font-family: var(--font-display);
            font-size: 15px;
            font-weight: 700;
            color: var(--primary);
        }

        .progress-track {
            height: 6px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 9999px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            border-radius: 9999px;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            transform-origin: left;
            transition: width 1s ease-in-out;
        }

        /* Chart container */
        .chart-wrapper {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 32px;
            backdrop-filter: blur(16px);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            max-width: 680px;
            margin: 0 auto;
        }

        .chart-wrapper h4 {
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #ffffff;
        }

        .chart-wrapper p {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 24px;
        }

        .chart-wrapper img {
            max-width: 100%;
            height: auto;
            border-radius: var(--radius-md);
        }

        /* ── Projects Section ── */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 28px;
        }

        .project-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            backdrop-filter: blur(16px);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .project-card:hover {
            transform: translateY(-8px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.65);
        }

        .project-banner-wrap {
            position: relative;
            width: 100%;
            height: 220px;
            overflow: hidden;
            background: #090e1a;
        }

        .project-banner-wrap img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .project-card:hover .project-banner-wrap img {
            transform: scale(1.06);
        }

        .project-status-badge {
            position: absolute;
            top: 14px;
            right: 14px;
            padding: 5px 12px;
            border-radius: 9999px;
            font-size: 11.5px;
            font-weight: 700;
            background: rgba(3, 7, 18, 0.75);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #7dd3fc;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #34d399;
            box-shadow: 0 0 6px #34d399;
        }

        .project-content {
            padding: 28px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }

        .project-tag {
            font-size: 11.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--primary);
            margin-bottom: 8px;
        }

        .project-title {
            font-family: var(--font-display);
            font-size: 21px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 12px;
            line-height: 1.3;
        }

        .project-desc {
            font-size: 14.5px;
            color: var(--text-muted);
            line-height: 1.65;
            margin-bottom: 22px;
            flex-grow: 1;
        }

        .project-tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 24px;
        }

        .tech-pill {
            font-size: 12px;
            font-weight: 500;
            color: #cbd5e1;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            padding: 4px 10px;
            border-radius: 6px;
        }

        .project-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .btn-project-primary {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 9px 18px;
            border-radius: var(--radius-sm);
            font-size: 13.5px;
            font-weight: 600;
            color: #030712;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            text-decoration: none;
            transition: all 0.25s ease;
        }

        .btn-project-primary:hover {
            transform: translateY(-2px);
            filter: brightness(1.1);
            box-shadow: 0 5px 15px rgba(56, 189, 248, 0.3);
        }

        .btn-project-ghost {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 9px 16px;
            border-radius: var(--radius-sm);
            font-size: 13.5px;
            font-weight: 500;
            color: var(--text-muted);
            background: transparent;
            border: 1px solid var(--border);
            text-decoration: none;
            transition: all 0.25s ease;
        }

        .btn-project-ghost:hover {
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.25);
            background: rgba(255, 255, 255, 0.04);
        }

        /* ── Certifications Section ── */
        .certs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 28px;
        }

        .cert-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 36px 30px;
            backdrop-filter: blur(16px);
            display: flex;
            flex-direction: column;
            text-align: center;
            align-items: center;
            position: relative;
            overflow: hidden;
            transition: all 0.35s ease;
        }

        .cert-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        }

        .cert-card:hover {
            transform: translateY(-6px);
            border-color: rgba(129, 140, 248, 0.4);
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6);
        }

        .cert-icon-badge {
            width: 76px;
            height: 76px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.15), rgba(129, 140, 248, 0.05));
            border: 1px solid rgba(56, 189, 248, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin-bottom: 20px;
        }

        .cert-title {
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
        }

        .cert-issuer {
            font-size: 13.5px;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 14px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        .cert-desc {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.65;
            margin-bottom: 24px;
            flex-grow: 1;
        }

        .btn-cert {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 22px;
            border-radius: 9999px;
            font-size: 13.5px;
            font-weight: 600;
            color: #ffffff;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            text-decoration: none;
            transition: all 0.25s ease;
        }

        .btn-cert:hover {
            border-color: var(--primary);
            color: var(--primary);
            background: rgba(56, 189, 248, 0.08);
            transform: translateY(-2px);
        }

        /* ── Contact Section ── */
        .contact-layout {
            display: grid;
            grid-template-columns: 0.9fr 1.1fr;
            gap: 40px;
            align-items: stretch;
        }

        .contact-info-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 36px;
            backdrop-filter: blur(16px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .contact-info-card h3 {
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #ffffff;
        }

        .contact-info-card p {
            color: var(--text-muted);
            font-size: 15px;
            line-height: 1.7;
            margin-bottom: 32px;
        }

        .contact-links-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
            margin-bottom: 36px;
        }

        .contact-item {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            transition: all 0.25s ease;
        }

        .contact-item:hover {
            border-color: rgba(56, 189, 248, 0.3);
            background: rgba(56, 189, 248, 0.04);
        }

        .contact-icon-box {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: rgba(56, 189, 248, 0.1);
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
        }

        .contact-item-text .label {
            font-size: 11.5px;
            color: var(--text-sub);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .contact-item-text .value {
            font-size: 15px;
            font-weight: 600;
            color: #f1f5f9;
        }

        .social-links-row {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .social-pill-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 9999px;
            font-size: 13.5px;
            font-weight: 500;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            text-decoration: none;
            transition: all 0.25s ease;
        }

        .social-pill-btn:hover {
            color: #ffffff;
            border-color: var(--primary);
            background: rgba(56, 189, 248, 0.1);
            transform: translateY(-2px);
        }

        /* Contact Form */
        .contact-form-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 36px;
            backdrop-filter: blur(16px);
        }

        .contact-form-card h3 {
            font-family: var(--font-display);
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 24px;
            color: #ffffff;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: #cbd5e1;
            margin-bottom: 8px;
        }

        .form-control {
            width: 100%;
            background: rgba(3, 7, 18, 0.6);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 12px 16px;
            font-family: var(--font-body);
            font-size: 14.5px;
            color: #ffffff;
            transition: all 0.25s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
            background: rgba(3, 7, 18, 0.85);
        }

        textarea.form-control {
            min-height: 120px;
            resize: vertical;
        }

        /* ── Modern Toast Notification ── */
        .toast-msg {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid var(--primary);
            color: #ffffff;
            padding: 14px 24px;
            border-radius: var(--radius-md);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(16px);
            font-size: 14px;
            font-weight: 500;
            z-index: 9999;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            pointer-events: none;
        }

        .toast-msg.show {
            transform: translateY(0);
            opacity: 1;
        }

        /* ── Footer ── */
        footer {
            border-top: 1px solid var(--border);
            padding: 40px 6%;
            position: relative;
            z-index: 10;
            background: rgba(3, 7, 18, 0.9);
        }

        .footer-inner {
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .footer-left p {
            font-size: 14px;
            color: var(--text-muted);
        }

        .footer-left span {
            color: #7dd3fc;
            font-weight: 600;
        }

        .footer-links {
            display: flex;
            gap: 20px;
            list-style: none;
        }

        .footer-links a {
            color: var(--text-sub);
            text-decoration: none;
            font-size: 13.5px;
            transition: color 0.2s;
        }

        .footer-links a:hover {
            color: var(--primary);
        }

        /* Back to top button */
        .back-to-top {
            position: fixed;
            bottom: 28px;
            right: 28px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid var(--border);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            cursor: pointer;
            z-index: 900;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
            text-decoration: none;
        }

        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }

        .back-to-top:hover {
            border-color: var(--primary);
            background: rgba(56, 189, 248, 0.15);
            color: var(--primary);
            transform: translateY(-3px);
        }

        /* ── Scroll Reveal Animations ── */
        .reveal {
            opacity: 0;
            transform: translateY(28px);
            transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }

        /* ── Responsive Media Queries ── */
        @media (max-width: 992px) {
            .hero-section {
                grid-template-columns: 1fr;
                text-align: center;
                gap: 50px;
                padding-top: 120px;
            }

            .hero-bio {
                margin-left: auto;
                margin-right: auto;
            }

            .hero-btn-row {
                justify-content: center;
            }

            .hero-stats-grid {
                margin: 0 auto;
            }

            .typed-role-container {
                justify-content: center;
            }

            .about-grid {
                grid-template-columns: 1fr;
            }

            .contact-layout {
                grid-template-columns: 1fr;
            }

            .nav-links, .btn-resume {
                display: none;
            }

            .mobile-toggle {
                display: block;
            }
        }

        @media (max-width: 640px) {
            .hero-stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }

            .story-highlights {
                grid-template-columns: 1fr;
            }

            .avatar-glow-ring {
                width: 290px;
                height: 290px;
            }

            .avatar-inner {
                width: 282px;
                height: 282px;
            }

            .projects-grid {
                grid-template-columns: 1fr;
            }

            .footer-inner {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>
</head>
<body>

    <!-- Ambient glowing backgrounds -->
    <div class="ambient-bg">
        <div class="ambient-orb orb-blue"></div>
        <div class="ambient-orb orb-purple"></div>
        <div class="ambient-orb orb-cyan"></div>
    </div>
    <div class="grid-overlay"></div>
    <div id="cursor-glow"></div>

    <!-- ── Modern Floating Navbar ── -->
    <div class="navbar-wrap" id="navbarWrap">
        <nav class="navbar">
            <a href="#" class="logo">
                <span>{{ name.split()[0] }}</span><span class="dot">.</span>
            </a>

            <ul class="nav-links">
                <li><a href="#about" class="nav-item">About</a></li>
                <li><a href="#skills" class="nav-item">Skills</a></li>
                <li><a href="#projects" class="nav-item">Projects</a></li>
                <li><a href="#certificates" class="nav-item">Certifications</a></li>
                <li><a href="#contact" class="nav-item">Contact</a></li>
            </ul>

            <div class="nav-actions">
                <a href="/resume" class="btn-resume">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    Resume
                </a>
                <button class="mobile-toggle" id="mobileMenuBtn" aria-label="Toggle menu">☰</button>
            </div>
        </nav>
    </div>

    <!-- Mobile Drawer -->
    <div class="mobile-menu" id="mobileMenu">
        <ul>
            <li><a href="#about" class="mobile-nav-link">About Me</a></li>
            <li><a href="#skills" class="mobile-nav-link">Technical Skills</a></li>
            <li><a href="#projects" class="mobile-nav-link">Projects</a></li>
            <li><a href="#certificates" class="mobile-nav-link">Certifications</a></li>
            <li><a href="#contact" class="mobile-nav-link">Contact</a></li>
            <li><a href="/resume" class="mobile-nav-link" style="color:var(--primary);font-weight:700;">📄 Download Resume (PDF)</a></li>
        </ul>
    </div>

    <!-- ── Hero Section ── -->
    <section class="hero-section" id="hero">
        <div class="hero-content reveal">
            <div class="hero-greeting">
                <span class="dot-glow"></span>
                <span>Available for Internships & Projects</span>
            </div>

            <h1 class="hero-title">
                Hi, I'm <br>
                <span class="gradient-text">{{ name }}</span>
            </h1>

            <div class="typed-role-container">
                I am a <span class="typed-role" id="typedRole">Python Developer</span>
            </div>

            <p class="hero-bio">
                {{ about }}
            </p>

            <div class="hero-btn-row">
                <a href="#projects" class="btn-primary">
                    Explore Projects
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                </a>
                <a href="/resume" class="btn-secondary">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                    Download CV
                </a>
                <a href="#contact" class="btn-secondary">
                    Contact Me
                </a>
            </div>

            <div class="hero-stats-grid">
                <div class="stat-card">
                    <div class="stat-value">3<span>+</span></div>
                    <div class="stat-label">Projects Built</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">3</div>
                    <div class="stat-label">NPTEL Certs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">8<span>+</span></div>
                    <div class="stat-label">Tech Stack</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">100<span>%</span></div>
                    <div class="stat-label">Dedication</div>
                </div>
            </div>
        </div>

        <div class="hero-visual-wrap reveal">
            <div class="avatar-glow-ring">
                <div class="avatar-inner">
                    <img src="{{ profile_image }}" alt="{{ name }}" onerror="this.src='https://ui-avatars.com/api/?name=Soumadip+Kar&size=340&background=0a0f1d&color=38bdf8'">
                </div>
            </div>

            <!-- Floating badges -->
            <div class="floating-badge badge-pos-1">
                <span class="badge-icon">🐍</span>
                <span>Python Dev</span>
            </div>
            <div class="floating-badge badge-pos-2">
                <span class="badge-icon">📊</span>
                <span>Data Analytics</span>
            </div>
            <div class="floating-badge badge-pos-3">
                <span class="badge-icon">🧠</span>
                <span>Machine Learning</span>
            </div>
        </div>
    </section>

    <!-- ── About Section ── -->
    <section id="about">
        <div class="section-header reveal">
            <div class="pill-badge">
                <span class="dot-glow"></span>
                <span>Who I Am</span>
            </div>
            <h2 class="section-title">About <span class="gradient-text">Me</span></h2>
            <div class="section-divider"></div>
            <p class="section-subtitle">
                Passionate about data analysis, machine learning algorithms, and building clean web applications that transform complex ideas into intuitive solutions.
            </p>
        </div>

        <div class="about-grid">
            <div class="about-story-card reveal">
                <h3>My Journey & Vision</h3>
                <p>
                    I am a Computer Science Engineering student based in <strong>Kolkata, India 🇮🇳</strong>, specializing in Python development, exploratory data analysis, and predictive modeling.
                </p>
                <p>
                    My workflow centers on writing clean, modular code, extracting meaningful business insights from raw datasets, and engineering accessible web dashboards using Flask and Streamlit. I constantly challenge myself by exploring new algorithms, frameworks, and tools.
                </p>

                <div class="story-highlights">
                    <div class="highlight-item">
                        <span class="highlight-emoji">🧠</span>
                        <span>Machine Learning & Scikit-learn</span>
                    </div>
                    <div class="highlight-item">
                        <span class="highlight-emoji">📊</span>
                        <span>Data Wrangling with Pandas & NumPy</span>
                    </div>
                    <div class="highlight-item">
                        <span class="highlight-emoji">🌐</span>
                        <span>Web Development (Flask & Streamlit)</span>
                    </div>
                    <div class="highlight-item">
                        <span class="highlight-emoji">📈</span>
                        <span>Visual Analytics & Power BI</span>
                    </div>
                </div>
            </div>

            <div class="timeline-card-group reveal">
                <div class="timeline-box">
                    <div class="timeline-badge">2023 — 2027 · Undergrad</div>
                    <h4 class="timeline-title">B.Tech in Computer Science Engineering</h4>
                    <div class="timeline-institute">Brainware University, Kolkata</div>
                    <p class="timeline-desc">
                        Focusing on data structures, algorithmic problem solving, database management systems (SQL), and machine learning applications.
                    </p>
                </div>

                <div class="timeline-box">
                    <div class="timeline-badge">Continuous Learning</div>
                    <h4 class="timeline-title">NPTEL Certified Developer</h4>
                    <div class="timeline-institute">IIT Madras & IIT Kharagpur</div>
                    <p class="timeline-desc">
                        Recognized with top honors across Python Programming, Java Object-Oriented Programming, and Machine Learning fundamentals.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- ── Skills & Tech Toolbox Section ── -->
    <section id="skills">
        <div class="section-header reveal">
            <div class="pill-badge">
                <span class="dot-glow"></span>
                <span>Tech Toolbox</span>
            </div>
            <h2 class="section-title">Skills & <span class="gradient-text">Expertise</span></h2>
            <div class="section-divider"></div>
            <p class="section-subtitle">
                A breakdown of programming languages, libraries, databases, and analytical tools I leverage to craft reliable applications.
            </p>
        </div>

        <div class="skills-filter-row reveal">
            <button class="filter-btn active" data-filter="all">All Skills</button>
            <button class="filter-btn" data-filter="languages">Languages</button>
            <button class="filter-btn" data-filter="datascience">Data Science & AI</button>
            <button class="filter-btn" data-filter="web">Web & Database</button>
        </div>

        <div class="skills-grid">
            {% for skill in skills %}
            <div class="skill-card reveal" data-category="{{ skill.category }}">
                <div class="skill-top">
                    <div class="skill-meta">
                        <div class="skill-logo-wrap">
                            <img src="{{ skill.logo }}" alt="{{ skill.name }}" onerror="this.src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg'">
                        </div>
                        <div>
                            <div class="skill-name">{{ skill.name }}</div>
                            <div class="skill-category-tag">{{ skill.tag }}</div>
                        </div>
                    </div>
                    <div class="skill-pct">{{ skill.level }}%</div>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: {{ skill.level }}%;"></div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Matplotlib Skills Breakdown Chart -->
        <div class="chart-wrapper reveal">
            <h4>Proficiency Breakdown Visualization</h4>
            <p>Generated automatically with Python Matplotlib</p>
            <img src="/static/skills_pie_chart.png" alt="Skills Proficiency Chart">
        </div>
    </section>

    <!-- ── Featured Projects Section ── -->
    <section id="projects">
        <div class="section-header reveal">
            <div class="pill-badge">
                <span class="dot-glow"></span>
                <span>What I've Built</span>
            </div>
            <h2 class="section-title">Featured <span class="gradient-text">Projects</span></h2>
            <div class="section-divider"></div>
            <p class="section-subtitle">
                Explore a selection of my real-world applications spanning machine learning predictive models, analytical dashboards, and web systems.
            </p>
        </div>

        <div class="projects-grid">
            {% for project in projects %}
            <div class="project-card reveal">
                <div class="project-banner-wrap">
                    <img src="{{ project.image }}" alt="{{ project.name }}" onerror="this.src='/static/heart.png'">
                    <div class="project-status-badge">
                        <span class="status-dot"></span>
                        <span>{{ project.status }}</span>
                    </div>
                </div>

                <div class="project-content">
                    <div class="project-tag">{{ project.tag }}</div>
                    <h3 class="project-title">{{ project.name }}</h3>
                    <p class="project-desc">{{ project.description }}</p>

                    <div class="project-tech-stack">
                        {% for tech in project.tech %}
                        <span class="tech-pill">{{ tech }}</span>
                        {% endfor %}
                    </div>

                    <div class="project-actions">
                        <a href="/project/{{ project.id }}" target="_blank" class="btn-project-primary">
                            <span>Live Demo</span>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                        </a>
                        {% if project.github %}
                        <a href="{{ project.github }}" target="_blank" class="btn-project-ghost">
                            <span>GitHub</span>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- ── Certifications & Milestones Section ── -->
    <section id="certificates">
        <div class="section-header reveal">
            <div class="pill-badge">
                <span class="dot-glow"></span>
                <span>Credentials</span>
            </div>
            <h2 class="section-title">Certifications & <span class="gradient-text">Achievements</span></h2>
            <div class="section-divider"></div>
            <p class="section-subtitle">
                Accredited academic certifications from premier national institutes validating theoretical mastery and practical development capability.
            </p>
        </div>

        <div class="certs-grid">
            {% for cert in certificates %}
            <div class="cert-card reveal">
                <div class="cert-icon-badge">{{ cert.emoji }}</div>
                <h3 class="cert-title">{{ cert.name }}</h3>
                <div class="cert-issuer">{{ cert.issuer }}</div>
                <p class="cert-desc">{{ cert.description }}</p>
                <a href="/certificate/{{ cert.id }}" target="_blank" class="btn-cert">
                    <span>View Credential</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                </a>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- ── Contact Section ── -->
    <section id="contact">
        <div class="section-header reveal">
            <div class="pill-badge">
                <span class="dot-glow"></span>
                <span>Let's Connect</span>
            </div>
            <h2 class="section-title">Get In <span class="gradient-text">Touch</span></h2>
            <div class="section-divider"></div>
            <p class="section-subtitle">
                Have a project idea, internship opportunity, or question? Feel free to reach out directly or send a message.
            </p>
        </div>

        <div class="contact-layout">
            <div class="contact-info-card reveal">
                <div>
                    <h3>Contact Information</h3>
                    <p>
                        I'm currently available for developer internships, data analyst roles, and collaborative projects. Let's build something remarkable together!
                    </p>

                    <div class="contact-links-list">
                        <div class="contact-item" style="cursor:pointer;" onclick="copyEmail('{{ email }}')" title="Click to copy email">
                            <div class="contact-icon-box">✉️</div>
                            <div class="contact-item-text">
                                <div class="label">Email Address (Click to Copy)</div>
                                <div class="value">{{ email }}</div>
                            </div>
                        </div>

                        <div class="contact-item">
                            <div class="contact-icon-box">📱</div>
                            <div class="contact-item-text">
                                <div class="label">Phone / WhatsApp</div>
                                <div class="value">{{ phone }}</div>
                            </div>
                        </div>

                        <div class="contact-item">
                            <div class="contact-icon-box">📍</div>
                            <div class="contact-item-text">
                                <div class="label">Location</div>
                                <div class="value">{{ location }}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div>
                    <div style="font-size:12px;font-weight:700;color:var(--text-sub);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">
                        Social Profiles
                    </div>
                    <div class="social-links-row">
                        {% if github %}
                        <a href="{{ github }}" target="_blank" class="social-pill-btn">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                            GitHub
                        </a>
                        {% endif %}
                        {% if linkedin %}
                        <a href="{{ linkedin }}" target="_blank" class="social-pill-btn">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                            LinkedIn
                        </a>
                        {% endif %}
                        <a href="mailto:{{ email }}" class="social-pill-btn">
                            ✉️ Email
                        </a>
                    </div>
                </div>
            </div>

            <div class="contact-form-card reveal">
                <h3>Send a Message</h3>
                <form id="contactForm" onsubmit="handleContactSubmit(event)">
                    <div class="form-group">
                        <label for="nameInput">Your Full Name</label>
                        <input type="text" id="nameInput" name="name" class="form-control" placeholder="e.g. John Doe" required>
                    </div>

                    <div class="form-group">
                        <label for="emailInput">Your Email Address</label>
                        <input type="email" id="emailInput" name="email" class="form-control" placeholder="e.g. john@example.com" required>
                    </div>

                    <div class="form-group">
                        <label for="subjectInput">Subject</label>
                        <input type="text" id="subjectInput" name="subject" class="form-control" placeholder="Project Inquiry / Job Opportunity" required>
                    </div>

                    <div class="form-group">
                        <label for="messageInput">Message</label>
                        <textarea id="messageInput" name="message" class="form-control" placeholder="Hi Soumadip, I would love to talk about..." required></textarea>
                    </div>

                    <button type="submit" class="btn-primary" style="width:100%;justify-content:center;">
                        <span>Send Message</span>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- ── Modern Footer ── -->
    <footer>
        <div class="footer-inner">
            <div class="footer-left">
                <p>© 2026 <span>{{ name }}</span> · Designed with precision & Python Flask</p>
            </div>
            <ul class="footer-links">
                <li><a href="#about">About</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#certificates">Certificates</a></li>
                <li><a href="#contact">Contact</a></li>
                <li><a href="/resume">Resume</a></li>
            </ul>
        </div>
    </footer>

    <!-- Back to top button -->
    <a href="#" class="back-to-top" id="backToTop" aria-label="Back to top">↑</a>

    <!-- Toast Notification -->
    <div class="toast-msg" id="toastMsg">Notification</div>

    <!-- ── Interactive JavaScript ── -->
    <script>
        // 1. Mouse glow tracking
        const glow = document.getElementById('cursor-glow');
        window.addEventListener('mousemove', e => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });

        // 2. Typing Role Animation
        const roles = [
            "Python Web Developer",
            "Data Analyst & Enthusiast",
            "Machine Learning Explorer",
            "B.Tech CSE Student"
        ];
        let roleIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        const typedElement = document.getElementById('typedRole');

        function typeRole() {
            const currentRole = roles[roleIndex];
            if (isDeleting) {
                typedElement.textContent = currentRole.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typedElement.textContent = currentRole.substring(0, charIndex + 1);
                charIndex++;
            }

            let typeSpeed = isDeleting ? 40 : 80;

            if (!isDeleting && charIndex === currentRole.length) {
                typeSpeed = 1800; // Pause at end of word
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                roleIndex = (roleIndex + 1) % roles.length;
                typeSpeed = 400; // Pause before new word
            }

            setTimeout(typeRole, typeSpeed);
        }
        document.addEventListener('DOMContentLoaded', typeRole);

        // 3. Navbar scroll blur & back-to-top toggle
        const navbarWrap = document.getElementById('navbarWrap');
        const backToTop = document.getElementById('backToTop');
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-links a');

        window.addEventListener('scroll', () => {
            const scrollPos = window.scrollY;

            if (scrollPos > 30) {
                navbarWrap.classList.add('scrolled');
                backToTop.classList.add('visible');
            } else {
                navbarWrap.classList.remove('scrolled');
                backToTop.classList.remove('visible');
            }

            // Scroll spy
            let current = '';
            sections.forEach(sec => {
                const sectionTop = sec.offsetTop - 140;
                const sectionHeight = sec.clientHeight;
                if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                    current = sec.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        });

        // 4. Mobile Menu toggle
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const mobileMenu = document.getElementById('mobileMenu');
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
        });

        document.querySelectorAll('.mobile-nav-link').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
            });
        });

        // 5. Skills Category Filter
        const filterBtns = document.querySelectorAll('.filter-btn');
        const skillCards = document.querySelectorAll('.skill-card');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filter = btn.getAttribute('data-filter');
                skillCards.forEach(card => {
                    const cat = card.getAttribute('data-category');
                    if (filter === 'all' || cat === filter) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });

        // 6. Scroll Reveal Observer
        const observerOptions = { threshold: 0.12, rootMargin: '0px 0px -40px 0px' };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

        // 7. Toast Message & Clipboard Copy
        function showToast(message) {
            const toast = document.getElementById('toastMsg');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        function copyEmail(email) {
            navigator.clipboard.writeText(email).then(() => {
                showToast("✓ Email copied to clipboard: " + email);
            }).catch(() => {
                showToast("Email: " + email);
            });
        }

        // 8. Contact Form Submission
        function handleContactSubmit(e) {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);

            fetch('/contact', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast("🎉 Thank you! Your message was received.");
                    form.reset();
                } else {
                    showToast("Message received! Thank you for connecting.");
                    form.reset();
                }
            })
            .catch(() => {
                showToast("🎉 Thank you! Your message was received.");
                form.reset();
            });
        }
    </script>
</body>
</html>
"""

# ── Certificates Data ─────────────────────────────────────────────────────────
CERTIFICATES = {
    "python": {
        "name": "Python Programming",
        "issuer": "NPTEL · IIT Madras",
        "description": "Comprehensive certification covering Python core concepts, OOP design, algorithmic thinking, and application development.",
        "emoji": "🐍",
        "file": "p.jpg.png"
    },
    "java": {
        "name": "Java Programming",
        "issuer": "NPTEL · IIT Kharagpur",
        "description": "Object-oriented programming, data structures, multi-threading, and core application development certification.",
        "emoji": "☕",
        "file": "j.jpg.png"
    },
    "ml": {
        "name": "Machine Learning",
        "issuer": "NPTEL · IIT",
        "description": "Hands-on machine learning covering regression, classification, clustering, model evaluation, and predictive pipelines.",
        "emoji": "🤖",
        "file": "M.jpg.png"
    }
}

# ── Projects Data ─────────────────────────────────────────────────────────────
PROJECTS = {
    "heart": {
        "id": "heart",
        "name": "Heart Disease Prediction",
        "tag": "Machine Learning · Streamlit",
        "status": "Live Demo",
        "description": "ML-powered diagnostic web app predicting cardiovascular disease risk based on clinical patient indicators with real-time risk score inference.",
        "tech": ["Python", "Scikit-Learn", "Pandas", "Streamlit"],
        "image": "/static/heart.png",
        "link": "https://heart-disease-prediction-kzxn8hqkappjonxv2bvvckm.streamlit.app/",
        "github": "https://github.com/SoumadipKar"
    },
    "student": {
        "id": "student",
        "name": "Student Result Dashboard",
        "tag": "Analytics · Python & Flask",
        "status": "Active Project",
        "description": "Semester-wise academic performance and GPA tracking dashboard with interactive grade distributions, subject analytics, and student progress reports.",
        "tech": ["Python", "Flask", "Pandas", "Matplotlib"],
        "image": "/static/project_student.jpg",
        "link": "https://github.com/SoumadipKar",
        "github": "https://github.com/SoumadipKar"
    },
    "sales": {
        "id": "sales",
        "name": "Sales Performance Dashboard",
        "tag": "Business Intelligence · Visualization",
        "status": "Active Project",
        "description": "Interactive business analytics dashboard for monitoring regional revenue, monthly sales KPIs, product category margins, and performance trends.",
        "tech": ["Power BI", "SQL", "Python", "Data Analytics"],
        "image": "/static/project_sales.jpg",
        "link": "https://github.com/SoumadipKar",
        "github": "https://github.com/SoumadipKar"
    }
}

# ── Skills Data ───────────────────────────────────────────────────────────────
SKILLS = [
    {"name": "Python",       "tag": "Core Language",      "category": "languages",   "logo": "/static/py.png",      "level": 92},
    {"name": "Java",         "tag": "OOP & Backend",      "category": "languages",   "logo": "/static/java.jpg",    "level": 85},
    {"name": "SQL / MySQL",  "tag": "Relational DB",      "category": "web",         "logo": "/static/mysql.png",   "level": 88},
    {"name": "Pandas",       "tag": "Data Manipulation",  "category": "datascience", "logo": "/static/pandas.jpg",  "level": 88},
    {"name": "NumPy",        "tag": "Numerical Computing","category": "datascience", "logo": "/static/numpy.png",   "level": 82},
    {"name": "Matplotlib",   "tag": "Data Visualization", "category": "datascience", "logo": "/static/matplot.png", "level": 86},
    {"name": "Power BI",     "tag": "BI Dashboards",      "category": "datascience", "logo": "/static/powerbi.png", "level": 80},
    {"name": "Flask",        "tag": "Web Framework",     "category": "web",         "logo": "/static/py.png",      "level": 82},
    {"name": "Streamlit",    "tag": "ML Web Apps",        "category": "datascience", "logo": "/static/py.png",      "level": 85}
]

# ── Chart Generator (Optimized & Cached) ──────────────────────────────────────
def ensure_chart(static_folder):
    path = os.path.join(static_folder, "skills_pie_chart.png")
    if os.path.exists(path):
        return  # Cache hit, avoid re-rendering on every request

    skills_data = {
        "Python": 92,
        "Java": 85,
        "SQL": 88,
        "Pandas": 88,
        "NumPy": 82,
        "Matplotlib": 86,
        "Power BI": 80
    }

    os.makedirs(static_folder, exist_ok=True)
    COLORS = ["#38bdf8", "#818cf8", "#a855f7", "#34d399", "#f59e0b", "#ec4899", "#06b6d4"]
    BG = "#090e1a"

    fig, ax = plt.subplots(figsize=(6.5, 6.5), facecolor=BG)
    ax.set_facecolor(BG)

    wedges, texts, autotexts = ax.pie(
        skills_data.values(),
        labels=None,
        autopct="%1.0f%%",
        startangle=90,
        colors=COLORS,
        wedgeprops={"edgecolor": BG, "linewidth": 3, "width": 0.6},
        pctdistance=0.76
    )

    for at in autotexts:
        at.set_color("#ffffff")
        at.set_fontsize(10)
        at.set_fontweight("bold")

    ax.set_title("Skills Proficiency Breakdown", fontsize=14, fontweight="bold", color="#f8fafc", pad=18)

    legend_patches = [
        mpatches.Patch(color=COLORS[i], label=f"{k} ({v}%)")
        for i, (k, v) in enumerate(skills_data.items())
    ]
    ax.legend(
        handles=legend_patches,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=3,
        frameon=False,
        fontsize=10,
        labelcolor="#94a3b8"
    )

    ax.axis("equal")
    plt.tight_layout(pad=1.2)
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    static_folder = os.path.join(app.root_path, "static")
    ensure_chart(static_folder)

    data = {
        "name": "Soumadip Kar",
        "title": "Python Web Developer · Data Analyst Student",
        "about": "I am an enthusiastic Python developer and aspiring data analyst passionate about creating modern data-driven websites, interactive dashboards, and machine learning models. I enjoy solving real-world challenges through clean, modular code.",
        "profile_image": "/static/SK.jpg.png",
        "skills": SKILLS,
        "projects": list(PROJECTS.values()),
        "certificates": [
            {
                "id": k,
                "name": v["name"],
                "issuer": v["issuer"],
                "description": v["description"],
                "emoji": v["emoji"]
            }
            for k, v in CERTIFICATES.items()
        ],
        "email": "karsoumadip9@gmail.com",
        "phone": "+91 99088 98604",
        "location": "Kolkata, West Bengal, India 🇮🇳",
        "github": "https://github.com/SoumadipKar",
        "linkedin": "https://www.linkedin.com/in/soumadip-kar-9a1b4b1b2/"
    }

    return render_template_string(HTML, **data)


@app.route("/resume")
def download_resume():
    folder = os.path.join(app.root_path, "static")
    resume_file = "ck2.pdf"
    if not os.path.exists(os.path.join(folder, resume_file)):
        abort(404)
    return send_from_directory(folder, resume_file, as_attachment=True, download_name="Soumadip_Kar_Resume.pdf")


@app.route("/view-resume")
def view_resume():
    folder = os.path.join(app.root_path, "static")
    resume_file = "ck2.pdf"
    if not os.path.exists(os.path.join(folder, resume_file)):
        abort(404)
    return send_from_directory(folder, resume_file)


@app.route("/certificate/<cert_id>")
def view_certificate(cert_id):
    cert = CERTIFICATES.get(cert_id)
    if not cert:
        abort(404)
    folder = os.path.join(app.root_path, "static")
    return send_from_directory(folder, cert["file"])


@app.route("/project/<project_id>")
def view_project(project_id):
    project = PROJECTS.get(project_id)
    if not project:
        abort(404)
    return redirect(project["link"])


@app.route("/contact", methods=["POST"])
def contact():
    # Handle contact form submissions gracefully
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Please provide your name, email, and message."}), 400

    # In a full deployment, this can send an email via SMTP or store in SQLite.
    return jsonify({
        "success": True,
        "message": f"Thank you {name}! Your message has been received."
    })


if __name__ == "__main__":
    static_folder = os.path.join(app.root_path, "static")
    ensure_chart(static_folder)
    app.run(debug=True, port=5000)