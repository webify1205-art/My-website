// === Video Showcase Modal Logic ===

const projectModal = document.getElementById('projectModal');
const modalBackdrop = document.getElementById('modalBackdrop');
const modalContent = document.getElementById('modalContent');
const modalCloseBtn = document.getElementById('modalCloseBtn');

const modalVideo = document.getElementById('modalVideo');
const modalVideoSource = document.getElementById('modalVideoSource');
const modalCategory = document.getElementById('modalCategory');
const modalTitle = document.getElementById('modalTitle');
const modalDescription = document.getElementById('modalDescription');
const modalLiveLink = document.getElementById('modalLiveLink');
// Particles.js Configuration
    particlesJS('particles-js', {
        particles: {
            number: {
                value: 100,
                density: {
                    enable: true,
                    value_area: 800
                }
            },
            color: {
                value: '#C59B85'
            },
            shape: {
                type: 'circle'
            },
            opacity: {
                value: 0.6,
                random: true,
                anim: {
                    enable: true,
                    speed: 1,
                    opacity_min: 0.1,
                    sync: false
                }
            },
            size: {
                value: 3,
                random: true,
                anim: {
                    enable: true,
                    speed: 2,
                    size_min: 0.1,
                    sync: false
                }
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: '#C59B85',
                opacity: 0.3,
                width: 1
            },
            move: {
                enable: true,
                speed: 1.5,
                direction: 'none',
                random: false,
                straight: false,
                out_mode: 'out',
                bounce: false,
                attract: {
                    enable: true,
                    rotateX: 600,
                    rotateY: 1200
                }
            }
        },
        interactivity: {
            detect_on: 'canvas',
            events: {
                onhover: {
                    enable: true,
                    mode: 'grab'
                },
                onclick: {
                    enable: true,
                    mode: 'push'
                },
                resize: true
            },
            modes: {
                grab: {
                    distance: 180,
                    line_linked: {
                        opacity: 1
                    }
                },
                bubble: {
                    distance: 200,
                    size: 6,
                    duration: 2,
                    opacity: 0.8
                },
                push: {
                    particles_nb: 4
                }
            }
        }
    });
    
    // GSAP Hero Animations
    // Text reveal animation for headline
    gsap.from('.reveal-text', {
        duration: 1.5,
        y: 100,
        opacity: 0,
        ease: 'power4.out',
        delay: 0.5
    });
    
    // Subheadline fade in
    gsap.to('.hero-subheadline', {
        duration: 1,
        opacity: 1,
        y: 0,
        ease: 'power3.out',
        delay: 1.2
    });
    
    // Description fade in
    gsap.to('.hero-description', {
        duration: 1,
        opacity: 1,
        y: 0,
        ease: 'power3.out',
        delay: 1.5
    });
    
    // CTA button fade in with scale
    gsap.to('.hero-cta', {
        duration: 1,
        opacity: 1,
        scale: 1,
        ease: 'back.out(1.7)',
        delay: 1.8
    });
    
    // Portfolio Filter Functionality
    const filterBtns = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            
            // Update active button
            filterBtns.forEach(b => {
                b.classList.remove('bg-[var(--color-rose-gold)]', 'text-[var(--color-charcoal-black)]');
                b.classList.add('border', 'border-[var(--color-rose-gold)]', 'text-[var(--color-rose-gold)]');
            });
            btn.classList.add('bg-[var(--color-rose-gold)]', 'text-[var(--color-charcoal-black)]');
            btn.classList.remove('border', 'border-[var(--color-rose-gold)]', 'text-[var(--color-rose-gold)]');
            
            // Filter items
            portfolioItems.forEach(item => {
                if (filter === 'all' || item.dataset.category === filter) {
                    gsap.to(item, {
                        opacity: 1,
                        scale: 1,
                        duration: 0.3,
                        display: 'block'
                    });
                } else {
                    gsap.to(item, {
                        opacity: 0,
                        scale: 0.8,
                        duration: 0.3,
                        display: 'none'
                    });
                }
            });
        });
    });
    
    // Floating Dock Navigation Spotlight Animation
    const dockItems = document.querySelectorAll('.dock-item');
    const spotlight = document.getElementById('spotlight');
    
    function moveSpotlight(targetItem) {
        const dockRect = targetItem.parentElement.getBoundingClientRect();
        const itemRect = targetItem.getBoundingClientRect();
        
        const relativeLeft = itemRect.left - dockRect.left;
        
        gsap.to(spotlight, {
            left: relativeLeft,
            opacity: 1,
            duration: 0.15,
            ease: 'power2.out'
        });
    }
    
    // Initialize spotlight on first active item
    const initialActive = document.querySelector('.dock-item.active');
    if (initialActive) {
        setTimeout(() => moveSpotlight(initialActive), 500);
    }
    
    // Handle click events
    dockItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active state
            dockItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            // Move spotlight
            moveSpotlight(item);
            
            // Smooth scroll to section
            const targetSection = item.getAttribute('href');
            const section = document.querySelector(targetSection);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Handle scroll-based active state
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        dockItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${current}`) {
                item.classList.add('active');
                moveSpotlight(item);
            }
        });
    });
 


/**
 * Opens the project showcase modal and animates it in.
 * @param {Object} project - { title, description, category, video_filename, live_link }
 */
function showProject(project) {
    // Populate content
    modalCategory.textContent = project.category || '';
    modalTitle.textContent = project.title || '';
    modalDescription.textContent = project.description || '';

    if (project.live_link) {
        modalLiveLink.href = project.live_link;
        modalLiveLink.classList.remove('hidden');
    } else {
        modalLiveLink.classList.add('hidden');
    }

    if (project.video_filename) {
        modalVideoSource.src = `/static/uploads/videos/${project.video_filename}`;
        modalVideo.load();
    }

    // Reset state before animating in
    gsap.set(modalContent, { opacity: 0, scale: 0.95 });
    gsap.set(modalBackdrop, { opacity: 0 });
    gsap.set('.modalDescription', { y: 30, opacity: 0 });
    gsap.set(modalVideo, { opacity: 0, rotateY: 30, rotateX: 12 });

    projectModal.classList.remove('hidden');
    projectModal.classList.add('flex');
    document.body.style.overflow = 'hidden';

    const tl = gsap.timeline();

    // 1. Fade in modal backdrop + container
    tl.to(modalBackdrop, {
        opacity: 1,
        duration: 0.4,
        ease: 'power2.out'
    })
    .to(modalContent, {
        opacity: 1,
        scale: 1,
        duration: 0.5,
        ease: 'power3.out'
    }, '-=0.3')
    // 2. Video settles into its 3D tilt position
    .to(modalVideo, {
        opacity: 1,
        rotateY: 16,
        rotateX: 6,
        duration: 0.7,
        ease: 'power4.out'
    }, '-=0.2')
    // 3. Staggered text glide-up, right after video settles
    .to('.modal-detail', {
        y: 0,
        opacity: 1,
        duration: 0.6,
        stagger: 0.12,
        ease: 'power3.out'
    }, '-=0.3');

    if (modalVideo.play) {
        modalVideo.play().catch(() => {});
    }
}

/**
 * Closes the project showcase modal with a reverse animation.
 */
function closeProject() {
    const tl = gsap.timeline({
        onComplete: () => {
            projectModal.classList.add('hidden');
            projectModal.classList.remove('flex');
            document.body.style.overflow = '';
            modalVideo.pause();
            modalVideoSource.src = '';
        }
    });

    tl.to('.modal-detail', {
        y: 20,
        opacity: 0,
        duration: 0.3,
        stagger: 0.05,
        ease: 'power2.in'
    })
    .to(modalVideo, {
        opacity: 0,
        rotateY: 24,
        rotateX: 10,
        duration: 0.4,
        ease: 'power2.in'
    }, '-=0.2')
    .to(modalContent, {
        opacity: 0,
        scale: 0.95,
        duration: 0.3,
        ease: 'power2.in'
    }, '-=0.2')
    .to(modalBackdrop, {
        opacity: 0,
        duration: 0.3
    }, '-=0.2');
}

// Close interactions
modalCloseBtn.addEventListener('click', closeProject);
modalBackdrop.addEventListener('click', closeProject);
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !projectModal.classList.contains('hidden')) {
        closeProject();
    }
});
// Wire up portfolio grid clicks to open the modal
document.querySelectorAll('.portfolio-item').forEach(item => {
    item.addEventListener('click', () => {
        showProject({
            title: item.dataset.title,
            description: item.dataset.description,
            category: item.dataset.category,
            video_filename: item.dataset.video
        });
    });
});