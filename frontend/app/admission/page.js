'use client'

import { useCallback, useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import AppShell from '@/components/AppShell'
import { useAuth } from '@/lib/auth'
import { admission as admissionApi } from '@/lib/api'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Loader2, Sparkles, CheckCircle2, Bot, User, ChevronRight } from 'lucide-react'

const FIELD_ORDER = [
  { key: 'full_name', label: 'Full Name', example: 'e.g. Chetan Sharma', question: "Let's start with your full name.", placeholder: 'e.g. Chetan Sharma' },
  { key: 'email', label: 'Email', example: 'e.g. chetan@gmail.com', question: "What's your email address?", placeholder: 'e.g. chetan@gmail.com' },
  { key: 'phone', label: 'Phone', example: 'e.g. +91 9876543210', question: 'Please share your mobile number.', placeholder: 'e.g. +91 9876543210' },
  { key: 'date_of_birth', label: 'Date of Birth', example: 'e.g. 2005-08-17', question: "What's your date of birth?", placeholder: 'e.g. 2005-08-17' },
  { key: 'program_choice', label: 'Program / Branch', example: 'e.g. B.Tech CSE', question: 'Which program or branch do you want to apply for?', placeholder: 'e.g. B.Tech CSE' },
  { key: 'previous_institution', label: 'Previous School', example: 'e.g. Delhi Public School', question: 'Which school did you complete your 12th from?', placeholder: 'e.g. Delhi Public School' },
  { key: 'board_10', label: '10th Board', example: 'e.g. CBSE / ICSE / State Board', question: 'Which board was your 10th from?', placeholder: 'e.g. CBSE / ICSE / State Board' },
  { key: 'percentage_10', label: '10th Percentage', example: 'e.g. 89%', question: 'What was your 10th percentage?', placeholder: 'e.g. 89%' },
  { key: 'board_12', label: '12th Board', example: 'e.g. CBSE', question: 'Which board was your 12th from?', placeholder: 'e.g. CBSE' },
  { key: 'percentage_12', label: '12th Percentage', example: 'e.g. 91%', question: 'What was your 12th percentage?', placeholder: 'e.g. 91%' },
  { key: 'address_line1', label: 'Address', example: 'e.g. H.No 21, MG Road', question: 'Please enter your address.', placeholder: 'e.g. H.No 21, MG Road' },
  { key: 'city', label: 'City', example: 'e.g. Pune', question: 'Which city do you live in?', placeholder: 'e.g. Pune' },
  { key: 'state', label: 'State', example: 'e.g. Maharashtra', question: 'Your state?', placeholder: 'e.g. Maharashtra' },
  { key: 'postal_code', label: 'Postal Code', example: 'e.g. 411001', question: 'Please enter your postal code.', placeholder: 'e.g. 411001' },
  { key: 'country', label: 'Country', example: 'e.g. India', question: 'Which country are you from?', placeholder: 'e.g. India' },
  { key: 'guardian_name', label: 'Guardian Name', example: "e.g. Rajesh Sharma", question: "What's your parent/guardian's name?", placeholder: 'e.g. Rajesh Sharma' },
  { key: 'guardian_phone', label: 'Guardian Phone', example: 'e.g. +91 9876543210', question: 'Please share guardian contact number.', placeholder: 'e.g. +91 9876543210' },
]

function validate(key, value) {
  const v = (value || '').trim()
  if (!v) return { valid: false, msg: 'This field is required.' }
  switch (key) {
    case 'email':
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? { valid: true } : { valid: false, msg: 'Please enter a valid email (e.g. name@domain.com).' }
    case 'phone':
    case 'guardian_phone':
      return /^\+?[\d\s\-()]{7,15}$/.test(v) ? { valid: true } : { valid: false, msg: 'Please enter a valid phone number with country code (e.g. +91 9876543210).' }
    case 'percentage_10':
    case 'percentage_12': {
      const n = parseFloat(v.replace('%', ''))
      return (!isNaN(n) && n >= 0 && n <= 100) ? { valid: true } : { valid: false, msg: 'Please enter a percentage between 0 and 100 (e.g. 89).' }
    }
    case 'date_of_birth':
      return /^\d{4}-\d{2}-\d{2}$/.test(v) ? { valid: true } : { valid: false, msg: 'Please enter date in YYYY-MM-DD format (e.g. 2005-08-17).' }
    case 'postal_code':
      return /^\d{4,6}$/.test(v) ? { valid: true } : { valid: false, msg: 'Please enter a valid postal code (e.g. 411001).' }
    default:
      return v.length >= 2 ? { valid: true } : { valid: false, msg: `Please provide a valid ${FIELD_ORDER.find(f => f.key === key)?.label || 'value'}.` }
  }
}

