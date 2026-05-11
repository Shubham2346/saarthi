'use client'

import { useState, useRef, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { chat } from '@/lib/api'
import styles from './page.module.css'

const CATEGORY_FILTERS = [
  { value: null, label: 'All Topics' },
  { value: 'ADMISSION', label: '🎓 Admissions' },
  { value: 'FEE', label: '💰 Fees' },
  { value: 'HOSTEL', label: '🏠 Hostel' },
  { value: 'ACADEMIC', label: '📖 Academic' },
  { value: 'LMS', label: '💻 LMS' },
  { value: 'EXAM', label: '📝 Exams' },
  { value: 'PLACEMENT', label: '💼 Placements' },
  { value: 'GENERAL', label: '📌 General' },
]

const QUICK_QUESTIONS = [
  'What documents do I need for admission?',
  'What is the fee structure?',
  'How do I access the LMS portal?',
  'What are the hostel rules?',
]

export default function ChatPage() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [category, setCategory] = useState(null)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend(text) {
    const message = text || input.trim()
    if (!message || loading) return

    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setLoading(true)

    try {
      const res = await chat.send(message, category)

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.answer,
        intent: res.intent,
        confidence: res.confidence,
        sources: res.sources,
        agentMessages: res.agent_messages,
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I had trouble processing that. Please try again.',
        error: true,
      }])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const isEmpty = messages.length === 0

  return (
    <AppShell>
      <div className={styles.page}>
        <div className={styles.chatContainer}>
          {/* Header */}
          <div className={styles.chatHeader}>
            <div>
              <h2 className={styles.chatTitle}>Ask Saarthi</h2>
              <p className={styles.chatSubtitle}>Your AI onboarding assistant</p>
            </div>
            <select
              className={styles.categorySelect}
              value={category || ''}
              onChange={(e) => setCategory(e.target.value || null)}
            >
              {CATEGORY_FILTERS.map((cat) => (
                <option key={cat.value || 'all'} value={cat.value || ''}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          {/* Messages Area */}
          <div className={styles.messagesArea}>
            {isEmpty ? (
              <div className={styles.emptyState}>
                <span className={styles.emptyIcon}>🎓</span>
                <h3>How can I help you today?</h3>
                <p>Ask me anything about admissions, fees, hostel, academics, or your onboarding tasks.</p>
                <div className={styles.quickQuestions}>
                  {QUICK_QUESTIONS.map((q, i) => (
                    <button
                      key={i}
                      className={styles.quickBtn}
                      onClick={() => handleSend(q)}
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className={styles.messagesList}>
                {messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`${styles.message} ${msg.role === 'user' ? styles.userMsg : styles.botMsg} ${msg.error ? styles.errorMsg : ''}`}
                  >
                    {msg.role === 'assistant' && (
                      <div className={styles.botAvatar}>🎓</div>
                    )}
                    <div className={styles.msgContent}>
                      <div className={styles.msgText}>{msg.content}</div>
                      {msg.intent && (
                        <div className={styles.msgMeta}>
                          <span className="badge badge-accent">{msg.intent}</span>
                          {msg.confidence != null && (
                            <span className={styles.confidence}>
                              {Math.round(msg.confidence * 100)}% confident
                            </span>
                          )}
                          {msg.sources?.length > 0 && (
                            <span className={styles.sourceCount}>
                              {msg.sources.length} sources
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className={`${styles.message} ${styles.botMsg}`}>
                    <div className={styles.botAvatar}>🎓</div>
                    <div className={styles.msgContent}>
                      <div className={styles.typing}>
                        <span /><span /><span />
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input */}
          <div className={styles.inputArea}>
            <div className={styles.inputWrapper}>
              <textarea
                ref={inputRef}
                className={styles.input}
                placeholder="Ask me anything..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={1}
                disabled={loading}
              />
              <button
                className={styles.sendBtn}
                onClick={() => handleSend()}
                disabled={!input.trim() || loading}
              >
                {loading ? <div className="spinner" /> : '↑'}
              </button>
            </div>
            <p className={styles.inputHint}>
              Saarthi uses AI to answer your questions. Always verify important details with the admin office.
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  )
}
