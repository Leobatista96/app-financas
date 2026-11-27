/* ============================================================
   Verba — js/main.js
   Comportamentos copiados do design system (design_system/design_system.html):
   - shadow da navbar ao rolar
   - reveals GSAP + ScrollTrigger (reveal-text / reveal-visual / reveal-section)
   Respeita prefers-reduced-motion.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // --- NAVBAR ---
  var navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 20) {
        navbar.classList.add('shadow-lg');
      } else {
        navbar.classList.remove('shadow-lg');
      }
    });
  }

  // --- ANIMATIONS ---
  if (reduceMotion || typeof gsap === 'undefined') return;

  var splitTextToSpans = function (element) {
    var text = element.innerText;
    var words = text.split(' ');
    var newContent = words.map(function (word) {
      return '<span class="inline-block overflow-hidden align-top leading-tight"><span class="inline-block translate-y-full reveal-word-inner">' + word + '&nbsp;</span></span>';
    }).join('');
    element.innerHTML = newContent;
  };

  document.querySelectorAll('.reveal-text').forEach(function (el) {
    splitTextToSpans(el);
    gsap.to(el.querySelectorAll('.reveal-word-inner'), {
      y: 0,
      duration: 0.8,
      stagger: 0.03,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        toggleActions: 'play none none reverse'
      }
    });
  });

  gsap.utils.toArray('.reveal-visual').forEach(function (visual) {
    gsap.from(visual, {
      scrollTrigger: {
        trigger: visual,
        start: 'top 80%'
      },
      scale: 0.95,
      opacity: 0,
      duration: 1.2,
      ease: 'power2.out'
    });
  });

  gsap.utils.toArray('.reveal-section').forEach(function (section) {
    gsap.from(section.children, {
      scrollTrigger: {
        trigger: section,
        start: 'top 80%'
      },
      y: 30,
      opacity: 0,
      duration: 0.8,
      stagger: 0.1,
      ease: 'power3.out'
    });
  });
});
