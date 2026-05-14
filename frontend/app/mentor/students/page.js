'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { useAuth } from '@/lib/auth'
import { mentors } from '@/lib/api'
import styles from './page.module.css'

export default function MentorStudents() {
  const { user } = useAuth()
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const data = await mentors.getStudents()
        setStudents(data)
      } catch (err) {
        console.error('Failed to load students', err)
      } finally {
        setLoading(false)
      }
    }
    if (user?.role?.toUpperCase() === 'MENTOR') {
      load()
    } else {
      setLoading(false)
    }
  }, [user])

  if (!user || user.role?.toUpperCase() !== 'MENTOR') {
    return (
      <AppShell>
        <div className={styles.emptyState}>Access Denied. Mentor role required.</div>
      </AppShell>
    )
  }

  return (
    <AppShell>
      <div className={styles.page}>
        <div className={styles.header}>
          <div>
            <h1>My Assigned Students</h1>
            <p>Track your cohort&apos;s onboarding progress and flag issues.</p>
          </div>
          <div className="badge badge-success">{students.length} Students</div>
        </div>

        {loading ? (
          <p>Loading students...</p>
        ) : students.length > 0 ? (
          <div className={styles.grid}>
            {students.map((student) => (
              <div key={student.id} className={styles.studentCard}>
                <div className={styles.studentHeader}>
                  <div className={styles.avatar}>
                    {student.avatar_url ? (
                      <img src={student.avatar_url} alt="" referrerPolicy="no-referrer" />
                    ) : (
                      student.full_name.charAt(0)
                    )}
                  </div>
                  <div className={styles.info}>
                    <span className={styles.name}>{student.full_name}</span>
                    <span className={styles.email}>{student.email}</span>
                  </div>
                </div>

                <div className={styles.meta}>
                  <span className={styles.badge}>Stage: {student.stage.replace('_', ' ')}</span>
                  {student.department && <span className={styles.badge}>{student.department}</span>}
                  {student.batch && <span className={styles.badge}>Batch {student.batch}</span>}
                </div>

                <div className={styles.actions}>
                  <button className={`${styles.btn} ${styles.primary}`}>View Progress</button>
                  <button className={`${styles.btn} ${styles.secondary}`}>Send Message</button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={styles.emptyState}>
            <h2>No students assigned yet</h2>
            <p>Admin staff has not mapped any students to your advisory cohort.</p>
          </div>
        )}
      </div>
    </AppShell>
  )
}
