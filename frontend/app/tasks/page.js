'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { tasks as tasksApi } from '@/lib/api'
import styles from './page.module.css'

const STATUS_MAP = {
  pending: { label: 'Pending', badge: 'badge-warning' },
  in_progress: { label: 'In Progress', badge: 'badge-info' },
  completed: { label: 'Completed', badge: 'badge-success' },
  overdue: { label: 'Overdue', badge: 'badge-error' },
}

const CATEGORY_ICONS = {
  DOCUMENT: '📄',
  FEE: '💰',
  ACADEMIC: '📖',
  ORIENTATION: '🎯',
  GENERAL: '📌',
}

export default function TasksPage() {
  const [taskList, setTaskList] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [progress, setProgress] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const [list, prog] = await Promise.all([
          tasksApi.list(),
          tasksApi.progress(),
        ])
        setTaskList(list)
        setProgress(prog)
      } catch (err) {
        console.error('Failed to load tasks:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const pct = progress?.percentage || 0

  const filtered = filter === 'all'
    ? taskList
    : (taskList || []).filter((ut) => ut.status === filter)

  return (
    <AppShell>
      <div className={styles.page}>
        <div className={styles.header}>
          <div>
            <h1 className="text-gray-900 dark:text-white">My Onboarding Tasks</h1>
            <p className={`${styles.subtitle} text-gray-600 dark:text-slate-400`}>
              {progress?.completed || 0} of {progress?.total || 0} tasks completed
            </p>
          </div>
          <div className={styles.progressRing}>
            <svg viewBox="0 0 100 100" className={styles.ringSvg}>
              <circle cx="50" cy="50" r="42" className={styles.ringBg} />
              <circle
                cx="50" cy="50" r="42"
                className={styles.ringFill}
                strokeDasharray={`${pct * 2.64} 264`}
              />
            </svg>
            <span className={styles.ringText}>{pct}%</span>
          </div>
        </div>

        {/* Filters */}
        <div className={styles.filters}>
          {['all', 'pending', 'in_progress', 'completed', 'overdue'].map((f) => (
            <button
              key={f}
              className={`${styles.filterBtn} ${filter === f ? styles.activeFilter : ''}`}
              onClick={() => setFilter(f)}
            >
              {f === 'all' ? 'All' : STATUS_MAP[f]?.label || f}
            </button>
          ))}
        </div>

        {/* Task List */}
        {loading ? (
          <div className={styles.loadingGrid}>
            {[1, 2, 3, 4].map(i => <div key={i} className={`skeleton ${styles.skelCard}`} />)}
          </div>
        ) : filtered.length === 0 ? (
          <div className={styles.empty}>
            <span>🎉</span>
            <p className="text-gray-500 dark:text-slate-400">{filter === 'all' ? 'No tasks assigned yet' : `No ${filter} tasks`}</p>
          </div>
        ) : (
          <div className={styles.taskGrid}>
            {filtered.map((ut) => {
              const task = ut.task || {}
              const status = STATUS_MAP[ut.status] || STATUS_MAP.pending
              const icon = CATEGORY_ICONS[task.category] || '📌'

              return (
                <div key={ut.id} className={`card ${styles.taskCard}`}>
                  <div className={styles.taskTop}>
                    <span className={styles.taskIcon}>{icon}</span>
                    <span className={`badge ${status.badge}`}>{status.label}</span>
                  </div>
                  <h3 className={styles.taskTitle}>{task.title}</h3>
                  <p className={styles.taskDesc}>{task.description}</p>
                  <div className={styles.taskMeta}>
                    {task.is_mandatory && <span className={styles.mandatory}>Required</span>}
                    {task.requires_document && <span className={styles.docTag}>📎 Document</span>}
                    {task.deadline && (
                      <span className={styles.deadline}>
                        Due: {new Date(task.deadline).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
                      </span>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </AppShell>
  )
}
