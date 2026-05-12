'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { useAuth } from '@/lib/auth'
import { tasks, chat } from '@/lib/api'
import styles from './page.module.css'

export default function Dashboard() {
  const { user } = useAuth()
  const [progress, setProgress] = useState(null)
  const [systemHealth, setSystemHealth] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [prog, health] = await Promise.allSettled([
          tasks.progress(),
          chat.health(),
        ])
        if (prog.status === 'fulfilled') setProgress(prog.value)
        if (health.status === 'fulfilled') setSystemHealth(health.value)
      } catch (err) {
        console.error('Dashboard load error:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const pct = progress?.percentage || 0

  return (
    <AppShell>
      <div className={styles.page}>
        <div className={styles.greeting}>
          <h1>Welcome back, {user?.full_name?.split(' ')[0] || 'Student'} 👋</h1>
          <p className={styles.greetingSub}>Here&apos;s your onboarding overview</p>
        </div>

        {/* Stats Grid */}
        <div className={styles.statsGrid}>
          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>📊</span>
            <div>
              <span className={styles.statValue}>{pct}%</span>
              <span className={styles.statLabel}>Completed</span>
            </div>
            <div className={styles.progressBar}>
              <div className={styles.progressFill} style={{ width: `${pct}%` }} />
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>📌</span>
            <div>
              <span className={styles.statValue}>{progress?.pending || 0}</span>
              <span className={styles.statLabel}>Pending Tasks</span>
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>✅</span>
            <div>
              <span className={styles.statValue}>{progress?.completed || 0}</span>
              <span className={styles.statLabel}>Completed</span>
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>⚠️</span>
            <div>
              <span className={styles.statValue}>{progress?.overdue || 0}</span>
              <span className={styles.statLabel}>Overdue</span>
            </div>
          </div>
        </div>

        {/* Quick Actions + System Status */}
        <div className={styles.bottomGrid}>
          <div className={`card ${styles.actionsCard}`}>
            <h3 className={styles.cardTitle}>Quick Actions</h3>
            <div className={styles.actions}>
              <a href="/chat" className={styles.actionBtn}>
                <span>💬</span>
                <div>
                  <strong>Ask Saarthi</strong>
                  <small>Get instant answers about admissions, fees, hostel, etc.</small>
                </div>
              </a>
              <a href="/tasks" className={styles.actionBtn}>
                <span>📋</span>
                <div>
                  <strong>View Tasks</strong>
                  <small>Check your onboarding checklist and deadlines</small>
                </div>
              </a>
              <a href="/documents" className={styles.actionBtn}>
                <span>📄</span>
                <div>
                  <strong>Upload Documents</strong>
                  <small>Submit verification documents</small>
                </div>
              </a>
              <a href="/tickets" className={styles.actionBtn}>
                <span>🎫</span>
                <div>
                  <strong>Support Tickets</strong>
                  <small>Check status of your escalated queries</small>
                </div>
              </a>
            </div>
          </div>

          <div className={`card ${styles.statusCard}`}>
            <h3 className={styles.cardTitle}>System Status</h3>
            <div className={styles.statusList}>
              <div className={styles.statusItem}>
                <span>AI Assistant</span>
                <span className={`badge ${systemHealth?.ollama?.status === 'connected' ? 'badge-success' : 'badge-error'}`}>
                  {systemHealth?.ollama?.status || 'checking...'}
                </span>
              </div>
              <div className={styles.statusItem}>
                <span>Knowledge Base</span>
                <span className={`badge ${systemHealth?.vector_store?.status === 'healthy' ? 'badge-success' : 'badge-error'}`}>
                  {systemHealth?.vector_store?.document_count || 0} docs
                </span>
              </div>
              <div className={styles.statusItem}>
                <span>Agent Graph</span>
                <span className={`badge ${systemHealth?.agent_graph?.status === 'compiled' ? 'badge-success' : 'badge-warning'}`}>
                  {systemHealth?.agent_graph?.status || 'checking...'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  )
}
