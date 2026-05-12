'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { tickets } from '@/lib/api'
import styles from './page.module.css'

export default function TicketsPage() {
  const [ticketList, setTicketList] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTickets()
  }, [])

  async function fetchTickets() {
    try {
      const data = await tickets.listMy()
      setTicketList(data)
    } catch (err) {
      console.error('Failed to load tickets', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'resolved': return <span className="badge badge-success">Resolved</span>
      case 'closed': return <span className="badge badge-info">Closed</span>
      case 'open': return <span className="badge badge-warning">Open</span>
      default: return <span className="badge badge-accent">{status}</span>
    }
  }

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'high':
      case 'urgent': return <span className="badge badge-error">High</span>
      case 'low': return <span className="badge badge-info">Low</span>
      default: return <span className="badge badge-warning">Medium</span>
    }
  }

  return (
    <AppShell>
      <div className={styles.page}>
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>Support Tickets</h1>
            <p className={styles.subtitle}>Track your escalated issues and support requests.</p>
          </div>
        </div>

        <div className={styles.list}>
          {loading ? (
            <div className="skeleton" style={{ height: 120, borderRadius: 12 }}></div>
          ) : ticketList.length === 0 ? (
            <div className={styles.emptyState}>
              <span className={styles.emptyIcon}>🎫</span>
              <p>No support tickets yet.</p>
              <p className={styles.hint}>If you need help, ask Saarthi in the chat!</p>
            </div>
          ) : (
            ticketList.map(ticket => (
              <div key={ticket.id} className={`card ${styles.ticketCard}`}>
                <div className={styles.ticketHeader}>
                  <h3>{ticket.subject}</h3>
                  <div className={styles.badges}>
                    {getPriorityBadge(ticket.priority)}
                    {getStatusBadge(ticket.status)}
                  </div>
                </div>
                <p className={styles.description}>{ticket.description}</p>
                <div className={styles.meta}>
                  <span>ID: {ticket.id.slice(0, 8)}</span>
                  <span>Dept: {ticket.department || 'General'}</span>
                  <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                  {ticket.source === 'ai_escalation' && (
                    <span className={styles.aiBadge}>✨ AI Escalated</span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </AppShell>
  )
}
