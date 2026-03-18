/* ============================================
   Tuition Connect — Main JavaScript
   ============================================
   Lenis smooth scrolling, GSAP animations,
   navbar behavior, and global utilities.
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ── Initialize Lucide Icons ────────────────
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // ── Select2 Initialization ─────────────────
    if (typeof jQuery !== 'undefined' && typeof jQuery.fn.select2 !== 'undefined') {
        jQuery('.neu-select-multiple').select2({
            placeholder: "Select options",
            allowClear: true,
            width: '100%',
            tags: true
        });
        jQuery('.neu-select').select2({
            minimumResultsForSearch: Infinity,
            width: '100%'
        });
    }
    let lenis;
    try {
        lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            orientation: 'vertical',
            smoothWheel: true,
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);

        // Connect Lenis with GSAP ScrollTrigger
        if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);

            lenis.on('scroll', ScrollTrigger.update);

            gsap.ticker.add((time) => {
                lenis.raf(time * 1000);
            });
            gsap.ticker.lagSmoothing(0);
        }
    } catch (e) {
        console.log('Lenis not loaded, using native scrolling');
    }

    // ── Navbar Scroll Effect ───────────────────
    const navbar = document.getElementById('navbar');
    if (navbar) {
        let lastScroll = 0;
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            lastScroll = currentScroll;
        });
    }

    // ── Mobile Nav Toggle ──────────────────────
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navLinks.classList.toggle('open');
        });

        // Close on link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navLinks.classList.remove('open');
            });
        });
    }

    // ── GSAP Scroll Reveal Animations ──────────
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {

        // Fade up reveals
        gsap.utils.toArray('.reveal').forEach((el) => {
            gsap.to(el, {
                opacity: 1,
                y: 0,
                duration: 0.8,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                    toggleActions: 'play none none none',
                },
            });
        });

        // Slide from left
        gsap.utils.toArray('.reveal-left').forEach((el) => {
            gsap.to(el, {
                opacity: 1,
                x: 0,
                duration: 0.8,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                },
            });
        });

        // Slide from right
        gsap.utils.toArray('.reveal-right').forEach((el) => {
            gsap.to(el, {
                opacity: 1,
                x: 0,
                duration: 0.8,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                },
            });
        });

        // Scale reveals
        gsap.utils.toArray('.reveal-scale').forEach((el) => {
            gsap.to(el, {
                opacity: 1,
                scale: 1,
                duration: 0.6,
                ease: 'back.out(1.7)',
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                },
            });
        });

        // Stagger children
        gsap.utils.toArray('.stagger-children').forEach((container) => {
            const children = container.children;
            gsap.from(children, {
                opacity: 0,
                y: 30,
                duration: 0.6,
                stagger: 0.1,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: container,
                    start: 'top 80%',
                },
            });
        });

        // Hero animations (if on landing page)
        const heroTag = document.querySelector('.hero-tag');
        const heroTitle = document.querySelector('.hero h1');
        const heroSubtitle = document.querySelector('.hero-subtitle');
        const heroActions = document.querySelector('.hero-actions');
        const heroStats = document.querySelector('.hero-stats');
        const heroVisual = document.querySelector('.hero-visual');

        if (heroTag) {
            const heroTl = gsap.timeline({ delay: 0.3 });
            heroTl
                .from(heroTag, { opacity: 0, y: 20, duration: 0.6, ease: 'power3.out' })
                .from(heroTitle, { opacity: 0, y: 40, duration: 0.8, ease: 'power3.out' }, '-=0.3')
                .from(heroSubtitle, { opacity: 0, y: 30, duration: 0.6, ease: 'power3.out' }, '-=0.4')
                .from(heroActions, { opacity: 0, y: 20, duration: 0.6, ease: 'power3.out' }, '-=0.3')
                .from(heroStats, { opacity: 0, y: 20, duration: 0.6, ease: 'power3.out' }, '-=0.3');

            if (heroVisual) {
                heroTl.from(heroVisual, {
                    opacity: 0,
                    x: 60,
                    duration: 1,
                    ease: 'power3.out'
                }, '-=1.2');
            }
        }
    }

    // ── Auto-dismiss Alerts ────────────────────
    document.querySelectorAll('.alert').forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'all 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });

    // ── Counter Animation ──────────────────────
    function animateCounter(el, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        const isFloat = target % 1 !== 0;

        function step() {
            start += increment;
            if (start >= target) {
                el.textContent = isFloat ? target.toFixed(0) : target.toLocaleString();
                return;
            }
            el.textContent = isFloat ? Math.floor(start).toLocaleString() : Math.floor(start).toLocaleString();
            requestAnimationFrame(step);
        }
        step();
    }

    // Observe stat numbers
    const statNumbers = document.querySelectorAll('[data-count]');
    if (statNumbers.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.dataset.count);
                    animateCounter(entry.target, target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statNumbers.forEach(el => observer.observe(el));
    }

    console.log('%c✨ Tuition Connect loaded', 'color: #6c5ce7; font-weight: bold; font-size: 14px;');
});
