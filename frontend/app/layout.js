import './globals.css'
import { AuthProvider } from '@/lib/auth'

export const metadata = {
  title: 'Saarthi — Smart Student Onboarding',
  description: 'AI-powered onboarding assistant for college students. Track tasks, get answers, and breeze through admissions.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
