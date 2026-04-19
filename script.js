/* ============================================
   EDGE ENTERPRISE LLC - INTERACTIVE SCRIPT
   GSAP Animations, Custom Cursor, CountUp
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ---- Preloader ----
    const preloader = document.getElementById('preloader');
    let animationsInitialized = false;

    function startSite() {
        if (animationsInitialized) return;
        animationsInitialized = true;
        preloader.classList.add('hidden');
        document.body.style.overflow = '';
        initAnimations();
    }

    // Fire after short delay regardless of load state
    setTimeout(startSite, 2500);

    window.addEventListener('load', () => {
        setTimeout(startSite, 1500);
    });

    // ---- Custom Cursor ----
    const cursorDot = document.getElementById('cursorDot');
    const cursorRing = document.getElementById('cursorRing');
    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    if (window.innerWidth > 768) {
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            cursorDot.style.left = mouseX + 'px';
            cursorDot.style.top = mouseY + 'px';
        });

        function animateCursor() {
            ringX += (mouseX - ringX) * 0.15;
            ringY += (mouseY - ringY) * 0.15;
            cursorRing.style.left = ringX + 'px';
            cursorRing.style.top = ringY + 'px';
            requestAnimationFrame(animateCursor);
        }
        animateCursor();

        // Hover effect on interactive elements
        const hoverElements = document.querySelectorAll('a, button, .project-card, .service-card, .testimonial-card');
        hoverElements.forEach(el => {
            el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
            el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
        });
    }

    // ---- Navigation ----
    const nav = document.getElementById('mainNav');
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    // Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 60) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // Mobile toggle
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close mobile nav on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // ---- GSAP Animations ----
    function initAnimations() {
        gsap.registerPlugin(ScrollTrigger);

        // Hero animations handled by pure CSS keyframes
        // No GSAP touches hero elements to avoid conflicts

        // Scroll-triggered section animations
        const animateElements = document.querySelectorAll('[data-animate]');
        animateElements.forEach(el => {
            const type = el.getAttribute('data-animate');
            const delay = parseFloat(el.getAttribute('data-delay')) || 0;

            let fromProps = { opacity: 0, duration: 0.8, ease: 'power3.out', delay };

            switch (type) {
                case 'fade-up':
                    fromProps.y = 60;
                    break;
                case 'fade-left':
                    fromProps.x = 60;
                    break;
                case 'fade-right':
                    fromProps.x = -60;
                    break;
                default:
                    fromProps.y = 40;
            }

            gsap.from(el, {
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                },
                ...fromProps
            });
        });

        // Service card stagger
        gsap.from('.service-card', {
            scrollTrigger: {
                trigger: '.services-grid',
                start: 'top 80%'
            },
            y: 60,
            opacity: 0,
            stagger: 0.1,
            duration: 0.7,
            ease: 'power3.out'
        });

        // Process timeline animation
        gsap.from('.process-line', {
            scrollTrigger: {
                trigger: '.process-timeline',
                start: 'top 80%',
                end: 'bottom 20%',
                scrub: 1
            },
            scaleY: 0,
            transformOrigin: 'top'
        });

        // Parallax for about image
        gsap.to('.about-image', {
            scrollTrigger: {
                trigger: '.about-image-card',
                start: 'top bottom',
                end: 'bottom top',
                scrub: 1
            },
            y: -30
        });
    }

    // ---- CountUp Stats ----
    const statNumbers = document.querySelectorAll('.stat-number');

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-count'));
                const duration = 2;

                // Simple count animation
                let start = 0;
                const startTime = performance.now();

                function updateCount(currentTime) {
                    const elapsed = (currentTime - startTime) / 1000;
                    const progress = Math.min(elapsed / duration, 1);

                    // Ease out cubic
                    const eased = 1 - Math.pow(1 - progress, 3);
                    const current = Math.round(eased * target);

                    el.textContent = current;

                    if (progress < 1) {
                        requestAnimationFrame(updateCount);
                    }
                }

                requestAnimationFrame(updateCount);
                statsObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => statsObserver.observe(el));

    // ---- GLightbox ----
    if (typeof GLightbox !== 'undefined') {
        GLightbox({
            selector: '.glightbox',
            touchNavigation: true,
            loop: true,
            autoplayVideos: true,
            skin: 'clean'
        });
    }

    // ---- Contact Form ----
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const btn = contactForm.querySelector('button[type="submit"]');
            const originalHTML = btn.innerHTML;

            btn.innerHTML = '<span>Sending...</span>';
            btn.disabled = true;

            // Simulate send (replace with actual form handler)
            setTimeout(() => {
                btn.innerHTML = '<span>Message Sent!</span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
                btn.style.background = '#22C55E';

                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.background = '';
                    btn.disabled = false;
                    contactForm.reset();
                }, 3000);
            }, 1500);
        });
    }

    // ---- Magnetic Buttons ----
    if (window.innerWidth > 768) {
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = '';
            });
        });
    }

    // ---- Tilt Effect on Cards ----
    if (window.innerWidth > 768) {
        document.querySelectorAll('.service-card, .testimonial-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;

                const rotateX = (0.5 - y) * 8;
                const rotateY = (x - 0.5) * 8;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    // ---- Active Nav Link on Scroll ----
    const sections = document.querySelectorAll('section[id]');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY + 200;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });

    // ---- Text Reveal on Scroll ----
    // Skipped word-split to preserve inner HTML spans

});