function parseMultiFieldInput(text, missingFields, currentValues) {
  const updates = {}
  const lower = text.toLowerCase()

  // Name patterns: "My name is X", "I'm X", "I am X"
  if (missingFields.includes('full_name')) {
    const m = lower.match(/(?:my name is|i'm|i am|name is)\s+([a-z\s]+?)(?:\s+(?:and|my email|my phone|i want|my|,|$))/i)
    if (m) updates.full_name = m[1].trim().replace(/^./, c => c.toUpperCase())
    else if (!lower.match(/(?:email|phone|program|10th|12th|cbse|icse)/) && text.split(' ').length <= 4) {
      updates.full_name = text.trim()
    }
  }

  // Email pattern
  const emailMatch = text.match(/[\w.+-]+@[\w-]+\.[\w.]+/)
  if (emailMatch && missingFields.includes('email')) updates.email = emailMatch[0]

  // Phone pattern
  const phoneMatch = text.match(/\+?\d[\d\s\-()]{7,15}/)
  if (phoneMatch && missingFields.includes('phone')) updates.phone = phoneMatch[0].trim()

  // Program pattern: "I want X", "B.Tech", "BCA", "B.Com"
  if (missingFields.includes('program_choice')) {
    const m = lower.match(/(?:i want|program|branch|course)\s+([a-z.\s]+?)(?:\s+(?:and|my|,|$))/i)
    if (m) updates.program_choice = m[1].trim()
    const direct = text.match(/\b(B\.?\w+|M\.?\w+|BCA|MCA|BBA|MBA|BCom|MCom|BSc|MSc|BTech|MTech|Diploma)\b/i)
    if (direct) updates.program_choice = direct[0]
  }

  // Board patterns: "CBSE", "ICSE", "State Board"
  if (missingFields.includes('board_10') || missingFields.includes('board_12')) {
    const boardMatch = text.match(/\b(CBSE|ICSE|IB|State Board|ISC|SSC|HSC)\b/i)
    if (boardMatch) {
      if (missingFields.includes('board_10') && !updates.board_10) updates.board_10 = boardMatch[0].toUpperCase()
      else if (missingFields.includes('board_12') && !updates.board_12) updates.board_12 = boardMatch[0].toUpperCase()
    }
  }

  // Percentage patterns: "89%", "92 percent"
  const pctMatches = [...text.matchAll(/(\d{2,3})\s*%/g)]
  if (pctMatches.length > 0) {
    if (missingFields.includes('percentage_10') && !updates.percentage_10) updates.percentage_10 = pctMatches[0][1]
    if (pctMatches.length > 1 && missingFields.includes('percentage_12') && !updates.percentage_12) updates.percentage_12 = pctMatches[1][1]
  }

  return updates
}

const emptyApp = {
  full_name: '', email: '', phone: '', date_of_birth: '', program_choice: '',
  previous_institution: '', board_10: '', percentage_10: '', board_12: '', percentage_12: '',
  address_line1: '', city: '', state: '', postal_code: '', country: '',
  guardian_name: '', guardian_phone: '',
}

function mergeApp(base, incoming) {
  if (!incoming) return base
  const next = { ...base }
  for (const k of Object.keys(emptyApp)) {
    if (incoming[k] != null && incoming[k] !== '') next[k] = incoming[k]
  }
  return next
}

export default function AdmissionPage() {
  const router = useRouter()
  const { user, loading: authLoading } = useAuth()
  const formRef = useRef(null)
  const chatEndRef = useRef(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [application, setApplication] = useState(emptyApp)
  const [currentStep, setCurrentStep] = useState(0)
  const [completedFields, setCompletedFields] = useState(new Set())
  const [activeField, setActiveField] = useState(null)
  const [validationMsg, setValidationMsg] = useState(null)
  const [showSummary, setShowSummary] = useState(false)
  const [confirmed, setConfirmed] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [initialized, setInitialized] = useState(false)

  useEffect(() => {
    if (!authLoading && !user) router.replace('/login')
  }, [authLoading, user, router])

  useEffect(() => {
    if (!initialized) {
      setMessages([{ role: 'assistant', content: "Hi! I'm your admission copilot. Let's get your application started!\n\nFirst up — **what's your full name?**" }])
      setActiveField('full_name')
      setInitialized(true)
    }
  }, [initialized])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (activeField) {
      const el = document.getElementById(`field-${activeField}`)
      el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }, [activeField])

  const getMissingFields = useCallback(() => {
    return FIELD_ORDER.filter(f => !application[f.key]?.trim()).map(f => f.key)
  }, [application])

  const askNext = useCallback((updatedApp) => {
    const missing = FIELD_ORDER.filter(f => !updatedApp[f.key]?.trim())
    if (missing.length === 0) {
      setShowSummary(true)
      setActiveField(null)
      setMessages(prev => [...prev, { role: 'assistant', content: "**All fields completed!** 🎉\n\nHere's a quick summary of your application. Would you like to confirm and submit?" }])
      return
    }
    const next = missing[0]
    setCurrentStep(FIELD_ORDER.findIndex(f => f.key === next.key))
    setActiveField(next.key)
    setMessages(prev => [...prev, { role: 'assistant', content: `${next.question}\n\n*${next.example}*` }])
    setValidationMsg(null)
  }, [])

  const processInput = useCallback((text) => {
    const missingFields = getMissingFields()
    const fieldDef = FIELD_ORDER[currentStep]
    if (!fieldDef) return

    // Try to parse multi-field input
    const parsed = parseMultiFieldInput(text, missingFields, application)
    
    // If no multi-parse match, treat entire input as current field value
    if (Object.keys(parsed).length === 0) {
      parsed[fieldDef.key] = text.trim()
    }

    // Validate
    const updates = {}
    let firstError = null
    for (const [key, value] of Object.entries(parsed)) {
      const result = validate(key, value)
      if (result.valid) {
        updates[key] = value
      } else if (!firstError) {
        firstError = { key, msg: result.msg }
      }
    }

    if (firstError && Object.keys(updates).length === 0) {
      setValidationMsg(firstError.msg)
      setMessages(prev => [...prev, { role: 'assistant', content: `${firstError.msg}\n\n*${fieldDef.example}*` }])
      return
    }

    // Apply updates
    const updatedApp = { ...application, ...updates }
    for (const key of Object.keys(updates)) {
      setCompletedFields(prev => new Set([...prev, key]))
    }
    setApplication(updatedApp)
    setValidationMsg(null)

    // Save to backend
    for (const [key, value] of Object.entries(updates)) {
      admissionApi.patchApplication({ [key]: value }).catch(() => {})
    }

    // Feedback message
    const updatedNames = Object.keys(updates).map(k => FIELD_ORDER.find(f => f.key === k)?.label || k)
    if (updatedNames.length > 0) {
      setMessages(prev => [...prev, { role: 'assistant', content: `Got it! **${updatedNames.join(', ')}** saved. ✅` }])
    }

    // Ask next
    setTimeout(() => askNext(updatedApp), 400)
  }, [currentStep, application, getMissingFields, askNext])

  const handleSubmit = (e) => {
    e?.preventDefault()
    const text = input.trim()
    if (!text) return
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: text }])
    if (showSummary) {
      if (text.toLowerCase().match(/^(yes|confirm|submit|y)$/)) {
        setConfirmed(true)
        setSubmitting(true)
        setMessages(prev => [...prev, { role: 'assistant', content: "**Application submitted!** 🎉\n\nYour admission application has been marked as ready. The admissions team will review it shortly." }])
        setSubmitting(false)
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: "No problem! Let me know if you'd like to change anything or type **confirm** when you're ready." }])
      }
      return
    }
    processInput(text)
  }

  const pct = Math.round((completedFields.size / FIELD_ORDER.length) * 100)

  return (
    <AppShell>
      <div className="min-h-[calc(100vh-4rem)]">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-primary mb-1">
            <Sparkles className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">AI Admission Copilot</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Your application, guided by AI</h1>
          <p className="text-muted-foreground mt-1">Chat naturally to fill your admission form step by step.</p>
        </div>

        {/* Progress */}
        <div className="flex items-center gap-4 mb-6 p-4 rounded-xl bg-card border border-border">
          <div className="relative w-14 h-14 flex-shrink-0">
            <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
              <circle cx="50" cy="50" r="42" fill="none" stroke="hsl(var(--muted))" strokeWidth="8" />
              <circle cx="50" cy="50" r="42" fill="none" stroke="hsl(var(--primary))" strokeWidth="8" strokeDasharray={`${(pct / 100) * 264} 264`} strokeLinecap="round" className="transition-all duration-500" />
            </svg>
            <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-foreground">{pct}%</span>
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-foreground">Application Progress</p>
            <div className="flex gap-1 mt-1.5">
              {FIELD_ORDER.map((f, i) => (
                <div key={f.key} className={`h-1.5 flex-1 rounded-full transition-colors duration-300 ${completedFields.has(f.key) ? 'bg-primary' : i === currentStep ? 'bg-primary/40' : 'bg-muted'}`} />
              ))}
            </div>
          </div>
          <span className="text-xs text-muted-foreground">{completedFields.size}/{FIELD_ORDER.length} fields</span>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Chat Panel */}
          <div className="flex flex-col rounded-xl border border-border bg-card min-h-[500px]">
            <div className="border-b border-border px-5 py-3.5 flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <span className="font-semibold text-sm text-foreground">Admission Copilot</span>
              {confirmed && <span className="ml-auto text-xs text-emerald-500 font-medium flex items-center gap-1"><CheckCircle2 className="w-3 h-3" /> Submitted</span>}
            </div>

            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3 max-h-[460px] scrollbar-thin">
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex items-start gap-2.5 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-gradient-to-br from-emerald-400 to-teal-500 text-white'
                  }`}>
                    {msg.role === 'user' ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
                  </div>
                  <div className={`max-w-[85%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-primary text-primary-foreground rounded-tr-md'
                      : 'bg-accent text-foreground rounded-tl-md'
                  }`}>
                    <div className="[&_strong]:font-semibold [&_em]:italic whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </motion.div>
              ))}
              {submitting && (
                <div className="flex items-start gap-2.5">
                  <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
                    <Bot className="w-3.5 h-3.5 text-white" />
                  </div>
                  <div className="bg-accent px-4 py-3 rounded-2xl rounded-tl-md">
                    <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
                  </div>
                </div>
              )}
              {validationMsg && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="px-3 py-2 rounded-lg bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-800/50 text-xs text-rose-600 dark:text-rose-400">
                  {validationMsg}
                </motion.div>
              )}
              <div ref={chatEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="p-4 border-t border-border">
              <div className="flex gap-2">
                <input
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  placeholder={showSummary ? 'Type confirm to submit or anything to update...' : 'Type your answer here...'}
                  className="flex-1 h-10 rounded-lg border border-input bg-background px-3 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring/30 transition-all"
                  disabled={confirmed}
                />
                <button
                  type="submit"
                  disabled={!input.trim() || confirmed}
                  className="h-10 px-4 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center gap-1.5 text-sm font-medium"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
              {!showSummary && !confirmed && (
                <p className="text-[10px] text-muted-foreground mt-2 text-center">You can also include multiple details at once (e.g. &quot;My name is Rahul, email rahul@mail.com, I want BCA&quot;)</p>
              )}
            </form>
          </div>

          {/* Form Panel */}
          <div ref={formRef} className="rounded-xl border border-border bg-card p-5">
            <h3 className="text-sm font-semibold text-foreground mb-4 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-primary" />
              Live Application Form
              {activeField && !confirmed && <span className="ml-auto text-[10px] text-muted-foreground">Active: {FIELD_ORDER.find(f => f.key === activeField)?.label}</span>}
            </h3>
            <div className="grid sm:grid-cols-2 gap-3 max-h-[520px] overflow-y-auto pr-1 scrollbar-thin">
              {FIELD_ORDER.map((field) => {
                const isCompleted = completedFields.has(field.key)
                const isActive = activeField === field.key
                const value = application[field.key] || ''
                return (
                  <div key={field.key} id={`field-${field.key}`} className={field.key === 'address_line1' ? 'sm:col-span-2' : ''}>
                    <label className="block text-xs font-medium text-muted-foreground mb-1">
                      {field.label}
                      {isCompleted && <CheckCircle2 className="inline w-3 h-3 ml-1 text-emerald-500" />}
                    </label>
                    <input
                      className={`w-full h-9 rounded-lg border px-3 text-sm bg-background transition-all duration-300 ${
                        isActive && !confirmed
                          ? 'border-primary/50 ring-2 ring-primary/20 shadow-sm shadow-primary/10'
                          : isCompleted
                            ? 'border-emerald-300 dark:border-emerald-700/50 bg-emerald-50/30 dark:bg-emerald-500/5'
                            : 'border-input'
                      } ${confirmed ? 'opacity-70' : ''}`}
                      value={value}
                      placeholder={isActive && !value ? field.placeholder : ''}
                      onChange={e => setApplication(prev => ({ ...prev, [field.key]: e.target.value }))}
                      onBlur={e => {
                        if (e.target.value.trim()) {
                          admissionApi.patchApplication({ [field.key]: e.target.value }).catch(() => {})
                          setCompletedFields(prev => new Set([...prev, field.key]))
                        }
                      }}
                      readOnly={confirmed}
                    />
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  )
}
