
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Lenis from 'lenis'
import './App.css'

gsap.registerPlugin(ScrollTrigger)

function App() {
  const pageRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const root = pageRef.current
    if (!root) return

    const reducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)',
    ).matches

    const context = gsap.context(() => {
      if (reducedMotion) return

      gsap.from('.hero-copy > *', {
        y: 28,
        opacity: 0,
        duration: 0.85,
        stagger: 0.12,
        ease: 'power3.out',
      })

      gsap.from('.orb-assembly', {
        scale: 0.86,
        opacity: 0,
        duration: 1.2,
        ease: 'power3.out',
      })

      gsap.to('.orb-assembly', {
        x: 90,
        y: 100,
        scale: 0.78,
        rotateZ: 22,
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero-section',
          start: 'top top',
          end: 'bottom top',
          scrub: 0.6,
        },
      })

      
    gsap.to('.orb-ring--outer', {
      rotate: 360,
      ease: 'none',
      scrollTrigger: {
        trigger: '.story-section',
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1,
      },
    })

    gsap.to('.orb-ring--middle', {
      rotate: -180,
      scale: 1.08,
      ease: 'none',
      scrollTrigger: {
        trigger: '.story-section',
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1,
      },
    })

    gsap.to('.orb-core', {
      rotateY: 18,
      rotateX: -10,
      ease: 'none',
      scrollTrigger: {
        trigger: '.hero-section',
        start: 'top top',
        end: 'bottom top',
        scrub: 1,
      },
    })


      gsap.from('.feature-card', {
        y: 32,
        opacity: 0,
        duration: 0.7,
        stagger: 0.14,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: '.features-grid',
          start: 'top 82%',
          once: true,
        },
      })
    }, root)

    let lenis: Lenis | null = null
    let lenisFrame: ((time: number) => void) | null = null

    if (!reducedMotion) {
      lenis = new Lenis()
      lenis.on('scroll', ScrollTrigger.update)

      lenisFrame = (time: number) => {
        lenis?.raf(time * 1000)
      }

      gsap.ticker.add(lenisFrame)
      gsap.ticker.lagSmoothing(0)
    }

    return () => {
      if (lenisFrame) gsap.ticker.remove(lenisFrame)
      lenis?.destroy()
      context.revert()
    }
  }, [])

  return (
    <div className="site-shell" ref={pageRef}>
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>

      <header className="site-header">
        <a className="brand" href="#" aria-label="BioSync AI home">
          <span className="brand-mark" aria-hidden="true">
            <span />
            <span />
            <span />
          </span>
          <span>BioSync<span className="brand-ai"> AI</span></span>
        </a>

        <nav className="main-nav" aria-label="Main navigation">
          <a href="#platform">Platform</a>
          <a href="#how-it-works">How it works</a>
          <a href="#dashboard-preview">Your health</a>
        </nav>

        <a className="header-cta" href="#get-started">
          Get started <span aria-hidden="true">↗</span>
        </a>
      </header>

      <main id="main-content">
        <section className="hero-section" id="platform">
          <div className="hero-grid" aria-hidden="true" />

          <div className="hero-inner">
            <div className="hero-copy">
              <div className="eyebrow">
                <span className="status-dot" />
                YOUR HEALTH, CONNECTED
              </div>

              <h1>
                Understand your health.
                <span> Move forward.</span>
              </h1>

              <p className="hero-description">
                Your health data tells a story. BioSync AI brings your
                health records, daily activity, and recovery trends
                together to help you understand the bigger picture.
              </p>

              <div className="hero-actions">
                <a className="button-primary" href="#get-started">
                  Explore BioSync <span aria-hidden="true">→</span>
                </a>
                <a className="button-secondary" href="#how-it-works">
                  Discover how it works
                </a>
              </div>

              <div className="hero-note">
                <span className="note-check" aria-hidden="true">✓</span>
                One connected view of your health
              </div>
            </div>

            <div
              className="hero-visual"
              role="img"
              aria-label="Abstract teal 3D orb representing connected health data"
            >
              <div className="orb-assembly">
                <div className="orb-shadow" />
                <div className="orb-ring orb-ring--outer" />
                <div className="orb-ring orb-ring--middle" />
                <div className="orb-ring orb-ring--inner" />

                <div className="orb-core">
                  <div className="orb-highlight" />
                  <div className="orb-contour orb-contour--one" />
                  <div className="orb-contour orb-contour--two" />
                  <div className="orb-contour orb-contour--three" />
                  <div className="orb-center">
                    <span className="pulse-line" />
                  </div>
                </div>

                <div className="orb-node orb-node--top" />
                <div className="orb-node orb-node--right" />
                <div className="orb-node orb-node--bottom" />

                <div className="floating-label floating-label--top">
                  <span className="label-indicator" />
                  HEALTH DATA
                </div>

                <div className="floating-label floating-label--bottom">
                  <span className="label-sparkle">✳</span>
                  CONNECTED INSIGHTS
                </div>
              </div>

              <div className="visual-caption">
                <span className="caption-line" />
                A clearer view of you
              </div>
            </div>
          </div>

          <div className="hero-bottom">
            <span>DESIGNED AROUND YOUR HEALTH</span>
            <a href="#how-it-works">
              SCROLL TO EXPLORE <span aria-hidden="true">↓</span>
            </a>
          </div>
        </section>

        <section className="story-section section-padding" id="how-it-works">
          <div className="section-kicker">THE BIGGER PICTURE</div>

          <div className="story-layout">
            <div className="story-heading">
              <h2>
                Your health isn't
                <span> just one number.</span>
              </h2>
            </div>

            <div className="story-copy">
              <p>
                Health information often lives in different places.
                BioSync AI brings these pieces together so you can explore
                patterns across your records and everyday activity.
              </p>
              <a className="text-link" href="#dashboard-preview">
                See the connected experience <span aria-hidden="true">↗</span>
              </a>
            </div>
          </div>

          <div className="features-grid">
            <article className="feature-card">
              <span className="feature-number">01 / CONNECT</span>
              <div className="feature-symbol symbol-connect" aria-hidden="true">
                <span /><span /><span />
              </div>
              <h3>Bring it together.</h3>
              <p>
                Explore health records, wearable measurements, and
                manually recorded information in one place.
              </p>
            </article>

            <article className="feature-card feature-card--accent">
              <span className="feature-number">02 / UNDERSTAND</span>
              <div className="feature-symbol symbol-insight" aria-hidden="true">
                <span /><span /><span /><span /><span />
              </div>
              <h3>Find the patterns.</h3>
              <p>
                Review recorded trends and wellness insights to better
                understand changes over time.
              </p>
            </article>

            <article className="feature-card">
              <span className="feature-number">03 / ACT</span>
              <div className="feature-symbol symbol-action" aria-hidden="true">
                <span>↗</span>
              </div>
              <h3>Take the next step.</h3>
              <p>
                Receive general wellness suggestions informed by your
                recorded wearable trends.
              </p>
            </article>
          </div>
        </section>

        <section className="dashboard-preview section-padding" id="dashboard-preview">
          <div className="preview-copy">
            <div className="section-kicker">YOUR PERSONAL HEALTH SPACE</div>
            <h2>
              The details,
              <span> in perspective.</span>
            </h2>
            <p>
              A dedicated health dashboard brings your timeline, wellness
              score, trends, and AI-generated explanations into one
              organized experience.
            </p>
            <p className="preview-disclaimer">
              Insights depend on the health data available and are not a
              substitute for professional medical advice.
            </p>
          </div>

          <div className="preview-panel">
            <div className="preview-panel-header">
              <div>
                <span className="panel-overline">BIOSYNC OVERVIEW</span>
                <h3>Your health at a glance</h3>
              </div>
              <span className="preview-live-dot" aria-label="Preview" />
            </div>

            <div className="preview-metrics">
              <div className="preview-metric">
                <span>Wellness</span>
                <strong>—</strong>
                <small>Awaiting your data</small>
              </div>
              <div className="preview-metric">
                <span>Sleep</span>
                <strong>—</strong>
                <small>Wearable data</small>
              </div>
              <div className="preview-metric">
                <span>Activity</span>
                <strong>—</strong>
                <small>Daily movement</small>
              </div>
            </div>

            <div className="preview-chart">
              <div className="chart-heading">
                <span>HEALTH TRENDS</span>
                <span>Personal overview</span>
              </div>
              <div className="chart-illustration" aria-hidden="true">
                <span /><span /><span /><span /><span /><span /><span />
              </div>
              <p>Your recorded trends will appear here.</p>
            </div>
          </div>
        </section>

        <section className="closing-section" id="get-started">
          <div className="closing-orb" aria-hidden="true" />
          <div className="section-kicker">A MORE CONNECTED PERSPECTIVE</div>
          <h2>
            Get to know your
            <span> health story.</span>
          </h2>
          <p>
            Start with a clearer view of the information you already have.
          </p>
          <a className="button-primary" href="#platform">
            Explore the platform <span aria-hidden="true">↑</span>
          </a>
          <span className="closing-note">
            Login and account creation will be connected in a later step.
          </span>
        </section>
      </main>

      <footer className="site-footer">
        <a className="brand" href="#platform">
          <span className="brand-mark" aria-hidden="true">
            <span /><span /><span />
          </span>
          <span>BioSync<span className="brand-ai"> AI</span></span>
        </a>
        <p>Connected health. Clearer perspective.</p>
        <span>© {new Date().getFullYear()} BioSync AI</span>
      </footer>
    </div>
  )
}

export default App
