'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google'
import styles from './page.module.css'

// Using the backend client ID as configured in .env
const GOOGLE_CLIENT_ID = "1092970477426-u9oe8so5qvh7mhqddvcpk419jb2l1dtu.apps.googleusercontent.com"

export default function LoginPage() {
  const { user, login } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (user) router.push('/dashboard')
  }, [user, router])

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // Send the Google JWT ID token to our backend
      await login(credentialResponse.credential)
      router.push('/dashboard')
    } catch (err) {
      console.error('Login failed:', err)
    }
  }

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <div className={styles.page}>
        <div className={styles.glow} />

        <div className={styles.card}>
          <div className={styles.header}>
            <span className={styles.icon}>🎓</span>
            <h1 className={styles.title}>Saarthi</h1>
            <p className={styles.subtitle}>Smart Student Onboarding Assistant</p>
          </div>

          <div className={styles.features}>
            <div className={styles.feature}>
              <span>📋</span>
              <span>Track your onboarding tasks</span>
            </div>
            <div className={styles.feature}>
              <span>💬</span>
              <span>Ask questions, get instant answers</span>
            </div>
            <div className={styles.feature}>
              <span>📄</span>
              <span>Upload documents seamlessly</span>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '1rem', width: '100%' }}>
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => console.error('Google login failed')}
              theme="filled_blue"
              size="large"
              shape="pill"
              text="continue_with"
            />
          </div>

          <p className={styles.disclaimer}>
            By continuing, you agree to the college&apos;s terms of service and privacy policy.
          </p>
        </div>
      </div>
    </GoogleOAuthProvider>
  )
}
