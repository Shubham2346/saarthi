'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { useAuth } from '@/lib/auth'
import { tasks, chat, analytics } from '@/lib/api'
import styles from './page.module.css'

export default function Dashboard() {
  const { user } = useAuth()
  const [progress, setProgress] = useState(null)
  const [systemHealth, setSystemHealth] = useState(null)
  const [adminMetrics, setAdminMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const promises = [chat.health()]
        
        const userRole = user?.role?.toUpperCase()
        if (userRole === 'ADMIN' || userRole === 'SYSTEM_ADMIN') {
          promises.push(analytics.dashboard())
        } else {
          promises.push(tasks.progress())
        }

        const results = await Promise.allSettled(promises)
        
        if (results[0].status === 'fulfilled') setSystemHealth(results[0].value)
        
        if (results[1].status === 'fulfilled') {
          const userRole = user?.role?.toUpperCase()
          if (userRole === 'ADMIN' || userRole === 'SYSTEM_ADMIN') {
            setAdminMetrics(results[1].value)
          } else {
            setProgress(results[1].value)
          }
        }
      } catch (err) {
        console.error('Dashboard load error:', err)
      } finally {
        setLoading(false)
      }
    }
    
    if (user) load()
  }, [user])

  const renderStudentDashboard = () => {
    const pct = progress?.percentage || 0
    return (
      <>
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
          {renderSystemStatus()}
        </div>
      </>
    )
  }

  const renderAdminDashboard = () => {
    return (
      <>
        {/* Stats Grid */}
        <div className={styles.statsGrid}>
          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>👥</span>
            <div>
              <span className={styles.statValue}>{adminMetrics?.users?.students || 0}</span>
              <span className={styles.statLabel}>Enrolled Students</span>
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>📄</span>
            <div>
              <span className={styles.statValue}>{adminMetrics?.documents?.pending_verification || 0}</span>
              <span className={styles.statLabel}>Pending Documents</span>
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>🎫</span>
            <div>
              <span className={styles.statValue}>{adminMetrics?.tickets?.open || 0}</span>
              <span className={styles.statLabel}>Open Support Tickets</span>
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>📈</span>
            <div>
              <span className={styles.statValue}>{adminMetrics?.tasks?.completion_rate || 0}%</span>
              <span className={styles.statLabel}>Platform Task Completion</span>
            </div>
            <div className={styles.progressBar}>
              <div className={styles.progressFill} style={{ width: `${adminMetrics?.tasks?.completion_rate || 0}%` }} />
            </div>
          </div>
        </div>

        {/* Quick Actions + System Status */}
        <div className={styles.bottomGrid}>
          <div className={`card ${styles.actionsCard}`}>
            <h3 className={styles.cardTitle}>Admin Actions</h3>
            <div className={styles.actions}>
              <a href="/documents" className={styles.actionBtn}>
                <span>📄</span>
                <div>
                  <strong>Verify Documents</strong>
                  <small>Review AI verifications and approve documents</small>
                </div>
              </a>
              <a href="/tickets" className={styles.actionBtn}>
                <span>🎫</span>
                <div>
                  <strong>Resolve Tickets</strong>
                  <small>Handle escalated queries from students</small>
                </div>
              </a>
              <a href="/tasks" className={styles.actionBtn}>
                <span>📋</span>
                <div>
                  <strong>Manage Task Templates</strong>
                  <small>Create and edit onboarding task templates</small>
                </div>
              </a>
            </div>
          </div>
          {renderSystemStatus()}
        </div>
      </>
    )
  }

  const renderSystemStatus = () => (
    <div className={`card ${styles.statusCard}`}>
      <h3 className={styles.cardTitle}>System Status</h3>
      <div className={styles.statusList}>
        <div className={styles.statusItem}>
          <span>AI Assistant (Ollama)</span>
          <span className={`badge ${systemHealth?.ollama?.status === 'connected' ? 'badge-success' : 'badge-error'}`}>
            {systemHealth?.ollama?.status || 'checking...'}
          </span>
        </div>
        <div className={styles.statusItem}>
          <span>Knowledge Base (ChromaDB)</span>
          <span className={`badge ${systemHealth?.vector_store?.status === 'healthy' ? 'badge-success' : 'badge-error'}`}>
            {systemHealth?.vector_store?.document_count || 0} docs
          </span>
        </div>
        <div className={styles.statusItem}>
          <span>Agent Graph Workflow</span>
          <span className={`badge ${systemHealth?.agent_graph?.status === 'compiled' ? 'badge-success' : 'badge-warning'}`}>
            {systemHealth?.agent_graph?.status || 'checking...'}
          </span>
        </div>
      </div>
    </div>
  )

  const renderMentorDashboard = () => {
    return (
      <>
        {/* Stats Grid */}
        <div className={styles.statsGrid}>
          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>👨‍🎓</span>
            <div>
              <span className={styles.statValue}>12</span>
              <span className={styles.statLabel}>Assigned Students</span>
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>⚠️</span>
            <div>
              <span className={styles.statValue}>3</span>
              <span className={styles.statLabel}>Escalation Alerts</span>
            </div>
          </div>
        </div>

        {/* Quick Actions + System Status */}
        <div className={styles.bottomGrid}>
          <div className={`card ${styles.actionsCard}`}>
            <h3 className={styles.cardTitle}>Mentor Actions</h3>
            <div className={styles.actions}>
              <a href="/mentor/students" className={styles.actionBtn}>
                <span>👨‍🎓</span>
                <div>
                  <strong>View Assigned Students</strong>
                  <small>Track onboarding completion and progress</small>
                </div>
              </a>
              <a href="/tickets" className={styles.actionBtn}>
                <span>🎫</span>
                <div>
                  <strong>Review Escalations</strong>
                  <small>Communicate guidance for flagged students</small>
                </div>
              </a>
            </div>
          </div>
        </div>
      </>
    )
  }

  const renderSystemAdminDashboard = () => {
    return (
      <>
        {/* Stats Grid */}
        <div className={styles.statsGrid}>
          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>👥</span>
            <div>
              <span className={styles.statValue}>{adminMetrics?.users?.total || 0}</span>
              <span className={styles.statLabel}>Total Platform Users</span>
            </div>
          </div>

          <div className={`card ${styles.statCard}`}>
            <span className={styles.statIcon}>📈</span>
            <div>
              <span className={styles.statValue}>{adminMetrics?.tasks?.completion_rate || 0}%</span>
              <span className={styles.statLabel}>Platform Task Completion</span>
            </div>
            <div className={styles.progressBar}>
              <div className={styles.progressFill} style={{ width: `${adminMetrics?.tasks?.completion_rate || 0}%` }} />
            </div>
          </div>
        </div>

        {/* Quick Actions + System Status */}
        <div className={styles.bottomGrid}>
          <div className={`card ${styles.actionsCard}`}>
            <h3 className={styles.cardTitle}>System Admin Actions</h3>
            <div className={styles.actions}>
              <a href="/admin/users" className={styles.actionBtn}>
                <span>👥</span>
                <div>
                  <strong>Manage User Roles</strong>
                  <small>Control system access permissions</small>
                </div>
              </a>
              <a href="/admin/templates" className={styles.actionBtn}>
                <span>⚙️</span>
                <div>
                  <strong>Configure Workflows</strong>
                  <small>Maintain task templates and system settings</small>
                </div>
              </a>
              <a href="/admin/knowledge" className={styles.actionBtn}>
                <span>📚</span>
                <div>
                  <strong>System Logs</strong>
                  <small>Monitor logs and maintain knowledge base</small>
                </div>
              </a>
            </div>
          </div>
          {renderSystemStatus()}
        </div>
      </>
    )
  }

  const renderDashboardByRole = () => {
    const userRole = user?.role?.toUpperCase()
    if (userRole === 'SYSTEM_ADMIN') return renderSystemAdminDashboard()
    if (userRole === 'ADMIN') return renderAdminDashboard()
    if (userRole === 'MENTOR') return renderMentorDashboard()
    return renderStudentDashboard()
  }

  const getRoleDisplayName = (role) => {
    const userRole = role?.toUpperCase()
    if (userRole === 'SYSTEM_ADMIN') return 'System Admin'
    if (userRole === 'ADMIN') return 'Admin'
    if (userRole === 'MENTOR') return 'Mentor'
    return 'Student'
  }

  return (
    <AppShell>
      <div className={styles.page}>
        <div className={styles.greeting}>
          <h1>Welcome back, {user?.full_name?.split(' ')[0] || getRoleDisplayName(user?.role)} 👋</h1>
          <p className={styles.greetingSub}>
            Here is your {getRoleDisplayName(user?.role).toLowerCase()} overview
          </p>
        </div>

        {loading ? (
          <p>Loading dashboard...</p>
        ) : (
          renderDashboardByRole()
        )}
      </div>
    </AppShell>
  )
}
