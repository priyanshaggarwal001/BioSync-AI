
import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import './IntroScreen.css'

type IntroScreenProps = {
  onComplete: () => void
}

export default function IntroScreen({ onComplete }: IntroScreenProps) {
  const introRef = useRef<HTMLDivElement>(null)
  const [finished, setFinished] = useState(false)

  useEffect(() => {
    const root = introRef.current
    if (!root) return

    const finish = () => {
      if (finished) return
      setFinished(true)
      onComplete()
    }

    const reducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)',
    ).matches

    if (reducedMotion) {
      finish()
      return
    }

    const ctx = gsap.context(() => {
      const timeline = gsap.timeline({
        onComplete: finish,
      })

      timeline
        .fromTo(
          '.intro-logo',
          { opacity: 0, scale: 0.88, filter: 'blur(10px)' },
          {
            opacity: 1,
            scale: 1,
            filter: 'blur(0px)',
            duration: 0.9,
            ease: 'power3.out',
          },
        )
        .fromTo(
          '.intro-wordmark',
          { opacity: 0, y: 10 },
          { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out' },
          '-=0.35',
        )
        .fromTo(
          '.intro-progress-fill',
          { scaleX: 0 },
          { scaleX: 1, duration: 1.15, ease: 'power2.inOut' },
          '-=0.05',
        )
        
        // The emblem surges forward and fills the screen.
        .to(
          '.intro-logo',
          {
            scale: 18,
            rotation: -8,
            filter:
              'drop-shadow(0 0 45px rgba(56, 200, 178, 0.9)) drop-shadow(0 0 120px rgba(56, 200, 178, 0.55))',
            duration: 1.05,
            ease: 'power3.in',
          },
          '+=0.12',
        )
        // The wordmark and loading details dissolve behind it.
        .to(
          ['.intro-wordmark', '.intro-tagline', '.intro-progress', '.intro-loading'],
          {
            opacity: 0,
            duration: 0.22,
            ease: 'power1.out',
          },
          '<',
        )
        // Reveal the existing homepage through the expanded emblem.
        .to(
          root,
          {
            opacity: 0,
            duration: 0.65,
            ease: 'power2.inOut',
          },
          '-=0.18',
        )

        .to(
          root,
          {
            opacity: 0,
            duration: 0.55,
            ease: 'power2.inOut',
          },
          '-=0.15',
        )
    }, root)

    return () => ctx.revert()
  }, [onComplete])

  return (
    <div
      ref={introRef}
      className={`intro-screen${finished ? ' intro-screen--finished' : ''}`}
      role="status"
      aria-label="Welcome to BioSync AI"
    >
      <div className="intro-glow" aria-hidden="true" />

      <div className="intro-content">
        <img
          className="intro-logo"
          src="/biosync-loading-icon.png"
          alt="BioSync AI logo"
        />

        <div className="intro-wordmark">
          <span>BioSync</span>
          <span className="intro-ai"> AI</span>
        </div>

        <p className="intro-tagline">LIVING HEALTH INTELLIGENCE</p>

        <div
          className="intro-progress"
          role="progressbar"
          aria-label="Intro animation"
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <span className="intro-progress-fill" />
        </div>

        <span className="intro-loading">CONNECTING YOUR HEALTH STORY</span>
      </div>

      <button
        className="intro-skip"
        type="button"
        onClick={() => {
          gsap.killTweensOf([introRef.current, '.intro-content'])
          onComplete()
        }}
      >
        Skip intro <span aria-hidden="true">↗</span>
      </button>
    </div>
  )
}
