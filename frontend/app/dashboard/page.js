'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { api } from '@/lib/api'
import AppShell from '@/components/AppShell'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Skeleton } from '@/components/ui/skeleton'
import { motion } from 'framer-motion'
import {
  Sparkles, MessageCircle, CheckSquare, FileText,
  TrendingUp, Clock, AlertCircle, CheckCircle2,
  CreditCard, Rocket, ChevronRight, GraduationCap, ArrowRight, Bot
} from 'lucide-react'

const colors = {
  indigo: 'bg-indigo-100 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400',
  emerald: 'bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
  amber: 'bg-amber-100 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400',
  rose: 'bg-rose-100 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400',
  blue: 'bg-blue-100 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400',
}

function StatCard({ label, value, icon: Icon, color = 'indigo', delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="stats-card"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{label}</p>
          <p className="text-2xl font-bold text-foreground mt-0.5">{value}</p>
        </div>
        {Icon && (
          <div className={`h-11 w-11 rounded-xl flex items-center justify-center flex-shrink-0 ${colors[color]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default function StudentDashboard() {
  return <AppShell><StudentDashboardContent /></AppShell>
}

function StudentDashboardContent() {
  const { user } = useAuth()
  const router = useRouter()
  const [progress, setProgress] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [progressData] = await Promise.allSettled([api.get('/tasks/my-progress')])
        if (progressData.status === 'fulfilled') setProgress(progressData.value)
      } catch (e) {
        console.error('Failed to load dashboard', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const getGreeting = () => {
    const h = new Date().getHours()
    if (h < 12) return 'Good morning'
    if (h < 17) return 'Good afternoon'
    return 'Good evening'
  }

  const firstName = user?.full_name?.split(' ')[0] || 'Student'
  const progressPct = progress?.percentage || 0
  const completed = progress?.completed || 0
  const pending = progress?.pending || 0
  const overdue = progress?.overdue || 0

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-72" />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-28 rounded-xl" />)}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-500 via-indigo-600 to-purple-700 p-6 sm:p-8">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-50" />
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-3">
            <div className="px-2.5 py-1 rounded-full bg-white/10 backdrop-blur-sm text-[10px] font-medium text-white/80">Admission Portal</div>
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">{getGreeting()}, {firstName}!</h1>
          <p className="text-indigo-100 mt-1 max-w-xl">Welcome to your admission portal. Let&apos;s get you onboarded with AI-powered assistance.</p>
          <div className="flex flex-wrap gap-2 mt-4">
            <Button size="sm" variant="secondary" className="bg-white/10 text-white border-white/20 hover:bg-white/20 backdrop-blur-sm" onClick={() => router.push('/admission')}>
              <Sparkles className="w-3.5 h-3.5 mr-1.5" /> Start Application
            </Button>
            <Button size="sm" variant="secondary" className="bg-white/10 text-white border-white/20 hover:bg-white/20 backdrop-blur-sm" onClick={() => router.push('/chat')}>
              <MessageCircle className="w-3.5 h-3.5 mr-1.5" /> Ask AI
            </Button>
          </div>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Overall Progress" value={`${progressPct}%`} icon={TrendingUp} color="indigo" delay={0.1} />
        <StatCard label="Completed" value={completed} icon={CheckCircle2} color="emerald" delay={0.15} />
        <StatCard label="Pending" value={pending} icon={Clock} color="amber" delay={0.2} />
        <StatCard label="Overdue" value={overdue} icon={AlertCircle} color={overdue > 0 ? 'rose' : 'slate'} delay={0.25} />
      </div>

      <Progress value={progressPct} className="h-2" />

      {/* Quick Action Cards */}
      <div>
        <h2 className="section-title">Quick Actions</h2>
        <p className="section-desc mb-4">Continue your admission journey</p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { href: '/admission', icon: Sparkles, label: 'AI Admission', desc: 'Fill application with AI', color: 'from-indigo-500 to-purple-600', border: 'border-indigo-200/50 dark:border-indigo-800/50' },
            { href: '/chat', icon: MessageCircle, label: 'Ask Saarthi', desc: 'Get answers instantly', color: 'from-emerald-500 to-teal-600', border: 'border-emerald-200/50 dark:border-emerald-800/50' },
            { href: '/tasks', icon: CheckSquare, label: 'My Tasks', desc: `${pending} pending tasks`, color: 'from-amber-500 to-orange-600', border: 'border-amber-200/50 dark:border-amber-800/50' },
            { href: '/documents', icon: FileText, label: 'Documents', desc: 'Upload & manage docs', color: 'from-blue-500 to-cyan-600', border: 'border-blue-200/50 dark:border-blue-800/50' },
          ].map((item, i) => {
            const Icon = item.icon
            return (
              <motion.div
                key={item.href}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 * i }}
              >
                <Card className={`cursor-pointer hover:shadow-elevated hover:-translate-y-0.5 transition-all duration-200 group ${item.border}`} onClick={() => router.push(item.href)}>
                  <CardContent className="p-5">
                    <div className={`h-10 w-10 bg-gradient-to-br ${item.color} rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="font-semibold text-foreground">{item.label}</h3>
                    <p className="text-xs text-muted-foreground mt-1">{item.desc}</p>
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Checklist + Status */}
      <div className="grid gap-6 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card>
            <CardHeader>
              <CardTitle>Getting Started Checklist</CardTitle>
              <CardDescription>Complete these steps to finish onboarding</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  { num: 1, title: 'Fill your admission application', done: progressPct > 0, href: '/admission' },
                  { num: 2, title: 'Upload required documents (marksheets, certificates)', done: false, href: '/documents' },
                  { num: 3, title: 'Pay admission fee', done: false, href: '/payment' },
                  { num: 4, title: 'Complete orientation registration', done: false, href: '/tasks' },
                ].map((step) => (
                  <div key={step.num} className="flex items-center gap-3 p-2 rounded-lg hover:bg-accent/50 transition-colors">
                    <div className={`h-8 w-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ${
                      step.done ? 'bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' : 'bg-accent text-muted-foreground'
                    }`}>
                      {step.done ? <CheckCircle2 className="w-4 h-4" /> : step.num}
                    </div>
                    <div className="flex-1">
                      <p className={`text-sm ${step.done ? 'text-muted-foreground line-through' : 'text-foreground'}`}>{step.title}</p>
                    </div>
                    {!step.done && (
                      <button onClick={() => router.push(step.href)} className="text-xs font-medium text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1">
                        Start <ArrowRight className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}>
          <Card>
            <CardHeader>
              <CardTitle>Admission Status</CardTitle>
              <CardDescription>Current stage of your application</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 rounded-xl bg-gradient-card dark:bg-gradient-card-dark border border-indigo-200/50 dark:border-indigo-800/50">
                  <div className="flex items-center gap-3 mb-3">
                    <Rocket className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                    <span className="text-sm font-semibold text-indigo-700 dark:text-indigo-300 capitalize">
                      {user?.admission_status?.replace(/_/g, ' ') || 'Not Started'}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {user?.onboarding_stage ? `Stage: ${user.onboarding_stage.replace(/_/g, ' ')}` : 'Begin your admission journey in the AI Admission section.'}
                  </p>
                </div>

                <div className="space-y-2">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">Need Help?</p>
                  <button onClick={() => router.push('/chat')} className="w-full flex items-center gap-2.5 p-3 rounded-lg border border-border hover:bg-accent/50 transition-colors text-left">
                    <Bot className="w-4 h-4 text-indigo-500" />
                    <span className="text-sm text-foreground flex-1">Ask Saarthi AI Assistant</span>
                    <ChevronRight className="w-4 h-4 text-muted-foreground" />
                  </button>
                  <button onClick={() => router.push('/payment')} className="w-full flex items-center gap-2.5 p-3 rounded-lg border border-border hover:bg-accent/50 transition-colors text-left">
                    <CreditCard className="w-4 h-4 text-emerald-500" />
                    <span className="text-sm text-foreground flex-1">View Fee & Payment</span>
                    <ChevronRight className="w-4 h-4 text-muted-foreground" />
                  </button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
