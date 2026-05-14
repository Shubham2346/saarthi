'use client'

import { useState, useRef, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { motion, AnimatePresence } from 'framer-motion'
import AppShell from '@/components/AppShell'
import {
  MessageCircle, Send, Bot, User, Sparkles, FileText,
  GraduationCap, BookOpen, Lightbulb, ArrowRight,
  Loader2, ChevronRight, AlertCircle, CheckCircle2
} from 'lucide-react'

const CATEGORIES = [
  { id: 'all', label: 'All', icon: MessageCircle },
  { id: 'admissions', label: 'Admissions', icon: GraduationCap },
  { id: 'fees', label: 'Fees', icon: FileText },
  { id: 'academic', label: 'Academic', icon: BookOpen },
  { id: 'general', label: 'General', icon: Lightbulb },
]

const SUGGESTED_QUESTIONS = [
  'What documents are needed for admission?',
  'What is the fee structure?',
  'How do I check my application status?',
  'What programs are available?',
]

const WELCOME_MESSAGE = {
  role: 'assistant',
  content: `Hello! I'm **Saarthi**, your AI admission assistant. 👋

I can help you with:
- 📋 Admission requirements & documents
- 💰 Fee structure & payment info
- 📝 Application status & tracking
- 🎓 Program information & eligibility
- 🤔 Any other admission-related questions

How can I help you today?`,
}

function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 12, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <div className={`flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center ${
        isUser
          ? 'bg-gradient-to-br from-indigo-500 to-purple-600'
          : 'bg-gradient-to-br from-emerald-400 to-teal-500'
      }`}>
        {isUser ? <User className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4 text-white" />}
      </div>
      <div className={`max-w-[80%] ${isUser ? 'text-right' : ''}`}>
        <div className={`inline-block px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-primary text-primary-foreground rounded-tr-md'
            : 'bg-accent text-foreground rounded-tl-md'
        }`}>
          <div className="prose prose-sm dark:prose-invert max-w-none [&_strong]:font-semibold">
            {message.content}
          </div>
        </div>
        {message.sources && message.sources.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-1.5 justify-end">
            {message.sources.map((src, i) => (
              <Badge key={i} variant="outline" className="text-[10px]">
                {src}
              </Badge>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  )
}

function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-start gap-3"
    >
      <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
        <Bot className="w-4 h-4 text-white" />
      </div>
      <div className="bg-accent px-4 py-3 rounded-2xl rounded-tl-md">
        <div className="flex gap-1">
          <span className="w-2 h-2 rounded-full bg-primary/40 animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-2 h-2 rounded-full bg-primary/40 animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-2 h-2 rounded-full bg-primary/40 animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </motion.div>
  )
}

export default function ChatPage() {
  return <AppShell><ChatPage_ /></AppShell>
}
function ChatPage_() {
  const { user } = useAuth()
  const [messages, setMessages] = useState([WELCOME_MESSAGE])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [category, setCategory] = useState('all')
  const [showSuggestions, setShowSuggestions] = useState(true)
  const chatRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  const handleSend = async (text) => {
    const query = (text || input).trim()
    if (!query || loading) return

    setShowSuggestions(false)
    const userMsg = { role: 'user', content: query }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const response = await api.chat.send('public', query, category !== 'all' ? category : undefined)
      const assistantMsg = {
        role: 'assistant',
        content: response.answer || "I couldn't find an answer to that. Please try rephrasing or contact the admin.",
        sources: response.sources?.map((s) => s.category || s.title).filter(Boolean),
      }
      setMessages((prev) => [...prev, assistantMsg])
    } catch (e) {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] -mx-4 sm:-mx-6 lg:-mx-8">
      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex-shrink-0 px-4 sm:px-6 lg:px-8 py-4 border-b border-border bg-background/50 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-foreground">Ask Saarthi</h2>
                <p className="text-xs text-muted-foreground">AI Admission Assistant</p>
              </div>
            </div>
            <Badge variant="success" className="gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Online
            </Badge>
          </div>

          {/* Categories */}
          <div className="flex gap-2 mt-3 overflow-x-auto scrollbar-hide">
            {CATEGORIES.map((cat) => {
              const Icon = cat.icon
              const isActive = category === cat.id
              return (
                <button
                  key={cat.id}
                  onClick={() => setCategory(cat.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-primary text-primary-foreground shadow-sm'
                      : 'bg-accent text-muted-foreground hover:text-foreground hover:bg-accent/80'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  {cat.label}
                </button>
              )
            })}
          </div>
        </div>

        {/* Messages */}
        <div ref={chatRef} className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 space-y-4 scrollbar-thin">
          <AnimatePresence>
            {messages.map((msg, i) => (
              <MessageBubble key={i} message={msg} />
            ))}
          </AnimatePresence>

          {loading && <TypingIndicator />}

          {/* Suggested questions */}
          {showSuggestions && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="pt-6"
            >
              <p className="text-xs font-medium text-muted-foreground mb-3">Suggested questions</p>
              <div className="grid gap-2 sm:grid-cols-2">
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => handleSend(q)}
                    className="flex items-center gap-2 p-3 rounded-xl border border-border bg-card hover:border-primary/30 hover:bg-accent/50 transition-all text-left text-sm text-foreground group"
                  >
                    <Sparkles className="w-4 h-4 text-primary flex-shrink-0" />
                    <span className="flex-1">{q}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-muted-foreground group-hover:text-primary transition-colors flex-shrink-0" />
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </div>

        {/* Input */}
        <div className="flex-shrink-0 px-4 sm:px-6 lg:px-8 py-4 border-t border-border bg-background/50 backdrop-blur-sm">
          <div className="flex items-center gap-2">
            <div className="flex-1 relative">
              <Input
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask me anything about admissions..."
                className="pr-12 h-11 bg-accent/30 border-border focus:bg-background transition-colors"
              />
              <button
                onClick={() => handleSend()}
                disabled={!input.trim() || loading}
                className="absolute right-1.5 top-1/2 -translate-y-1/2 p-2 rounded-lg text-primary hover:bg-primary/10 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <p className="text-[10px] text-muted-foreground mt-2 text-center">
            Saarthi AI may make mistakes. Verify important information with the admissions office.
          </p>
        </div>
      </div>

      {/* Context Panel - Desktop Only */}
      <div className="hidden xl:block w-80 flex-shrink-0 border-l border-border bg-card/50">
        <div className="p-5 space-y-5">
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-3">Your Profile</h3>
            <div className="space-y-2">
              <div className="flex items-center gap-2.5 p-2.5 rounded-lg bg-accent/30">
                <User className="w-4 h-4 text-muted-foreground" />
                <span className="text-xs text-foreground">{user?.full_name || 'Student'}</span>
              </div>
              <div className="flex items-center gap-2.5 p-2.5 rounded-lg bg-accent/30">
                <GraduationCap className="w-4 h-4 text-muted-foreground" />
                <span className="text-xs text-foreground capitalize">{user?.admission_status?.replace(/_/g, ' ') || 'Not Applied'}</span>
              </div>
            </div>
          </div>

          <div className="border-t border-border pt-4">
            <h3 className="text-sm font-semibold text-foreground mb-3">Quick Actions</h3>
            <div className="space-y-2">
              {[
                { label: 'Start Application', icon: FileText, href: '/admission' },
                { label: 'Upload Documents', icon: Sparkles, href: '/documents' },
                { label: 'View Tasks', icon: CheckCircle2, href: '/tasks' },
              ].map((action) => {
                const Icon = action.icon
                return (
                  <a key={action.href} href={action.href}
                    className="flex items-center gap-2.5 p-2.5 rounded-lg hover:bg-accent/50 transition-colors text-sm text-foreground group">
                    <Icon className="w-4 h-4 text-primary" />
                    <span className="flex-1">{action.label}</span>
                    <ChevronRight className="w-3.5 h-3.5 text-muted-foreground group-hover:text-primary transition-colors" />
                  </a>
                )
              })}
            </div>
          </div>

          <div className="border-t border-border pt-4">
            <h3 className="text-sm font-semibold text-foreground mb-3">Tips</h3>
            <div className="p-3 rounded-xl bg-gradient-card dark:bg-gradient-card-dark border border-indigo-200/50 dark:border-indigo-800/50">
              <Lightbulb className="w-4 h-4 text-indigo-500 mb-2" />
              <p className="text-xs text-muted-foreground leading-relaxed">
                Try asking about specific programs, fee waivers, or document requirements for faster responses.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
